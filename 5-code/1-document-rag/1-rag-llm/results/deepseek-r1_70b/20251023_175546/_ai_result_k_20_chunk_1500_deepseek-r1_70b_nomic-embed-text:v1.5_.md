

### Workload Model
The workload model consists of **n periodic tasks** denoted as \( \tau_1, \tau_2, \ldots, \tau_n \), each with the following parameters:
- **Worst-case execution time (WCET):** \( C_i \) for task \( \tau_i \).
- **Period:** \( T_i \) for task \( \tau_i \), which is the minimum time between consecutive arrivals of the task.
- **Relative deadline:** \( D_i = T_i \) for implicit deadlines, meaning each task must complete within its period.

Tasks are **independent** and preemptive. Each task arrives periodically and requires \( C_i \) units of execution time per period.

---

### Resource Model
The system consists of **m identical processors**. Each processor executes tasks according to a scheduler, and there is no shared memory or communication overhead between tasks.

---

### Scheduler
The scheduler implements the **Earliest Deadline First (EDF)** policy in a global scheduling framework:
- At any time, the task with the earliest absolute deadline is selected for execution.
- Tasks can migrate between processors to balance the workload.

This differs from partitioned scheduling, where tasks are statically assigned to processors and scheduled using uniprocessor EDF.

---

### Analysis Framework
The analysis framework ensures that all tasks meet their deadlines under global EDF scheduling. The key constraints or invariants are derived from the following:

1. **Utilization Bound for Global EDF:**
   For a system of \( n \) tasks on \( m \) processors, the total utilization must satisfy:
   $$
   U = \sum_{i=1}^n \frac{C_i}{T_i} \leq m
   $$

2. **Response-Time Analysis (RTA):**
   For each task \( \tau_k \), the worst-case response time \( R_k \) is computed iteratively using:
   $$
   R_k^{(0)} = C_k
   $$
   $$
   R_k^{(i+1)} = C_k + \sum_{\substack{j=1 \\ T_j \leq T_k}}^n \left\lceil \frac{R_k^{(i)}}{T_j} \right\rceil C_j
   $$
   The task is schedulable if \( R_k = D_k \).

3. **Deadline Miss Condition:**
   If a job of \( \tau_k \) misses its deadline at time \( t_d \), the total workload in the interval \([t_a, t_d)\) must exceed the available processing capacity:
   $$
   \sum_{i=1}^n I(\tau_i) > m \cdot (A_k + D_k - C_k)
   $$
   Where:
   - \( A_k \): Time between the last idle instant and the arrival of \( \tau_k \).
   - \( I(\tau_i) \): Work contributed by task \( \tau_i \) in the interval.

4. **Necessary Condition for Deadline Miss:**
   For a deadline miss to occur, the total interference from other tasks must exceed:
   $$
   \sum_{i=1}^n \left\lfloor \frac{D_k}{T_i} \right\rfloor C_i > m \cdot D_k - C_k
   $$

5. **Schedulability Test:**
   The system is schedulable if all tasks pass the response-time analysis:
   $$
   R_k \leq D_k \quad \forall k = 1, 2, \ldots, n
   $$

---

### Key Constraints or Invariants
The following constraints ensure correct scheduling:

1. **Utilization Constraint:**
   The total CPU utilization must not exceed the number of processors:
   $$
   U = \sum_{i=1}^n \frac{C_i}{T_i} \leq m
   $$

2. **Response-Time Constraint:**
   For each task \( \tau_k \), its worst-case response time must meet its deadline:
   $$
   R_k \leq D_k
   $$

3. **No Overlap of Task Execution:**
   Tasks are preemptive, and their execution does not overlap on the same processor.

4. **Earliest Deadline First Priority:**
   The task with the earliest absolute deadline is always executed first.

5. **Workload Limitation:**
   In any interval of length \( t \), the total workload of all tasks must not exceed \( m \cdot t \):
   $$
   \sum_{i=1}^n \min(T_i, t) \cdot \frac{C_i}{T_i} \leq m \cdot t
   $$

---

### Notation Summary
- \( n \): Number of tasks.
- \( m \): Number of processors.
- \( C_i \): Worst-case execution time of task \( \tau_i \).
- \( T_i \): Period (and relative deadline) of task \( \tau_i \).
- \( D_k \): Absolute deadline of the job of \( \tau_k \).
- \( U \): Total CPU utilization.
- \( R_k \): Worst-case response time of task \( \tau_k \).
- \( A_k \): Time between the last idle instant and the arrival of \( \tau_k \).
- \( I(\tau_i) \): Work contributed by task \( \tau_i \) in a given interval.