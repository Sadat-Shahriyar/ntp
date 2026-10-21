### Example: Fixed-Priority Schedulability Analysis

**Assumptions:** Preemptive uniprocessor, independent sporadic tasks, fixed priorities, and no blocking.

#### Lemma 1 — Higher-Priority Interference Bound

During an interval of length $t$, the maximum interference on task $\tau_i$ is bounded by:

$$I_i(t) = \sum_{\tau_h \in hp(i)} \left\lceil \frac{t}{T_h} \right\rceil C_h$$

#### Lemma 2 — Worst-Case Response-Time Bound

The worst-case response time of task $\tau_i$ is given by:

$$R_i = C_i + \sum_{\tau_h \in hp(i)} \left\lceil \frac{R_i}{T_h} \right\rceil C_h$$

#### Theorem 1 — Schedulability Condition

If every task's worst-case response time does not exceed its deadline,

$$\forall \tau_i,\qquad R_i \leq D_i$$

then the task set is schedulable under the stated assumptions.