# Architecture Overview

## System Components

### Core Files
- **`scraper.py`** — Main scraping logic and orchestration  
- **`transformers.py`** — Data cleaning and numeric reward parsing  
- **`validators.py`** — Data validation and quality checking  
- **`requirements.txt`** — Python dependencies  
- **`docs/ETHICS.md`** — Web scraping ethics and compliance

### Data Flow
1. Raw HTML Extraction  
2. Data Transformation  
3. Data Validation  
4. Clean JSON Output  

---

## Architecture Details

### 1) Raw HTML Extraction (`scraper.py`)
- **Target**: Cointelegraph crypto bonus airdrop page  
- **Method**: HTTP requests using `requests`  
- **Parsing**: `BeautifulSoup4` with CSS selectors  
- **Rate Limiting**: 1-second delay between requests; **exponential backoff on 429/5xx**  
- **Output**: Raw dictionary objects with project/task/reward fields  

### 2) Data Transformation (`transformers.py`)
- **Input**: Raw scraped dictionaries  
- **Functions**:
  - `clean_text()` — Remove extra spaces and normalize whitespace  
  - `extract_reward_amount()` — Parse numeric reward amounts (USD, k, M suffixes, etc.)  
- **Output**: Transformed data with cleaner text and numeric reward field  

### 3) Data Validation (`validators.py`)
- **Input**: Transformed data objects  
- **Functions**:
  - `validate_airdrop()` — Check required fields (`project_name`, `task_title`)  
  - `validate_batch()` — Validate multiple records and return summary  
- **Output**: Boolean validity per record + summary counts  

### 4) Clean JSON Output
- **Format**: Array of standardized JSON objects  
- **Fields**:
  - `project_name` — Clean project identifier  
  - `task_title` — What needs to be done  
  - `reward` — Raw reward text  
  - `reward_amount` — Parsed numeric value (or `null`)  
  - `scraped_at` — Timestamp  
  - (plus optional detail fields: `detail_time_left`, `detail_project_link`, `detail_time_to_complete`, `detail_steps`, `detail_risk`)  

---

## Technical Stack

- **`requests`** — HTTP client for web scraping  
- **`beautifulsoup4`** — HTML parsing and CSS selection  
- **`lxml`** — Fast parser backend  
- **`tqdm`** — Progress bar  

---

## Design Principles

- **Modularity** — Each file has a single responsibility  
- **Pipeline flow** — Scrape → Transform → Validate → Output  
- **Error handling** — Retry with exponential backoff, skip invalid records  
- **Respectful scraping** — Rate limiting + polite delays  
- **Transparency** — Logs validation summary, saves JSON output  

---

## Usage Patterns

```bash
# Install dependencies
pip install -r requirements.txt

# Run scraper (collect up to 10 items by default)
python scraper.py

# View results in /data/sample_output.json
cat data/sample_output.json
