
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
