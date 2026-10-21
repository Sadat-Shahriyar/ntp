import requests
import math
from input_text import input_text as your_huge_input_text

HOST = "http://localhost:11434"

def count_tokens_chunked(text: str, model: str, chunk_chars: int = 8000):
    """
    Split text into smaller character chunks to avoid blowing VRAM.
    We approx token count per chunk using num_ctx ~ 4096, then sum.
    """
    total_tokens = 0
    for i in range(0, len(text), chunk_chars):
        chunk = text[i:i+chunk_chars]

        body = {
            "model": model,
            "prompt": chunk,
            "stream": False,
            "options": {
                "num_predict": 0,
                "num_ctx": 4096,   # keep this modest so VRAM doesn't explode
                # optional: "num_gpu": 0  # see Option 3 below
            },
        }

        r = requests.post(f"{HOST}/api/generate", json=body)
        r.raise_for_status()
        data = r.json()
        total_tokens += data["prompt_eval_count"]

    return total_tokens

big_text = your_huge_input_text  # your huge doc
print(count_tokens_chunked(big_text, "llama3.1:70b"))
