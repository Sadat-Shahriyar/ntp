# challenges
- No neural theorem prover for real time system
- We have gone through several theorem provers like coq, Lean etc but don't have native support for real time systems schedulibility analysis
- Only Prosa available
- Tried to generate prosa script with Chatpgt and claude but faced several issues
  - Had wrong import statements from gpt
  - It seemed like it was generating its own structure of library names. So did not have enoung knowledge about prosa library
  - From claude, the import staements were correct
  - But still there were error in the code
    - Variable declaration type
    - function definition
- So we had to develop our own model that would generate prosa script
- Allthought there are some benchmark datasets for math problems, to the best of our knowledge there is no benchmark for proving theorems in real time system schedulibility
- Found some papers in the prosa website which cited the prosa paper
- among them only 6 had prosa code available in the paper 
- and the rest 10 papers did not have any publicly available prosa script
- To train an LLM we needed a much larger Training data. So we are opting for generating our new dataset and then train the LLM with the library



# Methodology
- System Invariants Collection
  - As we had discussed above, the available scripts for prosa is very limited
  - So the method that we are willing to adopt is that, we will create a manual web travarsal algorithm that will visit the IEEE archive website for RTSS and other real time system conferences
  - We will implement this with the help of Selenium
  - On each papers page, we will extract the DOI number. Then we will download the paper with the help of PaperScrapper tool
  - Once downloaded, We will prompt a document LLM whether the paper is relevant to schedulibility analysis of real time system or not
  - If we get a positive response then, we will include the system invariants in the form of lemma and theorem in our dataset. If not we will discard it
  - Once we have shortlisted the papers, We will perform a RAG + LLM query on the document to extract the workload model, resource model, scheduler, analysis framework and the sytem invariants in the form of Lemma and Theorems.
  - This will create the initial dataset
  - Then after performing manual human curation and fact checking the extracted informations from the papers, Our goal would be to generate correct prosa script for this extracted lemmas and theorems. So these will be the system invariants that we are willing to solve with LLM generated mechanized proof
- Dataset generation and Model tuning
  - Once we have collected all the system invariants from the papers from renowned conferences, we are taking them as ground truth and expecting that the lemma and theorems mentioned in the papers are correct and if we follow the logical path of the described lemma and theorems, we will be able to solve the schedulibility problem
  - So our first step will be to bring all the lemma and theorem into a common source of language for LLM training. It will be an informal sketch, which is converting the lemma and theorems in plain structured english text. All the steps of the lemma and theorem will be translated in stepwise format. This will give us the high level structure of what we have to proof
  - Then we will take one lemma/theorem at a time and pass it through a RAG system. The RAG system will consist of Vector embeddings of the Prosa documentation. As mentioned before, the current state of the art LLMs can not perfectly create prosa script. So incorporating the documentation with RAG will be helpful in syntactical correctness and sematical accuracy
  - After retrieving the necessary documentation, the lemma along with the retrieved relevant code chunks will be passed to the LLM. The LLM will generate prosa script from the texts.
  - This prosa script will be passed through the prosa compiler. if it successfully compiles then the lemma/theorem will be updated in the informal sketch and this will be passed for the later lemma/theorems context so that variable integrity is maintained. 
  - if it does not compile successfully then the error message along with the prosa script and the informal sketch text will be again passed to the retriever. it will retrieve necessary context and pass it to the LLM so that the LLM can correct the code based on the error message. This wrong script will also be stored along with the correct scripts so that later on we can train our LLM with reinforcement learning
  - Once a code passes through the prosa compiler without any error, we will perform another semantic analysis with another LLM (Judge LLM) to check if the generated script agrees with the informal sketch for that lemma/theorem. If it passes then that will be considered as correct prosa script. otherwise discard and start generating new prosa script for the same example.
  - Once we have collected the necessary amount of correct scripts, we will structure our dataset like this: Workload model, resource model, scheduler, analysis framework, System invariants, Informal sketch and correct prosa script. The informal sketch would be incloded as a part of chain of thought process. 
  - With the substantial amount of correct scripst, we will supervised fine-tune our LLM. Then we will generate more scripts with the fine-tuned version. This process is called expert iteration.
  - After training our base LLM on substantial amount of data and successful collection of positive and negative pairs, we will train our LLM in another round with GRPO or DPO (Reinforcement learning). This trained version will be the final neural theorem prover version.

