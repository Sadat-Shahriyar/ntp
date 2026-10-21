From prosa Require Import prelude.  (* or whatever base modules you need *)
From prosa Require Import schedule.  (* job scheduling, service, etc. *)
From prosa Require Import schedulability.  (* maybe you build in a custom module *)
From mathcomp Require Import ssreflect ssrfun ssrbool eqtype ssrnat seq bigop.

Section Global_EDF_Model.

  (** --- Task and System Definitions --- **)

  (** You may either reuse or define your own task/workload interface. For instance: *)

  Variable Job : Type.
  Variable Task : Type.

  (* Arrival, cost, deadline, period *)
  Variable arr_time : Job → time.
  Variable task_of : Job → Task.
  Variable cost_of : Job → time.
  Variable dl_of : Job → time.
  Variable period_of : Task → time.

  (* Map tasks to their WCET, deadline, period: *)
  Variable C : Task → time.
  Variable D : Task → time.
  Variable T : Task → time.

  Hypothesis constrained_deadlines : forall τ, D τ <= T τ.

  (* You’ll also need consistency: for each job j, cost_of j = C (task_of j), etc. *)
  Hypothesis job_cost_correct : ∀ j, cost_of j = C (task_of j).
  Hypothesis job_deadline_correct : ∀ j, dl_of j = arr_time j + D (task_of j).

  (** Definition: Utilization, Density **)
  Definition u (τ : Task) : rat := (C τ) / (T τ).
  Definition δ (τ : Task) : rat := (C τ) / (D τ).

  (** Set of tasks / jobs in the system **)
  Variable tasks : seq Task.
  (* Optionally, we might define a predicate “is_a_job_of_system j” etc. *)

  Definition δ_sum := \sum_(τ in tasks) δ τ.
  Definition δ_max := \max_(τ in tasks) δ τ.

  (** The Density Test (prior work) — Lemma statement form **)
  Lemma density_test :
    δ_sum <= m%:R - (m.-1)%:R * δ_max → (* where m is a parameter you will fix *)
    (* then the system is schedulable under global EDF *)
    (* You’d express this by: no job ever misses deadline under a schedule that respects EDF assumptions *)
    (* e.g. schedulability_of_global_edf tasks ... *)
    schedulable_global_edf tasks.
  Proof.
    (* Proof sketch: you can reuse or adapt arguments from prior literature, but you’ll have to
       formalize the “if a job misses, then sum I > m * (Aₖ + Dₖ - Cₖ)” etc., and then
       rule out a counterexample by density bound. *)
  Admitted.

  (** --- Demand bound function definitions --- **)

  Definition DBF (τ : Task) (t : time) : time :=
    if (t < D τ) then 0 else
    (( (t - D τ) %/ (T τ) ) + 1) * C τ.

  Definition DBF′ (τ : Task) (t : time) : time :=
    (t %/ (T τ)) * C τ + min (C τ) (t %% (T τ)).

  (** Work contributions I₁, I₂, IDIFF **)

  Definition I1 (τi : Task) (τk : Task) (Aₖ : time) : time :=
    if τi != τk then
      min (DBF τi (Aₖ + D τk)) (Aₖ + D τk - C τk)
    else
      min ( (DBF τk (Aₖ + D τk) - C τk) ) Aₖ.

  Definition I2 (τi : Task) (τk : Task) (Aₖ : time) : time :=
    if τi != τk then
      min (DBF′ τi (Aₖ + D τk)) (Aₖ + D τk - C τk)
    else
      min ( (DBF′ τk (Aₖ + D τk) - C τk) ) Aₖ.

  Definition IDIFF (τi : Task) (τk : Task) (Aₖ : time) : time :=
    I2 τi τk Aₖ - I1 τi τk Aₖ.

  (** Now the “main schedulability test” theorem (Theorem 2 in your description) **)

  Theorem global_edf_schedulability_test :
    forall τk Aₖ,
      0 <= Aₖ →
      (\sum_(τi in tasks) I1 τi τk Aₖ)
        + (\sum_(τi in (take_largest (m.-1) (map (fun τ ⇒ IDIFF τ τk Aₖ) tasks)))
           (fun τ => IDIFF τ τk Aₖ))
      <= m * (Aₖ + D τk - C τk)
      → schedulable_global_edf tasks.
  Proof.
    (* Here you must relate this inequality to the necessary condition (Eq. 2) and show
       that violation would imply missing a deadline, then derive a contradiction, etc. *)
  Admitted.

  (** The search bound on Aₖ (Theorem 3) **)

  (* Precompute some bounds / quantities: sum of largest (m−1) WCETs, total utilization, etc. *)
  Definition C_sigma := \sum_(τ in top_k_largest (m.-1) (map C tasks)) (fun τ => C τ).
  Definition U_total := \sum_(τ in tasks) u τ.

  Theorem Ak_search_bound :
    forall τk Aₖ,
      0 <= Aₖ ≤
        (C_sigma - D τk * (m - U_total)%:R
         + \sum_(τ in tasks) ((T τ - D τ)%:R * u τ)
         + m%:R * C τk)
        / ( (m%:R) - U_total ) →
      (* It suffices to check only up to that bound *)
      (* I.e., if the schedulability test holds for all Aₖ in that range, then the system is_schedulable *)
      ( (∀ A' ≤ that_bound, (* instantiate same inequality from above for A' *)) →
        schedulable_global_edf tasks ).
  Proof.
    Admitted.

End Global_EDF_Model.
