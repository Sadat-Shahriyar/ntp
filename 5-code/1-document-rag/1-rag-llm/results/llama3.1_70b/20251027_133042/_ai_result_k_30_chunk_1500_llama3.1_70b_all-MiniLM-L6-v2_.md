**Workload Model**
===============

The workload model used in this research paper is a sporadic task model with precedence constraints. The tasks are characterized by their:

* Arrival patterns: Sporadic, with a minimum inter-arrival time of $T_i$
* Execution times: Worst-case execution time (WCET) of $C_i$ and best-case execution time (BCET) of $c_i$
* Deadlines: Relative deadline of $D_i$
* Precedence constraints: Tasks have precedence relationships, represented by a directed acyclic graph (DAG)

**Resource Model**
================

The resource model consists of a heterogeneous multi-core processor with:

* Multiple cores: Each core has a different processing capacity, represented by $\pi_j$ for core $j$
* Communication channels: Tasks can communicate with each other through a shared bus with a bandwidth constraint of $B$

**Scheduler**
=============

The scheduler used is an Earliest Deadline First (EDF) scheduler with a fixed priority assignment. The priorities are assigned based on the task's deadline and criticality level.

**Analysis Framework**
=====================

The analysis framework uses response-time analysis to determine whether the system is schedulable under the given workload, resource model, and scheduler. The framework provides timing guarantees and detects potential deadline misses.

**System Constraints or Invariants**
=====================================

### Lemma 1: Response-Time Analysis

$$
\begin{aligned}
R_i &= C_i + \sum_{j \in hp(i)} \left\lceil \frac{R_i}{T_j} \right\rceil C_j \\
&+ \max_{k \in cp(i)} \left( \frac{C_k}{B} + \frac{L_k}{\pi_{core(k)}} \right)
\end{aligned}
$$

* $R_i$: Response time of task $\tau_i$
* $C_i$: WCET of task $\tau_i$
* $hp(i)$: Set of tasks with higher priority than task $\tau_i$
* $cp(i)$: Set of tasks that communicate with task $\tau_i$
* $T_j$: Minimum inter-arrival time of task $\tau_j$
* $B$: Bandwidth constraint of the shared bus
* $L_k$: Size of the message sent by task $\tau_k$
* $\pi_{core(k)}$: Processing capacity of the core executing task $\tau_k$

This lemma provides an upper bound on the response time of each task, taking into account the execution times, deadlines, and communication constraints.

### Theorem 1: Schedulability Condition

$$
\sum_{i=1}^n \frac{C_i}{T_i} + \max_{k \in cp(i)} \left( \frac{L_k}{B} + \frac{C_k}{\pi_{core(k)}} \right) \leq 1
$$

* $n$: Number of tasks in the system
* $C_i$: WCET of task $\tau_i$
* $T_i$: Minimum inter-arrival time of task $\tau_i$
* $L_k$: Size of the message sent by task $\tau_k$
* $B$: Bandwidth constraint of the shared bus
* $\pi_{core(k)}$: Processing capacity of the core executing task $\tau_k$

This theorem provides a sufficient condition for schedulability, ensuring that the system can meet all deadlines under the given workload and resource constraints.

### Constraint 1: Deadline Monotonicity

$$
D_i \leq D_j \implies T_i \geq T_j
$$

* $D_i$: Relative deadline of task $\tau_i$
* $T_i$: Minimum inter-arrival time of task $\tau_i$

This constraint ensures that tasks with earlier deadlines have longer minimum inter-arrival times, allowing the scheduler to prioritize them accordingly.

### Constraint 2: Precedence Constraints

$$
\forall (i,j) \in E: T_i + C_i \leq T_j
$$

* $E$: Set of precedence constraints between tasks
* $T_i$: Minimum inter-arrival time of task $\tau_i$
* $C_i$: WCET of task $\tau_i$

This constraint ensures that the scheduler respects the precedence relationships between tasks, ensuring that a task is not executed before its predecessors have completed.