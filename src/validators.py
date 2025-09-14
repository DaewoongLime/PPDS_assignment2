"""
Simple validators for airdrop data.

This module validates transformed airdrop records and produces:
- Per-record validity (errors/warnings)
- A numeric quality score (0–100)
- Batch-level summary helpers
"""

from typing import Dict, List, Any


# ---------- Primitive field checks ----------

def is_valid_project_name(name: str) -> bool:
    """Project name must be non-empty and not a placeholder."""
    return bool(name and name.strip() and name != "unknown_project")


def is_valid_url(url: str) -> bool:
    """A very loose URL check: must start with 'http'."""
    return bool(url and url.startswith('http'))


def is_valid_reward_amount(amount) -> bool:
    """Reward amount (if present) must be a positive number."""
    return amount is not None and amount > 0


def has_required_fields(airdrop: Dict[str, Any]) -> bool:
    """
    Minimum schema requirements for a valid record.
    We standardized on 'project_name' + 'task_name' as required fields.
    """
    required_fields = ['project_name', 'task_name']
    return all(field in airdrop and airdrop[field] for field in required_fields)


# ---------- Record-level validation ----------

def validate_airdrop(airdrop: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate a single airdrop record and return a dict with:
      - valid: bool
      - errors: List[str]
      - warnings: List[str]
      - score: int (0–100)
    """
    errors: List[str] = []
    warnings: List[str] = []

    # 1) Required fields
    if not has_required_fields(airdrop):
        errors.append("Missing required fields: project_name or task_name")

    # 2) Project name sanity
    if not is_valid_project_name(airdrop.get('project_name', '')):
        warnings.append("Invalid or missing project name")

    # 3) Image URL is optional; warn if missing/invalid
    if not is_valid_url(airdrop.get('image_url', '')):
        warnings.append("Invalid or missing image URL")

    # 4) Reward amount is optional; if present, must be positive
    reward_amount = airdrop.get('reward_amount')
    if reward_amount is not None and not is_valid_reward_amount(reward_amount):
        warnings.append("Invalid reward amount")

    # 5) Categories (optional); encourage having more specific categories
    categories = airdrop.get('categories', [])
    if not categories or categories == ['general']:
        warnings.append("No specific categories found")

    # 6) Action type (optional); 'other' is too vague
    action = airdrop.get('action_required', '')
    if action == 'other':
        warnings.append("Could not determine required action")

    # (Optional) You can warn if step_count is missing.
    # This is purely informational and not an error.
    # if not airdrop.get('step_count'):
    #     warnings.append("No step_count info found")

    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'score': calculate_quality_score(airdrop, errors, warnings),
    }


# ---------- Scoring ----------

def calculate_quality_score(airdrop: Dict[str, Any], errors: List[str], warnings: List[str]) -> int:
    """
    Compute a simple quality score based on:
      - Penalties for errors/warnings
      - Bonuses for helpful fields
    """
    score = 100

    # Penalties
    score -= len(errors) * 30
    score -= len(warnings) * 10

    # Bonuses for good signals
    if is_valid_project_name(airdrop.get('project_name', '')):
        score += 5

    if is_valid_url(airdrop.get('image_url', '')):
        score += 5

    if airdrop.get('reward_token'):
        score += 10

    if airdrop.get('reward_amount') is not None and airdrop.get('reward_amount') > 0:
        score += 10

    if len(airdrop.get('categories', [])) > 1:
        score += 5

    if airdrop.get('action_required') != 'other':
        score += 5

    # Bonus points for richer detail
    if airdrop.get('time_to_complete'):
        score += 5

    if airdrop.get('project_links') and len(airdrop.get('project_links', [])) > 0:
        score += 5

    # IMPORTANT: use 'step_count' (matches scraper output), not 'steps'
    if airdrop.get('step_count') and airdrop.get('step_count', 0) > 0:
        score += 10

    if airdrop.get('project_description'):
        score += 5

    # Final clamp
    return max(0, min(100, score))


# ---------- Batch helpers ----------

def validate_batch(airdrop_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validate a list of airdrops and return aggregate statistics + per-record results.
    """
    results: List[Dict[str, Any]] = []
    valid_count = 0
    total_errors = 0
    total_warnings = 0

    for airdrop in airdrop_list:
        validation = validate_airdrop(airdrop)
        results.append(validation)

        if validation['valid']:
            valid_count += 1

        total_errors += len(validation['errors'])
        total_warnings += len(validation['warnings'])

    return {
        'total_records': len(airdrop_list),
        'valid_records': valid_count,
        'invalid_records': len(airdrop_list) - valid_count,
        'total_errors': total_errors,
        'total_warnings': total_warnings,
        'validation_results': results,
        'overall_quality_score': (
            sum(r['score'] for r in results) / len(results) if results else 0
        ),
    }


def filter_valid_airdrops(airdrop_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return only records that pass validation (no errors)."""
    valid_airdrops: List[Dict[str, Any]] = []

    for airdrop in airdrop_list:
        validation = validate_airdrop(airdrop)
        if validation['valid']:
            valid_airdrops.append(airdrop)

    return valid_airdrops


def get_validation_summary(airdrop_list: List[Dict[str, Any]]) -> str:
    """Return a short human-readable summary for console logs."""
    batch = validate_batch(airdrop_list)

    return f"""
Validation Summary:
- Total records: {batch['total_records']}
- Valid records: {batch['valid_records']}
- Invalid records: {batch['invalid_records']}
- Total errors: {batch['total_errors']}
- Total warnings: {batch['total_warnings']}
- Overall quality score: {batch['overall_quality_score']:.1f}/100
""".strip()
