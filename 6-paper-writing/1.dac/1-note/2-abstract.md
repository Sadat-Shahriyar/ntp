Offline verification of real-time system schedulability is an NP-hard problem. One effective approach to analyze schedulability is through mechanized proofs using formal verification libraries. Prosa is one such open-source framework built on the Coq proof assistant, enabling mechanical verification of schedulability analyses for real-time systems. However, current state-of-the-art large language models (LLMs) still struggle with syntactic and functional correctness when generating mechanized proofs using the Prosa library. To address this limitation, we develop a framework that significantly improves LLM correctness and output quality in generating Prosa scripts. Our approach integrates four key components: (1) generation of informal theorem sketches to improve LLM understanding, (2) creation of a high-quality dataset for translating sketches into Prosa scripts, (3) a two-stage LLM fine-tuning process, and (4) domain-specific retrieval-augmented generation. A systematic evaluation demonstrates substantial improvements in the syntactic validity and semantic correctness of generated Prosa scripts compared to existing LLMs. To the best of our knowledge, this is the first work to explore automated generation of Prosa proofs for real-time system schedulability analysis.



Jean email response on dataset: 
Lemma
theorem
definitions
corollary
claim


rename variables into code like format
U(T) -> U_T
σ_j -> sigma_j
S(τ) -> S_T

The informal sketch steps looks promising. I had some couple of remarks
1. Some of the informal sketches have "claim 1" or some other things as dependencies. but the claim 1 is not found in the whole json. So we have to extract the following things from the papers: 
   1. Lemma
   2. Theorems
   3. Definitions
   4. Corollary
   5. Claims
2. Also about the notations, it will be helpful if we could simplify different notations into code style variable name. Some examples might be:
   1. U(T) -> U_T
   2. σ_j -> sigma_j
   3. S(τ) -> S_T
3. Also I am attaching a file in the attachments. Can you please convert the informal sketeches in such format? It will be helpful if you could provide me the informal sketeches in the format because my code is working with that format. 
    