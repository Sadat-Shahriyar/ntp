import os
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import PyMuPDFLoader
import pprint
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langchain_ollama import OllamaEmbeddings
from datetime import datetime
from langchain_core.messages.utils import count_tokens_approximately

RETRIEVAL_DOCS_K = 30
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 200
OLLAMA_INFERENCE_MODEL_NAME = "llama3.1:70b"
EMBEDDING_MODEL_TYPE = {"huggingface": 1, "ollama": 2}
EMBEDDING_MODEL_TYPE_DECLARED = EMBEDDING_MODEL_TYPE['huggingface']
HUGGINGFACE_EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
OLLAMA_EMBEDDING_MODEL_NAME = "nomic-embed-text:v1.5"
# OLLAMA_EMBEDDING_MODEL_NAME = "embeddinggemma:300m"
FILE_PATH = "papers/paper_1.pdf"

EMBEDDING_MODEL_NAME = HUGGINGFACE_EMBEDDING_MODEL_NAME
if EMBEDDING_MODEL_TYPE_DECLARED == EMBEDDING_MODEL_TYPE['ollama']:
    EMBEDDING_MODEL_NAME = OLLAMA_EMBEDDING_MODEL_NAME

# Langsmith environment initialization
os.environ['LANGSMITH_TRACING'] = 'true'
os.environ['LANGSMITH_API_KEY'] = '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'


def get_time_string():
    now = datetime.now()
    timestamp_str = now.strftime("%Y%m%d_%H%M%S")
    return str(timestamp_str)

TIME_STAMP_STRING = get_time_string()

def print_to_file(start_string, message):
    result_file_name = start_string + "_result_k_" + str(RETRIEVAL_DOCS_K) + "_chunk_" + str(CHUNK_SIZE) + "_" + "_".join(OLLAMA_INFERENCE_MODEL_NAME.split(":")) + "_" + "_".join(EMBEDDING_MODEL_NAME.split(":")) + "_" + ".md"
    result_folder = "results" + "/" + "_".join(OLLAMA_INFERENCE_MODEL_NAME.split(":")) + "/" + TIME_STAMP_STRING
    if not os.path.isdir(result_folder):
        os.makedirs(result_folder, exist_ok=True)
    
    result_save_file_dir = result_folder + "/" + result_file_name
    with open(result_save_file_dir, "w", encoding="utf-8") as f:
        f.write(message)


# Load chat model, embedding model and vector store
model = ChatOllama(
    model=OLLAMA_INFERENCE_MODEL_NAME,  # or another DeepSeek model you pulled
    temperature=0.2
)

if EMBEDDING_MODEL_TYPE_DECLARED == EMBEDDING_MODEL_TYPE['huggingface']:
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
elif EMBEDDING_MODEL_TYPE_DECLARED == EMBEDDING_MODEL_TYPE['ollama']:
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL_NAME)
# embeddings = OllamaEmbeddings(model="nomic-embed-text")

vector_store = InMemoryVectorStore(embeddings)


# Load pdf
loader = PyMuPDFLoader(FILE_PATH)

docs = loader.load()
# pprint.pp(docs[0].metadata)

# print(f"Total charecters: {len(docs[0].page_content)}")
# print(docs[0].page_content[:500])


# SPlit document:

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    add_start_index=True,
)
all_splits = text_splitter.split_documents(docs)

# print(f"Split blog post into {len(all_splits)} sub-documents.")

# Store in vector database
document_ids = vector_store.add_documents(documents=all_splits)

# print(document_ids[:3])


# RAG Agent

@dynamic_prompt
def prompt_with_context(request: ModelRequest) -> str:
    """Inject context into state messages."""
    last_query = request.state["messages"][-1].text
    print(f'==== Last query ==== \n {last_query}')
    retrieved_docs = vector_store.similarity_search(last_query, k=RETRIEVAL_DOCS_K)


    docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)

    system_message = (
        """You are a helpful AI assistant. """
        # f"\n\n{docs_content}"
    )
    
    start_string = "_system"
    message_to_print = f"=========== system message ===============\n{system_message}"
    print_to_file(start_string=start_string, message=message_to_print)

    return system_message


agent = create_agent(model, tools=[], middleware=[prompt_with_context])

# Query the agent

# query = '''
# Extract the following structured information from the paper content:

# - Workload model (e.g., sporadic tasks, parameters Ci, Di, Ti)
# - Resource model (e.g., processors, platform assumptions)
# - Scheduler (e.g., EDF, DM, FJP, FTP, priority rules)
# - Analysis framework (e.g., DBF, load test, conditions, test strategy)
# - Lemmas, Theorems, Corollaries (exact statements)

# Output the result in clean JSON with this format:

# {
#   "workload_model": "...",
#   "resource_model": "...",
#   "scheduler": "...",
#   "analysis_framework": "...",
#   "lemmas_theorems_corollaries": [
#     {"type": "Lemma", "title": "Lemma 1", "statement": "..."}
#   ]
# }
# '''

