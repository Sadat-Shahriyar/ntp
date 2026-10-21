We need to produce answer: identify workload model, resource model, scheduler, analysis framework used in the paper.

From paper: The workload model: sporadic task system; each task τ_i has execution requirement C_i, deadline D_i, period T_i, etc. We need to state exactly: tasks specified as τ_i = (C_i, D_i, T_i). They also mention the sporadic model, arrival intervals, worst-case execution. Provide description.

Resource model: m unit-capacity processors (homogeneous, identical). So the resources are m identical processors each with capacity 1 (unit). There may also be memory? Not explicitly. But the resource model defined as m identical processors with capacity 1.

Scheduler: Earliest Deadline First (EDF). They consider global EDF on multiprocessors.

Analysis framework: demand bound functions (dbf), dbf', difference between carry-in and no-carry-in. Theorem 2 provides exact schedulability test. Provide equations: Condition 8, etc.

We must extract all system constraints, lemmas, theorems, etc.

Let's collect:

Definitions:

- Task system τ: set of sporadic tasks τ_i = (C_i, D_i, T_i). Not defined earlier but typical.

- Utilization: U(τ) = Σ_i C_i / T_i.

- Demand-bound function: dbf(τ_i, t) = floor(t / T_i) * C_i + min(D_i, t mod T_i) * C_i? Actually typical dbf: floor(t/T_i)*C_i + max(0, min(C_i, t - kT_i)). Wait typical dbf: For sporadic tasks with period T_i and worst-case execution C_i and deadline D_i, dbf_i(t) = max_{k} { floor((t - D_i)/T_i) + 1 }? Let's extract the exact definitions from paper: There is equation: "The demand bound function (dbf)" typical formula: $$dbf(\tau_i, t) = \left\lfloor \frac{t - D_i}{T_i}\right\rfloor C_i + \min(C_i, t \bmod T_i)$$ Actually in paper they use expression: $\left\lfloor\frac{t}{T_i}\right\rfloor C_i + \min(C_i, t \bmod T_i)$. Wait they defined dbf'(τ_i, t) as eqn (4). But the usual dbf(τ_i, t) defined earlier maybe? They refer to demand bound function earlier. Let's search in paper text for definition: At some point they mention:

"In the notation of the paper, the demand bound function of τ_i is defined as: dbf(τ_i, t) = ..."

But I can't find the explicit formula in excerpt provided; maybe earlier in introduction they mention standard dbf: It's not explicitly defined in excerpt but earlier they reference [10], [9], etc. The typical dbf: For sporadic tasks with period T_i and execution C_i, the demand bound function is defined as: dbf(τ_i, t) = floor((t - D_i)/T_i) * C_i + max(0, min(C_i, t - (floor((t - D_i)/T_i) + 1)*T_i)). Wait.

But we need to extract all constraints exactly as in the paper. Let's scan the excerpt for equations:

- Condition 8: $$\left(\sum_{\tau_{i}\in \tau} I_{1}(\tau_{i}) + \sum_{\text{the } (m-1) \text{ largest}} I_{\text{dif}}(\tau_{i})\right) \leq m(A_{k} + D_{k} - C_{k})$$

We need to write each constraint exactly.

- Equation 3: definition of I1(τ_i):

$$I_{1}(\tau_i) \stackrel{\text{iny def}}{=} \begin{cases}
\min(\operatorname{dbf}(\tau_i, A_k + D_k), A_k + D_k - C_k) & \text{if } i \neq k \\
\min(\operatorname{dbf}(\tau_i, A_k + D_k) - C_k, A_k) & \text{if } i = k
\end{cases}$$

- Equation 4: definition of dbf* (dbf prime) but we need to preserve as given: They defined dbf^*(τ_i, t) = floor(t/T_i) * C_i + min(C_i, t mod T_i). But they denote with star? They wrote:

$$\operatorname{dbf}^{*}(\tau_i, t) \stackrel{\text{iny def}}{=}\ \left\lfloor \frac{t}{T_i}\right\rfloor \times C_i + \min(C_i, t \bmod T_i)$$

