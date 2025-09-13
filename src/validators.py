"""
Minimal validator module.

- validate_airdrop: checks required fields only (project_name, task_title)
- validate_batch: tiny helper that returns a summary + per-item results
"""

from typing import Dict, Any, List, Tuple


def validate_airdrop(airdrop: Dict[str, Any]) -> Dict[str, Any]:
    """Check if essential keys exist and are non-empty."""
    required = ["project_name", "task_title"]
    missing = [k for k in required if not airdrop.get(k)]
    return {
        "valid": len(missing) == 0,
        "errors": missing,  # e.g., ["project_name"]
    }


def validate_batch(items: List[Dict[str, Any]]) -> Tuple[Dict[str, int], List[Dict[str, Any]]]:
    """Return (summary_dict, per_item_results)."""
    results = [validate_airdrop(i) for i in items]
    summary = {
        "total": len(items),
        "valid": sum(1 for r in results if r["valid"]),
        "invalid": sum(1 for r in results if not r["valid"]),
    }
    return summary, results
