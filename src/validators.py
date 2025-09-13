"""
Simple validators for airdrop data.
"""

from typing import Dict, List, Any


def is_valid_project_name(name: str) -> bool:
    """Check if project name is valid."""
    return bool(name and name.strip() and name != "unknown_project")


def is_valid_url(url: str) -> bool:
    """Check if URL looks valid."""
    return bool(url and url.startswith('http'))


def is_valid_reward_amount(amount) -> bool:
    """Check if reward amount is valid."""
    return amount is not None and amount > 0


def has_required_fields(airdrop: Dict[str, Any]) -> bool:
    """Check if airdrop has minimum required fields."""
    required_fields = ['project_name', 'task_title']
    return all(field in airdrop and airdrop[field] for field in required_fields)


def validate_airdrop(airdrop: Dict[str, Any]) -> Dict[str, Any]:
    """Validate a single airdrop record and return validation results."""
    errors = []
    warnings = []
    
    # Check required fields
    if not has_required_fields(airdrop):
        errors.append("Missing required fields: project_name or task_title")
    
    # Check project name
    if not is_valid_project_name(airdrop.get('project_name', '')):
        warnings.append("Invalid or missing project name")
    
    # Check image URL
    if not is_valid_url(airdrop.get('image_url', '')):
        warnings.append("Invalid or missing image URL")
    
    # Check reward amount
    reward_amount = airdrop.get('reward_amount')
    if reward_amount is not None and not is_valid_reward_amount(reward_amount):
        warnings.append("Invalid reward amount")
    
    # Check categories
    categories = airdrop.get('categories', [])
    if not categories or categories == ['general']:
        warnings.append("No specific categories found")
    
    # Check action type
    action = airdrop.get('action_required', '')
    if action == 'other':
        warnings.append("Could not determine required action")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'score': calculate_quality_score(airdrop, errors, warnings)
    }


def calculate_quality_score(airdrop: Dict[str, Any], errors: List[str], warnings: List[str]) -> int:
    """Calculate data quality score from 0-100."""
    score = 100
    
    # Subtract for errors and warnings
    score -= len(errors) * 30
    score -= len(warnings) * 10
    
    # Add points for having good data
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
    
    # Bonus points for detailed information
    if airdrop.get('time_to_complete'):
        score += 5
        
    if airdrop.get('project_links') and len(airdrop.get('project_links', [])) > 0:
        score += 5
        
    if airdrop.get('steps') and len(airdrop.get('steps', [])) > 0:
        score += 10
        
    if airdrop.get('project_description'):
        score += 5
    
    return max(0, min(100, score))


def validate_batch(airdrop_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Validate a batch of airdrop records."""
    results = []
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
        'overall_quality_score': sum(r['score'] for r in results) / len(results) if results else 0
    }


def filter_valid_airdrops(airdrop_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return only valid airdrop records."""
    valid_airdrops = []
    
    for airdrop in airdrop_list:
        validation = validate_airdrop(airdrop)
        if validation['valid']:
            valid_airdrops.append(airdrop)
    
    return valid_airdrops


def get_validation_summary(airdrop_list: List[Dict[str, Any]]) -> str:
    """Get a simple text summary of validation results."""
    batch_validation = validate_batch(airdrop_list)
    
    return f"""
Validation Summary:
- Total records: {batch_validation['total_records']}
- Valid records: {batch_validation['valid_records']}
- Invalid records: {batch_validation['invalid_records']}
- Total errors: {batch_validation['total_errors']}
- Total warnings: {batch_validation['total_warnings']}
- Overall quality score: {batch_validation['overall_quality_score']:.1f}/100
""".strip()