query = '''
You are analyzing a research paper on real-time systems. Use the following definitions as background:

1. Workload Model:
The workload model specifies the set of computational tasks in the system. It describes characteristics such as arrival patterns (periodic, sporadic, aperiodic), execution times (worst-case, best-case, average), deadlines, precedence constraints, and criticality levels. In short, it defines what tasks need to be scheduled and when they arrive.
2. Resource Model:
The resource model describes the computing and hardware resources available for executing tasks. This includes processors (single-core, multi-core, heterogeneous cores), communication channels, memory, I/O devices, and their timing or capacity constraints. It defines where and how tasks can execute.
3. Scheduler:
The scheduler is the decision-making mechanism that assigns tasks from the workload model to resources from the resource model, according to specific scheduling policies and algorithms (e.g., Rate-Monotonic, Earliest Deadline First, Fixed Priority). Its purpose is to ensure that tasks meet their timing requirements while respecting resource constraints.
4. Analysis Framework:
The analysis framework provides the formal methods and tools used to determine whether the system is schedulable under the given workload, resource model, and scheduler. It encompasses techniques such as response-time analysis, utilization bounds, demand-bound functions, and model checking. The framework evaluates timing guarantees, detects potential deadline misses, and quantifies metrics like worst-case response time, jitter, and resource utilization. In short, it defines how the correctness and performance of the system are verified.

Task:
From the paper you are analyzing:
1. Identify and describe the workload model, resource model, scheduler and analysis framework used.
2. Extract all  of the system constraints or invariants from the paper that guarantee correct scheduling of workloads. These are typically presented as equations, lemmas, theorems or constraints. Don't miss out on any of the theorem or lemma or system invariants. Write the constraints exactly as they appear in the paper. For each constraint, explain the meaning of every notation or symbol used.

Write your answer in markdown format. Use $$ for multi-line equation and $ for single line equations. 

The following content is from the paper:

```
# Techniques for Multiprocessor Global Schedulability Analysis+
Footnote †: Supported in part by NSF Grant Nos. CNS-0408996, CCF-0541056, and CCR-0615197, ARO Grant No. W911NF-06-1-0425, and funding from the Intel Corporation.

Sanjoy Baruah

The University of North Carolina at Chapel Hill

###### Abstract

The scheduling of sporadic task systems upon multiprocessor platforms is considered, when inter-processor migration is permitted. It is known that current schedulability tests for such systems perform quite poorly when compared to schedulability tests for partitioned scheduling. Limitations of current tests are identified, which may be responsible for the unsatisfactory performance of these tests. A new test that overcomes some of these limitations is proposed and proved correct.

## 1 Introduction and Motivation

A real-time system is often modelled as a finite collection of independent recurring tasks, each of which generates a potentially infinite sequence of _jobs_. Every job is characterized by an arrival time, an execution requirement, and a deadline, and it is required that a job complete execution between its arrival time and its deadline. Different formal models for recurring tasks place different restrictions on the values of the parameters of jobs generated by each task. One of the more commonly used formal models is the _sporadic task model_[23, 9], which will be considered in this paper.

Scheduling is the allocation of processor time to jobs, and a _scheduling algorithm_ is used for determining such allocation. A _schedulability test_ for a given scheduling algorithm accepts as input the specifications of a real-time system, and determines whether the scheduling algorithm can guarantee to schedule the system such that all jobs of all tasks will meet all deadlines, under all permissible combinations of job-arrival sequences by the different tasks comprising the system. In this paper, we study the scheduling of systems of sporadic tasks upon a platform comprised of several identical processors. In scheduling a task system upon such a platform, it is possible to divide the processors into clusters and assign each task to a cluster. A scheduling algorithm is then applied locally in each cluster, to the jobs generated by the tasks that are assigned to the cluster. It is assumed that inter-processor communication within a cluster incurs no overhead. We focus here on the two extremes of clustering. In _partitioned scheduling_, each processor is a cluster of size one. That is, each task is assigned to one processor and all the jobs generated by a task are constrained to execute only upon the processor to which the task has been assigned. In _global scheduling_, by contrast, there is only one cluster containing all the processors. A job may execute upon any processor, and a preempted job may later resume execution upon the same processor as, or a different processor from, the one on which it had previously been executing. However, each job may execute on at most one processor at each instant in time.

Current state of the art.Currently, the partitioned scheduling of sporadic task systems is much better understood than global scheduling. Sufficient schedulability tests of polynomial time-complexity have been designed [7, 17, 8] for various commonly-used scheduling algorithms (such as Earliest Deadline First (edf) [22, 14] and Deadline Monotonic (DM) [21]). Worst-case resource-augmentation bounds, that provide a quantitative measure of how effective these tests are, have been obtained. These schedulability tests have also been extensively evaluated via simulations [4, 6], and shown to have much better average-case behavior than indicated by their worst-case guarantees. In contrast, we are not aware of non-trivial theoretical bounds on the performance of known sufficient schedulability tests [2, 3, 10] for global scheduling (other than a relatively naive resource-augmentation bound on global DM [16]), and simulation experiments have tended to indicate that they perform poorly in comparison to the partitioned schedulability tests.

This research.This research is aimed at obtaining a better understanding of global schedulability for sporadic task systems. After formally defining the task and machine models in Section 2, we start out in Section 3 by highlighting what appears to be one of the root causes of difficulty in such analysis: our failure thus far to come up with techniques for characterizing the "worst case" behavior of such systems. In Section 4, we demonstrate that global and partitioned scheduling are _incomparable_ for priority-based scheduling algorithms that are not allowed to dynamically change the priorities of jobs; this extends a result of Leung and Whitehead [21], who obtained a similar incomparability result for algorithms in which all jobs of each task are required to have the same priority. In Section 5, we briefly summarize prior tests for global edf-schedulability analysis, and highlight their features and disadvantages. In Section 6, we derive and analyze a new global-edf schedulability test that overcomes some of the disadvantages of these prior tests. We conclude in Section 7 with a summary of the main results in this paper.

For the sake of concreteness, we have chosen to focus in this paper upon a specific global scheduling algorithm - edf. However, the issues are similar for many other scheduling algorithms, and many of the techniques that are applicable to global edf scheduling are likely to be applicable to these other scheduling algorithms as well. (For example, Baker has used similar techniques to study both global edf-schedulability [2, 3] and global DM-schedulability [2, 5], and Bertogna et al. have extended their global edf-schedulability results [10] to apply to DM scheduling [11].)

## 2 Model

A _sporadic task_\(\tau_{i}=(C_{i},D_{i},T_{i})\) is characterized by a _worst-case execution requirement_\(C_{i}\), a _(relative) deadline_\(D_{i}\), and a _minimum inter-arrival separation_\(T_{i}\), which is, for historical reasons, also referred to as the _period_ of the task. Such a sporadic task generates a potentially infinite sequence of jobs, with successive job-arrivals separated by at least \(T_{i}\) time units. Each job has a worst-case execution requirement equal to \(C_{i}\) and a deadline that occurs \(D_{i}\) time units after its arrival time. We refer to the interval, of size \(D_{i}\), between such a job's arrival instant and deadline as its _scheduling window_. We assume a fully _preemptive_ execution model: any executing job may be interrupted at any instant in time, and its execution resumed later with no cost or penalty. A _sporadic task system_ is comprised of several such sporadic tasks. Let \(\tau\) denote a system of such sporadic tasks: \(\tau=\{\tau_{1},\tau_{2},\ldots\tau_{n}\}\), with \(\tau_{i}=(C_{i},D_{i},T_{i})\) for all \(i\), \(1\leq i\leq n\). Task system \(\tau\) is said to be a _constrained_ sporadic task system if it is guaranteed that each task \(\tau_{i}\in\tau\) has its relative deadline parameter no larger than its period: \(D_{i}\leq T_{i}\), and an _implicit-deadline_ sporadic task system if \(D_{i}=T_{i}\) for all \(\tau_{i}\in\tau\). (Implicit-deadline systems are also known as _Liu and Layland_[22] task systems.) _In this paper, we restrict our attention to constrained and implicit-deadline task systems._

Schedulability.A real-time system implemented on a particular computing platform is said to be \(A\)-schedulable with respect to a given scheduling algorithm \(A\), if the algorithm \(A\) schedules the system such that all jobs of all tasks will meet all deadlines, under all permissible (also called _legal_) combinations of job-arrival sequences by the different tasks comprising the system. A _schedulability test_ for scheduling algorithm \(A\) (also called an _\(A\)-schedulability test_) accepts as input the specifications of a real-time system, and determines whether the system is \(A\)-schedulable or not. An \(A\)-schedulability test is said to be _exact_ if it correctly identifies all \(A\)-schedulable systems, and _sufficient_ if it may fail to identify some \(A\)-schedulable systems (it must guarantee, though, that all identified systems are indeed \(A\)-schedulable.)

Task and system characteristics.The concepts of task and system _utilization_ and _density_ prove useful in the analysis of sporadic task systems on multiprocessors. These concepts are defined as follows:

**Utilization:**: The utilization \(u_{i}\) of a task \(\tau_{i}\) is the ratio \(C_{i}/T_{i}\) of its execution time to its period. The total utilization \(u_{\mathrm{sum}}(\tau)\) and the largest utilization \(u_{\mathrm{max}}(\tau)\) of a task system \(\tau\) are defined as follows:

\[u_{\mathrm{sum}}(\tau)\stackrel{{\mbox{\tiny{\rm def}}}}{{=}} \sum_{\tau_{i}\in\tau}u_{i};\hskip 14.226378ptu_{\mathrm{max}}(\tau) \stackrel{{\mbox{\tiny{\rm def}}}}{{=}}\max_{\tau_{i}\in\tau}(u_ {i})\]
**Density:**: The density \(\delta_{i}\) of a task \(\tau_{i}\) is the ratio \(C_{i}/D_{i}\) of its execution time to its relative deadline. The total density \(\delta_{\mathrm{sum}}(\tau)\) and the largest density \(\delta_{\mathrm{max}}(\tau)\) of a task system \(\tau\) are defined as follows:

\[\delta_{\mathrm{sum}}(\tau)\stackrel{{\mbox{\tiny{\rm def}}}}{{=}} \sum_{\tau_{i}\in\tau}\delta_{i};\hskip 14.226378pt\delta_{\mathrm{max}}(\tau) \stackrel{{\mbox{\tiny{\rm def}}}}{{=}}\max_{\tau_{i}\in\tau}( \delta_{i})\]

An additional concept that plays a critical role in the schedulability analysis of sporadic task systems is that of **demand bound function**. For any interval length \(t\), the demand bound function \(\textsc{dbf}(\tau_{i},t)\) of a sporadic task \(\tau_{i}\) bounds the maximum cumulative execution requirement by jobs of \(\tau_{i}\) that both arrive in, and have deadlines within, any interval of length \(t\). It has been shown [9] that

\[\textsc{dbf}(\tau_{i},t)=\max\left(0,\left(\left\lfloor\frac{t-D_{i}}{T_{i}} \right\rfloor+1\right)C_{i}\right)\]

A **load** parameter, based upon the dbf function, may be defined for any sporadic task system \(\tau\) as follows:

\[\textsc{load}(\tau)\stackrel{{\mbox{\tiny{\rm def}}}}{{=}}\max_{t>0 }\left(\frac{\sum_{\tau_{i}\in\tau}\textsc{dbf}(\tau_{i},t)}{t}\right)\] Fixed job-priority (FJP) scheduling.Run-time scheduling algorithms are typically implemented as follows: at each time instant, a _priority_ is assigned to each job that has been released but not yet completed, and the available processors are allocated to the highest-priority jobs. In edf scheduling, jobs are assigned priorities according to their deadline parameters: the earlier the deadline of a job, the greater its priority.

It has long been known that global edf, in common with many other global scheduling schemes, suffers from the so-called Dhall effect [15] which results in task systems with arbitrarily low utilization and density not being edf-schedulable. In order to circumvent the Dhall effect, hybrid variants of edf have been designed [18] in which all the jobs of some selected tasks are assigned highest priority, and the remaining tasks' jobs are assigned priorities according to edf. Such priority-driven scheduling algorithms are instances of a class of algorithms called _fixed job-priority_ (FJP) scheduling algorithms. In FJP scheduling algorithms, the priority of a job may not change between its arrival time and the instant it completes execution; however, different jobs of the same task may have different priorities. (In contrast, fixed task-priority (FTP) algorithms require that all jobs of a task have the same -fixed- priority, while in dynamic-priority (DP) algorithms the priority of a job may change between its arrival time and its completion time. It is evident from these definitions that FJP scheduling is a generalization of FTP scheduling, and DP scheduling is a generalization of FJP scheduling.)

## 3 Global scheduling and Worst-case behavior

Recall that in order for a sporadic task system to be considered \(A\)-schedulable for a given scheduling algorithm \(A\), \(A\) must generate schedules meeting all deadlines for all legal job-arrival sequences of the task system. Since any sporadic task system has infinitely many different legal job arrival sequences, an approach of exhaustive enumeration of such sequences, followed by simulating algorithm \(A\) on each of these sequences, will not yield an effective schedulability test. Instead, the typical approach has been to identify one or a few _worst-case job arrival sequences_ for a task system for which it can be proved that if algorithm \(A\) successfully schedules all these worst-case job arrival sequences, then \(A\) is guaranteed to successfully schedule all legal job arrival sequences of the task system. For example, with respect to edf or Deadline-Monotonic (DM) scheduling upon preemptive uniprocessors it is known [22, 20, 9] that there is a unique worst-case job arrival sequence: every task has one job arrive at the same instant in time, and each task has subsequent jobs arrive as soon as legally permitted to do so. (Such a job arrival sequence is often called the _synchronous arrival sequence_ for the task system.) It has been shown [7, 17, 8] that the synchronous arrival sequence is also the worst-case job arrival sequence for partitioned multiprocessor edf and DM scheduling.

For global scheduling, however, the synchronous arrival sequence is not necessarily the worst-case arrival sequence, as the following example illustrates with respect to edf scheduling.

**Example 1**: Consider the task system comprised of the three tasks \(\tau_{1}=(1,1,2)\), \(\tau_{2}=(1,1,3)\), and \(\tau_{3}=(5,6,6)\), executing upon two unit-capacity processors. It may be seen (Figure 1 (a)) that the synchronous arrival sequence is successfully scheduled by edf to meet all deadlines. However, if task \(\tau_{1}\)'s second job were to arrive three, rather than two, time units after the first (Figure 1 (b)), then edf would miss some deadline over the interval \([0,6]\) (and indeed, no scheduling algorithm can possibly guarantee to meet all deadlines for this job arrival sequence). \(\blacksquare\)

Without knowing what the worst-case behavior of a sporadic task system may be, it is not possible to design simulation-based exact (necessary as well as sufficient) schedulability tests. To our knowledge, no finite collection of worst-case job arrival sequences has been identified for global scheduling of sporadic task systems. This, at a basic level, is the fundamental difference between our understanding of partitioned and global scheduling of sporadic task systems. As stated above, it is known that the synchronous arrival sequence represents the worst-case behavior of a task system under partitioned scheduling. Hence, partitioned schedulability testing can be solved in principle by determining whether it is possible to partition the tasks among the processors such that no deadlines are missed in the synchronous arrival sequence. An exact algorithm for solving this is provably highly intractable, but approximation algorithms that run in polynomial time and exhibit excellent average-case and provably bounded worst-case behavior have been devised [7, 17, 8].

In the global case, however, we do not know how to determine schedulability even if computational tractability were not an issue. That is, we do not yet have an adequate understanding of what precisely the characteristics of a globally schedulable system are; without knowing these characteristics, it seems futile to seek accurate, efficient tests for identifying such systems. (In this regard, Example 1 above illustrates that load is not an exact indicator of schedulability: while load\((\tau)\leq m\) is clearly necessary for \(\tau\) to be edf-schedulable on an \(m\)-processor platform, the task system in Example 1 illustrates that this is not sufficient.) 

## 4 Partitioned versus global FJP scheduling

As stated in Section 1 above, simulation experiments [4, 6] have shown that currently-known global schedulability tests perform poorly compared to partitioned schedulability tests. That is, it appears that a far greater fraction of randomly-generated sporadic task systems are deemed schedulable by currently-known partitioned schedulability tests than by currently-known global schedulability tests.

One might consider this result surprising, since at first glance it appears that partitioned scheduling (which forbids jobs from migrating between processors) is a special case of global scheduling (which allows, but does not require, such migration). However, this is erroneous. It has previously been shown by Leung and Whitehead [21, page 242] with regard to fixed task priority (FTP) scheduling schemes that there are sporadic task systems schedulable by some global algorithm but not by any partitioned algorithm, and that there are other sporadic task systems that are schedulable by some partitioned algorithm but not by any global algorithm. Theorem 1 below demonstrates similar incomparability between global and partitioned scheduling for the more general class of FJP scheduling algorithms as well.

As one might expect, there are systems that global algorithms can schedule but partitioned ones cannot; this is formally shown in Lemma 1 below. Somewhat counter-intuitively, it turns out (Lemma 2 below) that there are systems which partitioned FJP algorithms can schedule, which cannot be scheduled by any global FJP algorithm.

**Lemma 1**: _There are task systems that are schedulable using global FJP algorithms that partitioned FJP algorithms cannot schedule._

**Proof Sketch:** Here's an example task system, on \(2\) processors:

\[\tau_{1}=(2,2,3),\tau_{2}=(3,3,4),\tau_{3}=(5,12,12)\]

Clearly, this system cannot be scheduled using partitioning, since \(u_{1}+u_{2}\), \(u_{1}+u_{3}\), and \(u_{2}+u_{3}\) are each \(>1\). To show that a global FJP algorithm can schedule this task system, consider any FJP algorithm which assigns lowest priority to \(\tau_{3}\)'s jobs. Since there are two processors, \(\tau_{1}\) and \(\tau_{2}\)'s jobs are guaranteed to meet all deadlines. Now observe that each job of \(\tau_{3}\) needs to execute for \(5\) time-slots over an interval of \(12\) slots1. Now over any \(12\) contiguous slots, \(\tau_{1}\) may execute during at most \(8\) slots, thereby leaving at least \(4\) slots for \(\tau_{3}\)'s job upon one processor.

Footnote 1: For ease of exposition, we are assuming a slotted model of time for this proof sketch; however, it is easily generalized to a non-slotted model.

* If \(\tau_{1}\) executes for fewer than \(8\) slots between a job of \(\tau_{3}\)'s scheduling window, then it is straightforward to see that the job of \(\tau_{3}\) completes execution by its deadline, since no more than one other job (of \(\tau_{2}\)) will be active during the at least \(5\) time units of this job's scheduling window.
* If \(\tau_{1}\)'s jobs execute for exactly \(8\) slots during the scheduling window of one of \(\tau_{3}\)'s jobs, it is easily seen that \(\tau_{1}\)'s jobs must be arriving exactly 3 time-units apart. Hence, it is not possible that \(\tau_{3}\)'s jobs execute in parallel with \(\tau_{1}\)'s jobs during all \(8\) of the time-slots during which \(\tau_{1}\)'s jobs execute within this scheduling window. Therefore there are at least 5 slots within this scheduling window during which one of both processors is idle after both \(\tau_{1}\) and \(\tau_{2}\) have been scheduled.

Perhaps surprisingly, the converse of the above lemma is also true:

**Lemma 2**: _There are task systems that are schedulable using partitioned FJP algorithms that global FJP algorithms cannot schedule._

**Proof Sketch:** Here's an example task system, on \(2\) processors:

\[\tau_{1}=(2,2,3),\tau_{2}=(3,3,4),\tau_{3}=(4,12,12),\tau_{4}=(3,12,12)\]

This task system may be partitioned by assigning \(\tau_{1}\) and \(\tau_{3}\) to one processor and the other two tasks to the remaining

Figure 1: Figure for Example 1, illustrating that the synchronous arrival sequence does not represent the worst case.

processor, and scheduling each processor using uniprocessor edf.

To show that no global FJP priority assignment scheme can meet all deadlines, consider the synchronous arrival sequence over the interval \([0,12)\). It may be verified that whichever of \(\tau_{3}\)'s and \(\tau_{4}\)'s job has lower priority ends up missing its deadline while one processor goes idle over \([11,12)\). \(\blacksquare\)

Hence our intuition that global is a generalization of partitioned turns out to be incorrect for FJP scheduling as well as FTP scheduling:

**Theorem 1**: _Global and partitioned FJP scheduling are **incomparable**._

One implication of this is that the current state of the art -- partitioned schedulability tests being far superior to global ones -- are not contradicted by facts (only intuition). That is, it has not been ruled out that a far larger fraction of sporadic task systems are schedulable under partitioned FJP scheduling as compared to global FJP scheduling.

## 5 Global edf schedulability: Prior results

In this section, we provide brief summaries of currently-known tests for global edf-schedulability analysis of sporadic task systems. In addition, we highlight salient features and drawbacks of these tests; efforts to overcome these drawbacks will drive the design of the new test we propose in the next section.

**The density, [bak], and [bcl] tests.** The global multiprocessor scheduling of implicit-deadline (Liu and Layland) sporadic task systems was studied in [18]. It was shown that \([u_{\mathrm{sum}}(\tau)\leq m-(m-1)u_{\mathrm{max}}(\tau)]\) is a sufficient condition for implicit-deadline sporadic task system \(\tau\) to be global edf-schedulable upon \(m\) unit-capacity processors. Minor extensions to the proofs in [18] can be used to obtain the following sufficient global-edf schedulability test for constrained-deadline sporadic task systems:

\[\delta_{\mathrm{sum}}(\tau)\leq m-(m-1)\delta_{\mathrm{max}}(\tau)\;.\] (1)

This test is often referred to in the literature as the _density_ test for global edf-schedulability of sporadic task systems.

Meanwhile Baker [2, 3, 10] designed a test, based on some deep insights, for global-edf schedulability analysis. In essence, Baker's test - henceforth referred to here as the [bak] test - is obtained by assuming that a task \(\tau_{k}\)'s job misses its deadline, and then determining necessary conditions on the parameters of all the tasks that must be satisfied in order for such a deadline miss to occur. Then _negating_ these conditions for each \(\tau_{k}\) yields a sufficient test for global-edf schedulability.

In 2005, Bertogna et al. [10] used ideas very similar to Baker's to came up with a simpler test that occasionally outperformed both the density and the [bak] tests. The test from [10] will be referred to here as the [bcl] test.

Overview of the [bak] and [bcl] tests.Both tests are built around the following general strategy, first introduced by Baker [2]. Suppose that \(\tau\) is not global edf-schedulable, and consider a legal sequence of job requests of \(\tau\) on which global edf misses one or more deadlines. Suppose that a job of \(\tau_{k}\) is the first job that misses its deadline, at some time-instant \(t_{d}\). Both tests analyze the situation over some interval \([t_{o},t_{d})\), where \(t_{o}\) is different in the [bak] and [bcl] tests (and is precisely defined for each test). Both tests compute upper bounds on the amount of work that edf can be required to execute over the interval \([t_{o},t_{d})\), and obtain an unschedulability condition by setting this bound to be large enough to deny \(\tau_{k}\)'s job \(C_{k}\) units of execution over its scheduling window.

In bounding the total amount of work that each task \(\tau_{i}\) needs to have executed over \([t_{o},t_{d})\) in the edf schedule, one must consider **(i)** jobs of \(\tau_{i}\) that arrive within the interval, _and_ **(ii)** possibly one additional job that arrives prior to \(t_{o}\) but has not completed execution by time-instant \(t_{o}\) and hence "carries in" some execution into the interval. The contribution of jobs arriving within the interval may be computed using the demand bound abstraction (Section 2 above), but new techniques are needed for bounding the carry-in. Both the [bak] and [bcl] tests use different bounds on the amount of such work for each \(\tau_{i}\).

Differences between the [bak] and [bcl] tests.Despite the similarities in overall approach, the two tests differ quite significantly in the details:

1. In [bcl], \(t_{o}\) is set equal to \((t_{d}-D_{k})\); i.e., the arrival time of the job that misses its deadline. In [bak], it is set equal to the earliest time-instant prior to this job's arrival time, at which a certain condition2 is satisfied. Footnote 2: It is not essential for us to know what this condition is, in order to understand the remainder of this paper. Please consult [3] for details.
2. In [bcl], fairly primitive techniques are used to bound the amount of work that \(\tau_{i}\) may contribute to this interval, while [bak] uses a far more sophisticated analysis. Specifically, while [bak] is able to show that parts of "carry-in" jobs - jobs whose scheduling windows span \(t_{o}\) - must have completed execution before \(t_{o}\), [bcl] pessimistically assumes that each carry-in job executed as late as possible, immediately before their deadlines and hence carried in as much work as possible.
3. The length of the interval \([t_{o},t_{d})\) could be larger in the [bak] tests than in the [bcl] test. This is desir able since any additive inaccuracy introduced in computing bounds on the amount of work that must be executed over \([t_{o},t_{d})\) gets amortized over a larger interval. (However, a closer examination of the [bak] test indicates that this potential advantage is not exploited - a final step in the derivation of the [bak] test lower-bounds the size of the interval \([t_{o},t_{d})\) by \(D_{k}\), which is the value used by the [bcl] test as well.)

Comparison.Although the [bak] test employs considerably more sophisticated analysis than the [bcl] test, it does not unequivocally outperform the [bcl] test. Baker has conducted extensive simulation experiments comparing the density, [bak] and [bcl] tests. These simulations have demonstrated that all three tests are incomparable: there are task systems deemed edf-schedulable by each test but not by the other two tests. They also seem to demonstrate that the density and [bcl] tests, taken together, are able to cover most of the task systems that are handled by the [bak] test; in Baker's words (Email communication, February 2007) _it seems that many of the cases where my test does better than the [bcl] test are also cases where the density test works, and many of the cases where my test does better than the density test the [bcl] test also works._

Shortcomings common to both tests.The [bak] and [bcl] tests share certain shortcomings.

1. First, in analyzing a possible deadline miss for \(\tau_{k}\) both tests consider a "worst-case" scenario in which it is assumed that _every_ one of the \(n\) tasks in the system carries work into the interval that must be considered. In systems with a large number of tasks (\(n\gg m\)), this results in severe over-estimation of the cumulative carry-in. This is further aggravated by the feature of both tests - outlined above - of amortizing this carry-in over an interval of size \(D_{k}\). Due perhaps to these facts, our observation has been that _these tests tend to perform poorly on "non-uniform" task systems_: they are likely to flag as being not schedulable an inordinately large fraction of task systems in which different tasks' parameters are of different orders of magnitude.
2. Second, both tests have run-time polynomial in the representation of the task system: the [bcl] test runs in \(\mathcal{O}(n^{2})\) time and the [bak] test in \(\mathcal{O}(n^{3})\) time, where \(n\) is the number of tasks in the system. It may seem strange to refer to this low run-time complexity as a "shortcoming," but the fact is that, in real-time scheduling theory, _pseudo-polynomial_ run-time complexity is usually considered satisfactory for schedulability analysis; this is a consequence of the fact that task parameters are typically not too large in such systems. (For example, commonly-used exact uniprocessor edf[9, 24] and DM [19, 1] schedulability tests have pseudo-polynomial run-time.) It would be nice if the [bcl] and [bak] tests could be rendered more accurate by being allowed to run for pseudo-polynomial time; however, we are not aware of any technique that enables such a trade-off. So this low run-time complexity is a "shortcoming" in the sense that it provides a benefit (polynomial run-time) that is not particularly needed, and which we cannot trade in for a more needed benefit (greater accuracy).

## 6 An improved schedulability algorithm

We have designed a new global edf-schedulability test that overcomes some of these shortcomings of the [bak] and [bcl] tests. Our test possesses the following features that distinguishes it from the [bak] and [bcl] tests: _(i)_ it runs in time pseudo-polynomial in the representation of the task system; _(ii)_ it considers intervals \([t_{o},t_{d})\) that do not necessarily coincide with the scheduling window of the task \(\tau_{k}\) being assumed to miss its deadline; _(iii)_ it allows us to bound the number of tasks carrying in work into the interval \([t_{o},t_{d})\) at \((m-1)\), where \(m\) is the number of processors in the system. In contrast to the [bak] and [bcl] tests, it will be shown (Corollary 1) that our test generalizes the known exact edf-schedulability test on uniprocessors.

Our algorithm, like the [bcl] test, draws inspiration from the seminal work of Baker [2, 3] that yielded the [bak] test, and follows the same general framework. We consider each task \(\tau_{k}\) separately; when considering a specific \(\tau_{k}\), we identify sufficient conditions for ensuring that \(\tau_{k}\) cannot miss any deadlines. To ensure that no deadlines are missed by any task in \(\tau\), these conditions must be checked for each of the \(n\) tasks \(\tau_{1}\), \(\tau_{2},\ldots,\tau_{n}\).

Consider any legal sequence of job requests of task system \(\tau\), on which edf misses a deadline. Suppose that a job of task \(\tau_{k}\) is the one to first miss a deadline, and that this deadline miss occurs at time-instant \(t_{d}\) (see Figure 2). Let \(t_{a}\) denote this job's arrival time: \(t_{a}=t_{d}-D_{k}\).

Discard from the legal sequence of job requests all jobs with deadline \(>d_{k}\), and consider the edf schedule of the remaining (legal) sequence of job requests. Since later-deadline jobs have no effect on the scheduling of earlier-deadline ones under preemptive edf, it follows that a deadline miss of \(\tau_{k}\) occurs at time-instant \(t_{d}\) (and this is the earliest deadline miss), in this new edf schedule

Let \(t_{o}\) denote the latest time-instant \(\leq t_{a}\) at which at least one processor is idled in this edf schedule. Let \(A_{k}\stackrel{{\mbox{\tiny{\it def}}}}{{=}}t_{a}-t_{o}\).

As in [2, 3], our goal now is to identify conditions necessary for a deadline miss to occur; i.e., for \(\tau_{k}\)'s job to execute for strictly less than \(C_{k}\) time units over \([t_{a},t_{d})\). In order for \(\tau_{k}\)'s job to execute for strictly less than \(C_{k}\) time units over \([t_{a},t_{d})\), it is necessary that all \(m\) processors be executing jobs other than \(\tau_{k}\)'s job for strictly more than \((D_{k}-C_{k})\) time units over \([t_{a},t_{d})\). Let us denote by \(\Gamma_{k}\) a collection of intervals, not necessarily contiguous, of cumulative length \((D_{k}-C_{k})\) over \([t_{a},t_{d})\), during which all \(m\) processors are executing jobs other than \(\tau_{k}\)'s job in this edf schedule.

For each \(i\), \(1\leq i\leq n\), let \(I(\tau_{i})\) denote the contribution of \(\tau_{i}\) to the work done in this edf schedule during \([t_{o},t_{a})\bigcup\Gamma_{k}\). In order for the deadline miss to occur, it is necessary that the total amount of work that executes over \([t_{o},t_{a})\bigcup\Gamma_{k}\) satisfy the following condition

\[\sum_{\tau_{i}\in\tau}I(\tau_{i})>m\times(A_{k}+D_{k}-C_{k})\;;\] (2)

this follows from the observation that all \(m\) processors are, by definition, completely busy executing this work over the \(A_{k}\) time units in the interval \([t_{o},t_{a})\), as well as the intervals in \(\Gamma_{k}\) of total length \((D_{k}-C_{k})\).

It is important to understand exactly what Equation 2 means. Equation 2 represents necessary conditions for task \(\tau_{k}\) to miss a deadline \(A_{k}\) time units after an instant at which at least one processor is idled. _To show that a task system is edf-schedulable, it therefore suffices to demonstrate that for all tasks \(\tau_{k}\) and for all values of \(A_{k}\), Equation 2 cannot be satisfied._

Observe that the total length of the intervals in \([t_{o},t_{a})\bigcup\Gamma_{k}\) is equal to \((A_{k}+D_{k}-C_{k})\).

Let us say that \(\tau_{i}\) has a _carry-in job_ in this edf schedule if there is a job of \(\tau_{i}\) that arrives before \(t_{o}\) and has not computed execution by \(t_{o}\). In the following, we compute upper bounds on \(I(\tau_{i})\) if \(\tau_{i}\) has no carry-in job (this is denoted as \(I_{1}(\tau_{i})\)), or if it does (denoted as \(I_{2}(\tau_{i})\)).

Computing \(I_{1}(\tau_{i})\).If a task \(\tau_{i}\) contributes no carry-in work, then its contribution to this total amount of work that must execute over \([t_{o},t_{a})\bigcup\Gamma_{k}\) is generated by jobs arriving in, and having deadlines within, the interval \([t_{o},t_{d})\). Let us first consider \(i\neq k\); in that case, it follows from the definition of the demand bound function (dbf -- see Section 2 above) that the total work is at most dbf\((\tau_{i},A_{k}+D_{k})\); furthermore, this total contribution cannot exceed the total length of the intervals in \([t_{o},t_{a})\bigcup\Gamma_{k}\). Hence, the contribution of \(\tau_{i}\) to the total work that must be done by edf over \([t_{o},t_{a})\bigcup\Gamma_{k}\) is at most

\[\min(\textsc{dbf}(\tau_{i},A_{k}+D_{k}),A_{k}+D_{k}-C_{k}).\]

Now, consider the case \(i=k\). In that case, the job of \(\tau_{k}\) arriving at time-instant \(t_{a}\) does not contribute to the work that must be done by edf over \([t_{o},t_{a})\bigcup\Gamma_{k}\); hence, its execution requirement must be subtracted. Also, this contribution cannot exceed the length of the interval \([t_{o},t_{a})\); i.e., \(A_{k}\).

Putting these pieces together, we get the following bound on the contribution of \(\tau_{i}\) to the total work that must be done by edf over \([t_{o},t_{a})\bigcup\Gamma_{k}\):

\[\begin{split} I_{1}(\tau_{i})&\stackrel{{ \text{\tiny def}}}{{=}}\\ &\left\{\begin{array}{ll}\min(\textsc{dbf}(\tau_{i},A_{k}+D_{k} ),A_{k}+D_{k}-C_{k})&\text{if $i\neq k$}\\ \min(\textsc{dbf}(\tau_{i},A_{k}+D_{k})-C_{k},A_{k})&\text{if $i=k$} \end{array}\right.\end{split}\] (3)

Computing \(I_{2}(\tau_{i})\).Let us now consider the situation when \(\tau_{i}\) is active at \(t_{o}\), and hence potentially carries in some work. It was shown in [10] that the total work of \(\tau_{i}\) in this case can be upper-bounded by considering the scenario in which some job of \(\tau_{i}\) has a deadline at \(t_{d}\), and all jobs of \(\tau_{i}\) execute at the very end of their scheduling windows.

Let us denote as dbf\({}^{\prime}(\tau_{i},t)\) the amount of work that can be contributed by \(\tau_{i}\) over a contiguous interval of length \(t\), if some job of \(\tau_{i}\) has its deadline at the very end of the interval and each job of \(\tau_{i}\) executes during the \(C_{i}\) units immediately preceding its deadline. It is easily seen (see Figure 3) that there are exactly \(\lfloor t/T_{i}\rfloor\) complete jobs of \(\tau_{i}\) within this interval, and an amount \(\min(D_{i},t\bmod T_{i})\) of the scheduling window of an additional - carry-in - job.

Figure 3: Computing dbf\({}^{\prime}(\tau_{i},t)\).

Figure 2: Notation. A job of task \(\tau_{k}\) arrives at \(t_{a}\) and misses its deadline at time-instant \(t_{d}\). The latest time-instant prior to \(t_{a}\) when not all \(m\) processors are busy is denoted \(t_{o}\).

 This carry-in scheduling window may bring in at most \(C_{i}\) units of execution, yielding the following expression for \(\textsc{dbf}^{\prime}(\tau_{i},t)\):

\[\textsc{dbf}^{*}(\tau_{i},t)\stackrel{{\mbox{\tiny{def}}}}{{=}} \left\lfloor\frac{t}{T_{i}}\right\rfloor\times C_{i}+\min(C_{i},t\bmod T_{i})\] (4)

In computing \(\tau_{i}\)'s contribution to the total amount of work that must execute over \([t_{o},t_{a})\bigcup\Gamma_{k}\), let us first consider \(i\neq k\). In that case, it follows from the definition of the demand bound function (dbf', as defined above) that the total work is at most \(\textsc{dbf}^{\prime}(\tau_{i},A_{k}+D_{k})\); furthermore, this total contribution cannot exceed the total length of the intervals in \([t_{o},t_{a})\bigcup\Gamma_{k}\). Hence, the contribution of \(\tau_{i}\) to the total work that must be done by edf over \([t_{o},t_{a})\bigcup\Gamma_{k}\) is at most

\[\min(\textsc{dbf}^{\prime}(\tau_{i},A_{k}+D_{k}),A_{k}+D_{k}-C_{k}).\]

Now, consider the case \(i=k\). In that case, the job of \(\tau_{k}\) arriving at time-instant \(t_{a}\) does not contribute to the work that must be done by edf over \([t_{o},t_{a})\bigcup\Gamma_{k}\); hence, its execution requirement must be subtracted. Also, this contribution cannot exceed the length of the interval \([t_{o},t_{a})\); i.e., \(A_{k}\).

From the discussion above, we get the following bound on the contribution of \(\tau_{i}\) to the total work that must be done by edf over \([t_{o},t_{a})\bigcup\Gamma_{k}\):

\[I_{2}(\tau_{i})\stackrel{{\mbox{\tiny{def}}}}{{=}}\] \[\left\{\begin{array}{ll}\min(\textsc{dbf}^{\prime}(\tau_{i},A_{k }+D_{k}),A_{k}+D_{k}-C_{k})&\mbox{if $i\neq k$}\\ \min(\textsc{dbf}^{\prime}(\tau_{i},A_{k}+D_{k})-C_{k},A_{k})&\mbox{if $i=k$} \end{array}\right.\] (5)

Putting the pieces together.Let us denote by \(I_{\textsc{dif}}(\tau_{i})\) the difference between \(I_{2}(\tau_{i})\) and \(I_{1}(\tau_{i})\):

\[I_{\textsc{dif}}(\tau_{i})\stackrel{{\mbox{\tiny{def}}}}{{=}}I_{ 2}(\tau_{i})-I_{1}(\tau_{i})\] (6)

By definition of \(t_{o}\), at most \((m-1)\) tasks are active at time-instant \(t_{o}\). Consequently, _there are at most \((m-1)\) tasks \(\tau_{i}\) that contribute at amount \(I_{2}(\tau_{i})\), and the remaining \((n-m+1)\) tasks must contribute \(I_{1}(\tau_{i})\)_. Hence Equation 2 may be rewritten as follows:

\[\sum_{\tau_{i}\in\tau}I_{1}(\tau_{i})+\sum_{\mbox{\scriptsize the $(m-1)$ largest}}I_{\textsc{dif}}(\tau_{i})\\ >m(A_{k}+D_{k}-C_{k})\] (7)

Observe that all the terms in Equation 7 above are completely defined for a given task system, once a value is chosen for \(A_{k}\). Hence for a deadline miss of \(\tau_{k}\) to occur, there must exist some \(A_{k}\) such that Equation 7 is satisfied. Conversely, in order for all deadlines of \(\tau_{k}\) to be met it is sufficient that Equation 7 be violated for all values of \(A_{k}\). Theorem 2 follows immediately:

**Theorem 2**: _Task system \(\tau\) is edf-schedulable upon \(m\) unit-capacity processors if for all tasks \(\tau_{k}\in\tau\) and all \(A_{k}\geq 0\),_

\[\left(\sum_{\tau_{i}\in\tau}I_{1}(\tau_{i})+\sum_{\mbox{\scriptsize the $(m-1)$ largest}}I_{\textsc{dif}}(\tau_{i})\right)\\ \leq m(A_{k}+D_{k}-C_{k})\] (8)

_where \(I_{1}(\tau_{i})\) and \(I_{\textsc{dif}}(\tau_{i})\) are as defined in Equations 3 and 6 respectively. \(\blacksquare\)_

The earlier tests -- the density, [bak] and [bcl] tests -- are not exact even for uniprocessor systems (the special case when \(m=1\)). (This is also indicated by the fact that all these prior tests have polynomial run-time, while edf-schedulability analysis of sporadic task systems on uniprocessors is not known to be in polynomial time.) The following corollary asserts that our test is superior to earlier tests in this regard:

**Corollary 1**: _The edf schedulability test of Theorem 2 is a generalization of the exact uniprocessor edf schedulability test of [9]._

**Proof Sketch:** For \(m=1\), there are \((m-1)=0\) tasks that are active at time-instant \(t_{o}\); i.e., \(t_{o}\) is the classical "idle instant" of uniprocessor real-time scheduling theory. By adding \(C_{k}\) to both the LHS and the RHS of Condition 8, it can be shown that the LHS reduces to the sum of the demand bound functions of all tasks over an interval of size \(A_{k}+D_{k}\), and the RHS reduces to the interval length. Hence, when \(m=1\) Condition 8 is asserting that the cumulative processor demand over all intervals must not exceed the interval length, which is exactly what the uniprocessor edf schedulability test of [9] checks. \(\blacksquare\)

Corollary 1 does not imply that we have obtained an exciting new result showing that uniprocessor edf-schedulability analysis can be done in polynomial time; Section 6.1 shows that our algorithm has pseudo-polynomial run-time when system utilization is bounded.

### Run-time complexity

For given \(\tau_{k}\) and \(A_{k}\), it is easy to see that Condition 8 can be evaluated in time linear in \(n\):

* Compute \(I_{1}(\tau_{i})\), \(I_{2}(\tau_{i})\), and \(I_{\textsc{dif}}(\tau_{i})\) for each \(i\) -- total time is \(\mathcal{O}(n)\).
* Use linear-time selection [12] on \(\{I_{\textsc{dif}}(\tau_{1}),I_{\textsc{dif}}(\tau_{2}),\ldots,I_{\textsc{dif}} (\tau_{n})\}\) to determine the \((m-1)\) tasks that contribute to the second sum on the LHS.

How many values of \(A_{k}\) must be tested, in order for us to be able to ascertain that Condition 8 is satisfied for all \(A_{k}\geq 0\)? Theorem 3 below provides the answer.

 

**Theorem 3**: _If Condition 8 is to be violated for any \(A_{k}\), then it is violated for some \(A_{k}\) satisfying the condition below:_

\[A_{k}\leq\frac{C_{\Sigma}-D_{k}(m-U(\tau))+\sum_{i}(T_{i}-D_{i})U_{i}+mC_{k}}{m- U(\tau)}\] (9)

_where \(C_{\Sigma}\) denotes the sum of the \((m-1)\) largest \(C_{i}\)'s._

**Proof:** It is easily seen that \(I_{1}(\tau_{i})\leq\texttt{dbf}(\tau_{i},A_{k}+D_{k})\), and \(I_{2}(\tau_{i})\leq\texttt{dbf}(\tau_{i},A_{k}+D_{k})+C_{i}\). From this, it can be shown that the LHS of Condition 8 is \(\leq C_{\Sigma}+\sum_{\tau_{i}\in\tau}\texttt{dbf}(\tau_{i},A_{k}+D_{k})\).

For this to exceed the RHS of Condition 8, it is necessary that

\[C_{\Sigma}+\texttt{dbf}(\tau,A_{k}+D_{k})>m(A_{k}+D_{k}-C_{k})\] \[\Rightarrow\text{(bounding dbf using the technique of \@@cite[cite]{[\@@bibref{}{Dj}{}{}]})}\] \[C_{\Sigma}+(A_{k}+D_{k})U(\tau)+\sum_{i}(T_{i}-D_{i})U_{i}>m(A_{ k}+D_{k}-C_{k})\] \[\equiv\,C_{\Sigma}+D_{k}U(\tau)+\sum_{i}(T_{i}-D_{i})U_{i}-m(D_{k} -C_{k})>A_{k}(m-U(\tau))\] \[\equiv A_{k}\leq\frac{C_{\Sigma}-D_{k}(m-U(\tau))+\sum_{i}(T_{i}-D _{i})U_{i}+mC_{k}}{m-U(\tau)}\]

which is as claimed in the theorem. \(\blacksquare\)

It can also be shown that Condition 8 need only be tested at those values of \(A_{k}\) at which \(\texttt{dbf}(\tau_{i},A_{k}+D_{k})\) changes for some \(\tau_{i}\). Corollary 2 follows.

**Corollary 2**: _The condition in Theorem 2 above can be tested in time pseudo-polynomial in the task parameters, for all task systems \(\tau\) for which \(U(\tau)\) is bounded by a constant strictly less than the number of processors \(m\). \(\blacksquare\)_

Comparison to the [bak] and [bcl] tests.By design, our test runs slower than the [bak], [bcl], and density tests: our test has pseudo-polynomial run-time complexity while all the other tests have polynomial complexity. In practice, we would expect that all tests be used within a single framework: a system be first tested for schedulability using the polynomial-time tests, and only those that are not determined to be schedulable by any of these tests be subjected to our slower test.

It is fairly easy to construct task systems that are determined to be schedulable by only our test (and not the other tests); indeed, Corollary 1 above demonstrates that our test is the only one that is optimal upon uniprocessors (i.e., when \(m=1\)). Furthermore, preliminary simulation experiments indicate that our test significantly outperforms the other tests upon task systems in which

* The number of tasks \(n\) is significantly greater than the number of processors \(m\) (i.e., \(n\gg m\)). This is probably a consequence of the fact that our test only considers carry-in from \(m-1\) tasks, while all the prior tests must account for carry-in from all \(n\) tasks.
* The parameters of the different tasks may be of widely varying orders of magnitude. Once again, this is by design: our test was specifically designed to handle such systems.

## 7 Conclusions

Recently, much attention has been focused upon the scheduling of systems of recurring tasks on multiprocessor platforms. A fairly deep and detailed understanding has been obtained concerning the multiprocessor scheduling of Liu and Layland task systems (see, e.g., [13] for a survey).

Encouraged by this success, researchers have been considering multiprocessor scheduling of task systems represented using more general models. Here the record is not quite as positive - despite some recent successes, this field of study has not yielded many results. In particular, while some encouraging results have been obtained concerning partitioned scheduling, our knowledge of global scheduling remains rudimentary for recurring real-time task systems represented in models more general than the Liu and Layland model. One of the observations that has come out of all this research is that _global scheduling is fundamentally different from, and seems much more difficult than, partitioned scheduling._

In this paper, we have described some of our recent findings concerning global multiprocessor scheduling. We have attempted to identify and highlight some of the fundamental issues that render global schedulability analysis so difficult. Building upon the techniques of Baker [2, 3] and of Bertogna et al. [10], we have designed a global-edf schedulability test that is quite a bit more sophisticated than earlier tests, and that has overcome several of the deficiencies of these earlier tests.

## References

* [1]Audsley, N. C. _Flexible Scheduling in Hard-Real-Time Systems_. PhD thesis, Department of Computer Science, University of York, 1993.
* [2]Baker, T. Multiprocessor EDF and deadline monotonic schedulability analysis. In _Proceedings of the IEEE Real-Time Systems Symposium_ (December 2003), IEEE Computer Society Press, pp. 120-129.
* [3]Baker, T. P. An analysis of EDF schedulability on a multiprocessor. _IEEE Transactions on Parallel and Distributed Systems 16_, 8 (2005), 760-768.
* [4]Baker, T. P. Comparison of empirical success rates of global vs. partitioned fixed-priority and EDF scheduling for hard real time. Tech. Rep. TR-050601,Department of Computer Science, Florida State University, 2005.
* [5]Baker, T. P. An analysis of fixed-priority schedulability on a multiprocessor. _Real-Time Systems: The International Journal of Time-Critical Computing 32_, 1-2 (2006), 49-71.
* [6]Baker, T. P. A comparison of global and partitioned EDF schedulability tests for multiprocessors. In _Proceeding of the International Conference on Real-Time and Network Systems_ (Poitiers, France, 2006).
* [7]Baruah, S., and Fisher, N. The partitioned multiprocessor scheduling of sporadic task systems. In _Proceedings of the IEEE Real-Time Systems Symposium_ (Miami, Florida, December 2005), IEEE Computer Society Press.
* [8]Baruah, S., and Fisher, N. The partitioned multiprocessor scheduling of deadline-constrained sporadic task systems. _IEEE Transactions on Computers 55_, 7 (July 2006), 918-923.
* [9]Baruah, S., Mok, A., and Rosier, L. Preemptively scheduling hard-real-time sporadic tasks on one processor. In _Proceedings of the 11th Real-Time Systems Symposium_ (Orlando, Florida, 1990), IEEE Computer Society Press, pp. 182-190.
* [10]Bertogna, M., Cirinei, M., and Lipari, G. Improved schedulability analysis of EDF on multiprocessor platforms. In _Proceedings of the EuroMicro Conference on Real-Time Systems_ (Palma de Mallorca, Balearic Islands, Spain, July 2005), IEEE Computer Society Press, pp. 209-218.
* [11]Bertogna, M., Cirinei, M., and Lipari, G. New schedulability tests for real-time tasks sets scheduled by deadline monotonic on multiprocessors. In _Proceedings of the 9th International Conference on Principles of Distributed Systems_ (Pisa, Italy, December 2005), IEEE Computer Society Press.
* [12]Blum, M., Floyd, R. W., Pratt, V., Rivest, R. L., and Tarjan, R. E. Time bounds for selection. _Journal of Computer and System Sciences 7_, 4 (Aug. 1973), 448-461.
* [13]Carpenter, J., Funk, S., Holman, P., Srinivasan, A., Anderson, J., and Baruah, S. A categorization of real-time multiprocessor scheduling problems and algorithms. In _Handbook of Scheduling: Algorithms, Models, and Performance Analysis_, J. Y.-T. Leung, Ed. CRC Press LLC, 2003.
* [14]Dertouzos, M. Control robotics : the procedural control of physical processors. In _Proceedings of the IFIP Congress_ (1974), pp. 807-813.
* [15]Dhall, S. _Scheduling Periodic Time-Critical Jobs on Single Processor and Multiprocessor Systems_. PhD thesis, Department of Computer Science, The University of Illinois at Urbana-Champaign, 1977.
* [16]Fisher, N., and Baruah, S. Global static-priority scheduling of sporadic task systems on multiprocessor platforms. In _Proceeding of the IASTED International Conference on Parallel and Distributed Computing and Systems_ (Dallas, TX, November 2006), IASTED.
* [17]Fisher, N., Baruah, S., and Baker, T. The partitioned scheduling of sporadic tasks according to static priorities. In _Proceedings of the EuroMicro Conference on Real-Time Systems_ (Dresden, Germany, July 2006), IEEE Computer Society Press.
* [18]Goossens, J., Funk, S., and Baruah, S. Priority-driven scheduling of periodic task systems on multiprocessors. _Real Time Systems 25_, 2-3 (2003), 187-205.
* [19]Joseph, M., and Pandya, P. Finding response times in a real-time system. _The Computer Journal 29_, 5 (Oct. 1986), 390-395.
* [20]Leung, J., and Merrill, M. A note on the preemptive scheduling of periodic, real-time tasks. _Information Processing Letters 11_ (1980), 115-118.
* [21]Leung, J., and Whitehead, J. On the complexity of fixed-priority scheduling of periodic, real-time tasks. _Performance Evaluation 2_ (1982), 237-250.
* [22]Liu, C., and Layland, J. Scheduling algorithms for multiprogramming in a hard real-time environment. _Journal of the ACM 20_, 1 (1973), 46-61.
* [23]Mok, A. K. _Fundamental Design Problems of Distributed Systems for The Hard-Real-Time Environment_. PhD thesis, Laboratory for Computer Science, Massachusetts Institute of Technology, 1983. Available as Technical Report No. MIT/LCS/TR-297.
* [24]Ripoll, I., Crespo, A., and Mok, A. K. Improvement in feasibility testing for real-time tasks. _Real-Time Systems: The International Journal of Time-Critical Computing 11_ (1996), 19-39.
```
'''

# query = '''what is the workload model in this paper?'''
print_counter = 1
for step in agent.stream(
    {"messages": [{"role": "user", "content": query}]},
    stream_mode="values",
):
    start_string = "_human"
    if print_counter == 1:
        start_string =  "_human"
        print_counter += 1
    elif print_counter == 2:
        start_string = "_ai"
    
    print_to_file(start_string=start_string, message=step["messages"][-1].content)


    step["messages"][-1].pretty_print()