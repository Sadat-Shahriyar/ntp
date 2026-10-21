# Prosa paper compatibility screening

## Scope and rule

Screened all **1843 PDF files** in `/lclhome/sshah169/Desktop/Sadat/0_phd/2_projects/4_neural_theorem_prover/14.code/Papers`. Every PDF was text-extracted; files with fewer than 1,000 extracted words are flagged.

A paper is recommended only when its model, scheduler, preemption semantics, analysis quantities, and theorem shape can be represented with the current Prosa documentation without a semantic extension. The decision is conservative. A final guarantee still requires the pipeline to classify every requirement as `EXACT_MATCH` or `COMPOSITIONAL_MATCH`, compile the Rocq output, and pass semantic fidelity.

The current reader accepts UTF-8 Markdown, so selected PDFs must first be converted to structured Markdown while preserving headings, equations, theorems, and proofs. This is preprocessing, not an architecture change.

## Counts

- `RECOMMENDED_NOW`: 10
- `SECOND_WAVE`: 4
- `BORDERLINE_NOT_RECOMMENDED`: 20
- `NOT_DIRECT`: 1766
- `INSUFFICIENT_EXTRACTABLE_TEXT`: 41
- `DO_NOT_PROCESS_COPY`: 2

## Recommended now

1. `/lclhome/sshah169/Desktop/Sadat/0_phd/2_projects/4_neural_theorem_prover/14.code/Papers/From_Intuition_to_Coq_A_Case_Study_in_Verified_Response-Time_Analysis_1_of_FIFO_Scheduling.pdf`

   Best match: sporadic jobs, FIFO scheduling, workload/interference, busy-window RTA, and a theorem already mechanized with Prosa.

2. `/lclhome/sshah169/Desktop/Sadat/0_phd/2_projects/4_neural_theorem_prover/14.code/Papers/In_Search_of_Butterflies_Exceedance_Analysis_for_Real-Time_Systems_under_Transient_Overload.pdf`

   Best match: the current Prosa tree contains ideal-uniprocessor exceedance facts and a restricted-supply exceedance RTA result.

3. `/lclhome/sshah169/Desktop/Sadat/0_phd/2_projects/4_neural_theorem_prover/14.code/Papers/General_and_efficient_Response_Time_Analysis_for_EDF_scheduling.pdf`

   Strong match: EDF, request/demand bounds, supply bounds, slack, and response-time theorems use existing Prosa vocabulary.

4. `/lclhome/sshah169/Desktop/Sadat/0_phd/2_projects/4_neural_theorem_prover/14.code/Papers/Fixed-Priority_Schedulability_of_Arbitrary-Deadline_Sporadic_Tasks_upon_Periodic_Resources.pdf`

   Strong match: sporadic tasks, arbitrary deadlines, fixed priorities, periodic resources, and restricted supply align with Prosa PRM/FP results.

5. `/lclhome/sshah169/Desktop/Sadat/0_phd/2_projects/4_neural_theorem_prover/14.code/Papers/Periodic_resource_model_for_compositional_real-time_guarantees.pdf`

   Strong match: periodic resource supply, EDF/RM, supply-bound functions, and compositional schedulability align with Prosa PRM modules.

6. `/lclhome/sshah169/Desktop/Sadat/0_phd/2_projects/4_neural_theorem_prover/14.code/Papers/Response_Time_Upper_Bounds_for_Fixed_Priority_Real-Time_Systems.pdf`

   Strong match: fixed-priority response-time bounds with jitter, blocking, and several preemption models map to current Prosa RTA results.

7. `/lclhome/sshah169/Desktop/Sadat/0_phd/2_projects/4_neural_theorem_prover/14.code/Papers/Worst-Case_Response_Time_Analysis_of_Real-Time_Tasks_under_Fixed-Priority_Scheduling_with_Deferred_Preemption_Revisited.pdf`

   Strong match: fixed-priority deferred/limited preemption and busy-window RTA match Prosa limited-preemption results.

8. `/lclhome/sshah169/Desktop/Sadat/0_phd/2_projects/4_neural_theorem_prover/14.code/Papers/Improved_schedulability_analysis_of_implicit_deadline_tasks_under_limited_preemption_EDF_scheduling.pdf`

   Strong match: uniprocessor EDF with implicit deadlines and limited preemption matches current Prosa EDF limited-preemption concepts.

9. `/lclhome/sshah169/Desktop/Sadat/0_phd/2_projects/4_neural_theorem_prover/14.code/Papers/Improvement_to_Quick_Processor-Demand_Analysis_for_EDF-Scheduled_Real-Time_Systems.pdf`

   Strong match: EDF, arbitrary deadlines, processor demand, and finite search-space refinement align with Prosa EDF analysis/refinements.

10. `/lclhome/sshah169/Desktop/Sadat/0_phd/2_projects/4_neural_theorem_prover/14.code/Papers/A_Sufficient_Condition_for_Rate_Monotonic_Schedulability_Based_on_Response_Time_Analysis.pdf`

   Strong match: independent periodic tasks, preemptive uniprocessor RM, response-time recurrence, and a sufficient schedulability theorem use current Prosa concepts.

## Second wave

Try these only after the recommended set; they are close, but exact matching or extraction is less certain.

1. `/lclhome/sshah169/Desktop/Sadat/0_phd/2_projects/4_neural_theorem_prover/14.code/Papers/Exact_response-time_analysis_for_fixed-priority_preemption-threshold_scheduling.pdf`

   Representable via Prosa priority and run-to-completion-threshold/limited-preemption concepts, but theorem labels are poorly exposed by extraction.

2. `/lclhome/sshah169/Desktop/Sadat/0_phd/2_projects/4_neural_theorem_prover/14.code/Papers/Generalized_Fixed-Priority_Scheduling_with_Limited_Preemptions.pdf`

   The vocabulary is supported, but the combined FPGS policy must be confirmed as a composition of current limited-preemption semantics.

3. `/lclhome/sshah169/Desktop/Sadat/0_phd/2_projects/4_neural_theorem_prover/14.code/Papers/Response_Time_Analysis_of_Asynchronous_Periodic_and_Sporadic_Tasks_Sheduled_by_a_Fixed_Priority_Preemptive_Algorithm.pdf`

   Periodic/sporadic arrivals, offsets, arbitrary deadlines, and FP preemption are supported, but key results are presented mainly as algorithms.

4. `/lclhome/sshah169/Desktop/Sadat/0_phd/2_projects/4_neural_theorem_prover/14.code/Papers/A_Matter_of_Overhead__Response_Time_Analysis_of_Hard_Real-Time_Systems_in_Theory_and_Practice.pdf`

   Prosa has generic overhead-aware FP RTA, but the paper’s concrete RTOS overhead accounting must match it exactly.

## Complete per-file results

`reports/prosa_paper_compatibility_all.csv` contains one row for each of the 1,843 PDFs with exact path, classification, text size, support/blocking signals, rationale, and review basis.