But the notation they used is: $\extsc{dbf}^{*}( \tau_i, t) = \left\lfloor \frac{t}{T_i}\right\rfloor \times C_i + \min(C_i, t \bmod T_i)$.

We need to replicate exactly as appears. So we should keep the latex macros like \extsc{dbf}^{*}.

But maybe the original had $\extsc{dbf}^{*}$? Let's capture exactly: They wrote:

```
\extsc{dbf}^{*}( \tau_i, t)\stackrel{{\mbox{iny{def}}}}{{=}} \left\lfloor\frac{t}{T_i}\right\rfloor \times C_i + \min(C_i, t \bmod T_i)
```

We need to keep that.

Equation 5: definition of I2(τ_i):

$$I_{2}(\tau_i) \stackrel{\text{iny def}}{=} \begin{cases}
\min(\operatorname{dbf}^{\prime}(\tau_i, A_k + D_k), A_k + D_k - C_k) & \text{if } i \neq k \\
\min(\operatorname{dbf}^{\prime}(\tau_i, A_k + D_k) - C_k, A_k) & \text{if } i = k
\end{cases}$$

Equation 6: definition of I_dif:

$$I_{\text{dif}}(\tau_i) \stackrel{\text{iny def}}{=} I_2(\tau_i) - I_1(\tau_i)$$

Equation 7: sum inequality:

$$\sum_{\tau_i \in \tau} I_1(\tau_i) + \sum_{\text{the }(m-1)\text{ largest}} I_{\text{dif}}(\tau_i) > m(A_k + D_k - C_k)$$

Equation 8: condition for schedulability:

$$\left(\sum_{\tau_i \in \tau} I_1(\tau_i) + \sum_{\text{the } (m-1) \text{ largest}} I_{\text{dif}}(\tau_i)\right) \leq m(A_k + D_k - C_k)$$

Equation 9: bound on Ak:

$$A_k \leq \frac{C_{\Sigma} - D_k (m-U(\tau)) + \sum_i (T_i - D_i) U_i + m C_k}{m - U(\tau)}$$

Other constraints: Theorem 1? Actually not. There are lemmas: Lemma 1, etc. But we need all system constraints or invariants that guarantee correct scheduling of workloads.

In paper, constraints include:

- Utilization bound: $U(\tau) < m$? They refer to $U(\tau)$ as sum of utilizations. For Theorem 3, they require $U(\tau)$ less than m.

- Condition (density, etc.). But we need all constraints exactly as appear. That includes definitions of dbf, dbf*, etc.

We also need to identify workload model: sporadic tasks with execution requirement, deadline, period. They use $\tau_i = (C_i, D_i, T_i)$.

Resource model: m unit-capacity processors.

Scheduler: global EDF (Earliest Deadline First).

Analysis framework: demand-bound function analysis with carry-in from at most m-1 tasks, etc.

Now we need to provide constraints exactly as they appear.

Also constraints such as U(τ) <= m? Actually Theorem 3 uses condition: $m - U(\tau) > 0$. So we need to mention that. But no equation.

Also Condition 8 may include sum of I1 and sum of m-1 largest I_dif. So that's constraint.

Also earlier constraints: load bound: $U(\tau) \le m$? They used load bound to bound utilization.

Also they mention "If a job of τ_k arrives at t_a and misses deadline at t_d, define A_k = t_d - t_a + (t_d - t_a)? Actually they defined A_k = t_d - t_a + (something?). But we can include constraint about A_k.

Better to systematically go through the excerpt.

Search for all equations:

Equation (1) earlier: $\operatorname{load}(\tau) = \sum_i \frac{C_i}{T_i}$? They mention load but not equation.

But the main constraints are Theorem 2 condition 8, Theorem 3 bound 9, Corollary 1, etc.

Let's scan for other invariants: "load bound" maybe? Actually the paper might mention "density test" but not equation.

Also we might include invariants like "load bound < m" to guarantee scheduling.

Let's extract the following:

