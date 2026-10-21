## 1.  What the paper models

| **Component** | **What is used in the paper** | **Typical notation in the paper** | **Brief description** |
|---------------|------------------------------|----------------------------------|-----------------------|
| **Work‑load model** | Sporadic task system.  Each task τᵢ is described by a triple (Cᵢ, Dᵢ, Tᵢ) – the worst‑case execution time, the absolute deadline and the minimum inter‑arrival (period) of the task. |  τ = {τ₁,…,τₙ}  where τᵢ = (Cᵢ, Dᵢ, Tᵢ)  and  Uᵢ = Cᵢ/Tᵢ  |  Tasks may arrive at any time as long as the time between two consecutive activations of τᵢ is at least Tᵢ. |
| **Resource model** | m identical, homogeneous, unit‑capacity processors. |  m   |  Every processor can execute one unit of work per unit of time. |
| **Scheduler** | Global Earliest‑Deadline‑First (EDF).  At any time the scheduler picks the m jobs with the smallest absolute deadlines and assigns them to the processors. |  EDF  |  A job may migrate across processors; the schedule is *global*. |
| **Analysis framework** | Demand‑Bound‑Function (dbf) analysis that distinguishes *carry‑in* (the job that may still be pending on the previous cycle) from *no‑carry‑in* (the interval starts at an idle instant).  The paper introduces a refined dbf called **dbf′** (eq. (4)) that is valid for the *carry‑in* case, and the ordinary dbf for the *no‑carry‑in* case.  A schedulability test (Theorem 2) is derived from the two cases. |  dbf(τᵢ,t),  dbf′(τᵢ,t)  (eq. (4))  and  I₁(τᵢ), I₂(τᵢ), I_dif(τᵢ)  (eqs. (3)–(6)).  |  The framework checks whether, for every task τₖ and every non‑negative value Aₖ (the length of the interval between the latest idle instant tₒ and the arrival of τₖ’s job at tₐ), the total demand of all tasks does not exceed the available processing capacity. |

---

## 2.  System constraints / invariants that guarantee correct scheduling

Below every mathematical statement is reproduced *exactly as it appears in the paper* (the formatting and macro names are kept).  For each constraint the symbols that appear in it are explained afterwards.

### 2.1  Definitions used in the schedulability test

1. **Demand‑bound‑function (no‑carry‑in)**  

   The paper uses the conventional demand‑bound function of a sporadic task τᵢ (notation \extsc{dbf}(\tauᵢ,t)).  
   (The explicit formula is given in the proof of Theorem 3 as \exttt{dbf}(\tauᵢ,t).)

2. **Carry‑in demand‑bound‑function** – dbf′ (eq. (4))

   ```latex
   \extsc{dbf}^{*}(\tau_i, t)\stackrel{{\mbox{iny{def}}}}{{=}}
      \left\lfloor\frac{t}{T_i}\right\rfloor \times C_i
      + \min(C_i, t \bmod T_i)
   ```

   In plain LaTeX this is  

   \[
   \operatorname{dbf}^{*}(\tau_i, t)
     = \Bigl\lfloor \tfrac{t}{T_i}\Bigr\rfloor \cdot C_i
       + \min\!\bigl(C_i,\; t\bmod T_i\bigr).
   \]

   **Explanation of symbols**  
   - \(t\) – any positive time instant.  
   - \(\tau_i\) – the \(i\)-th task in the set \(\tau\).  
   - \(T_i\) – period (minimum inter‑arrival time) of \(\tau_i\).  
   - \(C_i\) – worst‑case execution time of \(\tau_i\).  

3. **Functions \(I_{1}(\tau_i)\) and \(I_{2}(\tau_i)\)** – equations (3) and (5)

   Equation (3) (definition of \(I_{1}\)):

   ```latex
   I_{1}(\tau_i)&\stackrel{{  \ext{iny def}}}{{=}}\ &\left\{ \begin{array}{ll}
   \min( \operatorname{dbf}(\tau_i, A_k + D_k), \, A_k + D_k - C_k) & \text{if $i\neq k$}\\
   \min( \operatorname{dbf}(\tau_i, A_k + D_k)-C_k, \, A_k) & \text{if $i=k$}
   \end{array}\right.
   ```

   Equation (5) (definition of \(I_{2}\)):

   ```latex
   I_{2}(\tau_i) = \begin{array}{ll}
   \min( \operatorname{dbf}^{\prime}(\tau_i, A_k + D_k), \, A_k + D_k - C_k) & \text{if $i\neq k$}\\
   \min( \operatorname{dbf}^{\prime}(\tau_i, A_k + D_k)-C_k, \, A_k) & \text{if $i=k$}
   \end{array}
   ```

   (In the paper the symbols “dbf′” and “dbf*” appear as \extsc{dbf}^{*}.)

