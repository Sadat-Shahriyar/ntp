Require Import prosa.behavior.all.
(* Require Import prosa.implementation.all. *)
Require Import prosa.analysis.facts.behavior.all.
From mathcomp Require Import ssreflect ssrbool eqtype ssrnat seq fintype bigop div ssralg ssrnum rat.
Require Import mathcomp.ssreflect.ssrfun.

(** * Formalization of Global EDF Schedulability Analysis *)

Section SporadicTaskModel.

  (** Import rat for rational numbers *)
  Import Num.Theory.
  Open Scope ring_scope.

  (** Task type - we use eqType for tasks *)
  Variable Task : eqType.
  
  (** Task parameters as functions *)
  Variable task_cost : Task -> nat.
  Variable task_deadline : Task -> nat.
  Variable task_period : Task -> nat.

  (** Task set *)
  Variable ts : seq Task.
  
  (** Number of processors *)
  Variable m : nat.
  Hypothesis m_positive : m > 0.

  (** ** 1. Basic Task Model Definitions *)

  (** Utilization of a task *)
  Definition task_utilization (tsk : Task) : rat :=
    (task_cost tsk)%:Q / (task_period tsk)%:Q.

  (** Density of a task *)
  Definition task_density (tsk : Task) : rat :=
    (task_cost tsk)%:Q / (task_deadline tsk)%:Q.

  (** Total utilization *)
  Definition total_utilization : rat :=
    \sum_(tsk <- ts) task_utilization tsk.

  (** Total density *)
  Definition total_density : rat :=
    \sum_(tsk <- ts) task_density tsk.

  (** Maximum density *)
  Definition max_density : rat :=
    \big[Num.max/0]_(tsk <- ts) task_density tsk.

  (** Sum of m-1 largest execution times *)
  Definition C_sum : nat :=
    let costs := [seq task_cost tsk | tsk <- ts] in
    let sorted := sort geq costs in
    \sum_(i <- take (m.-1) sorted) i.

  (** ** 2. Demand Bound Function (DBF) *)

  (** Standard DBF without carry-in *)
  Definition DBF (tsk : Task) (t : nat) : nat :=
    let D := task_deadline tsk in
    let T := task_period tsk in
    let C := task_cost tsk in
    if t < D then 0
    else ((t - D) %/ T).+1 * C.

  (** DBF with carry-in (DBF') *)
  Definition DBF_with_carryin (tsk : Task) (t : nat) : nat :=
    let T := task_period tsk in
    let C := task_cost tsk in
    let full_jobs := t %/ T in
    let remainder := t %% T in
    full_jobs * C + minn C remainder.

  (** ** 3. Work Contribution Functions *)

  (** Work contribution without carry-in (I₁) *)
  Definition work_contribution_no_carryin 
    (tsk : Task) (tsk_k : Task) (A_k : nat) : nat :=
    let D_k := task_deadline tsk_k in
    let C_k := task_cost tsk_k in
    if tsk == tsk_k then
      minn (DBF tsk_k (A_k + D_k) - C_k) A_k
    else
      minn (DBF tsk (A_k + D_k)) (A_k + D_k - C_k).

  (** Work contribution with carry-in (I₂) *)
  Definition work_contribution_with_carryin 
    (tsk : Task) (tsk_k : Task) (A_k : nat) : nat :=
    let D_k := task_deadline tsk_k in
    let C_k := task_cost tsk_k in
    if tsk == tsk_k then
      minn (DBF_with_carryin tsk_k (A_k + D_k) - C_k) A_k
    else
      minn (DBF_with_carryin tsk (A_k + D_k)) (A_k + D_k - C_k).

  (** Difference in work contribution (IDIFF) *)
  Definition work_diff (tsk : Task) (tsk_k : Task) (A_k : nat) : nat :=
    work_contribution_with_carryin tsk tsk_k A_k - 
    work_contribution_no_carryin tsk tsk_k A_k.

  (** Sum of I₁ over all tasks *)
  Definition total_work_no_carryin (tsk_k : Task) (A_k : nat) : nat :=
    \sum_(tsk <- ts) work_contribution_no_carryin tsk tsk_k A_k.

  (** Sum of m-1 largest IDIFF values *)
  Definition sum_largest_diffs (tsk_k : Task) (A_k : nat) : nat :=
    let diffs := [seq work_diff tsk tsk_k A_k | tsk <- ts] in
    let sorted_diffs := sort geq diffs in
    \sum_(d <- take (m.-1) sorted_diffs) d.

  (** ** 4. Schedulability Tests *)

  (** Density Test (Equation 1) *)
  Definition density_test_holds : bool :=
    (total_density <= m%:Q - (m.-1)%:Q * max_density)%R.

  (** Main Schedulability Test (Theorem 2 / Equation 8) *)
  Definition schedulability_test (tsk_k : Task) (A_k : nat) : bool :=
    let D_k := task_deadline tsk_k in
    let C_k := task_cost tsk_k in
    let lhs := total_work_no_carryin tsk_k A_k + sum_largest_diffs tsk_k A_k in
    let rhs := m * (A_k + D_k - C_k) in
    lhs <= rhs.

  (** Search bound for A_k (Theorem 3 / Equation 9) *)
  Definition A_bound (tsk_k : Task) : rat :=
    let D_k := (task_deadline tsk_k)%:Q in
    let C_k := (task_cost tsk_k)%:Q in
    let U := total_utilization in
    let sum_slack := \sum_(tsk <- ts) 
      ((task_period tsk - task_deadline tsk)%:Q * task_utilization tsk) in
    let numerator := C_sum%:Q - D_k * (m%:Q - U) + sum_slack + m%:Q * C_k in
    let denominator := m%:Q - U in
    if (denominator > 0)%R then (numerator / denominator)%R else 0.

  (** Global schedulability condition *)
  Definition is_schedulable : bool :=
    all (fun tsk_k =>
      let bound := Num.trunc (A_bound tsk_k) in
      all (fun A_k => schedulability_test tsk_k A_k) (iota 0 bound.+1)
    ) ts.

  (** ** 5. Key Properties and Lemmas *)

  (** Lemma: DBF is monotonic *)
  Lemma DBF_monotonic : forall tsk t1 t2,
    t1 <= t2 -> DBF tsk t1 <= DBF tsk t2.
  Proof.
    move=> tsk t1 t2 Hle.
    rewrite /DBF.
    case: (boolP (t1 < task_deadline tsk)) => [Hlt1 | Hnlt1].
    - case: (boolP (t2 < task_deadline tsk)) => [Hlt2 | Hnlt2].
      + by [].
      + by [].
    - case: (boolP (t2 < task_deadline tsk)) => [Hlt2 | Hnlt2].
      + move: Hnlt1. rewrite -leqNgt => Hge1.
        move: Hlt2. rewrite ltnNge => /negP Hnge2.
        exfalso. apply: Hnge2. by apply: (leq_trans Hge1 Hle).
      + apply: leq_mul => //.
        apply: leq_div2r. by rewrite leq_sub2r.
  Qed.

  (** Lemma: DBF' is monotonic *)
  Lemma DBF_carryin_monotonic : forall tsk t1 t2,
    t1 <= t2 -> DBF_with_carryin tsk t1 <= DBF_with_carryin tsk t2.
  Proof.
    move=> tsk t1 t2 Hle.
    rewrite /DBF_with_carryin.
    apply: leq_add.
    - apply: leq_mul => //. by apply: leq_div2r.
    - rewrite leq_min. apply/andP; split.
      + by [].
      + by apply: (leq_trans (leq_mod _ _) Hle).
  Qed.

  (** Lemma: Work contribution is bounded *)
  Lemma work_contribution_bounded : forall tsk tsk_k A_k,
    work_contribution_no_carryin tsk tsk_k A_k <= 
    A_k + task_deadline tsk_k - task_cost tsk_k.
  Proof.
    move=> tsk tsk_k A_k.
    rewrite /work_contribution_no_carryin.
    case: (tsk == tsk_k).
    - rewrite leq_min. by apply/andP; split; [apply: leq_subr | apply: leqnn].
    - rewrite leq_min. by apply/andP; split; [apply: leq_addr | apply: leqnn].
  Qed.

  (** ** 6. Main Theorems (Statements) *)

  (** Theorem 2: Schedulability test is sufficient *)
  Theorem schedulability_test_sufficient :
    (forall tsk_k, tsk_k \in ts ->
      forall A_k, A_k <= Num.trunc (A_bound tsk_k) ->
        schedulability_test tsk_k A_k) ->
    (* Global EDF schedulability follows *)
    True. (* Placeholder - full proof requires job model *)
  Proof.
    move=> H.
    (* The complete proof would require:
       1. Job arrival model
       2. Schedule construction
       3. Deadline miss analysis
       4. Showing contradiction when test holds
       This is a research-level proof effort. *)
    by [].
  Qed.

  (** Theorem 3: A_bound is sufficient for search space *)
  Theorem search_bound_sufficient :
    forall tsk_k A_k,
      tsk_k \in ts ->
      A_k > Num.trunc (A_bound tsk_k) ->
      schedulability_test tsk_k A_k.
  Proof.
    move=> tsk_k A_k Hin Hgt.
    (* Proof sketch:
       - Show that beyond A_bound, the RHS grows faster than LHS
       - Use utilization constraint: m - U(τ) > 0
       - Apply arithmetic on equation (9) 
       This requires detailed workload analysis. *)
  Admitted.

  (** Density test implies schedulability for certain systems *)
  Theorem density_implies_schedulability :
    density_test_holds ->
    (total_utilization < m%:Q)%R ->
    is_schedulable.
  Proof.
    move=> Hdens Hutil.
    (* This is a known result - density test is sufficient
       when it holds. Proof requires showing that the 
       schedulability test is always satisfied. *)
  Admitted.

End SporadicTaskModel.

(** Close the ring scope *)
Close Scope ring_scope.

(** ** 7. Example Usage *)

Section Example.
  
  (* Define a concrete task type for demonstration *)
  Record concrete_task := {
    ct_id : nat;
    ct_cost : nat;
    ct_deadline : nat;
    ct_period : nat
  }.

  (* Equality for concrete tasks *)
  Definition concrete_task_eqb (t1 t2 : concrete_task) : bool :=
    (ct_id t1 == ct_id t2) && (ct_cost t1 == ct_cost t2) &&
    (ct_deadline t1 == ct_deadline t2) && (ct_period t1 == ct_period t2).

  Lemma concrete_task_eqP : Equality.axiom concrete_task_eqb.
  Proof.
    move=> [id1 c1 d1 p1] [id2 c2 d2 p2].
    rewrite /concrete_task_eqb /=.
    apply: (iffP idP).
    - move=> /andP [/andP [/andP [/eqP Hid /eqP Hc] /eqP Hd] /eqP Hp].
      by rewrite Hid Hc Hd Hp.
    - case=> -> -> -> ->.
      by rewrite !eq_refl.
  Qed.

  Canonical concrete_task_eqMixin := EqMixin concrete_task_eqP.
  Canonical concrete_task_eqType := Eval hnf in EqType concrete_task concrete_task_eqMixin.

  (* Example task set: 3 tasks on 2 processors *)
  Definition example_tasks : seq concrete_task := [::
    {| ct_id := 0; ct_cost := 1; ct_deadline := 3; ct_period := 3 |};
    {| ct_id := 1; ct_cost := 2; ct_deadline := 5; ct_period := 5 |};
    {| ct_id := 2; ct_cost := 1; ct_deadline := 7; ct_period := 7 |}
  ].

  (* Check density test *)
  Definition check_density := 
    density_test_holds ct_cost ct_deadline ct_period example_tasks 2.
  
  (* Compute check_density. *)

End Example.