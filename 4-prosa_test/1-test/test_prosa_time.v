From Coq Require Import Arith.
From Coq Require Import Lia.
From prosa.classic.model Require Import time.

Import Nat.

(* Open the Time module so we can use its contents directly *)
Import Time.

(* Define some sample time instants *)
Definition t1 : time := 5.
Definition t2 : time := 12.

(* Define a duration *)
Definition d1 : duration := 7.

(* Define a new instant obtained by adding duration to time *)
Definition t3 : instant := t1 + d1.

(* Compute results *)
Compute t1.
Compute t2.
Compute d1.
Compute t3.

(* Example property: show that t3 is less than t2 + 10 *)
Lemma t3_less_than_t2_plus_10 : t3 < t2 + 10.
Proof.
  unfold t3, t1, d1, t2; simpl; lia.
Qed.
