This regular paper was presented as part of the main technical program at IEEE ETFA’2011
A Component-Based Framework for Modeling and Analyzing Probabilistic
|     |                   |     |               |                 |        | Real-Time            | Systems      |            |                        |           |        |            |           |
| --- | ----------------- | --- | ------------- | --------------- | ------ | -------------------- | ------------ | ---------- | ---------------------- | --------- | ------ | ---------- | --------- |
|     |                   | L.  | Santinelli,P. |                 | Meumeu | Yomsi,D.             | MaximandL.   |            | Cucu-Grosjean          |           |        |            |           |
|     |                   |     |               |                 |        | INRIA NancyGrand-Est |              |            |                        |           |        |            |           |
|     | {luca.santinelli, |     |               |                 |        |                      |              |            | liliana.cucu}@inria.fr |           |        |            |           |
|     |                   |     |               | patrick.meumeu, |        |                      | dorin.maxim, |            |                        |           |        |            |           |
|     |                   |     | Abstract      |                 |        |                      | Related      | work       | A component-based      |           | view   | of         | real-time |
|     |                   |     |               |                 |        |                      | systems      | is defined | such                   | that each | system | elementcan | be        |
A challenging research issue of analyzing a real-time modeledasacomponent,[7,24,11,9,20,19]withanas-
|     |     |     |     |     |     |     | sociated | interface | describing | how | the component |     | relates |
| --- | --- | --- | --- | --- | --- | --- | -------- | --------- | ---------- | --- | ------------- | --- | ------- |
systemistomodelthetaskscomposingthesystemandthe
resourceprovidedtothesystem. Inthispaper,wepropose toothercomponentsaswellastheenvironment[10].
aprobabilisticcomponent-basedmodelwhichabstractsin Several timing analysis results are provided for the
the interfaces both the functionaland non-functionalre- component-based design problem using the hierarchical
quirementsofsuchsystems. Thisapproachallowsdesign- scheduling[22, 12, 1, 17] whichdecomposesthe system
|     |     |     |     |     |     |     | into manyindependentapplicationsto |     |     |     | which | is  | assigned |
| --- | --- | --- | --- | --- | --- | --- | ---------------------------------- | --- | --- | --- | ----- | --- | -------- |
erstounifyinthesameframeworkprobabilisticschedul-
ingtechniquesandcompositionalguaranteesthatgofrom a fraction of the computational resource through global
| soft to hard | real-time. |     | We provide | sufficientschedulabil- |     |     | schedulers. |     |     |     |     |     |     |
| ------------ | ---------- | --- | ---------- | ---------------------- | --- | --- | ----------- | --- | --- | --- | --- | --- | --- |
ity tests for task systems using such framework when the Concerningtheprobabilisticapproaches,thereal-time
scheduler is either preemptive Fixed-Priority or Earliest community has been using terms like stochastic analy-
sisregardlessoftheapproach(probabilisticorstatistical)
DeadlineFirst.
|     |     |     |     |     |     |     | [14, 18,      | 28, 8].  | In this         | paper | we use the        | notion         | of prob- |
| --- | --- | --- | --- | --- | --- | --- | ------------- | -------- | --------------- | ----- | ----------------- | -------------- | -------- |
|     |     |     |     |     |     |     | abilistic     | approach | to indicate     |       | that the approach |                | is based |
|     |     |     |     |     |     |     | on the theory |          | of probability. |       | Moreover,         | by probabilis- |          |
1 Introduction ticcomponent-basedsystemwemeanacomponent-based
systemwithatleastoneparameterdescribedbyarandom
variable.Thereforeaprobabilisticanalysisconsistsofthe
| The | performance | of  | a real-time | system |     | rely on both |     |     |     |     |     |     |     |
| --- | ----------- | --- | ----------- | ------ | --- | ------------ | --- | --- | --- | --- | --- | --- | --- |
temporalanalysisofsuchsystems.
| correctexecutionsandresults |     |     | that | are | producedon | time. |     |         |             |       |         |                 |     |
| --------------------------- | --- | --- | ---- | --- | ---------- | ----- | --- | ------- | ----------- | ----- | ------- | --------------- | --- |
|                             |     |     |      |     |            |       | The | closest | result that | could | be used | for probabilis- |     |
Overtheyears,numerousapproacheshavebeenproposed
|              |     |           |           |     |         |          | tic component-basedmodelingisprovidedin |     |     |     |     | [13] | where |
| ------------ | --- | --------- | --------- | --- | ------- | -------- | --------------------------------------- | --- | --- | --- | --- | ---- | ----- |
| for modeling | and | analyzing | real-time |     | systems | [7, 23]. |                                         |     |     |     |     |      |       |
theauthorsdefinethestochasticnetworkcalculus,derived
Thesesystemsarenowadaysmorecomplexandtherefore
|          |            |     |          |             |     |             | fromthenetworkcalculus[5]. |     |     |     | Nevertheless,thestochas- |     |     |
| -------- | ---------- | --- | -------- | ----------- | --- | ----------- | -------------------------- | --- | --- | --- | ------------------------ | --- | --- |
| they are | often seen | as  | a set of | independent |     | sub-systems |                            |     |     |     |                          |     |     |
ticnetworkcalculusdoesnotprovideresultsforreal-time
| or components. |     | This | paradigm | for addressing |     | real-time |     |     |     |     |     |     |     |
| -------------- | --- | ---- | -------- | -------------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
probabilisticcomponent-basedsystems,asitisthecaseof
issuesprovidesameanforreducingasinglecomplexde-
theframeworkweproposehere.
| signproblemintomultiplesimplerones. |     |          |              |     | Assuch,areal- |            |     |     |     |     |     |     |     |
| ----------------------------------- | --- | -------- | ------------ | --- | ------------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
| time system                         | is  | obtained | by composing |     | the           | components |     |     |     |     |     |     |     |
throughtheirinterfaces,eachofwhichabstractstheinter-
|     |     |     |     |     |     |     | Thisresearch |     | Inthispaper,wefocusandbuildourcon- |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --- | ---------------------------------- | --- | --- | --- | --- |
nalcomplexityofthecomponentandencodesthetiming tribution on techniques from Real-Time Calculus (RTC)
| requirementsof |     | the real-timecomponent. |     |     | In  | such a pro- |             |     |              |          |           |     |           |
| -------------- | --- | ----------------------- | --- | --- | --- | ----------- | ----------- | --- | ------------ | -------- | --------- | --- | --------- |
|                |     |                         |     |     |     |             | [25], which | is  | a worst-case | analysis | framework |     | for real- |
theoriginalsystemisusingtheso-calledhierarchi-
| cess, |     |     |     |     |     |     | time systems |     | based on | deterministic | bounds | by  | which |
| ----- | --- | --- | --- | --- | --- | --- | ------------ | --- | -------- | ------------- | ------ | --- | ----- |
calschedulingtechniquestoguaranteetemporalisolation the system behavior is modeled: non-deterministic de-
betweenthecomponents.
|     |     |     |     |     |     |     | cisions | can be | taken throughout |     | bounding | curves. | RTC |
| --- | --- | --- | --- | --- | --- | --- | ------- | ------ | ---------------- | --- | -------- | ------- | --- |
Acommonlyusedtechniqueinanalyzingcomponent- providesadequatematerialthatcharacterizeseventoccur-
based systems consists in considering a worst-case tim- rences related to the passage of a quantitative determin-
ing analysis to validate the system. However, a worst- istic time period. As such, non-deterministic decisions
case analysis provides pessimistic results and not all can be taken throughout bounding curves. We propose
component-based systems can afford such pessimism. anapproachwhichallowsdesignerstounifyin thesame
The pessimism can be decreased by using different ap- frameworkprobabilisticschedulingtechniquesand com-
proachesandweareinterestedintheutilisationofproba- positional guarantees for real-time systems with degrees
bilisticapproachesforcomponent-basedsystems. thatgofromhardtosoftreal-time. Theprobabilisticpa-
| 978-1-4577-0018-7/11/$26.00 |     |     |     | '2011 |     | IEEE |     |     |     |     |     |     |     |
| --------------------------- | --- | --- | --- | ----- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
Authorized licensed use limited to: FLORIDA INTERNATIONAL UNIVERSITY. Downloaded on February 11,2026 at 01:08:23 UTC from IEEE Xplore.  Restrictions apply.

