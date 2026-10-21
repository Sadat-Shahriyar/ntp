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
        """You are a helpful AI assistant. Use the following context in your response: """
        f"\n\n{docs_content}"
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