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