## RAG description:
- From our previous experiment with state of the art large langugae models, our experience shows that these models can not generate prosa script poperly. there is always syntactic or functional incorrectness. 
- To overcome this we employed a RAG system to guide the generation of syntactically correct prosa scripts with the help of LLM. 
- There are mainly two parts of the RAG. One is documentation rag, and another one is knowledge rag. 
- In the prosa repository, there are mainly there are mainly 5 directories. We used the different scripts available in the behavior, classic, model, util folder as the documentation database. These folders have the required library files to run prosa. While the scripts inside the analysis and results folder are used as knowledge database. there are many fully proven lemmas and theorems in these directories and a step by step guideline on how a theorem is proven for real time systems. So these examples extracted from the knowledge database help the model to guide on how a specific prosa script should be structured and the documentation database helps in finding the proper imports and necessary functions to use write a single script for a functional unit.
- Our RAG system works with the help of nomic-embed-code, a 7B parameter model. We initially downloaded the whole documentation of prosa from their official online repository. Then we parsed through each of the file and categorized them whether they should be in the documentattion database or knowledge database. 
- for docuemnts that should be included in the documentation database, we further extracted different sections as individual knowledge sections. These individual sections represented a unique function definitions, basic parameters that define different characteristics of real time systems and how different concepts in real time system should be presented with help of prosa. These unique sections are converted to embeddings with help of nomic-embed-code and stored in a FAISS vector database. 
- For documents relevant to knowledge database, we used them as a whole document for embedding. These documents had desctiptive information on how a specific real time system should be analyzed on a specific resource with a given workload model and scheduler. These descriptive proofs help guide the LLM on how a specific system should be analysed using the prosa. These whole documents were also embeded with the help of nomic-embed-code and stored in faiss vector databsed. 
- Once we have our documentation databse and knowledge databse, we search with the extracted informal sketches on these databases. For each informal sketch generated per paper, we divide and extract the individual definitions, claims, lemmas, theorems, coroallaries sequentially. And then perform cosine similarity with the individual sketeches on both documentation database and knowldege database. We fetch the top 5 documents from the documentation database and the top 2 docuemnts from the knowledge database. and feed it to the llm for guiding it to write prosa scripts. This helped to guide the model in writing the script without syntactic and functional correctness and help collect in initial data for fine-tuning llm. 

---
GPT:
From our earlier experiments with state-of-the-art large language models, we consistently observed that these models are unable to generate Prosa scripts reliably, often producing outputs with syntactic errors or functional inconsistencies. To address these issues, we introduced a Retrieval-Augmented Generation (RAG) system designed to guide the LLM toward producing syntactically correct and semantically coherent Prosa code. The RAG system consists of two complementary components: a documentation RAG and a knowledge RAG. The Prosa repository contains six major directories; among them, the behavior, classic, model, and util folders provide the core library functions necessary for building Prosa definitions and were therefore used as the documentation database. In contrast, the analysis and results directories include fully verified lemmas, theorems, and step-by-step mechanized proofs; these formed our knowledge database, offering concrete examples of how real-time scheduling analyses are structured within Prosa.

Our RAG pipeline is built using nomic-embed-code, a 7B-parameter embedding model. We collected the full Prosa repository from the official source and categorized each file into either the documentation or knowledge database. For the documentation database, we further segmented each file into finer sections representing individual definitions, parameters, or function specifications. These units capture essential building blocks—such as abstractions for tasks, jobs, arrival models, and scheduling behavior—that an LLM must reference when constructing a valid Prosa script. Each section was embedded using nomic-embed-code and indexed in a FAISS vector store. In contrast, documents in the knowledge database were embedded as entire files to preserve the logical structure and continuity of complete proofs demonstrating how specific real-time systems are analyzed under given workload models, resource assumptions, and schedulers.

Once the documentation and knowledge databases were prepared, we used informal theorem sketches extracted from research papers as queries. Each sketch was decomposed into its constituent elements—definitions, claims, lemmas, theorems, and corollaries—and we computed cosine similarity between these elements and both databases. For each component, we retrieved the top five relevant segments from the documentation database and the top two documents from the knowledge database. These retrieved contexts were then provided to the LLM to guide the generation of Prosa code. This approach significantly improved the syntactic correctness and functional validity of the generated scripts, enabling us to collect reliable initial training data for fine-tuning the model in later stages.

