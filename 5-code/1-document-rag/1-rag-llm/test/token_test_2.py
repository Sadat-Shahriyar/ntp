import requests
from input_text import input_text as your_huge_input_text

OLLAMA_HOST = "http://localhost:11434"

def count_tokens(text: str, model: str, num_ctx: int, num_predict: int) -> int:
    """
    Ask Ollama to eval the whole prompt using a large num_ctx,
    and return how many tokens the model actually consumed.
    """
    body = {
        "model": model,
        "prompt": text,
        "stream": False,
        "options": {
            "num_predict": num_predict,      # don't generate output
            "num_ctx": num_ctx     # <-- IMPORTANT: allow large prompt
        }
    }

    r = requests.post(f"{OLLAMA_HOST}/api/generate", json=body)
    r.raise_for_status()
    data = r.json()

    return data["prompt_eval_count"]  # tokens from *your* prompt

def fits_in_context(
    text: str,
    model: str,
    num_ctx: int,
    num_predict: int,
    reserved_for_generation: int = 512,
):
    """
    Check if text fits in the chosen context budget.
    """
    prompt_tokens = count_tokens(text, model, num_ctx, num_predict)
    max_prompt_tokens = num_ctx - reserved_for_generation
    return {
        "prompt_tokens": prompt_tokens,
        "context_window": num_ctx,
        "reserved_for_generation": reserved_for_generation,
        "fits": prompt_tokens <= max_prompt_tokens,
        "remaining_for_prompt": max(0, max_prompt_tokens - prompt_tokens),
    }

# ---- usage for YOUR model ----
MODEL_NAME = "llama3.1:70b"
MODEL_CONTEXT = 16384  # from `ollama show`
MODEL_PREDICT = 16384

stats = fits_in_context(
    text=your_huge_input_text,
    model=MODEL_NAME,
    num_ctx=MODEL_CONTEXT,
    num_predict=MODEL_PREDICT,
    reserved_for_generation=512,
)

print(stats)
