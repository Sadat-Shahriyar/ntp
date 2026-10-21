
input_text = '''
Here are the contents of the paper: 
```
## 2 Model

A _sporadic task_\(\tau_{i}=(C_{i},D_{i},T_{i})\) is characterized by a _worst-case execution requirement_\(C_{i}\), a _(relative) deadline_\(D_{i}\), and a _minimum inter-arrival separation_\(T_{i}\), which is, for historical reasons, also referred to as the _period_ of the task. Such a sporadic task generates a potentially infinite sequence of jobs, with successive job-arrivals separated by at least \(T_{i}\) time units. Each job has a worst-case execution requirement equal to \(C_{i}\) and a deadline that occurs \(D_{i}\) time units after its arrival time. We refer to the interval, of size \(D_{i}\), between such a job's arrival instant and deadline as its _scheduling window_. We assume a fully _preemptive_ execution model: any executing job may be interrupted at any instant in time, and its execution resumed later with no cost or penalty. A _sporadic task system_ is comprised of several such sporadic tasks. Let \(\tau\) denote a system of such sporadic tasks: \(\tau=\{\tau_{1},\tau_{2},\ldots\tau_{n}\}\), with \(\tau_{i}=(C_{i},D_{i},T_{i})\) for all \(i\), \(1\leq i\leq n\). Task system \(\tau\) is said to be a _constrained_ sporadic task system if it is guaranteed that each task \(\tau_{i}\in\tau\) has its relative deadline parameter no larger than its period: \(D_{i}\leq T_{i}\), and an _implicit-deadline_ sporadic task system if \(D_{i}=T_{i}\) for all \(\tau_{i}\in\tau\). (Implicit-deadline systems are also known as _Liu and Layland_[22] task systems.) _In this paper, we restrict our attention to constrained and implicit-deadline task systems._

Schedulability.A real-time system implemented on a particular computing platform is said to be \(A\)-schedulable with respect to a given scheduling algorithm \(A\), if the algorithm \(A\) schedules the system such that all jobs of all tasks will meet all deadlines, under all permissible (also called _legal_) combinations of job-arrival sequences by the different tasks comprising the system. A _schedulability test_ for scheduling algorithm \(A\) (also called an _\(A\)-schedulability test_) accepts as input the specifications of a real-time system, and determines whether the system is \(A\)-schedulable or not. An \(A\)-schedulability test is said to be _exact_ if it correctly identifies all \(A\)-schedulable systems, and _sufficient_ if it may fail to identify some \(A\)-schedulable systems (it must guarantee, though, that all identified systems are indeed \(A\)-schedulable.)

Task and system characteristics.The concepts of task and system _utilization_ and _density_ prove useful in the analysis of sporadic task systems on multiprocessors. These concepts are defined as follows:

**Utilization:**: The utilization \(u_{i}\) of a task \(\tau_{i}\) is the ratio \(C_{i}/T_{i}\) of its execution time to its period. The total utilization \(u_{\mathrm{sum}}(\tau)\) and the largest utilization \(u_{\mathrm{max}}(\tau)\) of a task system \(\tau\) are defined as follows:

\[u_{\mathrm{sum}}(\tau)\stackrel{{\mbox{\tiny{\rm def}}}}{{=}} \sum_{\tau_{i}\in\tau}u_{i};\hskip 14.226378ptu_{\mathrm{max}}(\tau) \stackrel{{\mbox{\tiny{\rm def}}}}{{=}}\max_{\tau_{i}\in\tau}(u_ {i})\]
**Density:**: The density \(\delta_{i}\) of a task \(\tau_{i}\) is the ratio \(C_{i}/D_{i}\) of its execution time to its relative deadline. The total density \(\delta_{\mathrm{sum}}(\tau)\) and the largest density \(\delta_{\mathrm{max}}(\tau)\) of a task system \(\tau\) are defined as follows:

\[\delta_{\mathrm{sum}}(\tau)\stackrel{{\mbox{\tiny{\rm def}}}}{{=}} \sum_{\tau_{i}\in\tau}\delta_{i};\hskip 14.226378pt\delta_{\mathrm{max}}(\tau) \stackrel{{\mbox{\tiny{\rm def}}}}{{=}}\max_{\tau_{i}\in\tau}( \delta_{i})\]

An additional concept that plays a critical role in the schedulability analysis of sporadic task systems is that of **demand bound function**. For any interval length \(t\), the demand bound function \(\textsc{dbf}(\tau_{i},t)\) of a sporadic task \(\tau_{i}\) bounds the maximum cumulative execution requirement by jobs of \(\tau_{i}\) that both arrive in, and have deadlines within, any interval of length \(t\). It has been shown [9] that

\[\textsc{dbf}(\tau_{i},t)=\max\left(0,\left(\left\lfloor\frac{t-D_{i}}{T_{i}} \right\rfloor+1\right)C_{i}\right)\]

A **load** parameter, based upon the dbf function, may be defined for any sporadic task system \(\tau\) as follows:

\[\textsc{load}(\tau)\stackrel{{\mbox{\tiny{\rm def}}}}{{=}}\max_{t>0 }\left(\frac{\sum_{\tau_{i}\in\tau}\textsc{dbf}(\tau_{i},t)}{t}\right)\] Fixed job-priority (FJP) scheduling.Run-time scheduling algorithms are typically implemented as follows: at each time instant, a _priority_ is assigned to each job that has been released but not yet completed, and the available processors are allocated to the highest-priority jobs. In edf scheduling, jobs are assigned priorities according to their deadline parameters: the earlier the deadline of a job, the greater its priority.

It has long been known that global edf, in common with many other global scheduling schemes, suffers from the so-called Dhall effect [15] which results in task systems with arbitrarily low utilization and density not being edf-schedulable. In order to circumvent the Dhall effect, hybrid variants of edf have been designed [18] in which all the jobs of some selected tasks are assigned highest priority, and the remaining tasks' jobs are assigned priorities according to edf. Such priority-driven scheduling algorithms are instances of a class of algorithms called _fixed job-priority_ (FJP) scheduling algorithms. In FJP scheduling algorithms, the priority of a job may not change between its arrival time and the instant it completes execution; however, different jobs of the same task may have different priorities. (In contrast, fixed task-priority (FTP) algorithms require that all jobs of a task have the same -fixed- priority, while in dynamic-priority (DP) algorithms the priority of a job may change between its arrival time and its completion time. It is evident from these definitions that FJP scheduling is a generalization of FTP scheduling, and DP scheduling is a generalization of FJP scheduling.)

## 3 Global scheduling and Worst-case behavior

Recall that in order for a sporadic task system to be considered \(A\)-schedulable for a given scheduling algorithm \(A\), \(A\) must generate schedules meeting all deadlines for all legal job-arrival sequences of the task system. Since any sporadic task system has infinitely many different legal job arrival sequences, an approach of exhaustive enumeration of such sequences, followed by simulating algorithm \(A\) on each of these sequences, will not yield an effective schedulability test. Instead, the typical approach has been to identify one or a few _worst-case job arrival sequences_ for a task system for which it can be proved that if algorithm \(A\) successfully schedules all these worst-case job arrival sequences, then \(A\) is guaranteed to successfully schedule all legal job arrival sequences of the task system. For example, with respect to edf or Deadline-Monotonic (DM) scheduling upon preemptive uniprocessors it is known [22, 20, 9] that there is a unique worst-case job arrival sequence: every task has one job arrive at the same instant in time, and each task has subsequent jobs arrive as soon as legally permitted to do so. (Such a job arrival sequence is often called the _synchronous arrival sequence_ for the task system.) It has been shown [7, 17, 8] that the synchronous arrival sequence is also the worst-case job arrival sequence for partitioned multiprocessor edf and DM scheduling.

For global scheduling, however, the synchronous arrival sequence is not necessarily the worst-case arrival sequence, as the following example illustrates with respect to edf scheduling.

**Example 1**: Consider the task system comprised of the three tasks \(\tau_{1}=(1,1,2)\), \(\tau_{2}=(1,1,3)\), and \(\tau_{3}=(5,6,6)\), executing upon two unit-capacity processors. It may be seen (Figure 1 (a)) that the synchronous arrival sequence is successfully scheduled by edf to meet all deadlines. However, if task \(\tau_{1}\)'s second job were to arrive three, rather than two, time units after the first (Figure 1 (b)), then edf would miss some deadline over the interval \([0,6]\) (and indeed, no scheduling algorithm can possibly guarantee to meet all deadlines for this job arrival sequence). \(\blacksquare\)

Without knowing what the worst-case behavior of a sporadic task system may be, it is not possible to design simulation-based exact (necessary as well as sufficient) schedulability tests. To our knowledge, no finite collection of worst-case job arrival sequences has been identified for global scheduling of sporadic task systems. This, at a basic level, is the fundamental difference between our understanding of partitioned and global scheduling of sporadic task systems. As stated above, it is known that the synchronous arrival sequence represents the worst-case behavior of a task system under partitioned scheduling. Hence, partitioned schedulability testing can be solved in principle by determining whether it is possible to partition the tasks among the processors such that no deadlines are missed in the synchronous arrival sequence. An exact algorithm for solving this is provably highly intractable, but approximation algorithms that run in polynomial time and exhibit excellent average-case and provably bounded worst-case behavior have been devised [7, 17, 8].

In the global case, however, we do not know how to determine schedulability even if computational tractability were not an issue. That is, we do not yet have an adequate understanding of what precisely the characteristics of a globally schedulable system are; without knowing these characteristics, it seems futile to seek accurate, efficient tests for identifying such systems. (In this regard, Example 1 above illustrates that load is not an exact indicator of schedulability: while load\((\tau)\leq m\) is clearly necessary for \(\tau\) to be edf-schedulable on an \(m\)-processor platform, the task system in Example 1 illustrates that this is not sufficient.) 

## 4 Partitioned versus global FJP scheduling

As stated in Section 1 above, simulation experiments [4, 6] have shown that currently-known global schedulability tests perform poorly compared to partitioned schedulability tests. That is, it appears that a far greater fraction of randomly-generated sporadic task systems are deemed schedulable by currently-known partitioned schedulability tests than by currently-known global schedulability tests.

One might consider this result surprising, since at first glance it appears that partitioned scheduling (which forbids jobs from migrating between processors) is a special case of global scheduling (which allows, but does not require, such migration). However, this is erroneous. It has previously been shown by Leung and Whitehead [21, page 242] with regard to fixed task priority (FTP) scheduling schemes that there are sporadic task systems schedulable by some global algorithm but not by any partitioned algorithm, and that there are other sporadic task systems that are schedulable by some partitioned algorithm but not by any global algorithm. Theorem 1 below demonstrates similar incomparability between global and partitioned scheduling for the more general class of FJP scheduling algorithms as well.

As one might expect, there are systems that global algorithms can schedule but partitioned ones cannot; this is formally shown in Lemma 1 below. Somewhat counter-intuitively, it turns out (Lemma 2 below) that there are systems which partitioned FJP algorithms can schedule, which cannot be scheduled by any global FJP algorithm.

**Lemma 1**: _There are task systems that are schedulable using global FJP algorithms that partitioned FJP algorithms cannot schedule._

**Proof Sketch:** Here's an example task system, on \(2\) processors:

\[\tau_{1}=(2,2,3),\tau_{2}=(3,3,4),\tau_{3}=(5,12,12)\]

Clearly, this system cannot be scheduled using partitioning, since \(u_{1}+u_{2}\), \(u_{1}+u_{3}\), and \(u_{2}+u_{3}\) are each \(>1\). To show that a global FJP algorithm can schedule this task system, consider any FJP algorithm which assigns lowest priority to \(\tau_{3}\)'s jobs. Since there are two processors, \(\tau_{1}\) and \(\tau_{2}\)'s jobs are guaranteed to meet all deadlines. Now observe that each job of \(\tau_{3}\) needs to execute for \(5\) time-slots over an interval of \(12\) slots1. Now over any \(12\) contiguous slots, \(\tau_{1}\) may execute during at most \(8\) slots, thereby leaving at least \(4\) slots for \(\tau_{3}\)'s job upon one processor.

Footnote 1: For ease of exposition, we are assuming a slotted model of time for this proof sketch; however, it is easily generalized to a non-slotted model.

* If \(\tau_{1}\) executes for fewer than \(8\) slots between a job of \(\tau_{3}\)'s scheduling window, then it is straightforward to see that the job of \(\tau_{3}\) completes execution by its deadline, since no more than one other job (of \(\tau_{2}\)) will be active during the at least \(5\) time units of this job's scheduling window.
* If \(\tau_{1}\)'s jobs execute for exactly \(8\) slots during the scheduling window of one of \(\tau_{3}\)'s jobs, it is easily seen that \(\tau_{1}\)'s jobs must be arriving exactly 3 time-units apart. Hence, it is not possible that \(\tau_{3}\)'s jobs execute in parallel with \(\tau_{1}\)'s jobs during all \(8\) of the time-slots during which \(\tau_{1}\)'s jobs execute within this scheduling window. Therefore there are at least 5 slots within this scheduling window during which one of both processors is idle after both \(\tau_{1}\) and \(\tau_{2}\) have been scheduled.

Perhaps surprisingly, the converse of the above lemma is also true:

**Lemma 2**: _There are task systems that are schedulable using partitioned FJP algorithms that global FJP algorithms cannot schedule._

**Proof Sketch:** Here's an example task system, on \(2\) processors:

\[\tau_{1}=(2,2,3),\tau_{2}=(3,3,4),\tau_{3}=(4,12,12),\tau_{4}=(3,12,12)\]

This task system may be partitioned by assigning \(\tau_{1}\) and \(\tau_{3}\) to one processor and the other two tasks to the remaining

Figure 1: Figure for Example 1, illustrating that the synchronous arrival sequence does not represent the worst case.

processor, and scheduling each processor using uniprocessor edf.

To show that no global FJP priority assignment scheme can meet all deadlines, consider the synchronous arrival sequence over the interval \([0,12)\). It may be verified that whichever of \(\tau_{3}\)'s and \(\tau_{4}\)'s job has lower priority ends up missing its deadline while one processor goes idle over \([11,12)\). \(\blacksquare\)

Hence our intuition that global is a generalization of partitioned turns out to be incorrect for FJP scheduling as well as FTP scheduling:

**Theorem 1**: _Global and partitioned FJP scheduling are **incomparable**._

One implication of this is that the current state of the art -- partitioned schedulability tests being far superior to global ones -- are not contradicted by facts (only intuition). That is, it has not been ruled out that a far larger fraction of sporadic task systems are schedulable under partitioned FJP scheduling as compared to global FJP scheduling.


## 6 An improved schedulability algorithm

We have designed a new global edf-schedulability test that overcomes some of these shortcomings of the [bak] and [bcl] tests. Our test possesses the following features that distinguishes it from the [bak] and [bcl] tests: _(i)_ it runs in time pseudo-polynomial in the representation of the task system; _(ii)_ it considers intervals \([t_{o},t_{d})\) that do not necessarily coincide with the scheduling window of the task \(\tau_{k}\) being assumed to miss its deadline; _(iii)_ it allows us to bound the number of tasks carrying in work into the interval \([t_{o},t_{d})\) at \((m-1)\), where \(m\) is the number of processors in the system. In contrast to the [bak] and [bcl] tests, it will be shown (Corollary 1) that our test generalizes the known exact edf-schedulability test on uniprocessors.

Our algorithm, like the [bcl] test, draws inspiration from the seminal work of Baker [2, 3] that yielded the [bak] test, and follows the same general framework. We consider each task \(\tau_{k}\) separately; when considering a specific \(\tau_{k}\), we identify sufficient conditions for ensuring that \(\tau_{k}\) cannot miss any deadlines. To ensure that no deadlines are missed by any task in \(\tau\), these conditions must be checked for each of the \(n\) tasks \(\tau_{1}\), \(\tau_{2},\ldots,\tau_{n}\).

Consider any legal sequence of job requests of task system \(\tau\), on which edf misses a deadline. Suppose that a job of task \(\tau_{k}\) is the one to first miss a deadline, and that this deadline miss occurs at time-instant \(t_{d}\) (see Figure 2). Let \(t_{a}\) denote this job's arrival time: \(t_{a}=t_{d}-D_{k}\).

Discard from the legal sequence of job requests all jobs with deadline \(>d_{k}\), and consider the edf schedule of the remaining (legal) sequence of job requests. Since later-deadline jobs have no effect on the scheduling of earlier-deadline ones under preemptive edf, it follows that a deadline miss of \(\tau_{k}\) occurs at time-instant \(t_{d}\) (and this is the earliest deadline miss), in this new edf schedule

Let \(t_{o}\) denote the latest time-instant \(\leq t_{a}\) at which at least one processor is idled in this edf schedule. Let \(A_{k}\stackrel{{\mbox{\tiny{\it def}}}}{{=}}t_{a}-t_{o}\).

As in [2, 3], our goal now is to identify conditions necessary for a deadline miss to occur; i.e., for \(\tau_{k}\)'s job to execute for strictly less than \(C_{k}\) time units over \([t_{a},t_{d})\). In order for \(\tau_{k}\)'s job to execute for strictly less than \(C_{k}\) time units over \([t_{a},t_{d})\), it is necessary that all \(m\) processors be executing jobs other than \(\tau_{k}\)'s job for strictly more than \((D_{k}-C_{k})\) time units over \([t_{a},t_{d})\). Let us denote by \(\Gamma_{k}\) a collection of intervals, not necessarily contiguous, of cumulative length \((D_{k}-C_{k})\) over \([t_{a},t_{d})\), during which all \(m\) processors are executing jobs other than \(\tau_{k}\)'s job in this edf schedule.

For each \(i\), \(1\leq i\leq n\), let \(I(\tau_{i})\) denote the contribution of \(\tau_{i}\) to the work done in this edf schedule during \([t_{o},t_{a})\bigcup\Gamma_{k}\). In order for the deadline miss to occur, it is necessary that the total amount of work that executes over \([t_{o},t_{a})\bigcup\Gamma_{k}\) satisfy the following condition

\[\sum_{\tau_{i}\in\tau}I(\tau_{i})>m\times(A_{k}+D_{k}-C_{k})\;;\] (2)

this follows from the observation that all \(m\) processors are, by definition, completely busy executing this work over the \(A_{k}\) time units in the interval \([t_{o},t_{a})\), as well as the intervals in \(\Gamma_{k}\) of total length \((D_{k}-C_{k})\).

It is important to understand exactly what Equation 2 means. Equation 2 represents necessary conditions for task \(\tau_{k}\) to miss a deadline \(A_{k}\) time units after an instant at which at least one processor is idled. _To show that a task system is edf-schedulable, it therefore suffices to demonstrate that for all tasks \(\tau_{k}\) and for all values of \(A_{k}\), Equation 2 cannot be satisfied._

Observe that the total length of the intervals in \([t_{o},t_{a})\bigcup\Gamma_{k}\) is equal to \((A_{k}+D_{k}-C_{k})\).

Let us say that \(\tau_{i}\) has a _carry-in job_ in this edf schedule if there is a job of \(\tau_{i}\) that arrives before \(t_{o}\) and has not computed execution by \(t_{o}\). In the following, we compute upper bounds on \(I(\tau_{i})\) if \(\tau_{i}\) has no carry-in job (this is denoted as \(I_{1}(\tau_{i})\)), or if it does (denoted as \(I_{2}(\tau_{i})\)).

Computing \(I_{1}(\tau_{i})\).If a task \(\tau_{i}\) contributes no carry-in work, then its contribution to this total amount of work that must execute over \([t_{o},t_{a})\bigcup\Gamma_{k}\) is generated by jobs arriving in, and having deadlines within, the interval \([t_{o},t_{d})\). Let us first consider \(i\neq k\); in that case, it follows from the definition of the demand bound function (dbf -- see Section 2 above) that the total work is at most dbf\((\tau_{i},A_{k}+D_{k})\); furthermore, this total contribution cannot exceed the total length of the intervals in \([t_{o},t_{a})\bigcup\Gamma_{k}\). Hence, the contribution of \(\tau_{i}\) to the total work that must be done by edf over \([t_{o},t_{a})\bigcup\Gamma_{k}\) is at most

\[\min(\textsc{dbf}(\tau_{i},A_{k}+D_{k}),A_{k}+D_{k}-C_{k}).\]

Now, consider the case \(i=k\). In that case, the job of \(\tau_{k}\) arriving at time-instant \(t_{a}\) does not contribute to the work that must be done by edf over \([t_{o},t_{a})\bigcup\Gamma_{k}\); hence, its execution requirement must be subtracted. Also, this contribution cannot exceed the length of the interval \([t_{o},t_{a})\); i.e., \(A_{k}\).

Putting these pieces together, we get the following bound on the contribution of \(\tau_{i}\) to the total work that must be done by edf over \([t_{o},t_{a})\bigcup\Gamma_{k}\):

\[\begin{split} I_{1}(\tau_{i})&\stackrel{{ \text{\tiny def}}}{{=}}\\ &\left\{\begin{array}{ll}\min(\textsc{dbf}(\tau_{i},A_{k}+D_{k} ),A_{k}+D_{k}-C_{k})&\text{if $i\neq k$}\\ \min(\textsc{dbf}(\tau_{i},A_{k}+D_{k})-C_{k},A_{k})&\text{if $i=k$} \end{array}\right.\end{split}\] (3)

Computing \(I_{2}(\tau_{i})\).Let us now consider the situation when \(\tau_{i}\) is active at \(t_{o}\), and hence potentially carries in some work. It was shown in [10] that the total work of \(\tau_{i}\) in this case can be upper-bounded by considering the scenario in which some job of \(\tau_{i}\) has a deadline at \(t_{d}\), and all jobs of \(\tau_{i}\) execute at the very end of their scheduling windows.

Let us denote as dbf\({}^{\prime}(\tau_{i},t)\) the amount of work that can be contributed by \(\tau_{i}\) over a contiguous interval of length \(t\), if some job of \(\tau_{i}\) has its deadline at the very end of the interval and each job of \(\tau_{i}\) executes during the \(C_{i}\) units immediately preceding its deadline. It is easily seen (see Figure 3) that there are exactly \(\lfloor t/T_{i}\rfloor\) complete jobs of \(\tau_{i}\) within this interval, and an amount \(\min(D_{i},t\bmod T_{i})\) of the scheduling window of an additional - carry-in - job.

Figure 3: Computing dbf\({}^{\prime}(\tau_{i},t)\).

Figure 2: Notation. A job of task \(\tau_{k}\) arrives at \(t_{a}\) and misses its deadline at time-instant \(t_{d}\). The latest time-instant prior to \(t_{a}\) when not all \(m\) processors are busy is denoted \(t_{o}\).

 This carry-in scheduling window may bring in at most \(C_{i}\) units of execution, yielding the following expression for \(\textsc{dbf}^{\prime}(\tau_{i},t)\):

\[\textsc{dbf}^{*}(\tau_{i},t)\stackrel{{\mbox{\tiny{def}}}}{{=}} \left\lfloor\frac{t}{T_{i}}\right\rfloor\times C_{i}+\min(C_{i},t\bmod T_{i})\] (4)

In computing \(\tau_{i}\)'s contribution to the total amount of work that must execute over \([t_{o},t_{a})\bigcup\Gamma_{k}\), let us first consider \(i\neq k\). In that case, it follows from the definition of the demand bound function (dbf', as defined above) that the total work is at most \(\textsc{dbf}^{\prime}(\tau_{i},A_{k}+D_{k})\); furthermore, this total contribution cannot exceed the total length of the intervals in \([t_{o},t_{a})\bigcup\Gamma_{k}\). Hence, the contribution of \(\tau_{i}\) to the total work that must be done by edf over \([t_{o},t_{a})\bigcup\Gamma_{k}\) is at most

\[\min(\textsc{dbf}^{\prime}(\tau_{i},A_{k}+D_{k}),A_{k}+D_{k}-C_{k}).\]

Now, consider the case \(i=k\). In that case, the job of \(\tau_{k}\) arriving at time-instant \(t_{a}\) does not contribute to the work that must be done by edf over \([t_{o},t_{a})\bigcup\Gamma_{k}\); hence, its execution requirement must be subtracted. Also, this contribution cannot exceed the length of the interval \([t_{o},t_{a})\); i.e., \(A_{k}\).

From the discussion above, we get the following bound on the contribution of \(\tau_{i}\) to the total work that must be done by edf over \([t_{o},t_{a})\bigcup\Gamma_{k}\):

\[I_{2}(\tau_{i})\stackrel{{\mbox{\tiny{def}}}}{{=}}\] \[\left\{\begin{array}{ll}\min(\textsc{dbf}^{\prime}(\tau_{i},A_{k }+D_{k}),A_{k}+D_{k}-C_{k})&\mbox{if $i\neq k$}\\ \min(\textsc{dbf}^{\prime}(\tau_{i},A_{k}+D_{k})-C_{k},A_{k})&\mbox{if $i=k$} \end{array}\right.\] (5)

Putting the pieces together.Let us denote by \(I_{\textsc{dif}}(\tau_{i})\) the difference between \(I_{2}(\tau_{i})\) and \(I_{1}(\tau_{i})\):

\[I_{\textsc{dif}}(\tau_{i})\stackrel{{\mbox{\tiny{def}}}}{{=}}I_{ 2}(\tau_{i})-I_{1}(\tau_{i})\] (6)

By definition of \(t_{o}\), at most \((m-1)\) tasks are active at time-instant \(t_{o}\). Consequently, _there are at most \((m-1)\) tasks \(\tau_{i}\) that contribute at amount \(I_{2}(\tau_{i})\), and the remaining \((n-m+1)\) tasks must contribute \(I_{1}(\tau_{i})\)_. Hence Equation 2 may be rewritten as follows:

\[\sum_{\tau_{i}\in\tau}I_{1}(\tau_{i})+\sum_{\mbox{\scriptsize the $(m-1)$ largest}}I_{\textsc{dif}}(\tau_{i})\\ >m(A_{k}+D_{k}-C_{k})\] (7)

Observe that all the terms in Equation 7 above are completely defined for a given task system, once a value is chosen for \(A_{k}\). Hence for a deadline miss of \(\tau_{k}\) to occur, there must exist some \(A_{k}\) such that Equation 7 is satisfied. Conversely, in order for all deadlines of \(\tau_{k}\) to be met it is sufficient that Equation 7 be violated for all values of \(A_{k}\). Theorem 2 follows immediately:

**Theorem 2**: _Task system \(\tau\) is edf-schedulable upon \(m\) unit-capacity processors if for all tasks \(\tau_{k}\in\tau\) and all \(A_{k}\geq 0\),_

\[\left(\sum_{\tau_{i}\in\tau}I_{1}(\tau_{i})+\sum_{\mbox{\scriptsize the $(m-1)$ largest}}I_{\textsc{dif}}(\tau_{i})\right)\\ \leq m(A_{k}+D_{k}-C_{k})\] (8)

_where \(I_{1}(\tau_{i})\) and \(I_{\textsc{dif}}(\tau_{i})\) are as defined in Equations 3 and 6 respectively. \(\blacksquare\)_

The earlier tests -- the density, [bak] and [bcl] tests -- are not exact even for uniprocessor systems (the special case when \(m=1\)). (This is also indicated by the fact that all these prior tests have polynomial run-time, while edf-schedulability analysis of sporadic task systems on uniprocessors is not known to be in polynomial time.) The following corollary asserts that our test is superior to earlier tests in this regard:

**Corollary 1**: _The edf schedulability test of Theorem 2 is a generalization of the exact uniprocessor edf schedulability test of [9]._

**Proof Sketch:** For \(m=1\), there are \((m-1)=0\) tasks that are active at time-instant \(t_{o}\); i.e., \(t_{o}\) is the classical "idle instant" of uniprocessor real-time scheduling theory. By adding \(C_{k}\) to both the LHS and the RHS of Condition 8, it can be shown that the LHS reduces to the sum of the demand bound functions of all tasks over an interval of size \(A_{k}+D_{k}\), and the RHS reduces to the interval length. Hence, when \(m=1\) Condition 8 is asserting that the cumulative processor demand over all intervals must not exceed the interval length, which is exactly what the uniprocessor edf schedulability test of [9] checks. \(\blacksquare\)

Corollary 1 does not imply that we have obtained an exciting new result showing that uniprocessor edf-schedulability analysis can be done in polynomial time; Section 6.1 shows that our algorithm has pseudo-polynomial run-time when system utilization is bounded.

### Run-time complexity

For given \(\tau_{k}\) and \(A_{k}\), it is easy to see that Condition 8 can be evaluated in time linear in \(n\):

* Compute \(I_{1}(\tau_{i})\), \(I_{2}(\tau_{i})\), and \(I_{\textsc{dif}}(\tau_{i})\) for each \(i\) -- total time is \(\mathcal{O}(n)\).
* Use linear-time selection [12] on \(\{I_{\textsc{dif}}(\tau_{1}),I_{\textsc{dif}}(\tau_{2}),\ldots,I_{\textsc{dif}} (\tau_{n})\}\) to determine the \((m-1)\) tasks that contribute to the second sum on the LHS.

How many values of \(A_{k}\) must be tested, in order for us to be able to ascertain that Condition 8 is satisfied for all \(A_{k}\geq 0\)? Theorem 3 below provides the answer.

 

**Theorem 3**: _If Condition 8 is to be violated for any \(A_{k}\), then it is violated for some \(A_{k}\) satisfying the condition below:_

\[A_{k}\leq\frac{C_{\Sigma}-D_{k}(m-U(\tau))+\sum_{i}(T_{i}-D_{i})U_{i}+mC_{k}}{m- U(\tau)}\] (9)

_where \(C_{\Sigma}\) denotes the sum of the \((m-1)\) largest \(C_{i}\)'s._

**Proof:** It is easily seen that \(I_{1}(\tau_{i})\leq\texttt{dbf}(\tau_{i},A_{k}+D_{k})\), and \(I_{2}(\tau_{i})\leq\texttt{dbf}(\tau_{i},A_{k}+D_{k})+C_{i}\). From this, it can be shown that the LHS of Condition 8 is \(\leq C_{\Sigma}+\sum_{\tau_{i}\in\tau}\texttt{dbf}(\tau_{i},A_{k}+D_{k})\).

For this to exceed the RHS of Condition 8, it is necessary that

\[C_{\Sigma}+\texttt{dbf}(\tau,A_{k}+D_{k})>m(A_{k}+D_{k}-C_{k})\] \[\Rightarrow\text{(bounding dbf using the technique of \@@cite[cite]{[\@@bibref{}{Dj}{}{}]})}\] \[C_{\Sigma}+(A_{k}+D_{k})U(\tau)+\sum_{i}(T_{i}-D_{i})U_{i}>m(A_{ k}+D_{k}-C_{k})\] \[\equiv\,C_{\Sigma}+D_{k}U(\tau)+\sum_{i}(T_{i}-D_{i})U_{i}-m(D_{k} -C_{k})>A_{k}(m-U(\tau))\] \[\equiv A_{k}\leq\frac{C_{\Sigma}-D_{k}(m-U(\tau))+\sum_{i}(T_{i}-D _{i})U_{i}+mC_{k}}{m-U(\tau)}\]

which is as claimed in the theorem. \(\blacksquare\)

It can also be shown that Condition 8 need only be tested at those values of \(A_{k}\) at which \(\texttt{dbf}(\tau_{i},A_{k}+D_{k})\) changes for some \(\tau_{i}\). Corollary 2 follows.

**Corollary 2**: _The condition in Theorem 2 above can be tested in time pseudo-polynomial in the task parameters, for all task systems \(\tau\) for which \(U(\tau)\) is bounded by a constant strictly less than the number of processors \(m\). \(\blacksquare\)_

Comparison to the [bak] and [bcl] tests.By design, our test runs slower than the [bak], [bcl], and density tests: our test has pseudo-polynomial run-time complexity while all the other tests have polynomial complexity. In practice, we would expect that all tests be used within a single framework: a system be first tested for schedulability using the polynomial-time tests, and only those that are not determined to be schedulable by any of these tests be subjected to our slower test.

It is fairly easy to construct task systems that are determined to be schedulable by only our test (and not the other tests); indeed, Corollary 1 above demonstrates that our test is the only one that is optimal upon uniprocessors (i.e., when \(m=1\)). Furthermore, preliminary simulation experiments indicate that our test significantly outperforms the other tests upon task systems in which

* The number of tasks \(n\) is significantly greater than the number of processors \(m\) (i.e., \(n\gg m\)). This is probably a consequence of the fact that our test only considers carry-in from \(m-1\) tasks, while all the prior tests must account for carry-in from all \(n\) tasks.
* The parameters of the different tasks may be of widely varying orders of magnitude. Once again, this is by design: our test was specifically designed to handle such systems.
```


You are analyzing a research paper on real-time systems. Use the following definitions as background:

1. Workload Model The workload model specifies the set of computational tasks in the system. It describes characteristics such as arrival patterns (periodic, sporadic, aperiodic), execution times (worst-case, best-case, average), deadlines, precedence constraints, and criticality levels. In short, it defines what tasks need to be scheduled and when they arrive.
2. Resource Model The resource model describes the computing and hardware resources available for executing tasks. This includes processors (single-core, multi-core, heterogeneous cores), communication channels, memory, I/O devices, and their timing or capacity constraints. It defines where and how tasks can execute.
3. Scheduler The scheduler is the decision-making mechanism that assigns tasks from the workload model to resources from the resource model, according to specific scheduling policies and algorithms (e.g., Rate-Monotonic, Earliest Deadline First, Fixed Priority). Its purpose is to ensure that tasks meet their timing requirements while respecting resource constraints.
4. Analysis Framework The analysis framework provides the formal methods and tools used to determine whether the system is schedulable under the given workload, resource model, and scheduler. It encompasses techniques such as response-time analysis, utilization bounds, demand-bound functions, and model checking. The framework evaluates timing guarantees, detects potential deadline misses, and quantifies metrics like worst-case response time, jitter, and resource utilization. In short, it defines how the correctness and performance of the system are verified.

Task: From the paper you are analyzing:

1. Identify and describe the workload model, resource model, scheduler and analysis framework used.
2. Extract all of the system constraints or invariants from the paper that guarantee correct scheduling of workloads. These are typically presented as equations, lemmas, theorems or constraints. Don't miss out on any of the theorem or lemma or system invariants. Write the constraints exactly as they appear in the paper. For each constraint, explain the meaning of every notation or symbol used.
Write your answer in markdown format. Use $$ for multi-line equation and $ for single line equations.
'''