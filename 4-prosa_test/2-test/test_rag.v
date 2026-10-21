Require Export prosa.behavior.schedule.
Require Export prosa.model.task.concept.

Section VarsCoreTypes.
  Context {Job : JobType}.
  Context {Task : TaskType}.
  Context {PState : ProcessorState Job}.

  Notation time := instant.

  Record interval := {
    t_start : time;
    t_end   : time
  }.

  Notation task := Task.
  Notation job  := Job.

  Definition schedule_t : Type := schedule PState.
End VarsCoreTypes.


Section VarsGlobalParameters.
  Context {Job : JobType}.
  Context {Task : TaskType}.
  Context {PState : ProcessorState Job}.

  (* platform and schedule context *)
  Variable m : nat.

  (* task set *)
  Variable ts : list Task.
  Notation task_set := ts.

  (* arrival sequence and schedule *)
  Variable arr_seq : arrival_sequence Job.
  Variable sch : schedule_t.

  (* see modeling assumptions for m and EDF scheduler :contentReference[oaicite:0]{index=0} *)
End VarsGlobalParameters.


(*
  ====section==== vars_task_parameters
  basic per-task parameters and ratios
*)
Section VarsTaskParameters.
  Context {Job : JobType}.
  Context {Task : TaskType}.
  Context {PState : ProcessorState Job}.

  Notation time := instant.
  Notation task := Task.

  (* declare function c_i (t : task) : time *)
  Variable c_i : task -> time.

  (* declare function d_i (t : task) : time *)
  Variable d_i : task -> time.

  (* declare function t_i (t : task) : time *)
  Variable t_i : task -> time.

  (* a placeholder type for rational numbers *)
  Parameter rational : Type.

  (* declare function u_i (t : task) : rational *)
  Variable u_i : task -> rational.
  (* intended: u_i t = c_i t / t_i t *)

  (* declare function delta_i (t : task) : rational *)
  Variable delta_i : task -> rational.
  (* intended: delta_i t = c_i t / d_i t *)

End VarsTaskParameters.
From mathcomp Require Import ssreflect ssrfun ssrbool eqtype ssrnat seq div.

Require Export prosa.util.rel.
Require Export prosa.model.task.arrivals.

(*
  ====section==== define_demand_bound_function
  define dbf with parameters tsk, len_t
  comment: return max(0, (floor((len_t - d_i(tsk))/t_i(tsk)) + 1) * c_i(tsk))
  comment: definition for constrained/implicit deadlines only
  comment: formal reference for dbf equation :contentReference[oaicite:2]{index=2}
*)
Section DefineDemandBoundFunction.
  Context {Job : JobType}.
  Context {Task : TaskType}.
  Context {PState : ProcessorState Job}.

  Notation time := instant.
  Notation task := Task.

  (* task parameters *)
  Variable c_i : task -> time.
  Variable d_i : task -> time.
  Variable t_i : task -> time.

  (* Constrained/implicit deadlines:
     dbf(tsk, Δ) = 0
                 , if Δ < d_i(tsk)
                 = (⌊(Δ - d_i(tsk))/t_i(tsk)⌋ + 1) * c_i(tsk)
                 , otherwise. *)
  Definition dbf (tsk : task) (len_t : time) : time :=
    if len_t < d_i tsk then 0
    else (((len_t - d_i tsk) %/ (t_i tsk)).+1) * (c_i tsk).

End DefineDemandBoundFunction.
