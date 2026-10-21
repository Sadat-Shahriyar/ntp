Improving performance on a **very small, highly specialized dataset** (like Prosa formal proofs) requires a **different strategy** than ordinary finetuning.
Below is a complete, practical roadmap tailored to your setup.

---

# ✅ **1. Use the smallest *capable* model**

Training Qwen2.5-Coder-14B on ~200–300 examples is extreme overkill.
The model will:

* overfit instantly
* not generalize
* require careful tuning
* produce unstable behavior

For formal reasoning tasks, **model size does not matter as much as specialization**.

### Recommended base models:

These work *much* better with small datasets:

| Model                          | Size | Why good                                       |
| ------------------------------ | ---- | ---------------------------------------------- |
| **DeepSeek-Coder-V2 Lite 16B** | 16B  | trained on code + reasoning + Coq-like formats |
| **Qwen2.5-Coder-3B**           | 3B   | much easier to finetune, still strong          |
| **Mistral-Nemo-12B**           | 12B  | strong coding model with fewer parameters      |
| **Phi-3.5-mini (3.8B)**        | 4B   | extremely data-efficient                       |

👉 With your dataset size, **3B–7B models outperform 14B models** after finetuning.

---

# ✅ **2. Perform *instruction-only* LoRA finetuning**

Instead of learning the entire Prosa script, the model should learn:

* how to **structure** a Prosa proof
* how to **follow your Coq/Prosa conventions**
* how to **translate informal sketches → script**

Do **NOT** force training on full long scripts unless necessary.
Instead, break the script into **atomic operations**, or train it on:

* lemma patterns
* structure patterns (e.g., `apply`, `intros`, `reflexivity`, case analysis)
* proof skeletons

The model can then *compose* them at inference time.

---

# ✅ **3. Use RAG (Retrieval-Augmented Generation) — extremely effective**

Your task is *domain-coded*, *syntax heavy*, and *documentation dependent*.
LLMs do NOT memorize formal library structures well.

**RAG helps far more than finetuning**.

During inference, attach:

* library definitions
* similar proofs
* templates
* lemma signatures

This increases correctness dramatically.

Even a small model (3B) becomes strong with RAG.

If you'd like, I can help you build the exact RAG pipeline.

---

# ✅ **4. Add synthetic data (MOST IMPORTANT)**

Your dataset is likely **< 1k** training examples.
You can generate **20× more data** using GPT-4/DeepSeek-V3:

### Example:

1. Provide an informal sketch
2. Ask GPT-4 to produce:

   * 3–5 alternative valid Prosa scripts
   * 3–5 diverse rephrasings of the informal sketch
   * 3–5 variants with different proof structures

Suddenly:

* 200 examples → 4000 examples (“weak supervised augmentation”)
* the small model can learn patterns
* overfitting reduces dramatically
* accuracy increases 2–10×

I can help you automate synthetic data generation.

---

# ✅ **5. Use smaller LoRA ranks + dropout**

### Best settings for small datasets:

```
r = 4
lora_dropout = 0.05
learning_rate = 5e-5
max_steps = 20–30
weight_decay = 0.03
warmup_ratio = 0.1
```

These force the model to generalize rather than memorize.

---

# ✅ **6. Curriculum learning**

Train in phases:

### Phase 1: Proof skeleton dataset

Example:

```
(* Informal Sketch *)
Show that arrival times are monotonically increasing.

(* Skeleton *)
intros.
unfold arrival.
...
Qed.
```

Teaches structure.

### Phase 2: Full proofs

Once the model understands skeletons, it handles long sequences better.

---

# ✅ **7. Train with shorter truncated examples**

Long sequences (like full Prosa scripts) cause:

* more noise
* more memorization
* harder gradient updates

Instead:

Create smaller training examples like:

```
(* Goal *)
forall t, valid_arrival t.

(* Solution *)
intros. unfold valid_arrival. ...
```

This improves learning.

---

# ✅ **8. Loss weighting on syntax tokens**

Prosa is extremely syntax-sensitive.
You can weight loss more heavily on:

* parentheses
* Coq keywords (`intros`, `apply`, `simpl`, `Qed`)
* punctuation (`.`, `:=`, `->`)

Better syntax → fewer Coqc failures.

---

# ✅ **9. Evaluate with "Prosa compile" loop**

Instead of evaluating on token loss, evaluate on:

### *Did the generated script compile?*

* synthetic correctness score
* syntactic correctness
* Coq compile result

This is more meaningful.

---

# ✅ **10. Use a syntax-enforcing decoder (constrained decoding)**

You can restrict the decoder to:

* produce only valid Coq tokens
* avoid forbidden symbol sequences
* force matching parentheses

There are libraries for constrained decoding.

This dramatically reduces syntax errors.

---

# 🚀 Final Recommended Pipeline for Tiny Prosa Dataset

### **Stage 1 — Data expansion**

Generate 10–50× more synthetic informal sketch ↔ script pairs
(rephrases + structure variants).

### **Stage 2 — Switch to smaller model**

Qwen2.5-Coder-3B or DS-Coder-V2-Lite.

### **Stage 3 — LoRA Finetuning**

With:

* r = 4
* dropout = 0.05
* LR = 5e-5
* steps = 20–30
* shuffle dataset

### **Stage 4 — RAG + Prosa library retrieval**

Attach relevant library code during inference.

### **Stage 5 — Syntax-constrained decoding**

Reduce Coq syntax errors.

---

# 🎁 If you want, I can help you with any of these:

✓ script to auto-generate synthetic examples using an LLM
✓ code to convert your Prosa library into a vector store (for RAG)
✓ constrained decoding setup for Coq syntax
✓ dataset format with multiple variants per prompt
✓ validation script that runs `coqc` and returns pass/fail
✓ optimal hyperparameters for your exact GPU setup

Tell me which direction you want to go and I’ll build it.
