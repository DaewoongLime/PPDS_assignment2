"""
Minimal transformer module.

Provides:
- clean_text: collapses whitespace and trims
- extract_reward_amount: best-effort numeric parsing from reward text
"""

import re
from typing import Optional


def clean_text(text: Optional[str]) -> str:
    """Remove leading/trailing spaces and collapse multiple spaces into one."""
    if not text:
        return ""
    return re.sub(r"\s+", " ", text.strip())


def extract_reward_amount(reward_text: Optional[str]) -> Optional[float]:
    """
    Best-effort parser to extract a numeric reward amount from free text.
    Examples it can handle:
      "$100", "100 USDT", "1,500", "2k", "1.2M", "Up to 50"
    Returns:
      float amount if parsed, else None
    """
    if not reward_text:
        return None

    text = reward_text.upper().replace("$", "")
    # Basic number with optional commas/decimal
    m = re.search(r"(\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+(?:\.\d+)?)", text)
    if not m:
        return None

    try:
        base = float(m.group(1).replace(",", ""))
    except Exception:
        return None

    # Suffix multipliers
    if "M" in text:
        base *= 1_000_000
    elif re.search(r"\bK\b", text):
        base *= 1_000

    return base
