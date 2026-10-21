**Workload Model**

The workload model used in the paper is the sporadic task model [23, 9], which models a real-time system as a finite collection of independent recurring tasks. Each task $au_i$ is characterized by:

*   A worst-case execution requirement $C_i$
*   A relative deadline $D_i$
*   A minimum inter-arrival separation (or period) $T_i$

The sporadic task model generates an infinite sequence of jobs, each with a worst-case execution requirement equal to $C_i$ and a deadline that occurs $D_i$ time units after its arrival time.

**Resource Model**

The resource model used in the paper describes a multiprocessor platform with several identical processors. The resources available for executing tasks include:

*   Unit-capacity processors (i.e., each processor has one processing unit)
*   Communication channels
*   Memory
*   I/O devices

The timing or capacity constraints of these resources are not explicitly mentioned in the paper.

**Scheduler**

The scheduler used in the paper is Earliest Deadline First (EDF) scheduling. In EDF, jobs are assigned priorities according to their deadline parameters: the earlier the deadline of a job, the greater its priority.

**Analysis Framework**

The analysis framework used in the paper is based on the demand bound function (DBF) abstraction [9]. The DBF bounds the maximum cumulative execution requirement by jobs of each task that both arrive in and have deadlines within any interval of length $t$. The load parameter, based on the DBF function, is defined as follows:

$\text{load}(au) = \max_{t>0} \left(\frac{\sum_{au_i\in au}\text{dbf}(au_i,t)}{t}\right)$

where $\text{dbf}(au_i,t)$ is the DBF of task $au_i$ over an interval of length $t$.

**System Constraints or Invariants**

The following are some system constraints or invariants that guarantee correct scheduling of workloads, as presented in the paper:

*   **Utilization and density**: The total utilization $u_{\text{sum}}(au)$ and largest utilization $u_{\text{max}}(au)$ of a task system $au$ are defined as follows: $u_{\text{sum}}(au) = \sum_{au_i\in au} u_i; u_{\text{max}}(au) = \max_{au_i\in au}(u_i)$ where $u_i = C_i/T_i$ is the utilization of task $au_i$. The total density $\delta_{\text{sum}}(au)$ and largest density $\delta_{\text{max}}(au)$ of a task system $au$ are defined as follows: $\delta_{\text{sum}}(au) = \sum_{au_i\in au} \delta_i; \delta_{\text{max}}(au) = \max_{au_i\in au}( \delta_i)$ where $\delta_i = C_i/D_i$ is the density of task $au_i$.
*   **Demand bound function**: The demand bound function (DBF) bounds the maximum cumulative execution requirement by jobs of each task that both arrive in and have deadlines within any interval of length $t$. It has been shown [9] that $\text{dbf}(au_i,t) = \max\left(0,\left(\left\lfloor\frac{t-D_i}{T_i}\right\rfloor + 1\right)C_i\right)$
*   **Load parameter**: The load parameter, based on the DBF function, is defined as follows: $\text{load}(au) = \max_{t>0} \left(\frac{\sum_{au_i\in au}\text{dbf}(au_i,t)}{t}\right)$
*   **Theorem 2**: Task system $au$ is EDF-schedulable upon $m$ unit-capacity processors if for all tasks $au_k\in au$ and all $A_k \geq 0$, $\left(\sum_{au_i\in au}I_1(au_i) + \sum_{\text{the $(m-1)$ largest}} I_{\text{diff}}(au_i)\right) \leq m(A_k + D_k - C_k)$ where $I_1(au_i)$ and $I_{\text{diff}}(au_i)$ are defined in Equations 3 and 6, respectively.
*   **Theorem 3**: If Condition 8 is to be violated for any $A_k$, then it is violated for some $A_k$ satisfying the condition: $A_k \leq \frac{C_\Sigma - D_k(m-U(au)) + \sum_{i}(T_i-D_i)U_i + mC_k}{m-U(au)}$

where $C_\Sigma$ denotes the sum of the $(m-1)$ largest $C_i$'s.