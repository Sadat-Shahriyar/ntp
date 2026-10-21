argument in that PL. The construction of \(\mathcal{D}\) is flexible: it can either be a comprehensive set of all available libraries and functions in a PL, or a customized subset for the scope of a specific project.

### Background: Retrieval-Conditioned Generation

Although a model may use the entire collection of documents \(\mathcal{D}\), only a few documents in \(\mathcal{D}\) are relevant for any particular intent. Further, it is usually computationally infeasible to directly condition on the entire, unbounded, collection of documents while making predictions. Thus, we first let the model _select_ a subset of documents \(\mathcal{D}_{n}=\{d_{1},d_{2},..,d_{k}\}\subseteq\mathcal{D}\) that are potentially relevant given \(n\), and refer to this subset while generating \(c\).

Overall, we decompose the probability of generating \(c\) into the probability of choosing a particular subset of documents \(P\left(\mathcal{D}_{n}\mid\mathcal{D},n\right)\), and the probability of generating the code conditioned on the intent and the selected documents \(P\left(c\mid\mathcal{D}_{n},n\right)\); finally, we marginalizing over all \(\mathcal{D}_{n}\subseteq\mathcal{D}\):

\[P\left(c\mid\mathcal{D},n\right)=\sum\nolimits_{\mathcal{D}_{n}\in\mathcal{D}} P\left(c\mid\mathcal{D}_{n},n\right)\cdot P\left(\mathcal{D}_{n}\mid\mathcal{D},n\right)\] (1)

assuming that \(c\) is independent of \(\mathcal{D}\) given \(\mathcal{D}_{n}\)(that is, \(\left(c\mathbin{\mathchoice{\vbox{\hbox{$\perp$}}}{\vbox{\hbox{$ \perp$}}}{\vbox{\hbox{$\perp$}}}{\vbox{\hbox{$ \perp$}}}}\mathcal{D}\mid\mathcal{D}_{n}\right)\)). Since enumerating all possible subsets \(\mathcal{D}_{n}\) is computationally infeasible, we follow the common practice and approximate the marginalization over \(\mathcal{D}_{n}\) in Equation (1) by taking the most probable subset of retrieved documents \(\mathcal{\hat{D}}_{n}\) and then conditioning the prediction of \(c\) on these most likely documents:

\[\mathcal{\hat{D}}_{n}:=\text{argmax}_{\mathcal{D}_{n}\mathbin{\mathchoice{ \vbox{\hbox{$\perp$}}}{\vbox{\hbox{$\perp$}}}{\vbox{ \hbox{$\perp$}}}{\vbox{\hbox{$\perp$}}}} \mathcal{D}}P\left(\mathcal{D}_{n}\mid\mathcal{D},n\right)\qquad\qquad P \left(c\mid\mathcal{D},n\right)\approx P(c\mid\mathcal{\hat{D}}_{n},n)\cdot P (\mathcal{\hat{D}}_{n}\mid\mathcal{D},n)\] (2)

### \(\mathrm{DocPrompting}\): Generating Code by Retrieving the Docs

Equation 2 implies that \(\mathrm{DocPrompting}\) relies of two main components: A _retriever_\(\mathcal{R}\) retrieves relevant documents \(\mathcal{\hat{D}}_{n}\) given the intent \(n\); and a _generator_\(\mathcal{G}\) generates the code snippet \(c\) conditioned on the retrieved documents \(\mathcal{\hat{D}}_{n}\) and the intent \(n\), which compose a new prompt. Specifically, \(\mathcal{R}\) computes a similarity score \(s\left(d_{i},n\right)\) between a intent \(n\) and every document \(d_{i}\in\mathcal{D}\). Thus, the subset \(\mathcal{\hat{D}}_{n}\mathbin{\mathchoice{\vbox{\hbox{$\perp$}}}{ \vbox{\hbox{$\perp$}}}{\vbox{\hbox{$\perp$}}}{\vbox{ \hbox{$\perp$}}}}\mathcal{D}\) is the top-\(k\) documents with the highest similarity scores: \(\mathcal{\hat{D}}_{n}=\text{top-}k_{d_{i}\in\mathcal{D}}\left(s\left(d_{i},n \right)\right)\).

An overview of our approach is illustrated in Figure 1 given the intent _Generate HTML with python syntax highlighting for "print(reading docs)"_, the retriever \(\mathcal{R}\) retrieves three relevant documents: \(d_{1}\) describes the syntax highlighting library payments, \(d_{2}\) describes the class PythonLexer, and \(d_{3}\) describes the HtmlFormatter class. Given these docs and the intent, the generator \(\mathcal{G}\) generates the code snippet \(c\), which uses PythonLexer and HtmlFormatter from the payment library.

## 3 Practical Instantiations of \(\mathrm{DocPrompting}\)

\(\mathrm{DocPrompting}\) is a general approach that is not bound to any specific model choices, and it can be instantiated with any base retriever and generator. This section presents the concrete instantiations of \(\mathcal{R}\) and \(\mathcal{G}\) that we found to provide the best performance in our experiments.

### Retriever Instantiation

We experiment with two main types of retrievers: _sparse_ retrievers and _dense_ retrievers. As our sparse retriever, we use Elasticsearch[2] with the standard BM25[17]. This retriever represents documents using sparse features that rely on word frequencies, such as BM25 and TF-IDF.

As our dense retriever, we follow prior work [20][20][21]: given a triplet \((n,c,\mathcal{D}_{n}^{*})\), where \(\mathcal{D}_{n}^{*}\) are the oracle docs for \(n\), each \(d_{i}^{*}\in\mathcal{D}_{n}^{*}\) and \(n\) form a _positive_ pair \((n,d_{i}^{+})\), while each \(d_{j}^{-}\notin\mathcal{D}_{n}^{*}\) and \(n\) form a _negative_ pair \(\left(n_{i},d_{j}^{-}\right)\). We train the retriever in a contrastive fashion where the similarity score of a positive pair is maximized while that of in-batch negative pairs is minimized. For a pair \((n_{i},d_{i}^{+})\), the loss function is defined as:

\[\mathcal{L}^{r}=-\log\frac{\exp\left(\text{sim}(\boldsymbol{h}_{n},\boldsymbol {h}_{d_{i}^{+}})\right)}{\exp\left(\text{sim}(\boldsymbol{h}_{n},\boldsymbol {h}_{d_{i}^{+}})\right)+\sum\nolimits_{d_{j}^{-}\in\mathcal{G}/\mathcal{D}_{n}^ {*}}\exp\left(\text{sim}(\boldsymbol{h}_{n},\boldsymbol{h}_{d_{j}^{-}})\right)}\] (3) 