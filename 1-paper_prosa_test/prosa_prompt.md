I am willing to perform mechanised proof of some theorems and lemmas for real time system for schedulibility analysis. This is the definitions in the real time system:

```

## 1. Workload Model

The paper uses the **sporadic task model**.

* Each task is represented as **τᵢ = (Cᵢ, Dᵢ, Tᵢ)**:

  * **Cᵢ** = worst-case execution time of the task
  * **Dᵢ** = relative deadline (≤ Tᵢ for constrained deadlines; = Tᵢ for implicit deadlines)
  * **Tᵢ** = minimum inter-arrival separation (period)
* Each sporadic task generates an infinite sequence of jobs with arrival separation ≥ Tᵢ, each requiring up to Cᵢ time units, and with deadline Dᵢ after arrival.
* The system workload is a task set τ = {τ₁, τ₂, …, τₙ}.

Additionally, the paper uses:

* **Utilization**: uᵢ = Cᵢ / Tᵢ
* **Density**: δᵢ = Cᵢ / Dᵢ
* **Demand Bound Function (DBF)**:

  $$
  DBF(τᵢ, t) = \max\Big(0, \Big(\big\lfloor \frac{t - Dᵢ}{Tᵢ} \big\rfloor + 1\Big) Cᵢ\Big)
  $$

  This is the maximum execution demand by τᵢ within an interval of length *t*.

---

## 2. Resource Model

* The platform is a **multiprocessor system with m identical unit-capacity processors**.
* **Global scheduling** is assumed:

  * A job may execute on any processor.
  * Jobs may migrate between processors (with no cost).
  * At any instant, a job executes on at most one processor.

---

## 3. Scheduler

* The paper focuses on **Global Earliest Deadline First (Global EDF)** scheduling:

  * Jobs are assigned priorities by absolute deadlines (earlier deadline = higher priority).
  * The scheduler is **fixed job-priority (FJP)**: priority does not change once a job arrives.
* The work compares EDF to partitioned scheduling, but the **main results derive new schedulability tests for global EDF**.

---

## 4. System Constraints / Invariants

These are the mathematical conditions that guarantee correct scheduling:

### (a) Density Test (Prior Work)

$$
\delta_{\text{sum}}(τ) \leq m - (m-1)\delta_{\max}(τ) \tag{1}
$$

* δ_sum(τ) = Σ δᵢ = total system density
* δ_max(τ) = max δᵢ = largest task density
* m = number of processors
  **Meaning**: Total density must not exceed this adjusted processor capacity bound.

---

### (b) Necessary Condition for Deadline Miss (Equation 2)

If task τₖ misses a deadline, then:

$$
\sum_{\tauᵢ \in τ} I(τᵢ) > m \times (Aₖ + Dₖ - Cₖ) \tag{2}
$$

* τₖ = task whose job misses deadline
* Dₖ = relative deadline of τₖ
* Cₖ = execution time of τₖ
* Aₖ = ta − to = slack between last idle instant to and τₖ’s arrival time ta
* I(τᵢ) = contribution of τᵢ’s work in that interval

**Meaning**: For τₖ to miss its deadline, the cumulative work from all tasks must exceed total processing capacity over the considered interval.

---

### (c) Work Contribution Bounds

* **Without carry-in (I₁):**

$$
I₁(τᵢ) =
\begin{cases}
\min(DBF(τᵢ, Aₖ + Dₖ), \, Aₖ + Dₖ - Cₖ) & i \neq k \\
\min(DBF(τₖ, Aₖ + Dₖ) - Cₖ, \, Aₖ) & i = k
\end{cases} \tag{3}
$$

* **With carry-in (I₂):**

$$
I₂(τᵢ) =
\begin{cases}
\min(DBF’(τᵢ, Aₖ + Dₖ), \, Aₖ + Dₖ - Cₖ) & i \neq k \\
\min(DBF’(τₖ, Aₖ + Dₖ) - Cₖ, \, Aₖ) & i = k
\end{cases} \tag{5}
$$

where

$$
DBF’(τᵢ, t) = \Big\lfloor \frac{t}{Tᵢ} \Big\rfloor Cᵢ + \min(Cᵢ, t \bmod Tᵢ) \tag{4}
$$

* **IDIFF (extra work due to carry-in):**

$$
IDIFF(τᵢ) = I₂(τᵢ) - I₁(τᵢ) \tag{6}
$$

---

### (d) Main Schedulability Test (Theorem 2)

$$
\sum_{\tauᵢ \in τ} I₁(τᵢ) + \sum_{\text{(m−1) largest}} IDIFF(τᵢ) \leq m(Aₖ + Dₖ - Cₖ) \tag{8}
$$

* Holds for all τₖ ∈ τ and all Aₖ ≥ 0.
* Ensures τ is **EDF-schedulable on m processors**.
* Intuition: Only (m−1) tasks can carry in work simultaneously, bounding pessimism.

---

### (e) Search Bound on Aₖ (Theorem 3)

It suffices to test Aₖ up to:

$$
Aₖ \leq \frac{C_\Sigma - Dₖ(m - U(τ)) + \sum_i (Tᵢ - Dᵢ)Uᵢ + mCₖ}{m - U(τ)} \tag{9}
$$

* CΣ = sum of the (m−1) largest execution times Cᵢ
* U(τ) = total utilization = Σ (Cᵢ/Tᵢ)

**Meaning**: This theorem bounds how far in time you need to check for possible violations, making the test pseudo-polynomial.

---
```

