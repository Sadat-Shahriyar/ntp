

### Workload Model
The workload model in this paper involves **sporadic tasks**, which are defined by their worst-case execution time (WCET), periods, and deadlines. Each task $\tau_i$ is characterized by:
- $C_i$: Worst-case execution time.
- $T_i$: Period (minimum interval between consecutive arrivals).
- $D_i$: Relative deadline.

Tasks arrive sporadically, meaning the first job of a task can arrive at any time, but subsequent jobs are separated by at least $T_i$ time units. The system is analyzed under the assumption that tasks have constrained deadlines ($D_i \leq T_i$).

### Resource Model
The resource model consists of:
- **Multiprocessor platform**: A set of $m$ identical processors.
- **Shared memory**: Tasks may share memory for communication, but this is not explicitly modeled in the scheduling framework.

Processors are preemptive and can execute tasks simultaneously. The focus is on global scheduling algorithms where tasks can migrate between processors.

### Scheduler
The scheduler analyzed in the paper is a **global EDF (Earliest Deadline First)** algorithm. Key features of the scheduler include:
- Tasks are prioritized based on their absolute deadlines.
- At any time, the $m$ tasks with the earliest deadlines are selected to execute on the $m$ processors.

### Analysis Framework
The analysis framework focuses on proving schedulability and identifying necessary and sufficient conditions for task sets to be schedulable under global EDF. Key components include:
1. **Response-Time Analysis (RTA)**: Computes the worst-case response time of each task.
2. **Utilization Tests**: Sufficient but not necessary conditions based on task utilization.
3. **Theorem Proofs**: Establishes bounds and constraints for schedulability.

---

### System Constraints and Invariants

#### 1. **Task Utilization Constraint**
$$
\sum_{i=1}^{n} \frac{C_i}{T_i} \leq m
$$
- **Explanation**:
  - $\sum_{i=1}^{n} \frac{C_i}{T_i}$: Total CPU utilization of all tasks.
  - $m$: Number of processors.
  - This is a necessary condition for schedulability under any scheduling algorithm.

#### 2. **Response-Time Analysis Bound**
$$
R_k = C_k + \sum_{\tau_j \in hp(k)} \left\lceil \frac{R_k}{T_j} \right\rceil C_j
$$
- **Explanation**:
  - $R_k$: Worst-case response time of task $\tau_k$.
  - $C_k$: Worst-case execution time of task $\tau_k$.
  - $hp(k)$: Set of tasks with priority higher than $\tau_k$ (under EDF, tasks with earlier deadlines).
  - This equation iteratively computes the worst-case response time considering preemption by higher-priority tasks.

#### 3. **Deadline Miss Condition**
$$
R_k > D_k
$$
- **Explanation**:
  - If the computed worst-case response time $R_k$ exceeds the deadline $D_k$, task $\tau_k$ is not schedulable under EDF.
  - This is a necessary and sufficient condition for schedulability.

#### 4. **Global Schedulability Theorem**
$$
\forall \tau_k, R_k \leq D_k
$$
- **Explanation**:
  - For the task set to be schedulable under global EDF, all tasks must meet their deadlines ($R_k \leq D_k$).
  - This is derived from the response-time analysis.

#### 5. **Processor Busy Interval Constraint**
$$
\sum_{\tau_i \in \tau} I(\tau_i) > m \times (A_k + D_k - C_k)
$$
- **Explanation**:
  - $I(\tau_i)$: Work contributed by task $\tau_i$ during the interval.
  - $A_k$: Time after which task $\tau_k$ misses its deadline.
  - $D_k$: Deadline of task $\tau_k$.
  - $C_k$: Worst-case execution time of task $\tau_k$.
  - This condition ensures that all processors are busy executing tasks during the interval, leading to a deadline miss for $\tau_k$.

#### 6. **Necessary Condition for Deadline Miss**
$$
\sum_{\tau_i \in \tau} I(\tau_i) > m \times (A_k + D_k - C_k)
$$
- **Explanation**:
  - This is a necessary condition for task $\tau_k$ to miss its deadline $D_k$ after an idle time of $A_k$ on one processor.
  - The total work executed during the interval exceeds the available processing capacity.

#### 7. **Schedulability Invariant**
$$
\forall \tau_k, \exists t \in [0, T_k], R_k(t) \leq D_k
$$
- **Explanation**:
  - For all tasks $\tau_k$, there exists a time $t$ within one period $T_k$ where the response time $R_k(t)$ does not exceed the deadline $D_k$.
  - This ensures that the task system is schedulable over all possible job arrival sequences.

---

### Summary
The paper focuses on **global EDF scheduling** for **sporadic tasks** on a **multiprocessor platform**. The analysis framework uses **response-time analysis** and **utilization bounds** to derive necessary and sufficient conditions for schedulability. Key constraints include task utilization, response-time bounds, and deadline miss conditions.