## Dataset generation:
- LLM inference
- Prosa Compile
- Majority voting

Our next phase to generate prosa script with guidance from the RAG and collect preliminary data to fine-tune an LLM.
After extracting the relevant documents from the RAG database with the informal sketch of a single invariant extracted from the paper, we prompt an LLM to write a prosa script following the informal sketch so that the invariant can be proofed. We use open source LLMs to generate the prosa scripts in this phase. For choosing the LLM we had to consider some things. First of all given the large context due to encorporating the results from the retrieval phase, we had to choose an llm which can handle very large context. Typically the length of our each prompt would range less than 10k. So we had to choose an llm which had a context length of  16k or above. Another thing to consider was the hardware resources. We ran all our experiments in nvidia A6000 ada (48 gb GPU). So the parameter count of the model could not be too large. Another thing was the ability to generate prosa script properly. From our experiments, we see that the performance of open source LLM gpt-oss: 20b from openai is satisfactory in writing prosa script compared to other open source alternatives (qwen-3:14b, deepseek-r1:32b, llama-3.1:8b). So we used gpt-oss: 20b to generate the initial prosa scripts. 

After generation of the script we passed it through prosa compiler to verify if the script has any compilation error. The inclusion of knowledge and documentation from the RAG improved the script generation quality and reduced the possibility of compilation error notably. If there was no compilation error then we performed an LLM-as-Judge phase to validate the script. In this phase we prompted 3 llms to convert the generated script back to the informal sketch. We used few-shot learning for the conversion from prosa script to the informal sketch. Once the LLMs converted the script back to the informal sketch we performed cosine similarity between the actual informal sketch and converted informal sketch. With a threshold we decided if a judge LLM is accepting the generated prosa script or rejecting it. Then we performed majority voting amongh the judge LLMs to finally accept a prosa script.

If a script is accepted then we use it as a context for the next informal sketch as well so that code integrity(Or whatever the proper word for declaration of variables or function signatures) is maintained. We gradually chain together all the generated scripts while generating script for the later informal sketch in the same paper. Also the accepted scripts are stored for further fine-tuning of LLM.

If a generated script had any compilation error or was rejected by the Judge LLMs then we went through a feedback loop to fix the error or regenerate the prosa script. For compilation error, we attached the error message along with the generated script and full generated code till now and fed it back to the LLM and asked it to suggest fixing the error. If the LLM could fix the error in some feedback loops then we included that script in the training data as well. otherwise skipped it and moved on to the next one. 

After completion of all the we collected 765 training samples from the 18 papers selected for training and 283 test samples from the 10 papers selected for testing performance. The training and testing samples had two categories, one was code completion and other was code generation. The code completion part incorporated the scripts from the previous system invariants in the same paper and then the informal sketch attached at last asking the model to complete the code following the informal sketch. The code generation dataset had only an informal sketch for a single system invariant and the llm was asked to generate the complete code with all the required dependency functions and everything so that the informal sketch was proven mechanically.


We further divided the system invariants collected from papers into smaller functional units. We created a dependency graph among the system invariants in a paper (Like lemma 2 depends on lemma 1 and definition 1) and further extracted the informal sketch for these smaller units individually. We kept the smaller functional units seperated for the training papers and testing papers.

## Model training

After completion of the dataset generation phase, we opted to adapt a large language model for prosa script generation and for so we fine-tuned LLM in a supervised way with lora. The goal of this stage was to teach the model to translate informal sketch into prosa script. Each sample of the training corpus contained either an informal sketch paired with a partially completed script (for code-completion tasks) or an informal sketch alone (for full code-generation tasks). 

As the token length of the input training corpus was below 10k, So we trained our model for 16k Context length. To accommodate the 16k-token context window of our dataset, we applied several memory-efficient training strategies. Gradient checkpointing and mixed-precision (bfloat16) training were used to lower memory consumption during backpropagation, enabling stable optimization over long sequences. An 8-bit optimizer minimized the memory footprint of optimizer states, and gradient accumulation allowed us to maintain a consistent effective batch size. Model improvement was monitored through evaluation loss computed on the same long-context input format.

Since the token length of our training samples stayed below 10k, we fine-tuned the model using a 16k context window to ensure enough capacity for longer proofs and chained invariants. To make this feasible, we relied on several memory-aware training techniques. Gradient checkpointing and mixed-precision (bfloat16) training helped reduce memory use during backpropagation, which allowed the model to handle long sequences reliably. We also used an 8-bit optimizer to keep the optimizer state lightweight, and gradient accumulation helped maintain a stable effective batch size. Throughout training, we tracked the model’s progress using the evaluation loss computed under the same long-context setting.

