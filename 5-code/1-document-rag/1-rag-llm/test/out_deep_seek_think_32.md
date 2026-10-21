The theorem provides an exact schedulability condition for EDF scheduling on multiple processors by considering carry-in from at most m-1 tasks, ensuring deadlines are met in the worst-case scenario. The condition involves checking a specific inequality across all tasks and relevant values of A_k, with the number of checks bounded to ensure practicality despite pseudo-polynomial runtime. This approach offers improved accuracy over previous tests but requires careful consideration of computational resources.

**Step-by-Step Explanation:**

1. **Task System Overview:** We have n sporadic task systems on m unit-capacity processors. Each task has parameters like execution time (C_i), period (T_i), and deadline (D_i).

2. **EDF Schedulability Test:** The goal is to determine if all tasks can meet their deadlines using EDF scheduling. This involves checking a specific inequality for each task k and variable A_k.

3. **Key Components:**
   - **I1(au_i):** Represents the base demand of task i without carry-in, calculated as min(C_i, (A_k + D_k)/T_i * C_i) or another expression based on thresholds.
   - **I_diff(au_i):** The additional demand due to carry-in for task i, computed as I2(au_i) - I1(au_i).

4. **Inequality Condition:** For all A_k ≥ 0 and each task k,
   \[
   \sum_{i} I_1(\tau_i) + \sum_{\text{largest } m-1} I_{\text{diff}}(\tau_i) \leq m(A_k + D_k - C_k)
   \]
   This ensures that the total required processing time does not exceed the available capacity.

5. **Bounded A_k Values:** Theorem 3 provides an upper bound on A_k, reducing the number of checks needed. This bound is derived from task parameters and utilization factors.

6. **Runtime Complexity:** While the algorithm has pseudo-polynomial runtime when system utilization is bounded, it's feasible for practical systems with low utilization or specific parameter distributions.

7. **Comparison to Previous Tests:** Unlike earlier polynomial-time tests (e.g., BAK, BCL), this test is exact for uniprocessors and more accurate in multi-processor scenarios, especially when n >> m or task parameters vary widely.

8. **Conclusion:** This test offers a precise schedulability analysis for EDF on multiple processors by considering carry-in from up to m-1 tasks, ensuring correctness despite higher computational requirements.

**Final Answer:**

The theorem establishes an exact EDF schedulability condition for multi-processor systems by evaluating the sum of base and top m-1 additional task demands against processor capacity across all relevant A_k values. This method ensures deadlines are met without overcounting carry-in, providing a more accurate but computationally intensive test compared to previous approaches.

**\boxed{\text{EDF Schedulability Test for Multi-Processor Systems}}**