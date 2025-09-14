"""
Simple data transformers for cleaning scraped airdrop data.
"""

import re
from datetime import datetime
from typing import Dict, List, Any


def clean_text(text: str) -> str:
    """Clean text by removing extra spaces and common prefixes."""
    if not text:
        return ""
    
    # Remove extra whitespace
    cleaned = re.sub(r'\s+', ' ', text.strip())
    
    # Remove common prefixes like "Get", "Earn", etc.
    cleaned = re.sub(r'^(Get|Earn|Claim|Join)\s+', '', cleaned, flags=re.IGNORECASE)
    
    return cleaned


def clean_project_name(name: str) -> str:
    """Clean project names."""
    if not name:
        return "unknown_project"
    
    return re.sub(r'\s+', ' ', name.strip())


def extract_token_symbol(reward_text: str) -> str:
    """Extract token symbol like $AITV from reward text."""
    if not reward_text:
        return ""
    
    match = re.search(r'\$([A-Z]{2,10})', reward_text)
    return match.group(1) if match else ""


def extract_reward_amount(reward_text: str):
    """Extract USD amount from reward text. Returns None if not found."""
    if not reward_text:
        return None
    
    # Look for patterns like "120 USDT", "$1M", etc.
    match = re.search(r'(\d+(?:,\d{3})*(?:\.\d+)?)', reward_text.replace('$', ''))
    
    if not match:
        return None
    
    try:
        amount = float(match.group(1).replace(',', ''))
        
        # Handle suffixes
        if 'M' in reward_text.upper():
            amount *= 1000000
        elif 'K' in reward_text.upper():
            amount *= 1000
            
        return amount
    except:
        return None


def standardize_categories(categories: List[str]) -> List[str]:
    """Standardize category names."""
    if not categories:
        return ['general']
    
    # Simple category mapping
    mapping = {
        'sign up bonus': 'signup_bonus',
        'trade bonus': 'trading_bonus',
        'yield farming': 'yield_farming',
        'retro drop': 'retroactive_drop'
    }
    
    result = []
    for cat in categories:
        if isinstance(cat, str):
            clean_cat = cat.lower().strip()
            standardized = mapping.get(clean_cat, clean_cat)
            if standardized not in result:
                result.append(standardized)
    
    return result if result else ['general']


def parse_days_remaining(time_display: str) -> int:
    """Extract number of days from time display text like '5 Days' or '2 hours'."""
    if not time_display:
        return 0
    
    # Look for patterns like "5 Days", "10 days", etc.
    day_match = re.search(r'(\d+)\s*days?', time_display, re.IGNORECASE)
    if day_match:
        return int(day_match.group(1))
    
    # If only hours are shown, assume 0 days
    hour_match = re.search(r'(\d+)\s*hours?', time_display, re.IGNORECASE)
    if hour_match:
        return 0
    
    # If only minutes are shown, assume 0 days  
    minute_match = re.search(r'(\d+)\s*minutes?', time_display, re.IGNORECASE)
    if minute_match:
        return 0
    
    return 0


def get_action_type(task_description: str, task_name: str) -> str:
    """Determine what action is required for the airdrop."""
    text = (task_description + ' ' + task_name).lower()
    
    if any(word in text for word in ['deposit', 'stake']):
        return 'deposit_stake'
    elif any(word in text for word in ['trade', 'swap']):
        return 'trading'  
    elif any(word in text for word in ['sign up', 'register']):
        return 'registration'
    elif any(word in text for word in ['refer', 'invite']):
        return 'referral'
    elif any(word in text for word in ['connect', 'link']):
        return 'connect_account'
    elif any(word in text for word in ['play', 'game', 'click']):
        return 'gaming'
    elif any(word in text for word in ['post', 'tweet', 'social']):
        return 'social_media'
    else:
        return 'other'


class AirdropDataTransformer:
    """Simple transformer for airdrop data."""
    
    def transform_airdrop(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform raw airdrop data to clean format."""
        # Start with all original data
        transformed = raw_data.copy()
        
        # Clean specific fields
        if 'project_name' in transformed:
            transformed['project_name'] = clean_project_name(transformed['project_name'])
        if 'task_name' in transformed:
            transformed['task_name'] = clean_text(transformed['task_name'])
        
        # TRIPLE CHECK: Add a unique field that proves we're using our transformer
        transformed['TRIPLE_CHECK_TRANSFORMER'] = 'LOCAL_FILE_USED'
        transformed['CHECK_10TH_TIME'] = 'YES_LOCAL_TRANSFORMERS_PY'
        
        # Remove labels field if it exists
        if 'labels' in transformed:
            del transformed['labels']
        
        return transformed
    
    def transform_batch(self, raw_data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transform multiple airdrop records."""
        return [self.transform_airdrop(item) for item in raw_data_list]


def transform_airdrop_data(raw_data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Simple function to transform a list of raw airdrop data."""
    transformer = AirdropDataTransformer()
    return transformer.transform_batch(raw_data_list)