=========== system message ===============
You are analyzing a research paper on real-time systems. Use the following definitions as background:

1. Workload Model:
The workload model specifies the set of computational tasks in the system. It describes characteristics such as arrival patterns (periodic, sporadic, aperiodic), execution times (worst-case, best-case, average), deadlines, precedence constraints, and criticality levels. In short, it defines what tasks need to be scheduled and when they arrive.
2. Resource Model:
The resource model describes the computing and hardware resources available for executing tasks. This includes processors (single-core, multi-core, heterogeneous cores), communication channels, memory, I/O devices, and their timing or capacity constraints. It defines where and how tasks can execute.
3. Scheduler:
The scheduler is the decision-making mechanism that assigns tasks from the workload model to resources from the resource model, according to specific scheduling policies and algorithms (e.g., Rate-Monotonic, Earliest Deadline First, Fixed Priority). Its purpose is to ensure that tasks meet their timing requirements while respecting resource constraints.
4. Analysis Framework:
The analysis framework provides the formal methods and tools used to determine whether the system is schedulable under the given workload, resource model, and scheduler. It encompasses techniques such as response-time analysis, utilization bounds, demand-bound functions, and model checking. The framework evaluates timing guarantees, detects potential deadline misses, and quantifies metrics like worst-case response time, jitter, and resource utilization. In short, it defines how the correctness and performance of the system are verified.

Use the following context in your response: 

m+1) tasks must contribute I1(τi). Hence Equation 2 may
be rewritten as follows:

τi∈τ
I1(τi) +

the (m −1) largest
IDIFF(τi)
> m(Ak + Dk −Ck)
(7)
Observe that all the terms in Equation 7 above are com-
pletely deﬁned for a given task system, once a value is cho-
sen for Ak. Hence for a deadline miss of τk to occur, there
must exist some Ak such that Equation 7 is satisﬁed. Con-
versely, in order for all deadlines of τk to be met it is sufﬁ-
cient that Equation 7 be violated for all values of Ak. The-
orem 2 follows immediately:
Theorem 2 Task system τ is EDF-schedulable upon m unit-
capacity processors if for all tasks τk ∈τ and all Ak ≥0,


τi∈τ
I1(τi) +

the (m −1) largest
IDIFF(τi)


