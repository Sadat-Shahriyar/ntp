

### 1. Workload Model, Resource Model, Scheduler, and Analysis Framework

#### **Workload Model**
The workload model in this paper consists of **sporadic tasks** with the following characteristics:
- Each task \( \tau_i \) is represented by a tuple \( (C_i, D_i, T_i) \), where:
  - \( C_i \): Worst-case execution time.
  - \( D_i \): Relative deadline (the time after arrival by which the task must complete).
  - \( T_i \): Minimum inter-arrival time (period).
- Tasks are **sporadic**, meaning successive job arrivals are separated by at least \( T_i \).
- The system is a **constrained sporadic task system**, ensuring \( D_i \leq T_i \) for all tasks.

#### **Resource Model**
The resource model consists of:
- A platform with \( m \) identical processors, each with unit processing capacity.
- Processors are fully preemptive, meaning any executing job can be interrupted and resumed later without penalty.

#### **Scheduler**
The scheduler used is **global EDF (Earliest Deadline First)**:
- All tasks are scheduled globally across the \( m \)-processor platform.
- Tasks are prioritized based on their absolute deadlines, with earlier deadlines receiving higher priority.
- The system assumes a fully preemptive execution model.

#### **Analysis Framework**
The analysis framework provides schedulability tests to determine whether a task system is guaranteed to meet all deadlines. Key components include:
1. **Demand Bound Function (DBF)**: For any interval length \( t \), the DBF of a task \( \tau_i \) is defined as:
   $$
   \text{DBF}(\tau_i, t) = \max\left(0, \left\lfloor \frac{t - D_i}{T_i} \right\rfloor + 1\right) C_i
   $$
   This function bounds the maximum cumulative execution requirement of jobs of \( \tau_i \) that both arrive in and have deadlines within any interval of length \( t \).

2. **Schedulability Test**: The paper introduces a global EDF schedulability test (Theorem 2) to determine whether a task system is schedulable on \( m \)-processors.

---

### 2. System Constraints or Invariants

#### **1. Necessary Condition for Deadline Miss (Equation 2)**  
$$
\sum_{\tau_i \in \tau} I(\tau_i) > m \cdot (A_k + B_k)
$$
- **Meaning**: This is a necessary condition for a task \( \tau_k \) to miss its deadline. Here:
  - \( I(\tau_i) \): Contribution of task \( \tau_i \) to the overload.
  - \( A_k, B_k \): Parameters related to the task \( \tau_k \)'s execution and scheduling window.

#### **2. Sufficient Condition for EDF-Schedulability (Theorem 2)**  
$$
\sum_{i=1}^n I_1(\tau_i) + \sum_{j=1}^{m-1} I_{\text{diff}}(\tau_j) \leq m \cdot t
$$
- **Meaning**: This is a sufficient condition for the task system \( \tau \) to be EDF-schedulable on \( m \)-processors. Here:
  - \( I_1(\tau_i) \): Contribution of task \( \tau_i \) without considering carry-in jobs.
  - \( I_{\text{diff}}(\tau_j) \): Contribution of tasks with carry-in jobs.
  - \( t \): The interval length being analyzed.

#### **3. Demand Bound Function (DBF)**  
$$
\text{DBF}(\tau_i, t) = \max\left(0, \left\lfloor \frac{t - D_i}{T_i} \right\rfloor + 1\right) C_i
$$
- **Meaning**: This function calculates the maximum execution requirement of task \( \tau_i \) over any interval of length \( t \). It ensures that the task's jobs arriving in and having deadlines within \( t \) do not exceed their worst-case execution requirements.

#### **4. Density and Utilization Bounds**  
- **Density**: The density \( \delta_i \) of a task \( \tau_i \) is defined as:
  $$
  \delta_i = \frac{C_i}{D_i}
  $$
  - **Meaning**: This represents the ratio of the task's execution time to its relative deadline.
- **Total Density**:
  $$
  \delta_{\text{sum}}(\tau) = \sum_{\tau_i \in \tau} \delta_i
  $$
- **Maximum Density**:
  $$
  \delta_{\text{max}}(\tau) = \max_{\tau_i \in \tau} \delta_i
  $$

#### **5. Utilization Parameters**  
- **Total Utilization**:
  $$
  u_{\text{sum}}(\tau) = \sum_{\tau_i \in \tau} u_i, \quad u_i = \frac{C_i}{T_i}
  $$
- **Maximum Utilization**:
  $$
  u_{\text{max}}(\tau) = \max_{\tau_i \in \tau} u_i
  $$

#### **6. Load Parameter**  
The load parameter is defined based on the DBF function and ensures that:
$$
\text{LOAD}(\tau) \leq m
$$
- **Meaning**: While this is a necessary condition for schedulability, it is not sufficient.

---

### Summary of Constraints
These constraints ensure that the task system \( \tau \) can be scheduled correctly on an \( m \)-processor platform using global EDF scheduling. The key invariants are:
1. The DBF-based schedulability test (Theorem 2).
2. Density and utilization bounds.
3. Load parameter constraints.

These constraints work together to guarantee that no deadlines will be missed under the given task and resource parameters.