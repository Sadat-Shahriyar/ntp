from __future__ import annotations

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from rts2prosa.config import LLMConfig


class HFChatModel:
    def __init__(self, cfg: LLMConfig):
        self.cfg = cfg
        self.tokenizer = AutoTokenizer.from_pretrained(
            cfg.model_id, trust_remote_code=cfg.trust_remote_code
        )
        quant = None
        if cfg.load_in_4bit:
            quant = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
                bnb_4bit_compute_dtype=torch.bfloat16,
            )
        self.model = AutoModelForCausalLM.from_pretrained(
            cfg.model_id,
            device_map="auto",
            torch_dtype=torch.bfloat16,
            quantization_config=quant,
            trust_remote_code=cfg.trust_remote_code,
        )
        self.model.eval()

    def generate(self, system_prompt: str, user_prompt: str, max_new_tokens: int | None = None) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        kwargs = dict(tokenize=False, add_generation_prompt=True)
        try:
            rendered = self.tokenizer.apply_chat_template(messages, enable_thinking=False, **kwargs)
        except TypeError:
            rendered = self.tokenizer.apply_chat_template(messages, **kwargs)
        inputs = self.tokenizer(rendered, return_tensors="pt").to(self.model.device)
        input_len = inputs["input_ids"].shape[-1]
        with torch.inference_mode():
            output = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens or self.cfg.max_new_tokens,
                do_sample=False,
                temperature=None,
                top_p=None,
            )
        return self.tokenizer.decode(output[0][input_len:], skip_special_tokens=True).strip()