rametersandboundsprovideasetoffunctionsexpressing (ki +1)and((cid:3)i +1)arerespectivelythenumberofcom-
theresourcegiventoataskflowandtheresourcedemand putationtimesandperiodsrepresentingtaskτi. Thecom-
of the task flow in terms of probabilistic bounds. With putationtimesareorderedinanoppositemannerthanthe
thosebounds,aschedulabilityanalysiscanbecarriedout. periodsforsake ofreadabilityandease ofrepresentation
Tothe bestofourknowledgethisworkisthefirstexten- ofthemathematicalexpressions.
sionofRTCtowardaprobabilisticversion1. InthispaperweassumealltherandomvariablesC iand
T i,∀i ≤ n, areindependent. Thisassumptionisnotun-
Paperorganization Thepaperisstructuredasfollows. realisticforrealsystems3. Fordependentvariablesthere-
Section 2 presents the probabilistic periodic task model, sultspresentedherecouldbeextendedusingcopulas[3],
the scheduler and the resource models that are used butthisisbeyondthepurposeofthispaper.
throughoutthe paper. Section 3providesthe readerwith All these parameters are given with the interpretation
basic concepts of probabilistic bounding curves. Sec- thattaskτigeneratesaninfinitenumberofsuccessivejobs
tion4 presentsinputsandoutputsof a probabilisticreal- τi,j, with j = 1,...,∞. Each such job has an execu-
timecomponent. Section5yieldsthecorrespondencebe- tionrequirementdescribedbyC iwhereforeachvalueC i k,
tweeneachtaskandeachresourceintermsofprobabilistic fCi (C i k) is its probabilityof occurrence. Instead, the ar-
boundingcurves. Section 6 elaboratesthe schedulability rivalofthejobsisdescribedbyT i,e.g. theprobabilityof
analysis of the system based on these curves. Section 7 havingT i k asthe arrivalforthenexttask jobis fTi (T i k).
presentsacasestudyapplyingtheproposedapproach.Fi- Allthe jobsare assumedto beindependentofotherjobs
nally, Section 8 concludesthe paperand proposesfuture ofthesametaskandthoseofothertasks.
work.
2.2 SchedulerandResourcespecifications
2 Model ofcomputation We consider that tasks are scheduled by using a pre-
emptivehierarchicalscheduler4uponauniprocessorplat-
form. The computational resource is assumed to be the
We consider here real-time systems with a model
uniqueresourceinthispaper. Hierarchicalschedulersal-
of computation consisting of probabilistic periodic
low:
constrained-deadline tasks and probabilistic resource
provisioning. This probabilisticmodelis providedin or-
(cid:4) generalizingtheroleofschedulersbyallowingthem
der to cope with uncertaintiesthat could come from dif-
to schedule other schedulers, thus leading to isola-
ferentsources.
tionpropertiestoberecursivelyappliedtogroupsof
tasks,ratherthanapplyingthemonlytoasingletask.
2.1 Taskspecifications
Weconsiderareal-timesystemΓcomposedofntasks, (cid:4) expressing complex composite schedulers as a col-
Γ d=ef {τ1,τ2,...,τn }. Each τi is modeled by a prob- lection of small, simple schedulers, thus providing
abilistic periodic and constrained-deadline task charac- increased flexibility compared to the “one size fits
terized by three parameters (C i,T i,Di ) where C i is a all”schedulers.
random variable2 representing the execution time with a
Moreover, we consider that the scheduler can be either
known Probability Function (PF) denotedby fCi (·) with
Fixed-Priority (FP) such as Rate Monotonic (RM) and
fCi (c)d=ef P(C i =c),T iisarandomvariableoftheperiod Deadline Monotonic (DM), or Dynamic-Priority (DP)
withaknownPFdenotedbyfTi (·)withfTi (p)d=ef P(T i = suchasEarliestDeadlineFirst(EDF).
p)andDiisthetaskrelativedeadline.Theexecutiontime
ofτi takesavalueboundedby[C
i
min,C
i
max]whereasthe 3 Concept ofprobabilisticbounding curves
period takes a value bounded by [Tmin,Tmax]. We as-
i i
sumethatC i max≤Di andDi ≤T i min. RTC allows characterizing a task by the maximum
ThePFofC iandT iarerespectivelyrepresentedasfol- amount of computation requested within any interval of
lows. time. Inthesamevein,itallowscharacterizingaresource
!
C0=Cmax C1 ··· Cki =Cmin via the minimum amount of computation that is guaran-
Ci= fC i i (C i m i ax) fCi (C i i 1) ··· f i Ci (C i mi i n) (1) teedtobedeliveredinanintervaloftime.TheRTCmodel
reliesoncurvesrepresentingsuchquantities.
and
!
T0=Tmin T1 ··· T(cid:2)i =Tmax 3.1 Probabilistictaskabstraction
Ti= f i Ti (T i m i in) fTi ( i T i 1) ··· f i Ti (T i m i ax) (2) Since we build our contribution on techniques from
(cid:2) (cid:2) RTC, task activations and executions are joined with
where k j= i 0 fCi (C i j)=1and (cid:2) j i =0 fTi (T i j)=1. Here, event streams. Consequently, one can derive an abstrac-
tion based on curves which is able to bound the event
1Exceptforapreliminaryversionofthispaper[21]
2Everywhereinthispaperwewilluseacalligraphictypefacetode- 3Formoredetailsseehttp://www.proartis-project.eu/
noterandomvariables. 4Weassumethateverypreemptionisperformedatnocostorpenalty.
Authorized licensed use limited to: FLORIDA INTERNATIONAL UNIVERSITY. Downloaded on February 11,2026 at 01:08:23 UTC from IEEE Xplore. Restrictions apply.