4. **Difference function** – equation (6)

   ```latex
   I_{\text{dif}}(\tau_i) \stackrel{{ \ext{iny def}}}{{=}}\ I_{2}(\tau_i)-I_{1}(\tau_i)
   ```

   which is simply  

   \[
   I_{\text{dif}}(\tau_i) = I_{2}(\tau_i)-I_{1}(\tau_i).
   \]

5. **Critical inequality (Theorem 2)** – equations (7) and (8)

   Equation (7) (necessary condition for a deadline miss):

   ```latex
   \sum_{\tau_i \in \tau} I_{1}(\tau_i) + \sum_{\text{the }(m-1)\text{ largest}}
   I_{\text{dif}}(\tau_i) > m(A_k + D_k - C_k)
   ```

   Equation (8) (exact EDF schedulability test – all tasks must satisfy it):

   ```latex
   \left(\sum_{\tau_i \in \tau} I_{1}(\tau_i) +
          \sum_{\text{the } (m-1) \text{ largest}} I_{\text{dif}}(\tau_i)\right)
   \leq m(A_k + D_k - C_k)
   ```

6. **Upper bound on the test variable \(A_k\)** – Theorem 3 (equation (9))

   ```latex
   A_k \leq \frac{C_{\Sigma} - D_k (m-U(\tau)) + \sum_i (T_i - D_i) U_i + m C_k}
                 {m - U(\tau)}
   ```

   where  

   \[
   C_{\Sigma}\;\text{denotes the sum of the $(m-1)$ largest }C_i\text{'s},\qquad
   U_i = \frac{C_i}{T_i},\qquad
   U(\tau)=\sum_i U_i.
   \]

---

### 2.2  Other implicit invariants

The paper assumes that the **total utilization** of the task set is strictly less than the number of processors; this is implicit in the denominator of (9):

\[
m - U(\tau) > 0
\]

(If \(U(\tau)\ge m\), EDF can never be schedulable on \(m\) identical processors.)

No other explicit algebraic invariants appear in the excerpt; the remaining constraints are the usual load bound ($U(\tau)\le m$) and the requirement that each $A_k$ be non‑negative ($A_k \ge 0$).

---

## 3.  Summary of symbols used in the constraints

| Symbol | Meaning |
|--------|---------|
| \(\tau\) | Set of all sporadic tasks. |
| \(\tau_i\) | The \(i\)-th task in \(\tau\). |
| \(C_i\) | Worst‑case execution time of \(\tau_i\). |
| \(D_i\) | Absolute deadline of \(\tau_i\). |
| \(T_i\) | Minimum inter‑arrival time (period) of \(\tau_i\). |
| \(U_i\) | Utilization of \(\tau_i\): \(U_i = C_i/T_i\). |
| \(U(\tau)\) | Total utilization of the task set: \(U(\tau)=\sum_i U_i\). |
| \(m\) | Number of identical unit‑capacity processors. |
| \(A_k\) | Length of the interval \([t_o,\,t_a)\); the time between the latest idle instant \(t_o\) and the arrival instant \(t_a\) of a job of task \(\tau_k\). It is a non‑negative test parameter. |
| \(\operatorname{dbf}(\tau_i,t)\) | Standard demand‑bound function of task \(\tau_i\). |
| \(\operatorname{dbf}^{*}(\tau_i,t)\) (eq. (4)) | Carry‑in demand‑bound function: \(\left\lfloor\frac{t}{T_i}\right\rfloor C_i + \min(C_i,t\bmod T_i)\). |
| \(I_1(\tau_i)\) | Demand when the interval \([t_o,t_a)\) starts with a non‑full processor (eq. (3)). |
| \(I_2(\tau_i)\) | Demand when the interval \([t_o,t_a)\) starts with a full processor (carry‑in) (eq. (5)). |
| \(I_{\text{dif}}(\tau_i)\) | Difference \(I_2(\tau_i)-I_1(\tau_i)\) (eq. (6)). |
| \(C_{\Sigma}\) | Sum of the \((m-1)\) largest \(C_i\) values. |

These constraints, taken together, form the exact analytical test that guarantees that a global EDF scheduler on \(m\) identical unit‑capacity processors can always meet all deadlines of the given sporadic task system.