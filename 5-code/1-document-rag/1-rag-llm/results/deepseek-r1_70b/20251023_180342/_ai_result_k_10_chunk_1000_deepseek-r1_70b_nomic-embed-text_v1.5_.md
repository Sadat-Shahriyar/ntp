

### 1. Identification and Description of Key Components

#### Workload Model:
The workload model in this research is based on **sporadic task systems**. Each task τi ∈ τ is characterized by:
- **Arrival Pattern**: Sporadic, meaning tasks arrive repeatedly but not periodically.
- **Execution Time**: Worst-case execution time Ci.
- **Deadlines**: Relative deadline Di, with constraints Di ≤ Ti (constrained sporadic) or Di = Ti (implicit-deadline).
- **Periodicity**: Tasks are recurring and generate an infinite sequence of jobs.

#### Resource Model:
The resource model consists of a **multiprocessor platform** where tasks can migrate between processors. The specifics of the hardware (e.g., number of cores, heterogeneity) are not detailed in the provided context but are implied to be general multiprocessor architectures.

#### Scheduler:
The scheduler used is **global EDF (Earliest Deadline First)**. This means that at any time, the task with the earliest absolute deadline is selected for execution across all processors. Task migration between processors is permitted to balance load and meet deadlines.

#### Analysis Framework:
The analysis framework employs **schedulability tests** based on:
- **Demand Bound Function (DBF)**: Bounds the maximum cumulative execution requirement of a task over any interval.
- **Utilization and Density Metrics**: Total utilization usum(τ), largest utilization umax(τ), total density δsum(τ), and largest density δmax(τ).
- **Load Parameter**: A measure derived from DBF to assess system schedulability.

---

### 2. System Constraints or Invariants

The paper identifies several constraints and invariants that guarantee correct scheduling of workloads. These are presented as equations, definitions, and properties:

#### 1. Task Parameters:
For each task τi ∈ τ:
- **Execution Time**: Ci (worst-case execution time).
- **Period**: Ti (minimum interval between consecutive arrivals of the task).
- **Relative Deadline**: Di, with constraints:
  - $D_i \leq T_i$ for constrained sporadic systems.
  - $D_i = T_i$ for implicit-deadline (Liu and Layland) systems.

#### 2. Utilization Metrics:
- **Task Utilization**:
  $$ u_i = \frac{C_i}{T_i} $$
- **Total Utilization**:
  $$ u_{\text{sum}}(\tau) = \sum_{\tau_i \in \tau} u_i $$
- **Largest Utilization**:
  $$ u_{\text{max}}(\tau) = \max_{\tau_i \in \tau} u_i $$

#### 3. Density Metrics:
- **Task Density**:
  $$ \delta_i = \frac{C_i}{D_i} $$
- **Total Density**:
  $$ \delta_{\text{sum}}(\tau) = \sum_{\tau_i \in \tau} \delta_i $$
- **Largest Density**:
  $$ \delta_{\text{max}}(\tau) = \max_{\tau_i \in \tau} \delta_i $$

#### 4. Demand Bound Function (DBF):
For any interval length t, the demand bound function for a task τi is:
$$ DBF(\tau_i, t) = \max\left(0, \left\lfloor \frac{t - D_i}{T_i} \right\rfloor + 1\right) C_i $$

#### 5. Load Parameter:
The load parameter for the task system τ is defined as:
$$ L(\tau) = \sum_{\tau_i \in \tau} DBF(\tau_i, D_{\text{max}}) $$
where $D_{\text{max}}$ is the maximum relative deadline of any task in the system.

---

### Explanation of Notations and Symbols

- **Ci**: Worst-case execution time of task τi.
- **Ti**: Period (minimum interval between consecutive arrivals) of task τi.
- **Di**: Relative deadline of task τi.
- **ui**: Utilization of task τi, representing the fraction of processor time required by the task.
- **u_sum(τ)**: Total utilization of the task system, summing the utilizations of all tasks.
- **u_max(τ)**: Largest utilization among all tasks in the system.
- **δi**: Density of task τi, representing the ratio of execution time to relative deadline.
- **δ_sum(τ)**: Total density of the task system, summing the densities of all tasks.
- **δ_max(τ)**: Largest density among all tasks in the system.
- **DBF(τi, t)**: Demand bound function for task τi over an interval of length t, bounding the maximum cumulative execution requirement.
- **L(τ)**: Load parameter for the task system, derived from the DBF and used to assess schedulability.

These constraints and metrics are critical for ensuring that the workload can be scheduled correctly on the multiprocessor platform under global EDF scheduling.