streambehavior[25]. Insuchacontext,eachtaskτi gen- 4.1 ProbabilisticOutputBounds
eratesrandomrequestcurvesdependingonboththeactual In RTC the output curves are the executed task flow
period and execution time of the task at each activation. α(cid:3) andthe unusedresourceβ(cid:3) forschedulingsuch tasks.
ConsideringthefunctionRi (t)asthecumulativeamount Theprobabilisticoutputcurvescanbeinferredbyapply-
ofexecutionthattheprobabilistictaskτihasrequestedup ing the relationship among the arrivaland service inputs
to time t, each task τi can be characterized by a request as for the RTC [25]. In [13], the probabilisticoutputar-
curveαiwhichboundsRi (t). rivalcurvehasbeendefinedasthecurve(cid:6)α(cid:3)(Δ,x),f(cid:3)(x)(cid:7)
Parameterizingtherequestfunctionwith a variablex, with α(cid:3)(Δ,·) d=ef α(cid:8)β(Δ,·)5 and the boundingfunction
itfollowsthatforall0≤s≤tandΔd=ef t−s,theupper f(cid:3)(·)d=ef f∗g(·)6.Suchprobabilisticcurveboundsthecu-
boundingrequestcurveαi (Δ,x)d=ef αi (Δ,·)−xissuch mulativeamountofresourceexecuteduptotimet,R(cid:3)(t)
thatαi (Δ,·)−[Ri (t)−Ri (s)]≥x. Hence,wecandefine asfollows.
theprobabilisticrequestcurvefrom[27]asfollows.
P(α (cid:3)(Δ,·)−[R (cid:3)(t)−R (cid:3)(s)]≥x)≤f ∗g(x) (5)
i i i
Definition 1 (Probabilistic request curve). The request
curveαi (Δ,x) ofa requestRi is a non-decreasingnon- Theunusedresourcebyprocessingreal-timeschedul-
negativefunctionwhichsatisfies ing componentis passed to otherparts of the system ac-
cording to a specific strategy. In [21] it has been de-
P(αi (Δ,·)−[Ri (t)−Ri (s)]≥x)≤fi (x) (3) fined the probabilistic version of the residual curve as
(cid:6)β(cid:3)(Δ,y),g(cid:3)(y)(cid:7), with β(cid:3)(Δ,·) = β (cid:8) α(Δ,·)7, and
forall0≤s≤tandx≥0. g(cid:3)(·)=f∗g(·)boundingthecumulativeresidualresource
In Inequality (3), fi (x) is the probability that αi (Δ,x) amountS(cid:3)(t)asfollows.
upperboundstherequestcurveofτi intheinterval[s,t].
P([S (cid:3)(t)−S (cid:3)(s)]−β (cid:3)(Δ,·)≥y)≤f ∗g(y) (6)
3.2 Probabilisticresourceabstraction
It is possible to derive an abstraction based on curves We represent the interface of each prob-
for the resource provisioningby followingthe same rea- abilistic real-time component by the tuple
soning as for tasks. Naming S(t) the total amount of ((cid:6)α,f(cid:7),(cid:6)β,g(cid:7),(cid:6)α(cid:3),f(cid:3)(cid:7),(cid:6)β(cid:3),g(cid:3)(cid:7)). The input and out-
resource providedat time t, the resource provisioning is put curves and their probabilities are illustrated in
characterizedby consideringthe lower boundingservice Figure1.
curveβasafunctionofS(t).
(cid:6)β,g(cid:7)
Parameterizingtheresourceprovisioningfunctionwith
(cid:6)α,f(cid:7) (cid:6)α(cid:3),f(cid:3)(cid:7)
avariabley,itfollowsthatforall0≤s≤tandΔd=ef t−
s,thelowerboundingservicecurveβ(Δ,y)d=ef β(Δ,·)+ (cid:6)β(cid:3),g(cid:3)(cid:7)
yissuchthat[S(t)−S(s)]−β(Δ,·)≥y. Hence,wecan
Figure 1. Interface of a probabilistic real-
definetheprobabilisticservicecurvefrom[27]asfollows.
timecomponent.
Definition 2 (Probabilistic service curve). The service
curve β(Δ,y) of a resource provisioning S is a non-
decreasingnon-negativefunctionwhichsatisfies
5 Modeling tasks with probabilistic bound-
P([S(t)−S(s)]−β(Δ,·)≥y)≤g(y) (4) ing curves
forall0≤s≤tandy ≥0.
In this section we provide the correspondence of our
In Inequality (4), g(y) is the probability that β(Δ,y)
modelof computationintermsofprobabilisticbounding
lowerboundstheresourceprovisioningS(t).
curves. Subsections5.1and5.2addressthespecificcases
whereonly onetask parameteris describedbya random
4 ProbabilisticReal-TimeComponents variable, i.e., the period or the execution time, respec-
tively.Then,Subsection5.3addressesthecasewhereboth
parameters can be described by random variables at the
Thecomponent-basedviewofreal-timesystemsmod-
sametime.
els each system element as a component [23] with an
associated interface describing its functional and non-
5AsdefinedinRTC[25]andbythenotionofmax-plusdeconvolution
functionalaspects,includingitstimingrequirements. (cid:2),[15].
InthecontextofRTCwithrequestandresourceprovi- 6∗istheconvolutionbetweenfunctionsintheclassicalalgebra;⊗is
sioning functionsR(t) and S(t), the real-time interfaces themin-plusconvolutionforRTCcurves,and⊗isthemax-plusconvo-
includesinputcurvesα and β, and outputcurvesα(cid:3) and lutio 7A n. sdefinedinRTC[25]andbythenotionofmin-plusdeconvolution
β(cid:3). (cid:2),[15].
Authorized licensed use limited to: FLORIDA INTERNATIONAL UNIVERSITY. Downloaded on February 11,2026 at 01:08:23 UTC from IEEE Xplore. Restrictions apply.