- The demand bound function dbf(τ_i, t) typical formula: $\operatorname{dbf}(\tau_i, t) = \left\lfloor\frac{t - D_i}{T_i}\right\rfloor C_i + \min(C_i, t \bmod T_i)$? But they don't provide formula explicitly earlier. But we need to extract as appears: There is definition of dbf'(τ_i, t) eqn 4.

- They also mention dbf* notation as dbf^*? Actually they used $dbf^{*}$. So we need to capture exactly.

- They mention $\extsc{dbf}(\tau_i, t)$ for standard dbf.

- They mention $C_\Sigma$ denotes sum of (m-1) largest C_i's.

- They mention $U(\tau)$ is the total utilization.

- They mention $U_i$ is the utilization of task i: $U_i = C_i/T_i$.

- They mention $T_i$ and $D_i$ are period and deadline.

- They mention $C_\Sigma$ also used.

- They mention $m$ is number of processors.

- They mention $\exttt{dbf}$ used in Theorem 3 bounding. They use exttt? But we need to replicate exactly as in the paper: They used $\exttt{dbf}$. Actually they used \exttt{dbf} for something? In the proof of Theorem 3 they mention: $C_\Sigma + \sum_{i} \operatorname{dbf}(τ_i, A_k + D_k)$. Then bounding: "ext((bounding dbf using technique of Dj)". But they used \@@cite etc. But we just need the constraint as appears. In Theorem 3, they give bound as equation (9). We'll replicate exactly.

- Condition 8: they present as:

$$\left(\sum_{\tau_{i}\in \tau}I_{1}(\tau_{i})+\sum_{\mbox{\scriptsize the $(m-1)$ largest}}I_{\text{dif}}(\tau_{i})\right)\ \leq m(A_{k}+D_{k}-C_{k})$$

But there may be small differences: In condition 8 they used "I_dif" maybe I_dif? Let's capture exactly as in paper.

Also earlier they defined I_1 and I_dif.

- Equation 3: definition of I1(τ_i) exactly as given:

```
I_{1}(\tau_i) \stackrel{{ \ext{iny def}}}{=} 
\begin{cases}
\min(\operatorname{dbf}(\tau_i, A_k+ D_k), A_k + D_k - C_k) & \text{if } i \neq k\\
\min(\operatorname{dbf}(\tau_i, A_k+ D_k)-C_k, A_k) & \text{if } i = k
\end{cases}
```

But we need to replicate exactly the line as appears.

Better to copy directly from paper excerpt:

From the paper:

```
 I_{1}(\tau_i) \stackrel{ \ext{iny def}}{=} \{ \begin{array}{ll}
 \min(\operatorname{dbf}(\tau_i,A_k+ D_k ),A_k+ D_k - C_k) & \text{if } i \neq k \\
 \min(\operatorname{dbf}(\tau_i, A_k+ D_k)-C_k ,A_k) & \text{if } i = k \end{array} \}
```

But the actual text: It appears as:

```
 I_{1}(τ_i)=\{…\}
```

Let's examine original snippet:

```
 I_{1}(τ_i)&\stackrel{{ 	ext{	iny def}}}{{=}}\ &\left\{egin{array}{ll}\min(	extsc{dbf}(τ_i,A_{k}+D_{k} ),A_{k}+D_{k}-C_{k})&	ext{if $i\neq k$}\\
 \min(	extsc{dbf}(τ_i,A_{k}+D_{k})-C_{k},A_{k})&	ext{if $i=k$} \end{array}  \right.
```

So we need to capture that exactly.

Similarly equation 5:

```
 I_{2}(τ_i) = 
\begin{array}{ll}
\min(\operatorname{dbf}'(τ_i, A_k + D_k), A_k + D_k - C_k) & \text{if } i \neq k\\
\min(\operatorname{dbf}'(τ_i, A_k + D_k)-C_k, A_k) & \text{if } i = k
\end{array}
```

But we need the exact expression.

Equation 6:

```
 I_{dif}(τ_i) = I_2(τ_i) - I_1(τ_i)
```

Equation 7:

```
\sum_{τ_i∈τ} I_1(τ_i) + \sum_{\text{the }(m-1)\text{ largest}} I_{dif}(τ_i) > m(A_k + D_k - C_k)
```

Equation 8: same but with inequality <=.

Equation 9: Bound on A_k.

We also have Theorem 3 bound.

Also there might be constraints such as U(τ) < m? Theorem 3 includes denominator m - U(τ) > 0. So they require U(τ) < m.

Also Theorem 3 uses C_Σ denotes sum of the (m-1) largest C_i's.

Now for each constraint we need to explain each symbol.

Symbols:

- τ: set of tasks.
- τ_i: i-th task in τ.
- C_i: worst-case execution time of task τ_i.
- D_i: deadline of τ_i.
- T_i: period of τ_i (periodic or minimal inter-arrival for sporadic).
- U_i = C_i / T_i: utilization of τ_i.
- U(τ) = Σ_i U_i: total utilization.
- m: number of identical unit-capacity processors.
- A_k: time difference between the latest idle instant t_o and arrival of task τ_k? Actually A_k defined earlier as A_k = t_d - t_a? Wait they defined A_k earlier: They defined A_k as time between t_o and t_a? Actually earlier they defined A_k = t_d - t_a + (t_d - t_a)? Let's examine the notation: In Notation figure: A job arrives at t_a and misses deadline at t_d. t_o is last instant before t_a where not all m processors busy. Then A_k = t_d - t_a? Actually earlier they used A_k in Condition 8 as variable for testing. They defined A_k as value used in dbf arguments: A_k + D_k? So A_k is the time from t_o to t_a? Let's read: "For given τ_k and A_k, Condition 8 can be evaluated. How many values of A_k must be tested... Theorem 3 below provides the answer." So A_k is variable representing t_a - t_o? Wait earlier they defined A_k as a value representing the time between t_o and t_a. But we need to check the earlier definitions. In the algorithm design, they consider intervals [t_o, t_a) and [t_a, t_d). A_k appears in equations as A_k + D_k. So A_k seems to represent the time difference between t_o and t_a, i.e., the length of the interval of non-full processor busy before the arrival of the job. But we can define: A_k is the duration between the latest idle instant t_o and the arrival instant t_a of τ_k's job. They also mention earlier "For given τ_k and A_k, we compute I_1, I_2, etc." So A_k is non-negative.

Thus we should explain that.

Also I_dif refers to difference between I_2 and I_1.

Now we must provide all constraints exactly as appear. Also include equations for dbf' and dbf*.

Equation for dbf':

$$\operatorname{dbf}^{*}(\tau_i, t) = \left\lfloor \frac{t}{T_i} \right\rfloor \times C_i + \min(C_i, t \bmod T_i)$$

But they use star maybe: $\extsc{dbf}^{*}(\tau_i,t)$.

Actually in paper they use $\extsc{dbf}^{*}(\tau_i, t)$? Let's look: They use "dbf^{*}(τ_i, t)"? They wrote:

$$\extsc{dbf}^{*}(\tau_i, t)\stackrel{\mbox{iny{def}}}{=}\left\lfloor\frac{t}{T_i}\right\rfloor \times C_i + \min(C_i, t\bmod T_i)$$

They denote this as dbf*.

But earlier they wrote "dbf'" as defined above: "Define dbf'(τ_i,t) as ... we denote as dbf^{*}..." Wait confusion: Let's parse.

In text: "Define dbf' (τ_i, t) as ... we denote as dbf^*(τ_i,t)?" They wrote: "Define dbf'(τ_i,t) as ... we denote as dbf*"? Actually they wrote:

"In the notation of the paper, the demand bound function of τ_i is defined as: dbf(τ_i, t) = ... The demand bound function of τ_i, denoted dbf'(τ_i, t), is defined as follows." Then they defined equation (4). But they denote as dbf^*. Actually they used $\extsc{dbf}^{*}$.

But we can treat dbf* as dbf'.

Thus we need to capture equation exactly as appears: It uses \extsc{dbf}^{*}.

Equation 4: they used $\extsc{dbf}^{*}$ but may also denote with *.

