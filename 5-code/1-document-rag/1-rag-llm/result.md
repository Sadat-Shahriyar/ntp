### Workload Model
The workload model in this research paper involves a system of sporadic tasks. Each task $\tau_i$ is characterized by three parameters: worst-case execution time $C_i$, relative deadline $D_i$, and minimum inter-arrival separation (period) $T_i$. The tasks are constrained such that the relative deadline $D_i$ is no larger than the period $T_i$ for each task. This ensures that the system adheres to a constrained sporadic task model.

### Resource Model
The resource model consists of $m$ identical processors. These processors execute tasks in a fully preemptive manner, meaning any executing job can be interrupted at any time and resumed later without any cost or penalty. The scheduling algorithm used is Earliest Deadline First (EDF), which assigns priorities to jobs based on their deadlines.

### Scheduler
The scheduler implements the EDF policy, where each job's priority is determined by its deadline. Jobs with earlier deadlines have higher priority. This is a dynamic-priority scheduling algorithm because the priority of a job can change over time as new jobs arrive and deadlines approach.

### Analysis Framework
The analysis framework involves determining whether the task system $\tau$ is EDF-schedulable on $m$ processors. The key condition for schedulability is based on the demand bound function, which calculates the maximum processor utilization required by each task over any interval of length $L$. For a task $\tau_k$, the demand bound function is given by:
$$
\text{DBF}_k(L) = \max\left(0, \left\lfloor \frac{L}{T_k} \right\rfloor + 1\right) \cdot C_k - \max(0, L - D_k)
$$

The system is schedulable if the sum of the demand bound functions for all tasks over any interval $L$ does not exceed the total processor capacity available in that interval. Specifically, for each task $\tau_k$, we need to check:
$$
\sum_{i=1}^n \text{DBF}_i(A_k + D_k) \leq m(A_k + D_k)
$$

### System Constraints or Invariants with Explanations

1. **Task Parameters**:
   - $C_i$: Worst-case execution time of task $\tau_i$.
   - $D_i$: Relative deadline of task $\tau_i$, where $D_i \leq T_i$ (constrained sporadic task model).
   - $T_i$: Minimum inter-arrival separation (period) of task $\tau_i$.

2. **Demand Bound Function**:
   - $\text{DBF}_k(L)$: Maximum processor utilization required by task $\tau_k$ over any interval of length $L$.
     - $\left\lfloor \frac{L}{T_k} \right\rfloor + 1$: Number of job arrivals of $\tau_k$ in an interval of length $L$.
     - $\max(0, L - D_k)$: Adjustment to account for the deadline constraint.

3. **Schedulability Condition**:
   - For each task $\tau_k$, and for all values of $A_k$, the following must hold:
     $$
     \sum_{i=1}^n \text{DBF}_i(A_k + D_k) \leq m(A_k + D_k)
     $$

4. **Processor Utilization**:
   - The total processor utilization required by all tasks in any interval of length $A_k + D_k$ must not exceed the available processing capacity, which is $m(A_k + D_k)$.

5. **Necessary and Sufficient Condition**:
   - The condition ensures that no task $\tau_k$ will miss its deadline when scheduled under EDF on $m$ processors.

6. **Fully Preemptive Execution**:
   - Jobs can be preempted at any time, allowing higher-priority jobs to execute immediately upon arrival.

7. **EDF Priority Assignment**:
   - Jobs are assigned priorities based on their deadlines, with earlier deadlines having higher priority.

8. **Constrained Sporadic Task Model**:
   - Ensures that $D_i \leq T_i$ for all tasks $\tau_i$, which simplifies the analysis and guarantees certain properties of the system.

These constraints and invariants ensure that the task system is schedulable under EDF on $m$ processors, guaranteeing that no deadlines are missed.