5.1 Caseofprobabilisticperiods 5.2 Caseofprobabilisticexecutiontimes
Weprovidetheprobabilisticboundsontherequestofa We provide now bounds for tasks τi d=ef (C i,Ti,Di )
taskτi d=ef (Ci,T i,Di ),whereonlytheperiodisdescribed withtheexecutiontimedescribedbyarandomvariable.
byarandomvariable,asfollows.
Lemma3. Letτi d=ef (C i,Ti,Di )beataskwithC idefined
Lemma1. Letτi d=ef (Ci,T i,Di )beataskwiththeperiod asinExpression(1),then:(i)therequestcurveα u i ,C up-
T idefinedasinExpression(2).Then:(i)therequestcurve perboundsallthe requestcurvesofτi in anyintervalof
t α e u i rv ,T al u o p f p l e e r ng b t o h u Δ nd w s h a e ll re th α e u
i
r , e T q ( u Δ es ) t d= c e u f r (cid:10) v
T
es Δ
mi
o
n
f (cid:11) τ · i C in i; a (i n i y )t i h n e - c le u n r g v t e h α Δ (cid:2)
i
, , C w l h o e w r e e r α b u i o ,C un ( d Δ s ) a d l = l e t f h (cid:10) e T Δ r i e (cid:11) q · u C e i s m t a c x u ; rv (i e i s ) o th f e τi re in qu a e n s y t
request curve α
(cid:2)
i
,T
lower bounds all th
i
e request curves
intervaloflengthΔ,whereα (cid:2)
i
,C(Δ)d=ef (cid:12)
T
Δ
i
(cid:13)·C
i
min.
of τi in any interval of length Δ where α (cid:2)
i
,T(Δ) d=ef
Proof. Theproofofthislemmaissimilartotheproofof
(cid:12)
Tm
Δ
ax
(cid:13)·Ci .
Lemma1.
i
u,C (cid:2),C
Proof. The proofis madebycontradiction. We consider ThankstoLemma3,curvesα i andα i boundany
any interval of length Δ. (i) Let us assume there exists otherrequestcurvederivedfromtaskτiparametersbyse-
(cid:10) T T T i h i Δ i m ∈ s in im (cid:11) [T p · i m l C ie i i n s . , t S T h i i a m n t c a (cid:10) e x T ] Δ i s T (cid:11) u i · c ∈ h Ci t [ h T ≤ a i m t (cid:10) i (cid:10) n T T , Δ i Δ m i T i (cid:11) i n m (cid:11) · a C x · ] C i , i t > h , e h n e α n T u i Δ c i , e T ≤ w (Δ e T ) h i Δ m a d i = v n e e f . l t d b i e e o o c fi u n ti n n . n e d H g s o e a o t n h n d c e l i e y r ff a c a e s u r c e f r e o v n r r e t t s a p th i o i n e n s p s c b i e a b e r s l t c e e w e o n e e x f t e a e n t g h c e [ e u α t o p i (cid:2) i o f , e C n r ta i , o t s α i d k m u i s τ , , e C i i a t a ] t i c w s e ti a h p v c i o a c h t s h i s o a i u b n ct p l s i e . p v t e a o - r
T (cid:10) T h Δ i e (cid:11) p · r C oo i f ≤ for α ( u i i , i T ) ( c Δ om ), e w s h fr ic o h m c R on T t C rad a i n c d ts is th s e im as i s la u r m to pti t o h n at . Lem G m iv a en 3 d th e e fin P e F sth d e es f c o r l i l b o i w ng ing C i set as of in req E u x e p st re c s u s r i v o e n s ( r 1 el ) - ,
of(i). ativetotheactivationsoftaskτi, withxtheindexofthe
boundingcurves.
u,T (cid:2),T ⎧
ThankstoLemma1,curvesα andα boundany
b N o y t o h t s e e e r l t r e h e c a q t t i u n t e h g s e t a s c e d u c i r f v u f e e rv r d e e e n s r t i a v p r e e o d s u s f n i r b i o q l m e ue p t . i h e e H ri p o e a d n r c a a e t m , e i e a t i t c e is h rs p a o o c f s ti s t v a ib a s t l k i e o τ t n i o , . α C i (Δ,x)d=ef ⎨ ⎩ (cid:5) α α T u i (cid:2) i Δ , i , C C (cid:6) ( ( · Δ Δ C ) ) i x i i i f f f x x x > ∈ = [ k 0 1 i ,k i ] (9)
define other curves in between [α (cid:2) i ,T ,α u i ,T] which upper For any interval of size Δ, each curve in this set upper
boundonlyapercentageoftaskτiactivations. boundsacertainpercentageoftaskτi withtheassociated
Given the PF describing T i as in Expression (2), CDFFC definedasfollows.
i
Lemma1definesthefollowingsetofrequestcurvesrela- ⎧
tivetotheactivationsoftaskτiexploitingthedependency ⎨
(cid:2)
1 if x=0
onxasanindex. F i C(x)d=ef ⎩ j k = i− 0 x fCi (C i j) if x∈[1,ki ] (10)
⎧ 0 if x>ki
For an α y T i i ( n Δ te , r x v ) al d= o ef f ⎨ ⎩ size (cid:5) α α T u i (cid:2) i Δ Δ , i , x T T (cid:6) , ( ( Δ Δ · e C ) a ) c i h c i i i f f f u x x x rv ∈ > = e [ (cid:3) 0 i 1 n i ,(cid:3) t i h ] is set upp (7 e ) r t a L s e i l o e r l v m n t a h s m l e ( o 9 a r f ) e 4 l q a e . u n n e d g L s t ( e t h 1 t c 0 Δ (cid:6) u ) α r , . v C i th e ( s e Δ n o , α f x τ C i ) i , ( s Δ F u i C c ) h (cid:7) = t b h (cid:10) e a T Δ t d i C e (cid:11) fi · i n C ≤ e i x d C u a p s i x p i e i n n r E b a x o n p u y r n e i d n s s - -
boundsacertainpercentageoftaskτiactivationsdepend-
ingonthevalueassignedtoparameterx. Theassociated Proof. ThislemmaderivesfromthefactthatforallCi ≤
CumulativeDistributionFunction(CDF)F i T isdefinedas C i x,wehave(cid:10) T Δ i (cid:11)·Ci ≤ (cid:10) T Δ i (cid:11)·C i x. Thelemmafollows.
follows.
⎧
⎨ 1 if x=0
(cid:2) 5.3 Case of probabilistic execution times & proba-
F i T(x)d=ef ⎩ (cid:2) j i = − 0 x fTi (T i j) if x∈[1,(cid:3)i ] (8) bilisticperiods
0 if x>(cid:3)i In this section, we combine the results obtained in
the previous two sections by considering tasks τi
d=ef
Lemma 2. Let (cid:6)αT i (Δ,x),F i T(x)(cid:7) be defined as in Ex- (C i,T i,Di ), where both the execution time and the pe-
pressions (7) and (8), then αT
i
(Δ) = (cid:10)
T
Δ
x
(cid:11) · Ci upper
riodaredescribedbyrandomvariablesasinEquations(1)
i
bounds all the request curves of τi, in any interval of and(2).Wefirstderiveatotalorderontherequestcurves
lengthΔsuchthatTi ≥T
i
x.
associatedtoeachtaskτi(sincetheymayoverlap).
Proof. ThislemmaderivesfromthefactthatforallTi ≥ Definition 3 ((cid:15)). Let α1 and α2 be two request curves
T
i
x,wehave(cid:10)
T
Δ
i
(cid:11)·Ci ≤ (cid:10)
T
Δ
i x
(cid:11)·Ci. Thelemmafollows. a
if
n
f
d
α1
Δ
(Δ
th
,
e
·)
le
≥
ng
α
th
2 (
o
Δ
f
,
a
·)
ti
,
m
∀
e
Δ
in
.
terval. Wesaythatα1 (cid:15) α2
Authorized licensed use limited to: FLORIDA INTERNATIONAL UNIVERSITY. Downloaded on February 11,2026 at 01:08:23 UTC from IEEE Xplore. Restrictions apply.