We need to capture all constraints exactly as in excerpt.

Let's collect them:

From the excerpt:

Equation 3:

```
 I_{1}(τ_i)&\stackrel{{ \ext{iny def}}}{{=}}\ &\left\{egin{array}{ll}
 \min(\operatorname{dbf}(τ_i, A_k+ D_k ),A_k+ D_k- C_k)&\text{if } i\neq k\\
 \min(\operatorname{dbf}(τ_i, A_k+ D_k)-C_k ,A_k)&\text{if } i=k \end{array}\right.
```

But actual text uses extsc{dbf}. Provide that.

Equation 4:

$$\extsc{dbf}^{*}(\tau_i, t)\stackrel{\mbox{iny{def}}}{=}\left\lfloor \frac{t}{T_i}\right\rfloor \times C_i + \min(C_i, t \bmod T_i)$$

Equation 5:

```
 I_{2}(\tau_i) &\stackrel{ \ext{iny def}}{=} 
\begin{array}{ll}
 \min(\operatorname{dbf}'(\tau_i, A_k + D_k), A_k + D_k - C_k) & \text{if } i \neq k\\
 \min(\operatorname{dbf}'(\tau_i, A_k + D_k)-C_k, A_k) & \text{if } i = k
\end{array}
```

But they wrote exactly:

```
 I_{2}(\tau_i)\stackrel{{\mbox{iny def}}}{=}\begin{array}{ll}
 \min(\extsc{dbf}'(\tau_i, A_k + D_k), A_k + D_k - C_k) & \text{if } i \neq k \\
 \min(\extsc{dbf}'(\tau_i, A_k + D_k)-C_k, A_k) & \text{if } i = k
 \end{array}
```

Equation 6:

$$I_{\text{dif}}(\tau_i)=I_2(\tau_i)-I_1(\tau_i)$$

Equation 7:

$$\sum_{\tau_i\in\tau}I_1(\tau_i)+\sum_{\text{the }(m-1)\text{ largest}}I_{\text{dif}}(\tau_i)>m(A_k+D_k-C_k)$$

Equation 8:

$$\left(\sum_{\tau_i\in\tau}I_1(\tau_i)+\sum_{\text{the }(m-1)\text{ largest}}I_{\text{dif}}(\tau_i)\right)\leq m(A_k+D_k-C_k)$$

Equation 9:

$$A_k\leq \frac{C_{\Sigma} - D_k (m-U(\tau)) + \sum_i (T_i - D_i)U_i + m C_k}{m-U(\tau)}$$

Also earlier definitions:

Definition of dbf* (Equation 4) appears as:

```
\extsc{dbf}^{*}(τ_i, t)\stackrel{{\mbox{iny{def}}}}{{=}} \left\lfloor\frac{t}{T_i}\right\rfloor \times C_i + \min(C_i, t \bmod T_i)
```

Also there is "load bound" maybe earlier but not given.

Also they mention I_1 defined as:

```
I_{1}(\tau_i)\stackrel{{\ext{iny def}}}{=}\{…\}
```

Thus we need to replicate the constraints exactly as they appear.

Also they may mention "Condition 8" as above.

Also "Theorem 2" says: For any task system τ, the global EDF on m processors schedules τ if and only if condition 8 holds for all τ_k.

Thus we need to state Theorem 2: "Theorem 2: For any task system τ, the global EDF scheduler on m identical unit-capacity processors schedules τ if and only if condition 8 holds for all tasks τ_k and all non-negative values A_k." Provide constraint.

Now we need to produce answer with section:

- Workload model
- Resource model
- Scheduler
- Analysis framework

Then list constraints.

Also provide explanation of each symbol.

Now produce final answer.

We must ensure to include all constraints exactly as appear. That includes equations with macros. But we may rewrite using LaTeX with the macros to preserve. But we need to replicate the exact formatting? It's ambiguous. We need to replicate the equations as they appear in the paper excerpt. The macros like \extsc{dbf} appear.

But we can provide them in LaTeX environment; we can preserve macros.

Now let's craft answer accordingly.