I am willing to use coq-prosa to proof these theorems and lemmas using mechanised proof. write a script using coq-prosa so that I can verify these. my prosa version is 0.5 and coq version is 8.16.

this is the directory structure of the coq-prosa library:

```
.
├── analysis
│   ├── abstract
│   ├── definitions
│   ├── facts
│   │   ├── behavior
│   │   ├── busy_interval
│   │   │   └── ideal
│   │   ├── model
│   │   │   └── ideal
│   │   ├── periodic
│   │   ├── preemption
│   │   │   ├── job
│   │   │   ├── rtc_threshold
│   │   │   └── task
│   │   ├── priority
│   │   ├── readiness
│   │   ├── sporadic
│   │   └── transform
│   └── transform
├── behavior
├── classic
│   ├── analysis
│   │   ├── apa
│   │   ├── global
│   │   │   ├── basic
│   │   │   ├── jitter
│   │   │   └── parallel
│   │   └── uni
│   │       ├── arrival_curves
│   │       ├── basic
│   │       ├── jitter
│   │       └── susp
│   │           ├── dynamic
│   │           │   ├── jitter
│   │           │   └── oblivious
│   │           └── sustainability
│   │               ├── allcosts
│   │               └── singlecost
│   ├── implementation
│   │   ├── apa
│   │   ├── global
│   │   │   ├── basic
│   │   │   ├── jitter
│   │   │   └── parallel
│   │   └── uni
│   │       ├── basic
│   │       ├── jitter
│   │       └── susp
│   │           └── dynamic
│   │               └── oblivious
│   ├── model
│   │   ├── arrival
│   │   │   ├── basic
│   │   │   ├── curves
│   │   │   └── jitter
│   │   └── schedule
│   │       ├── apa
│   │       ├── global
│   │       │   ├── basic
│   │       │   ├── jitter
│   │       │   └── transformation
│   │       ├── partitioned
│   │       └── uni
│   │           ├── basic
│   │           ├── jitter
│   │           ├── limited
│   │           │   ├── abstract_RTA
│   │           │   ├── edf
│   │           │   │   └── nonpr_reg
│   │           │   │       └── concrete_models
│   │           │   ├── fixed_priority
│   │           │   │   └── nonpr_reg
│   │           │   │       └── concrete_models
│   │           │   └── platform
│   │           ├── nonpreemptive
│   │           ├── susp
│   │           └── transformation
│   └── util
├── implementation
│   ├── definitions
│   ├── facts
│   │   └── ideal_uni
│   └── refinements
│       ├── EDF
│       └── FP
├── model
│   ├── aggregate
│   ├── preemption
│   ├── priority
│   ├── processor
│   ├── readiness
│   ├── schedule
│   └── task
│       ├── arrival
│       ├── preemption
│       └── suspension
├── results
│   ├── edf
│   │   └── rta
│   ├── fifo
│   ├── fixed_priority
│   │   └── rta
│   │       └── comp
│   └── gel
│       └── rta
└── util
```

Use this directory structure to understand the import statements in the prosa script and try to write a script that executes without any error.