We used the casual language modeling loss (CLM). It is basically a token-wise cross entropy loss between the models next predicted token distribution and the ground truth token. In other words, for each position 𝑡, the model predicts 𝑝𝜃(𝑥𝑡∣𝑥<𝑡), and the loss penalizes the negative log-likelihood of the correct token.
L=−t=1∑T​logpθ​(xt​∣x<t​)

We used the causal language modeling (CLM) loss, which corresponds to a token-level cross-entropy objective between the model’s predicted next-token distribution and the ground-truth token. At each position \(t\), the model predicts \(p_{\theta}(x_t \mid x_{<t})\), and the loss penalizes the negative log-likelihood of the correct token. Formally, the objective is:

\[
\mathcal{L} = -\sum_{t=1}^{T} \log p_{\theta}(x_t \mid x_{<t})
\]


Once the lora fine-tuning was complete we merged the lora weights with the model and converted it gguf format with llama.cpp. this was done to efficiently deploy the fine-tuned model with the help of ollama. 

### Prompt example:
convert this to a equation section in latex without any header or any line number. just show it in an equation block. write everything inside the equation block. don't change a single word. write word by word. add a gray background, add a caption underneath, also this is making lines break. I want to add in a way image is added so that even if I insert it between other lines the other lines won't break and it will be shown at top of column.: 


I want to write a prosa script. use these as your context:

```
context 1: 
  Documentation data 1...

context 2: 
  Documentation data 2...
.
.
.
context 5: 
  Documentation data 5...

```

Here are some relevant examples on writing prosa scripts:

```
example 1: 
  Example data 1...

example 1: 
  Example data 2...


```

Here is the current code along with the comments describing what needs to be accomplished in the script. 

 ```
  Code geenrated for previous invariant 1
  Code geenrated for previous invariant 2
  Code geenrated for previous invariant 3
  .
  .
  .
  Informal sketch for current invariant 
```

