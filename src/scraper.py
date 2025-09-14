import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
from tqdm import tqdm
import transformers
import validators

class SimpleCointelegraphScraper:
    """Simplified scraper for Cointelegraph airdrop data."""
    
    def __init__(self):
        self.base_url = "https://cointelegraph.com/crypto-bonus/bonus-category/airdrop/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def scrape_basic_info(self, limit=10):
        """Scrape basic airdrop info from the main page with detail page enhancement"""
        # Retry with exponential backoff for main page
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.session.get(self.base_url)
                response.raise_for_status()
                break
            except requests.RequestException as e:
                wait_time = 2 ** attempt  # 1s, 2s, 4s
                print(f"⚠️  Main page request failed (attempt {attempt + 1}/{max_retries}), waiting {wait_time}s...")
                if attempt < max_retries - 1:
                    time.sleep(wait_time)
                else:
                    print(f"❌ Failed to fetch main page after {max_retries} attempts")
                    return []
        
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all airdrop cards - they might be inside links
            cards = soup.find_all('div', class_='card')[:limit]
            
            # Also try finding link elements that contain cards
            if not cards:
                link_cards = soup.find_all('a')[:limit]
                cards = [link for link in link_cards if link.find('div', class_='card')]
            
            airdrops = []
            for card in tqdm(cards, desc="Scraping airdrops", unit="card"):
                airdrop = self.parse_card_simple(card)
                if airdrop:
                    # Try to get more detailed data from detail page
                    detail_url = self.get_detail_url_from_card(card)
                    if detail_url:
                        detail_data = self.get_detail_data(detail_url)
                        if detail_data:
                            # Add detail page data
                            for key, value in detail_data.items():
                                airdrop[key] = value
                    
                    airdrops.append(airdrop)
            
            return airdrops
            
        except Exception as e:
            print(f"Error scraping: {e}")
            return []
    
    def parse_card_simple(self, card):
        """Parse a single card with just the essentials"""
        try:
            # Project name
            name_elem = card.find(class_='project-name-title')
            project_name = name_elem.get_text(strip=True) if name_elem else 'Unknown'
            
            # Task description
            task_elem = card.find(class_='task-name')
            task_name = task_elem.get_text(strip=True) if task_elem else ''
            
            # Reward
            reward_elem = card.find(class_='reward')
            reward = reward_elem.get_text(strip=True) if reward_elem else ''
            
            return {
                'project_name': project_name,
                'task_name': task_name, 
                'reward': reward,
                'scraped_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error parsing card: {e}")
            return None
    
    def get_detail_url_from_card(self, card):
        """Extract detail page URL from card element"""
        try:
            # Check if the card itself is a link (when we find link elements containing cards)
            if card.name == 'a' and card.get('href'):
                href = card.get('href')
                if href.startswith('/'):
                    return f"https://cointelegraph.com{href}"
                return href
            
            # Look for any links in the card
            links = card.find_all('a')
            for link in links:
                href = link.get('href')
                if href:
                    # Convert relative URL to absolute
                    if href.startswith('/'):
                        return f"https://cointelegraph.com{href}"
                    return href
            
            # Check if card is nested inside a link (parent element)
            parent = card.parent
            while parent and parent.name != 'body':
                if parent.name == 'a' and parent.get('href'):
                    href = parent.get('href')
                    if href.startswith('/'):
                        return f"https://cointelegraph.com{href}"
                    return href
                parent = parent.parent
                
        except Exception as e:
            print(f"Error extracting detail URL: {e}")
        return None
    
    def get_detail_data(self, detail_url):
        """Scrape detail page to get comprehensive data"""
        detail_data = {}
        
        # Retry with exponential backoff
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.session.get(detail_url)
                response.raise_for_status()
                break
            except requests.RequestException as e:
                wait_time = 2 ** attempt  # 1s, 2s, 4s
                print(f"⚠️  Request failed (attempt {attempt + 1}/{max_retries}), waiting {wait_time}s...")
                if attempt < max_retries - 1:
                    time.sleep(wait_time)
                else:
                    print(f"❌ Failed to fetch {detail_url} after {max_retries} attempts")
                    return detail_data
        
        try:
            
            # Add minimal delay and parse the page
            time.sleep(2)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Calculate timer from data-timer attribute (more reliable than JS)
            timer_container = soup.find(class_='single-card-container')
            if timer_container and timer_container.get('data-timer'):
                timestamp = timer_container.get('data-timer')
                try:
                    end_time = int(timestamp)
                    current_time = int(time.time())
                    seconds_remaining = end_time - current_time
                    
                    if seconds_remaining > 0:
                        days = int(seconds_remaining // 86400)
                        hours = int((seconds_remaining % 86400) // 3600) 
                        minutes = int((seconds_remaining % 3600) // 60)
                        
                        detail_data['time_left'] = {
                            'days': str(days),
                            'hours': str(hours), 
                            'minutes': str(minutes)
                        }
                    else:
                        detail_data['time_left'] = {
                            'days': '0',
                            'hours': '0',
                            'minutes': '0'
                        }
                except Exception as e:
                    print(f"Error calculating from timestamp: {e}")
            
            # Project links from social-container
            project_links = []
            social_container = soup.find(class_='social-container')
            if social_container:
                links = social_container.find_all('a')
                for link in links:
                    href = link.get('href')
                    if href:
                        project_links.append(href)
            if project_links:
                detail_data['project_links'] = project_links
            
            # Time to complete and risk level
            task_desc_blocks = soup.find_all(class_='task-description-block')
            for block in task_desc_blocks:
                text = block.get_text()
                
                # Extract time to complete
                if 'Time to complete:' in text:
                    try:
                        lines = text.split('\n')
                        for line in lines:
                            if 'Time to complete:' in line:
                                time_part = line.split('Time to complete:')[1].strip()
                                detail_data['time_to_complete'] = time_part
                                break
                    except:
                        pass
                
                # Extract risk level
                if 'Risk level:' in text:
                    try:
                        lines = text.split('\n')
                        for line in lines:
                            if 'Risk level:' in line:
                                risk_part = line.split('Risk level:')[1].strip()
                                detail_data['risk_level'] = risk_part
                                break
                    except:
                        pass
            
            # Count steps
            step_elements = soup.find_all(class_='step')
            if step_elements:
                detail_data['step_count'] = len(step_elements)
            
            # Extract CTA link from timer button
            timer_btn = soup.find(class_='timer-btn')
            if timer_btn:
                cta_link = timer_btn.find('a')
                if cta_link and cta_link.get('href'):
                    detail_data['cta_link'] = cta_link.get('href')
                    # Also get the CTA text
                    cta_span = cta_link.find('span')
                    if cta_span:
                        detail_data['cta_text'] = cta_span.get_text(strip=True)
            
            # Fallback to timestamp if timer not available
            if 'time_left' not in detail_data:
                timestamp_elem = soup.find('[data-timestamp]')
                if timestamp_elem:
                    timestamp = timestamp_elem.get('data-timestamp')
                    if timestamp:
                        try:
                            end_time = int(timestamp)
                            current_time = int(time.time())
                            seconds_remaining = end_time - current_time
                            days = max(0, int(seconds_remaining / 86400))
                            detail_data['time_left'] = {
                                'days': str(days),
                                'hours': '0',
                                'minutes': '0'
                            }
                        except:
                            detail_data['time_left'] = {
                                'days': '0',
                                'hours': '0',
                                'minutes': '0'
                            }
                        
        except Exception as e:
            print(f"Error getting detail data: {e}")
        
        # Add small delay between requests
        time.sleep(1)
        return detail_data
    
    def save_data(self, data, filename='data/sample_output.json'):
        """Save data to JSON file"""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Saved {len(data)} airdrops to {filename}")

if __name__ == "__main__":
    scraper = SimpleCointelegraphScraper()
    airdrops = scraper.scrape_basic_info(limit=5)
    
    # Transform data first
    transformed_airdrops = transformers.transform_airdrop_data(airdrops)
    
    # Validate transformed data and filter valid ones
    valid_airdrops = validators.filter_valid_airdrops(transformed_airdrops)
    validation_summary = validators.get_validation_summary(transformed_airdrops)
    print(f"✅ {validation_summary}")
    
    # Add simple business calculations  
    # Remove the TRIPLE_CHECK field before business logic
    for airdrop in valid_airdrops:
        if 'TRIPLE_CHECK_TRANSFORMER' in airdrop:
            del airdrop['TRIPLE_CHECK_TRANSFORMER']
        if 'CHECK_10TH_TIME' in airdrop:
            del airdrop['CHECK_10TH_TIME']
    
    for airdrop in valid_airdrops:
        # Priority score (urgent = higher priority)
        if 'time_left' in airdrop:
            days = int(airdrop['time_left'].get('days', 0))
            if days <= 1:
                airdrop['priority'] = 'HIGH'
            elif days <= 7:
                airdrop['priority'] = 'MEDIUM' 
            else:
                airdrop['priority'] = 'LOW'
        
        # Effort vs reward estimate
        steps = airdrop.get('step_count', 0)
        if steps <= 3:
            airdrop['effort'] = 'Easy'
        elif steps <= 6:
            airdrop['effort'] = 'Medium'
        else:
            airdrop['effort'] = 'Hard'
    
    print(f"\nScraped {len(valid_airdrops)} airdrops:")
    print("=" * 50)
    
    for airdrop in valid_airdrops:
        print(f"\n📋 {airdrop['project_name']}")
        print(f"   Task: {airdrop['task_name']}")
        print(f"   Reward: {airdrop['reward']}")
        
        if 'time_left' in airdrop:
            time_left = airdrop['time_left']
            print(f"   ⏰ Time left: {time_left['days']}d {time_left['hours']}h {time_left['minutes']}m")
        
        if 'step_count' in airdrop:
            print(f"   📝 Steps: {airdrop['step_count']}")
            
        if 'risk_level' in airdrop:
            print(f"   ⚠️  Risk: {airdrop['risk_level']}")
            
        if 'time_to_complete' in airdrop:
            print(f"   ⏱️  Duration: {airdrop['time_to_complete']}")
            
        if 'cta_text' in airdrop:
            print(f"   🔗 Action: {airdrop['cta_text']}")
        
        if 'project_links' in airdrop:
            print(f"   🌐 Links: {len(airdrop['project_links'])} social/project links")
            
        if 'priority' in airdrop:
            priority_emoji = {'HIGH': '🔥', 'MEDIUM': '⚡', 'LOW': '🟢'}
            print(f"   {priority_emoji.get(airdrop['priority'], '📊')} Priority: {airdrop['priority']}")
            
        if 'effort' in airdrop:
            print(f"   💪 Effort: {airdrop['effort']}")
    
    print(f"\n📁 Saved data to: data/sample_output.json")
    scraper.save_data(valid_airdrops)