≤m(Ak + Dk −Ck)
(8)
where I1(τi) and IDIFF(τi) are as deﬁned in Equations 3
and 6 respectively.
The earlier tests — the density, [BAK] and [BCL] tests
— are not exact even for uniprocessor systems (the special
case when m = 1). (This is also indicated by the fact that

necessary that the total amount of work that executes over
[to, ta)  Γk satisfy the following condition

τi∈τ
I(τi) > m × (Ak + Dk −Ck) ;
(2)
this follows from the observation that all m processors are,
by deﬁnition, completely busy executing this work over the
Ak time units in the interval [to, ta), as well as the intervals
in Γk of total length (Dk −Ck).
It is important to understand exactly what Equation 2
means. Equation 2 represents necessary conditions for task
τk to miss a deadline Ak time units after an instant at which
at least one processor is idled. To show that a task system
is EDF-schedulable, it therefore sufﬁces to demonstrate that
for all tasks τk and for all values of Ak, Equation 2 cannot
be satisﬁed.
Observe that the total length of the intervals in
[to, ta)  Γk is equal to (Ak + Dk −Ck).
Let us say that τi has a carry-in job in this EDF schedule
if there is a job of τi that arrives before to and has not com-

it can be shown that the LHS reduces to the sum of the de-
mand bound functions of all tasks over an interval of size
Ak+Dk, and the RHS reduces to the interval length. Hence,
when m = 1 Condition 8 is asserting that the cumulative
processor demand over all intervals must not exceed the in-
terval length, which is exactly what the uniprocessor EDF
schedulability test of [9] checks.
Corollary 1 does not imply that we have obtained
an exciting new result showing that uniprocessor EDF-
schedulability analysis can be done in polynomial time;
Section
6.1
shows
that
our
algorithm
has
pseudo-
polynomial run-time when system utilization is bounded.
6.1
Run-time complexity
For given τk and Ak, it is easy to see that Condition 8
can be evaluated in time linear in n:
• Compute I1(τi), I2(τi), and IDIFF(τi) for each i — total
time is O(n).
• Use
linear-time
selection
[12]
on
{IDIFF(τ1), IDIFF(τ2), . . . , IDIFF(τn)}
to
determine
the
(m −1) tasks that contribute to the second sum on the
LHS.

This carry-in scheduling window may bring in at most
Ci units of execution, yielding the following expression for
DBF′(τi, t):
DBF’(τi, t)
def=
 t
Ti

× Ci + min(Ci, t mod Ti)
(4)
In computing τi’s contribution to the total amount of work
that must execute over [to, ta)  Γk, let us ﬁrst consider
i ̸= k. In that case, it follows from the deﬁnition of the
demand bound function (DBF’, as deﬁned above) that the
total work is at most DBF′(τi, Ak + Dk); furthermore, this
total contribution cannot exceed the total length of the in-
tervals in [to, ta)  Γk. Hence, the contribution of τi to the
total work that must be done by EDF over [to, ta)  Γk is at
most
min(DBF′(τi, Ak + Dk), Ak + Dk −Ck).
Now, consider the case i = k. In that case, the job of τk ar-
riving at time-instant ta does not contribute to the work that
must be done by EDF over [to, ta)  Γk; hence, its execu-
tion requirement must be subtracted. Also, this contribution

[to, ta)  Γk is equal to (Ak + Dk −Ck).
Let us say that τi has a carry-in job in this EDF schedule
if there is a job of τi that arrives before to and has not com-
puted execution by to. In the following, we compute upper
bounds on I(τi) if τi has no carry-in job (this is denoted as
I1(τi)), or if it does (denoted as I2(τi)).
Computing I1(τi).
If a task τi contributes no carry-in
work, then its contribution to this total amount of work that
must execute over [to, ta)  Γk is generated by jobs arriv-
ing in, and having deadlines within, the interval [to, td). Let
us ﬁrst consider i ̸= k; in that case, it follows from the deﬁ-
nition of the demand bound function (DBF — see Section 2
above) that the total work is at most DBF(τi, Ak + Dk);
furthermore, this total contribution cannot exceed the total
length of the intervals in [to, ta)  Γk. Hence, the contribu-
tion of τi to the total work that must be done by EDF over
[to, ta)  Γk is at most
min(DBF(τi, Ak + Dk), Ak + Dk −Ck).

ciples of Distributed Systems (Pisa, Italy, December
2005), IEEE Computer Society Press.
[12] BLUM, M., FLOYD, R. W., PRATT, V., RIVEST,
R. L., AND TARJAN, R. E. Time bounds for selec-
tion. Journal of Computer and System Sciences 7, 4
(Aug. 1973), 448–461.
[13] CARPENTER, J., FUNK, S., HOLMAN, P., SRINI-
VASAN, A., ANDERSON, J., AND BARUAH, S. A
categorization of real-time multiprocessor scheduling
problems and algorithms. In Handbook of Schedul-
ing: Algorithms, Models, and Performance Analysis,
J. Y.-T. Leung, Ed. CRC Press LLC, 2003.
[14] DERTOUZOS, M. Control robotics : the procedural
control of physical processors. In Proceedings of the
IFIP Congress (1974), pp. 807–813.
[15] DHALL, S. Scheduling Periodic Time-Critical Jobs
on Single Processor and Multiprocessor Systems. PhD
thesis, Department of Computer Science, The Univer-
sity of Illinois at Urbana-Champaign, 1977.
[16] FISHER, N., AND BARUAH, S. Global static-priority
scheduling of sporadic task systems on multiprocessor

tion algorithms that run in polynomial time and exhibit ex-
cellent average-case and provably bounded worst-case be-
havior have been devised [7, 17, 8].
In the global case, however, we do not know how to
determine schedulability even if computational tractability
were not an issue. That is, we do not yet have an ade-
quate understanding of what precisely the characteristics of
a globally schedulable system are; without knowing these
characteristics, it seems futile to seek accurate, efﬁcient
tests for identifying such systems. (In this regard, Exam-
ple 1 above illustrates that LOAD is not an exact indicator
of schedulability: while LOAD(τ) ≤m is clearly necessary
for τ to be EDF-schedulable on an m-processor platform,
the task system in Example 1 illustrates that this is not suf-
ﬁcient.)
121
121
Authorized licensed use limited to: FLORIDA INTERNATIONAL UNIVERSITY. Downloaded on October 22,2025 at 12:47:31 UTC from IEEE Xplore.  Restrictions apply.

for historical reasons, also referred to as the period of the
task. Such a sporadic task generates a potentially inﬁnite
sequence of jobs, with successive job-arrivals separated by
at least Ti time units. Each job has a worst-case execution
requirement equal to Ci and a deadline that occurs Di time
units after its arrival time. We refer to the interval, of size
Di, between such a job’s arrival instant and deadline as its
scheduling window. We assume a fully preemptive execu-
tion model: any executing job may be interrupted at any
instant in time, and its execution resumed later with no cost
or penalty. A sporadic task system is comprised of several
such sporadic tasks. Let τ denote a system of such sporadic
tasks: τ = {τ1, τ2, . . . τn}, with τi = (Ci, Di, Ti) for all
i, 1 ≤i ≤n. Task system τ is said to be a constrained
sporadic task system if it is guaranteed that each task τi ∈τ
has its relative deadline parameter no larger than its period:

of its execution time to its period. The total utilization
usum(τ) and the largest utilization umax(τ) of a task
system τ are deﬁned as follows:
usum(τ)
def=

τi∈τ
ui;
umax(τ)
def= max
τi∈τ (ui)
Density: The density δi of a task τi is the ratio Ci/Di of
its execution time to its relative deadline. The total
density δsum(τ) and the largest density δmax(τ) of a
task system τ are deﬁned as follows:
δsum(τ)
def=

τi∈τ
δi;
δmax(τ)
def= max
τi∈τ (δi)
An additional concept that plays a critical role in the
schedulability analysis of sporadic task systems is that of
demand bound function. For any interval length t, the
demand bound function DBF(τi, t) of a sporadic task τi
bounds the maximum cumulative execution requirement by
jobs of τi that both arrive in, and have deadlines within, any
interval of length t. It has been shown [9] that
DBF(τi, t) = max

0, (
t −Di
Ti

+ 1) Ci

A load parameter, based upon the DBF function, may be
deﬁned for any sporadic task system τ as follows:

represented in models more general than the Liu and Lay-
land model. One of the observations that has come out of all
this research is that global scheduling is fundamentally dif-
ferent from, and seems much more difﬁcult than, partitioned
scheduling.
In this paper, we have described some of our recent ﬁnd-
ings concerning global multiprocessor scheduling. We have
attempted to identify and highlight some of the fundamen-
tal issues that render global schedulability analysis so dif-
ﬁcult. Building upon the techniques of Baker [2, 3] and of
Bertogna et al. [10], we have designed a global-EDF schedu-
lability test that is quite a bit more sophisticated than earlier
tests, and that has overcome several of the deﬁciencies of
these earlier tests.
References
[1] AUDSLEY, N. C. Flexible Scheduling in Hard-Real-
Time Systems. PhD thesis, Department of Computer
Science, University of York, 1993.
[2] BAKER, T. Multiprocessor EDF and deadline mono-
tonic schedulability analysis.

- time
to
ta
td
6
?
some proc. idled
@
@@
R
deadline miss




Ak

-
Dk

-
Figure 2. Notation. A job of task τk arrives at ta and misses its deadline at time-instant td. The latest
time-instant prior to ta when not all m processors are busy is denoted to.
τk’s job to execute for strictly less than Ck time units over
[ta, td), it is necessary that all m processors be executing
jobs other than τk’s job for strictly more than (Dk −Ck)
time units over [ta, td). Let us denote by Γk a collection of
intervals, not necessarily contiguous, of cumulative length
(Dk −Ck) over [ta, td), during which all m processors are
executing jobs other than τk’s job in this EDF schedule.
For each i, 1 ≤i ≤n, let I(τi) denote the contribu-
tion of τi to the work done in this EDF schedule during
[to, ta)  Γk. In order for the deadline miss to occur, it is
necessary that the total amount of work that executes over
[to, ta)  Γk satisfy the following condition

τi∈τ
I(τi) > m × (Ak + Dk −Ck) ;
(2)

i, 1 ≤i ≤n. Task system τ is said to be a constrained
sporadic task system if it is guaranteed that each task τi ∈τ
has its relative deadline parameter no larger than its period:
Di ≤Ti, and an implicit-deadline sporadic task system if
Di = Ti for all τi ∈τ. (Implicit-deadline systems are also
known as Liu and Layland [22] task systems.) In this pa-
per, we restrict our attention to constrained and implicit-
deadline task systems.
Schedulability.
A real-time system implemented on a
particular computing platform is said to be A-schedulable
with respect to a given scheduling algorithm A, if the al-
gorithm A schedules the system such that all jobs of all
tasks will meet all deadlines, under all permissible (also
called legal) combinations of job-arrival sequences by the
different tasks comprising the system. A schedulability test
for scheduling algorithm A (also called an A-schedulability
test) accepts as input the speciﬁcations of a real-time sys-

Time Systems. PhD thesis, Department of Computer
Science, University of York, 1993.
[2] BAKER, T. Multiprocessor EDF and deadline mono-
tonic schedulability analysis.
In Proceedings of
the IEEE Real-Time Systems Symposium (December
2003), IEEE Computer Society Press, pp. 120–129.
[3] BAKER, T. P. An analysis of EDF schedulability on
a multiprocessor. IEEE Transactions on Parallel and
Distributed Systems 16, 8 (2005), 760–768.
[4] BAKER, T. P.
Comparison of empirical success
rates of global vs. partitioned ﬁxed-priority and EDF
scheduling for hard real time. Tech. Rep. TR-050601,
127
127
Authorized licensed use limited to: FLORIDA INTERNATIONAL UNIVERSITY. Downloaded on October 22,2025 at 12:47:31 UTC from IEEE Xplore.  Restrictions apply.

different tasks comprising the system. A schedulability test
for scheduling algorithm A (also called an A-schedulability
test) accepts as input the speciﬁcations of a real-time sys-
tem, and determines whether the system is A-schedulable
or not. An A-schedulability test is said to be exact if it cor-
rectly identiﬁes all A-schedulable systems, and sufﬁcient if
it may fail to identify some A-schedulable systems (it must
guarantee, though, that all identiﬁed systems are indeed A-
schedulable.)
Task and system characteristics.
The concepts of task
and system utilization and density prove useful in the analy-
sis of sporadic task systems on multiprocessors. These con-
cepts are deﬁned as follows:
Utilization: The utilization ui of a task τi is the ratio Ci/Ti
of its execution time to its period. The total utilization
usum(τ) and the largest utilization umax(τ) of a task
system τ are deﬁned as follows:
usum(τ)
def=

τi∈τ
ui;
umax(τ)
def= max
τi∈τ (ui)

29, 5 (Oct. 1986), 390–395.
[20] LEUNG, J., AND MERRILL, M. A note on the pre-
emptive scheduling of periodic, real-time tasks. Infor-
mation Processing Letters 11 (1980), 115–118.
[21] LEUNG, J., AND WHITEHEAD, J. On the complex-
ity of ﬁxed-priority scheduling of periodic, real-time
tasks. Performance Evaluation 2 (1982), 237–250.
[22] LIU, C., AND LAYLAND, J. Scheduling algorithms
for multiprogramming in a hard real-time environ-
ment. Journal of the ACM 20, 1 (1973), 46–61.
[23] MOK, A. K. Fundamental Design Problems of Dis-
tributed Systems for The Hard-Real-Time Environ-
ment. PhD thesis, Laboratory for Computer Science,
Massachusetts Institute of Technology, 1983. Avail-
able as Technical Report No. MIT/LCS/TR-297.
[24] RIPOLL, I., CRESPO, A., AND MOK, A. K. Improve-
ment in feasibility testing for real-time tasks. Real-
Time Systems: The International Journal of Time-
Critical Computing 11 (1996), 19–39.
128
128

Discard from the legal sequence of job requests all jobs
with deadline > dk, and consider the EDF schedule of the
remaining (legal) sequence of job requests.
Since later-
deadline jobs have no effect on the scheduling of earlier-
deadline ones under preemptive EDF, it follows that a dead-
line miss of τk occurs at time-instant td (and this is the ear-
liest deadline miss), in this new EDF schedule
Let to denote the latest time-instant ≤ta at which at
least one processor is idled in this EDF schedule. Let Ak
def=
ta −to.
As in [2, 3], our goal now is to identify conditions neces-
sary for a deadline miss to occur; i.e., for τk’s job to execute
for strictly less than Ck time units over [ta, td). In order for
124
124
Authorized licensed use limited to: FLORIDA INTERNATIONAL UNIVERSITY. Downloaded on October 22,2025 at 12:47:31 UTC from IEEE Xplore.  Restrictions apply.

length of the intervals in [to, ta)  Γk. Hence, the contribu-
tion of τi to the total work that must be done by EDF over
[to, ta)  Γk is at most
min(DBF(τi, Ak + Dk), Ak + Dk −Ck).
Now, consider the case i = k. In that case, the job of τk ar-
riving at time-instant ta does not contribute to the work that
must be done by EDF over [to, ta)  Γk; hence, its execu-
tion requirement must be subtracted. Also, this contribution
cannot exceed the length of the interval [to, ta); i.e., Ak.
Putting these pieces together, we get the following bound
on the contribution of τi to the total work that must be done
by EDF over [to, ta)  Γk:
I1(τi)
def=
 min(DBF(τi, Ak + Dk), Ak + Dk −Ck)
if i ̸= k
min(DBF(τi, Ak + Dk) −Ck, Ak)
if i = k
(3)
Computing I2(τi).
Let us now consider the situation
when τi is active at to, and hence potentially carries in some
work. It was shown in [10] that the total work of τi in this
case can be upper-bounded by considering the scenario in

during which τ1’s jobs execute within this scheduling
window. Therefore there are at least 5 slots within this
scheduling window during which one of both proces-
sors is idle after both τ1 and τ2 have been scheduled.
Perhaps surprisingly, the converse of the above lemma is
also true:
Lemma 2 There are task systems that are schedulable us-
ing partitioned FJP algorithms that global FJP algorithms
cannot schedule.
Proof Sketch:
Here’s an example task system, on 2 pro-
cessors:
τ1 = (2, 2, 3), τ2 = (3, 3, 4), τ3 = (4, 12, 12), τ4 = (3, 12, 12)
This task system may be partitioned by assigning τ1 and τ3
to one processor and the other two tasks to the remaining
1For ease of exposition, we are assuming a slotted model of time for
this proof sketch; however, it is easily generalized to a non-slotted model.
122
122
Authorized licensed use limited to: FLORIDA INTERNATIONAL UNIVERSITY. Downloaded on October 22,2025 at 12:47:31 UTC from IEEE Xplore.  Restrictions apply.

derstood than global scheduling.
Sufﬁcient schedulabil-
ity tests of polynomial time-complexity have been de-
signed [7, 17, 8] for various commonly-used scheduling
algorithms (such as Earliest Deadline First (EDF) [22, 14]
and Deadline Monotonic (DM) [21]). Worst-case resource-
augmentation bounds, that provide a quantitative measure
of how effective these tests are, have been obtained. These
schedulability tests have also been extensively evaluated via
simulations [4, 6], and shown to have much better average-
case behavior than indicated by their worst-case guaran-
tees. In contrast, we are not aware of non-trivial theoreti-
cal bounds on the performance of known sufﬁcient schedu-
lability tests [2, 3, 10] for global scheduling (other than
a relatively naive resource-augmentation bound on global
DM [16]), and simulation experiments have tended to in-
dicate that they perform poorly in comparison to the parti-
tioned schedulability tests.
This research.

ates a potentially inﬁnite sequence of jobs. Every job is
characterized by an arrival time, an execution requirement,
and a deadline, and it is required that a job complete execu-
tion between its arrival time and its deadline. Different for-
mal models for recurring tasks place different restrictions
on the values of the parameters of jobs generated by each
task. One of the more commonly used formal models is the
sporadic task model [23, 9], which will be considered in this
paper.
Scheduling is the allocation of processor time to jobs,
and a scheduling algorithm is used for determining such al-
location. A schedulability test for a given scheduling algo-
rithm accepts as input the speciﬁcations of a real-time sys-
tem, and determines whether the scheduling algorithm can
guarantee to schedule the system such that all jobs of all
tasks will meet all deadlines, under all permissible combi-
nations of job-arrival sequences by the different tasks com-