Definition4(≡). Wesaythatα1 ≡α2iffthereexistsΔ a (cid:4) probability = 1 (level 1): in this case, the system
andΔ bsuchthatα1 (Δ a,·)≥α2 (Δ a,·)andα2 (Δ b,·)≥ isalwaysschedulablewiththeinterpretationthatall
α1 (Δ b,·),or∀Δ : α1 (Δ,·)=α2 (Δ,·). the deadlinesare always met for all the tasks in the
The ≡ relationship indicates when two bounding system.
curves are equivalent, so that we can group them into (cid:4) probability =0(level0): inthiscase,thesystemis
a single boundingcurvemax{α1 (Δ,·),α2 (Δ,·)} with a never schedulable with the interpretation that what-
probabilityofboundingPd=ef P(α1 )+P(α2 )8. evertheconfigurationofthetasksofthesystem,the
Once an order among bounding curves is imposed, availableresourceprovisioningwillnotbesufficient
Lemmas1 and 3 define the probabilisticboundingcurve toscheduleallofthem.
forτi,(cid:6)αi (Δ,x),Fi (x)(cid:7). ForanyintervalofsizeΔ,each
In the remainder of this section, Subsection 6.1
curveinthissetupperboundsacertainpercentageoftask
presentstheschedulabilityanalysisinthecasewheretasks
τiactivationsdependingonthevalueassignedtoparame-
arescheduledaccordingtoaFixed-Priorityschedulersuch
terx. TheassociatedcumulativedistributionfunctionFi
as RM or DM. Finally, Subsection 6.2 presents the case
canbedefinedasFi (x)d=ef F
i
T(x)∗F
i
C(x)toconsiderall
wheretasksarescheduledaccordingtotheEDFscheduler.
thecombinationsbetweenthecurvesandtheprobabilities
Inacomponent-basedreal-timesystemtheschedulability
associated. Again,theequivalentscurvesaregroupedto-
ofcomponentsrelatestotheircomposability,[23,21].
gether,resultinginasinglerepresentativeboundingcurve
withasingleboundingprobability,henceasingleCDF. 6.1 FixedPriority(FP)scheduler
Example 1. Let τi = (C i,T i,D(cid:6)i = 8) be a prob(cid:7)abilis- We consider the set Γ = {τ1,τ2,...,τn } of n prob-
6 4 3 abilistic real-time tasks with characteristics definedas in
tic per
(cid:6)
iodic task w
(cid:7)
here C i = 0.1 0.4 0.5 and Section2. Wesupposethatthetasksareorderedwithde-
12 15 creasing priority, i.e., τ1 is assigned the highest priority
T i = 0.7 0.3 . The probabilisticresource request whereasτnisassignedthelowestpriority.Wedenotedby
(cid:6)αi (Δ,x),Fi (x)(cid:7)isrepresentedbythefollowingfigures. hp(i) d=ef {τ1,τ2,...,τi } the sub-set of all tasks with a
Figure 2 describing the bounding curves of τi with the priorityhigherthanorequaltoτi.
groupingoftheequivalentcurves; whileFigure3forthe Sincetasks areorderedwith decreasingprioritywhen
CDFwiththeprobabilityofboundingpercurveαi (Δ,x) they are scheduled by following a FP scheduler, the
varyingx. schedulability conditions can be derived in a composi-
resource
tionalmannerbyapplyingthehierarchicalstructureofthe
taskset. Figure4depictssuchastructurewhereeachtask
τi ismodeledasacomponentwithitsprobabilisticinter-
Δ face. In this case, (cid:6)βi,Gi (cid:7) is the resource provisioning
Figure 2. Bounding curve αi (Δ,x). Multiple function passed to the ith componentand (cid:6)αi,Fi (cid:7) is the
curvesvaryingtheindexx. requestfunctionofcomponenti.
1 0.93
0.62 (cid:6)α1,F1 (cid:7) (cid:6)α2,F2 (cid:7) (cid:6)αn,Fn (cid:7)
0.15 0 (cid:6)β1,G1 (cid:7) (cid:6)β2,G2 (cid:7) (cid:6)β3,G3 (cid:7) (cid:6)βn,Gn (cid:7)
0 1 2 3 4
τ1 τ2 ... τn
Figure 3. Cumulative distribution function
Fi (x) with the index x from the ordered set
Figure4.HierarchicalFPscheduling.
ofcurves.
Forthiskindofschedulers,wedefinethelevel-iwork-
load as the contribution of all the tasks in hp(i) (with
6 Schedulability Analysis i = 1,2,...,n). From task τi view point, the level-i
workload is defined from the task arrivals and is given
Inthissectionweproposeschedulabilityconditionsfor by (cid:6)ωi (Δ,x),Hi (x)(cid:7), where wi (Δ,x) is a set of non-
a probabilistic real-time system when both the tasks and decreasingrequestcurvesandhi (x)isaprobabilityfunc-
theresourcearedescribedbyaprobabilisticmodelaspre- tion (cumulative distribution in this case), computed as
sented in Section 2. We assume that tasks are scheduled follows.
byusingapreemptivehierarchicalschedulerasspecified
in Subsection2.2. Thisanalysisencompassesthe proba-
(cid:4) wi (Δ,x) is obtainedbyperformingthe convolution
of the request curves of all the tasks in hp(i), i.e.,
bility level of the system schedulabilitybetween the fol-
lowingtwoextremes: ωi (Δ,x)d=ef ⊗ τj∈hp(i)αj (Δ,x),
8Even in case of probabilistic lower bounding resource curve (cid:4) Hi (x) is obtainedby performingthe convolutionof
t
(cid:8)
a
β
ti
(
v
Δ
e
,
c
y
u
)
rv
,
e
G
i
(
s
y
t
)
h
(cid:9)
e
e
n
q
t
u
h
i
e
va
m
le
i
n
n
t
im
cu
u
r
m
ve
a
s
m
ca
o
n
ng
al
t
s
h
o
em
be
w
gr
it
o
h
up
a
e
p
d
r
.
o
T
ba
h
b
e
il
r
i
e
ty
pr
e
e
q
se
u
n
a
-
l
the CDFs of all the tasks in hp(i), i.e., Hi (x) d=ef
tothesumoftheirprobabilities. ∗ j∈hp(i)Fj (x).
Authorized licensed use limited to: FLORIDA INTERNATIONAL UNIVERSITY. Downloaded on February 11,2026 at 01:08:23 UTC from IEEE Xplore. Restrictions apply.