Following the comment, complete the Prosa code using the provided context and examples as guidance. Write only the code corresponding to the comment section, and do not include anything additional. The output should be enclosed in a ```coq code block.

# Evaluation
## Experimental Setting
- Gpu
- Model selection due to low gpu memory
  - Context length of the inputs
- What are the models used in script generation
- what are the models used in embedding
- We define our baseline on how the state of the art llms perform 

We performed a series of experimentations to validate our framework and determine the performance improvement over the current state of the art LLMs. As mentioned earlier, to the best of our knowledge this is the first ever work to validate how well LLMs can generate prosa scripts for analyzing real time systems. So our experiment starts off with establishing baseline - how well does different LLMs (GPT-5, Gemini, Gpt-oss) generate prosa scripts and how well are they aqcuinted with the syntax of prosa. Then we moved on to determine how well does our framework work and how much did the whole rag system and training phase improved the performance of our framework. We conducted all the local experiments in relatively lower resource (small dataset and 48gb gpu). So the performance improvement is noteworthy

a. baseline
To establish our baseline we analyzed how the current state of the llms are performing when it comes to generating prosa scripts. To figure out the extent of the capability of llms to generate scripts we collected 212 full informal sketches maintaining their dependency. Here each of the informal sketch file consisted of all the informal sketches of the dependencies along with the informal sketch of the final system invariant. the goal was how the state of the art llms could generate prosa script if they were properly guided throughout the whole script generation phase. we performed the experiments with gpt-5 and gemini-2.5-flash and evaluated their generation capability. we employed pass@1 to see how syntactically correct scripts can the models could generate 

a. training setting:
- We performed all our experiments in one NVIDIA A6000 ada GPU (48 GB Vram) 
- input context length 10k
- model selection (nomic and llama/gptoss)
- Lora fine tune with gradient checkpointing
- 3% warmup ratio
- learning rate 2e-4

We performed our experiments on a single NVIDIA A6000 ada GPU with 48 gb vram. As the gpu resource was limited we had to consider several things like which model to choose and how much of training we can accumulate. As mentioned earlier, through empirical evaluation, we found out that none of the input prompts for generating system invariants crossed the threshold of 10k. So We had to choose a model with at 16k context length capability. Also due to small gpu vram, we could not go for models with billions of parameters. So we stuck to 7b or 8b variants of llms so that we can properly fine-tune them given our resource. We performed lora fine-tuning with rank 16 and lora alpha 32. while training we kept 3% of the steps as warmup steps and a learning rate of 2e-4 was used.

c. evaluation metrics: pass@1
We apply pass@k metric, a popular metric for evaluating LLMs in code generation task.It generates the probability of generating one correct answer from a among k repeated generations from model. The mathematical representation of the metric is as follows: 

**math equation**

where n denotes the number of generated outputs for each test case. we set n as 10 in our experiments and evaluate pass@1 and pass@5 metrics

d. test dataset:
We evaluated our framework with two different sets of data. The first data consisted of only informal sketch of a single system invariant and the task was to generate all the necessary prosa scripts (including different dependencies to proof a single system invariant) and the second one was to complete a prosa script given the previous dependencies and the informal sketch of a single system invariant. in the second task the necessary dependencies were provided for a single invariant and the task of the llm was to generate the necessary prosa script to mechanically proof that system invariant.  There were mainly 5 different variants of system invariants in the datasets and the models were tested on how well they can generate these 5 different types. The categories were definitions, claims, lemmas, theorems and corollaries.

This is what I have now: 
We evaluated our framework using two distinct datasets, each designed to test a different aspect of Prosa script generation:

1. \textit{Full-Generation Dataset:}
   This dataset contained only the informal sketch for a single system invariant. The task was to generate the complete Prosa script from scratch, including all supporting definitions and dependencies required to mechanically prove the invariant.

2. \textit{Code-Completion Dataset:}
   This dataset included the previously generated dependencies along with the informal sketch for the current invariant. Here, the model’s task was to complete the remaining portions of the Prosa script, ensuring that the final output was consistent with the provided context and sufficient to complete the mechanical proof.

I want to include the following: 
```There were mainly 5 different variants of system invariants in the datasets and the models were tested on how well they can generate these 5 different types. The categories were definitions, claims, lemmas, theorems and corollaries.  In the test dataset for generating full code there these samples: {'definition': 94, 'lemma': 24, 'theorem': 44, 'corollary': 1, 'claim': 1} and for the test dataset for completing the scripts there were these many samples: {'definition': 83, 'lemma': 7, 'theorem': 29}```

while including this part Convert this part to a table:
```
 In the test dataset for generating full code there these samples: {'definition': 94, 'lemma': 24, 'theorem': 44, 'corollary': 1, 'claim': 1} and for the test dataset for completing the scripts there were these many samples: {'definition': 83, 'lemma': 7, 'theorem': 29}
``` 

write a full overleaf code


## Experimental results
### Syntactically correct script generation
Our experiments show the effectiveness of our framework in generating prosa script for mechanically prooving different system invariants. As shown in table \ref{tab:id} we can see that the performance comparison of different state of the art Large Language models. We investigated initially how gpt and gemini perform for our test dataset and established the benchmark on how the current llms are performing. We can see the result of the base model deepseek-coder-v2 16b model. We are taking it as the base model and evaluating its performance on generating syntactically correct prosa scrtipts. Then we fine tuned this model with lora on the test dataset and then evaluated the performance again with the dataset. The imrovement of our framework can be seen from the table. 


Our experiments demonstrate the effectiveness of our framework in generating Prosa scripts for mechanically proving different system invariants. As shown in Table~\ref{tab:overall-pass}, we compare the performance of several state-of-the-art large language models. We first examined how GPT and Gemini perform on our test dataset to establish a baseline for current LLM capabilities. We then evaluated the base model, DeepSeek-Coder-V2 16B, and use it as our primary reference point for syntactically correct Prosa script generation. Next, we fine-tuned this model with LoRA on our training dataset and re-evaluated its performance on the test set. The improvement achieved by our framework, relative to both the baseline models and the unfine-tuned DeepSeek-Coder-V2 16B, is clearly reflected in the table.

### Evaluation Across Different Invariant Types
We also conducted an analysis on how well the models can perform when it comes to different types of invariant. We performed invariant wise analysis and checked how many of different types of invariant the llms can generate script for 

# Discussion
1. We used very small llms (8b models) to comprise our final framework. and the imrpovement of performance compared to the gian llms (gpt-5, gemini) is noteworthy
2. first benchmark dataset for validating and training prosa