from __future__ import annotations

import hashlib
import re


def normalize_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def normalize_key(text: str) -> str:
    return normalize_ws(text).lower()


def stable_id(prefix: str, *parts: str) -> str:
    payload = "|".join(normalize_key(str(x)) for x in parts)
    digest = hashlib.sha1(payload.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{digest}"


def strip_code_fences(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json|text|coq|rocq)?\s*", "", text, flags=re.I)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()