(cid:6)β,G(cid:7)
Consequently, a schedulability condition for a proba-
(cid:6)α1,F1 (cid:7)
bilistic real-timesystemwith probabilitylevelequalto1
canbederivedasfollows.
(cid:6)α2,F2 (cid:7)
Γ
Theorem5(1-FPSchedulability). Anyprobabilistictask ···
setΓ = {τ1,τ2,...,τn }isschedulablewithalevel1un-
(cid:6)αn,Fn (cid:7)
derFPandaprobabilisticresourceprovisioning(cid:6)β,G(cid:7)if
foralli∈{1,2,...,n}, Figure5.EDFscheduling.
∃Δ 0 ∈schedP i |ω i u(Δ 0,·)≤β (cid:2)(Δ 0,·) (11)
Theorem 7 (1-EDF Schedulability). Any probabilistic
t H h e e r s e c , h s e c d h u e l d a P b i ili r t e y p a re s s d e e n fi ts ne th d e in se [ t 4 o ], f ω po i u in is ts th w e h u e p r p e e t r o b v o e u ri n f d y t a a b s i k lit s y et le Γ ve = l1 { u τ p 1, o τ n 2 a ,. r . e . s , o τ u n r } ce i , s f s o c l h lo e w du in la g b a le n w E i D th F a sc p h ro ed b - -
of the probabilistic level-i workload (cid:6)ωi (Δ,x),Hi (x)(cid:7) uler,withaprovisioningcurve(cid:6)β,G(cid:7)if
andβ(cid:2) thelowerboundof(cid:6)β(Δ,x),g(x)(cid:7).
Proof. The theorem describes the classical real-time ∀Δ, α u(Δ,·)≤β (cid:2)(Δ,·)
schedulability condition with the level-i workload. The
Here, αu represents the request curve upper bounding
demonstrationisthenstraightforwardfrom[4,16].
(cid:6)α,f(cid:7) and β(cid:2) the resource provisioning curve lower
ThefollowingtheoremextendsTheorem5tothecase bounding(cid:6)β,G(cid:7).
wheretheprobabilitylevelequaltop∈[0,1[,thustaking
theprobabilityfunctionintoaccountintheschedulability Proof. Theproofofthistheoremfollowsdirectlyfromthe
conditions.
factthatbothαu andβ(cid:2)areboundingcurveswithaprob-
ability1each.
Theorem6(p-FPSchedulability). Anyprobabilistictask
set Γ = {τ1,τ2,...,τn } is schedulablewith a probabil- Theorem 8 (p-EDF Schedulability). Any probabilistic
itylevelp ∈ [0,1[underFPandaprobabilisticresource task set Γ = {τ1,τ2,...,τn } resulting in a probabilistic
provisioning(cid:6)β,G(cid:7)ifforalli∈{1,2,...,n} resource demand (cid:6)α,F(cid:7) is schedulable under EDF with
∃Δ
0
∈schedP
i
and∃x1,x2 ≥0suchthat a probability level p ∈ [0,1[ and upon a resource curve
(cid:6)β,G(cid:7)if
ωi (Δ 0,x1 )≤β(Δ 0,x2 )andHi (x1 )·G(x2 )≥p (12)
with(cid:6)ωi (Δ,x),Hi (x)(cid:7)theprobabilisticlevel-iworkload.
∀Δ, ∃x1,x2 ≥0suchthat
Proof. Since ωi (Δ,x) and β(Δ,x) are independentran-
α(Δ,x1 )≤β(Δ,x2 )andF(x1 )·G(x2 )≥p (13)
dom variables, ωi (Δ 0,x1 ) being less than or equal to
Proof. Theschedulabilityisguaranteedwhentherequest
β(Δ 0,x2 ) has a probability given by Hi (x1 ) · G(x2 ).
is less than the provisioning. Accordingly, to ensure a
Then, the level p-FP schedulability is guaranteed if
schedulability with a certain probability level it is suf-
Hi (x1 )·G(x2 )≥p. ficient to find a request curve α(Δ,x1 ) upper bounded
by β(Δ,x2 ). Since α(Δ,x) and β(Δ,x) are indepen-
6.2 EDFscheduler
dent random variables and F(x1 ) is the probability that
In the case where the tasks are scheduled by follow- α(Δ,x1 )upperboundstherequestfunction,thenF(x1 )·
inganEDFschedulingparadigm,theschedulabilitycon- G(x2 ) is the probabilitythat α(Δ,x1 ) upperboundsthe
dition is derived relative to the demand bound functions
requestfunctionononehand,andβ(Δ,x2 )lowerbounds
[2]. Here,thedemandboundfunctionofeachtaskcorre-
the resource provisioning on the other hand. As such,
spondstotheminimumresourceitrequirestoexecuteand
1−F(x1 )·G(x2 ) is the probability that the events are
meetsitstimingconstraint[6]. Accordingly,theresource
notboundedbythetwofunctions,i.e.,theprobabilitythat
demandcurveαi consideredfor each task τi is obtained
theeventsarenotschedulablebytheresourceprovision-
b th y e s t h as if k t , in i. g e. t , h α e i ( o Δ rig ,· i ) na d= l ef re α q i u ( e Δ st − cu D rv i, e ·) b . y U t s h i e ng d t e h a e dl p i r n o e b o a f - a ing pr β o ( b x a 2 b ) i . lit C y on le s v e e q l ue p n -E tly D , F as s c c h h e e d d u u l l a a b b i i l l i i t t y y c i o s nd g i u t a io ra n n w te i e th d
bilisticmodel,taskτiisrepresentedby(cid:6)αi (Δ,x),Fi (x)(cid:7), wheneverα(Δ,x1 ) ≤ β(Δ,x2 )andF(x1 )·G(x2 ) ≥ p.
whereαi (Δ,x) d=ef αi (Δ−Di,x),andFi (x) d=ef Fi (x), Thetheoremfollows.
i.e.,theoriginalcumulativedistributionofτi.
Since the EDF scheduler refers to the schedulability 7 CaseStudy
condition of the whole task set instead of each task, the
request curve of the task set Γ is given by (cid:6)α,f(cid:7) where We present an example of hierarchical scheduling to
α(Δ,x) d=ef ⊗n
i=1
αi (Δ,x)andF(x) d=ef ∗n
i=1
Fi (x). Fig- show the effectiveness of the analysis framework pro-
ure5illustratesanEDFscheduling. posed. We consider an EDF and an FP scheduler com-
From these observations, we derive the following re- ponenttogetherwith a globalschedulerthatprovidesre-
sults. sources to both. The resource is provided first to the
Authorized licensed use limited to: FLORIDA INTERNATIONAL UNIVERSITY. Downloaded on February 11,2026 at 01:08:23 UTC from IEEE Xplore. Restrictions apply.

EDF component, then to the FP one. This is equiv-
3+(cid:10)Δ−6(cid:11)·2.
Theprobabilisticresidualresourcecurve
6
alent to a fixed priority resource scheduling where the (cid:6)β(cid:3)(Δ,x),G(cid:3)(x)(cid:7),fromtheEDFschedulingisgivenby
EDF component has a higher priority than the FP one. ⎧
The EDF component locally sc(cid:6)hedul(cid:7)es t(cid:6)wo p(cid:7)robabilis- ⎨ β(cid:2)α EDF (Δ,2−x) if x=0
2 6 β (cid:3)(Δ,x) β(cid:2)α EDF (Δ,2−x) if x=1
tic tasks (cid:6) τ1 and τ2 wi (cid:7) th τ (cid:6) 1 = ( 1 (cid:7) , 1 ,6) and ⎩ β β(cid:2) (cid:2) u α EDF (Δ,2−x) i i f f x x= > 2 2,
3 2 10 12
τ2 = ( 0.6 0.4 , 0.8 0.2 ,10). The FP Its CDF is G(cid:3)(x) = FEDF since the CDF of the ini-
compone(cid:6)nt manages p(cid:7)rob(cid:6)abilistic task(cid:7)s τ3 and τ4 where tial resource was 1. The curves β(cid:3)(Δ,x) composing
4 3 12 16 (cid:6)β(cid:3)(Δ,x),G(cid:3)(x)(cid:7)arerepresentedinFigure7asmultiple
τ (cid:6) 3 = (cid:7) ( (cid:6) 0.6 (cid:7) 0.4 , 0.7 0.3 ,12) and τ4 = boundingcurves, althoughβ(cid:3)(Δ,1) and β(cid:3)(Δ,2) can be
2 10 groupedbecausetheyareequivalent.
( , ,10). Intermsofresources,theglobal
1 1
scheduler providesits entire resource (cid:6)β(Δ) = Δ,1(cid:7) to 10
the EDF scheduler. The residual resource (the resource
8
unused by it) is then passed to the FP scheduler which
6
applies it to schedule its set of tasks. The case study is
detailedinFigure6. 4
(cid:6)α1,F1 (cid:7) (cid:6)β,G(cid:7)
2
0
(cid:6)α2,F2 (cid:7)
EDF
0 2 4 6
Inte
8
rvals
10 12 14 16
(cid:6)β(cid:3),G(cid:3)(cid:7)≡(cid:6)β3,G3 (cid:7)
(cid:6)α3,F3 (cid:7)
(cid:6)β
1
(cid:3),G(cid:3)
1
(cid:7)≡(cid:6)β4,G4 (cid:7)
(cid:6)α4,F4 (cid:7)
FP
Figure 6. An hierarchical EDF and FP
scheduling.
Theresultsareobtainedwithaprobabilisticversionof
MPA[26]forperformanceanalysiswithRTC.
7.1 Schedulabilityanalysis
The schedulabilityanalysis of the hierarchicalsystem
addresses the EDF scheduler first. The probabilistic cu-
mulative resource demand of τ1 and τ2, once ordered
the composingcurves, results in (cid:6)αEDF,FEDF (cid:7), where
αEDF (Δ,x) = α1 (Δ,x)+α2 (Δ,x), with α1 (Δ,·) =
(cid:10)Δ−6(cid:11)·2and
6
⎧
⎪⎨ (cid:5)Δ 1 − 0 10(cid:6)·3 if x=0
α2 (Δ,x)= ⎪⎩ m (cid:5)Δ a
1
− x
2
{ 1 (cid:5) 0 Δ (cid:6)· 1 − 0 2 10(cid:6)·2,(cid:5)Δ 1 − 2 10(cid:6)·3} i i f f x x = = 2 1
(cid:10)Δ−10(cid:11)·2 if x>2. 12
TheCDFFEDF oncegroupedisgivenby
⎧
⎨ 1 if x=0
FEDF (x)=F1 ∗F2 =
⎩
0
0
.
.
5
3
2
2
i
i
f
f
x
x
=
=
1
2
0 if x>2
Compared with the resource provisioning (cid:6)Δ,1(cid:7) it re-
sults in a 1-EDF schedulability, being Δ > (cid:10)Δ−10(cid:11) ·
10
ecruoseR
resource2
resource0
resource1
Figure 7. Probabilistic residual resource
curve (cid:6)β(cid:3),G(cid:3)(cid:7) with the 3 composing curves
β(cid:3)(Δ,·) (resources in the legend) including
theminamongthem.
The FP scheduler accounts for the input resource
(cid:6)β(cid:3),G(cid:3)(cid:7). Theresultinglevel-iworkloadisthen
⎧
⎪⎨ (cid:5)
1
Δ
2
(cid:6)·4 if x=0
ωFP,1 (Δ,x)=
⎪⎩
m
(cid:5) 1 Δ
a
6
x
(cid:6)
{
·
(cid:5)
3
1 Δ 2 (cid:6)·3,(cid:5) 1 Δ 6 (cid:6)·4}
i
i
f
f
x
x
=
=
2
1
(cid:10)Δ(cid:11)·3 if x>2 16
⎧
⎨ 1 if x=0
HFP,1 (x)= ⎩ 0 0 . . 5 1 8 2 i i f f x x = = 1 2
0 if x>2
andωFP,2 (Δ,x)=ωFP,1 (Δ,x)+(cid:10) 1 Δ 0 (cid:11)·2,HFP,2 (x)=
HFP,1 (x). Comparing ωFP,2 (Δ,x) with β(cid:3)(Δ,x), the
maximumschedulabilitylevelachievableisp = 1·0.58,
see Figure 8. In this case study, the system is not 100%
fixedpriorityschedulable.Butwiththeprobabilisticanal-
ysis it is possible to conclude about a level p = 0.58 of
schedulability.
10
8
6
4
2
0 0 2 4 6 8 10 12 14 16 Intervals
ecruoseR
resource workload0 workload1
workload2
Figure 8. FP schedulability at level p = 0.58
derivedfromβ(cid:3)(Δ,0)andωFP,2 (Δ,x).
Authorized licensed use limited to: FLORIDA INTERNATIONAL UNIVERSITY. Downloaded on February 11,2026 at 01:08:23 UTC from IEEE Xplore. Restrictions apply.

8 Conclusion
[12] X.FengandA.K.Mok.Amodelofhierarchicalreal-time
|     |     |     |     |     |     |     | virtualresources. |     | InProceedingsofthe23rd |     |     |     | IEEEReal- |
| --- | --- | --- | --- | --- | --- | --- | ----------------- | --- | ---------------------- | --- | --- | --- | --------- |
TimeSystemsSymposium,pages26–35,Austin,TXUSA,
| We study       | in this | paper         | the | component-basedschedul- |         |        |               |                                  |     |     |     |     |         |
| -------------- | ------- | ------------- | --- | ----------------------- | ------- | ------ | ------------- | -------------------------------- | --- | --- | --- | --- | ------- |
| ing problem    | of      | probabilistic |     | real-time               | systems | upon a | Dec.2002.     |                                  |     |     |     |     |         |
|                |         |               |     |                         |         |        | [13] Y.Jiang. | Abasicstochasticnetworkcalculus. |     |     |     |     | SIGCOMM |
| givenresource. | We      | proposea      |     | newmodelunifyinginthe   |         |        |               |                                  |     |     |     |     |         |
Comput.Commun.Rev.,36(4):123–134,2006.
| same frameworkprobabilistic |     |     |     | schedulingtechniquesand |     |     |              |     |          |           |           |       |          |
| --------------------------- | --- | --- | --- | ----------------------- | --- | --- | ------------ | --- | -------- | --------- | --------- | ----- | -------- |
|                             |     |     |     |                         |     |     | [14] K. Kim, | J.  | Diaz, L. | Lo Bello, | J. Lopez, | C.-G. | Lee, and |
compositionalguaranteestogetherwiththeassociatedal-
|     |     |     |     |     |     |     | S.L.Min. |     | Anexactstochasticanalysisofpriority-driven |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | --- | ------------------------------------------ | --- | --- | --- | --- |
gebra. This model is the first probabilistic model with periodicreal-timesystemsanditsapproximations. Com-
both the execution time and the period of each task de- puters, IEEE Transactions on, 54(11):1460 – 1466, nov.
| finedbyrandomvariables. |     |     | Forsystemsusingthismodel |     |     |     | 2005. |     |     |     |     |     |     |
| ----------------------- | --- | --- | ------------------------ | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
we providea flexible analysis that matchesthe nature of [15] J. Y. Le Boudec and P. Thiran. Network calculus: A
todaysapplications(fromthepointofviewofcomplexity TheoryofDeterministicQueuingSystemsfortheInternet.
Springer-VerlagNewYork,Inc.,2001.
anduncertainties).
|             |      |             |     |        |           |     | [16] J. Lehoczky, |            | L. Sha, | and Y. | Ding.            | The rate | monotonic   |
| ----------- | ---- | ----------- | --- | ------ | --------- | --- | ----------------- | ---------- | ------- | ------ | ---------------- | -------- | ----------- |
| We consider | here | independent |     | random | variables | and |                   |            |         |        |                  |          |             |
|             |      |             |     |        |           |     | sheduling         | algorithm: |         | exact  | characterization |          | and average |
we leave as future work the propositionof results in the casebahavior.ProceedingsoftheIEEEReal-TimeSystems
caseofdependentrandomvariables.Computingtheexact
Symposium,1989.
complexityoftheproposedapproachaswellasproposing
|     |     |     |     |     |     |     | [17] G.LipariandE.Bini. |     |     | Amethodologyfordesigninghier- |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----------------------- | --- | --- | ----------------------------- | --- | --- | --- |
techniquestodecreaseitarealsoleftasfuturework. archicalschedulingsystems. JournalofEmbeddedCom-
puting,1(2),2004.
|     |     |     |     |     |     |     | [18] J.Lo´pez,J.D´ıaz,J.Entrialgo,andD.Garcia. |     |     |     |     |     | Stochastic |
| --- | --- | --- | --- | --- | --- | --- | ---------------------------------------------- | --- | --- | --- | --- | --- | ---------- |
References
|                |     |               |     |            |     |               | analysis | of          | real-time | systems | under        | preemptive | priority- |
| -------------- | --- | ------------- | --- | ---------- | --- | ------------- | -------- | ----------- | --------- | ------- | ------------ | ---------- | --------- |
|                |     |               |     |            |     |               | driven   | scheduling. |           | Journal | of Real-time | Systems,   | 40(2),    |
| [1] L. Almeida | and | P. Pedreiras. |     | Scheduling |     | with temporal |          |             |           |         |              |            |           |
2008.
| partitions: | Response-time |     | analysisand |     | server | design. In |                                       |     |     |     |     |               |     |
| ----------- | ------------- | --- | ----------- | --- | ------ | ---------- | ------------------------------------- | --- | --- | --- | --- | ------------- | --- |
|             |               |     |             |     |        |            | [19] S.P.MarimuthuandS.C.Chakraborty. |     |     |     |     | Aframeworkfor |     |
Proc.ofthe4thACMInternationalConferenceonEmbed- compositionalandhierarchicalreal-timescheduling.Real-
dedSoftware,pages95–103.ACMpress,2004. TimeComputingSystemsandApplications, International
[2] S.K.Baruah. Dynamicandstatic-priorityscheduling of Workshopon,0:91–96,2006.
recurringreal-timetasks. InReal-TimeSystem,pages93– [20] A.K.MokandA.K.Feng. Amodelofhierarchicalreal-
| 128,2003. |     |     |     |     |     |     | timevirtualresources. |     |     | InRTSS’02,IEEEComputerSoci- |     |     |     |
| --------- | --- | --- | --- | --- | --- | --- | --------------------- | --- | --- | --------------------------- | --- | --- | --- |
[3] G.BernatandM.Newby.ProbabilisticWCETanalysis,an ety,pages26–35.
approachusingcopulas.JournalofEmbeddedComputing, [21] L.SantinelliandL.Cucu-Grosjean. Towardsprobabilistic
| 2006. |     |     |     |     |     |     | real-timecalculus. |     |     | Specialissuerelatedtothe3rdWork- |     |     |     |
| ----- | --- | --- | --- | --- | --- | --- | ------------------ | --- | --- | -------------------------------- | --- | --- | --- |
[4] E. Bini and G. C. Buttazzo. Schedulability analysis of shoponCompositionalTheoryandTechnology forReal-
|          |       |          |          |      |              |     | Time | Embedded | Systems(CRTS |     | 2010) | at ACM | SIGBED |
| -------- | ----- | -------- | -------- | ---- | ------------ | --- | ---- | -------- | ------------ | --- | ----- | ------ | ------ |
| periodic | fixed | priority | systems. | IEEE | Transactions | on  |      |          |              |     |       |        |        |
Review,8(1),March2011.
Computers53(11),pp.1462-1473,November2004,pages
|     |     |     |     |     |     |     | [22] I. Shih | and | I. Lee. | Periodic | resource | model | for com- |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --- | ------- | -------- | -------- | ----- | -------- |
1462–1473,2004.
[5] J.L.BoudecandP.Thiran. NetweorkCalculus-AThe- positional real-time guarantees. In Proceedings of the
24thReal-TimeSystemsSymposium,pages2–13,Cancun,
| ory | of Deterministic |     | Queuing | Systems | for | the Internet. |     |     |     |     |     |     |     |
| --- | ---------------- | --- | ------- | ------- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- |
Mexico,Dec.2003.
SpringerVerlag,2001.
|     |     |     |     |     |     |     | [23] I. Shin | and | I. Lee. | Periodic | resource | model | for compo- |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --- | ------- | -------- | -------- | ----- | ---------- |
[6] S.Chakraborty,S.Ku¨nzli,andL.Thiele.Ageneralframe-
|      |               |     |        |            |                   |     | sitional | real-timeguarantees. |     |     | In RTSS’03: |     | Proceedings |
| ---- | ------------- | --- | ------ | ---------- | ----------------- | --- | -------- | -------------------- | --- | --- | ----------- | --- | ----------- |
| work | for analysing |     | system | properties | in platform-based |     |          |                      |     |     |             |     |             |
ofthe24thIEEEInternationalReal-TimeSystemsSympo-
| embedded | system | designs. |     | In DATE, | pages | 190–195, |       |      |                |     |          |       |           |
| -------- | ------ | -------- | --- | -------- | ----- | -------- | ----- | ---- | -------------- | --- | -------- | ----- | --------- |
| 2003.    |        |          |     |          |       |          | sium, | page | 2, Washington, |     | DC, USA, | 2003. | IEEE Com- |
puterSociety.
[7] S.Chakraborty,S.Kunzli,andS.Thiele.Ageneralframe-
|                       |               |     |                           |            |                   |     | [24] I. Shin | and | I. Lee.       | Compositional |     | real-time  | scheduling |
| --------------------- | ------------- | --- | ------------------------- | ---------- | ----------------- | --- | ------------ | --- | ------------- | ------------- | --- | ---------- | ---------- |
| work                  | for analysing |     | system                    | properties | in platform-based |     |              |     |               |               |     |            |            |
|                       |               |     |                           |            |                   |     | framework    |     | with periodic | model.        |     | ACM Trans. | Embed.     |
| embeddedsystemdesign. |               |     | InProc.oftheDATE’03,2003. |            |                   |     |              |     |               |               |     |            |            |
Comput.Syst.,7(3):1–39,2008.
| [8] L. Cucu | and | E. Tovar. | A   | framework | for | response time |                                           |     |     |     |     |     |               |
| ----------- | --- | --------- | --- | --------- | --- | ------------- | ----------------------------------------- | --- | --- | --- | --- | --- | ------------- |
|             |     |           |     |           |     |               | [25] L.Thiele,S.Chakraborty,andM.Naedele. |     |     |     |     |     | Real-timecal- |
analysisoffixed-prioritytaskswithstochasticinter-arrival
|        |                            |     |     |     |     |     | culusforschedulinghardreal-timesystems. |     |     |     |     |     | InProc.IS- |
| ------ | -------------------------- | --- | --- | --- | --- | --- | --------------------------------------- | --- | --- | --- | --- | --- | ---------- |
| times. | ACMSIGBEDReview,3(1),2006. |     |     |     |     |     |                                         |     |     |     |     |     |            |
CAS’00,volume4,pages101–104,2000.
| [9] R.I.DavisandA.Burns. |                    |             | Resourcesharinginhierarchi- |          |         |              |                  |                                         |        |                   |           |                |       |
| ------------------------ | ------------------ | ----------- | --------------------------- | -------- | ------- | ------------ | ---------------- | --------------------------------------- | ------ | ----------------- | --------- | -------------- | ----- |
|                          |                    |             |                             |          |         |              | [26] E. Wandeler |                                         | and L. | Thiele.           | Real-Time | Calculus       | (RTC) |
| cal                      | fixed priority     | pre-emptive |                             | systems. | In      | Proc. of the |                  |                                         |        |                   |           |                |       |
|                          |                    |             |                             |          |         |              | Toolbox.         | http://www.mpa.ethz.ch/Rtctoolbox,2006. |        |                   |           |                |       |
| 27th                     | IEEE International |             | Real-Time                   |          | Systems | Symposium    |                  |                                         |        |                   |           |                |       |
|                          |                    |             |                             |          |         |              | [27] J.XieandY.  |                                         | Jiang. | Stochasticnetwork |           | calculusmodels |       |
(RTSS’06),2006.
|     |     |     |     |     |     |     | under | max-plus | algebra. | In  | Proceedings |     | of the Global |
| --- | --- | --- | --- | --- | --- | --- | ----- | -------- | -------- | --- | ----------- | --- | ------------- |
[10] L.deAlfaroandT.Henzinger. Interface-baseddesign. In Communications Conference, 2009. GLOBECOM 2009,
Toappear intheproceedings of the2004 Marktoberdorf Honolulu,Hawaii,USA,30November-4December2009,
SummerSchool,2005.
pages1–6,2009.
| [11] A.Easwaran,I.Shin,O.Sokolsky,andI.Lee. |     |     |     |     |     | Incremen- |     |     |     |     |     |     |     |
| ------------------------------------------- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
[28] H.Zeng,M.D.Natale,P.Giusto,andA.L.Sangiovanni-
tal schedulability analysis of hierarchical real-time com- Vincentelli. Stochastic analysis of distributed real-time
ponents. In Proceedings of the 6th ACM & IEEE In- automotivesystems. IEEETrans.IndustrialInformatics,
| ternationalConferenceonEmbeddedSoftware(EMSOFT |     |     |     |     |     |     | 5(4):388–401,2009. |     |     |     |     |     |     |
| ---------------------------------------------- | --- | --- | --- | --- | --- | --- | ------------------ | --- | --- | --- | --- | --- | --- |
2006),pages272–281,October2006.
Authorized licensed use limited to: FLORIDA INTERNATIONAL UNIVERSITY. Downloaded on February 11,2026 at 01:08:23 UTC from IEEE Xplore.  Restrictions apply.