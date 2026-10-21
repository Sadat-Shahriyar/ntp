Require Import prosa.analysis.definitions.schedulability.
Section Simple_FP_RTA.

(* Task model: WCET, deadline, sporadic period *)
Context {Task : TaskType}.
Context `{TaskCost Task}.
Context `{TaskDeadline Task}.
Context `{SporadicModel Task}.
Context {FP : FP_policy Task}.
Variable ts : seq Task.

(* Lemma 1: Higher-priority interference expression *)
Definition interference_bound
    (tsk_i : Task) (t : duration) : duration :=
  \sum_(tsk_h <- ts | hp_task tsk_h tsk_i)
    (((t + task_min_inter_arrival_time tsk_h - 1)
       %/ task_min_inter_arrival_time tsk_h)
      * task_cost tsk_h).

(* Lemma 2: Response-time equation *)
Definition response_time_equation
    (tsk_i : Task) (R_i : duration) : Prop :=
  R_i =
    task_cost tsk_i
    + interference_bound tsk_i R_i.
.
.
.
(* Theorem 1: Schedulability Condition *)
Theorem schedulability_condition :
  schedulable_task arr_seq sched tsk_i.
Proof.
  eapply schedulability_from_response_time_bound.
  - exact H_completed.
  - exact H_deadline.
  - exact H_RTA.
Qed.

End Simple_FP_RTA.