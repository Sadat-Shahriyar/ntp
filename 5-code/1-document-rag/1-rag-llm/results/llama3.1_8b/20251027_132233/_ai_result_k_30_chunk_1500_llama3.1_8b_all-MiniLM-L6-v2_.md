**Workload Model**

The workload model used in this research paper is a periodic task set with sporadic tasks. The tasks are characterized by their:

* Period (T) - the minimum time between two consecutive releases of a task
* Execution Time (C) - the worst-case execution time of a task
* Deadline (D) - the maximum time allowed for a task to complete its execution

The workload model is described as follows:
```markdown
A = {τ1, τ2, ..., τn}
where each τi = < C_i, T_i, D_i > represents a periodic task with worst-case execution time Ci, period Ti, and deadline Di.
```
**Resource Model**

The resource model used in this paper is a single-core processor with a fixed number of processing units (PU). The processor has the following characteristics:

* Processing capacity (M) - the maximum number of tasks that can be executed concurrently
* Execution time (C) - the worst-case execution time of a task

The resource model is described as follows:
```markdown
R = < M, C >
```
**Scheduler**

The scheduler used in this paper is the Earliest Deadline First (EDF) scheduling algorithm. The EDF scheduler assigns tasks to the processor based on their deadlines.

**Analysis Framework**

The analysis framework used in this paper is a response-time analysis framework that uses the following equations:

$$
\begin{aligned}
& R_i = C_i + \sum_{j=1}^{n} \left( \frac{C_j}{M} \right) \cdot U_j \\
& U_j = \max \left( 0, \min \left( \frac{T_j}{T_i}, \frac{D_j - R_j}{T_i} \right) \right)
\end{aligned}
$$

where Ri is the response time of task τi, Cj and Tj are the execution time and period of task τj, M is the processing capacity, Uj is the utilization of task τj.

**System Constraints or Invariants**

The following system constraints or invariants are extracted from the paper:

* **Lemma 1**: For any task τi, if Ri ≤ Di, then the deadline of τi is met.
* **Theorem 1**: If the workload model A and resource model R satisfy the following conditions:
$$
\begin{aligned}
& \sum_{i=1}^{n} C_i / M < 1 \\
& \forall i, j: T_j > T_i \implies D_j > D_i
\end{aligned}
$$

then the EDF scheduler guarantees that all deadlines are met.

* **Constraint 1**: For any task τi, the following constraint must hold:
$$
R_i \leq D_i
$$

This constraint ensures that the response time of each task is less than or equal to its deadline.

* **Constraint 2**: The processing capacity M must satisfy the following condition:
$$
M > \sum_{i=1}^{n} C_i / T_i
$$

This constraint ensures that the processor has sufficient capacity to execute all tasks within their periods.

**Notation and Symbol Explanation**

* A: workload model (set of periodic tasks)
* R: resource model (single-core processor with fixed processing capacity M)
* τi: task i (periodic task with worst-case execution time Ci, period Ti, and deadline Di)
* C: worst-case execution time
* T: period
* D: deadline
* M: processing capacity
* EDF: Earliest Deadline First scheduling algorithm
* Ri: response time of task τi
* Uj: utilization of task τj