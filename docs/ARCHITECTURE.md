# Architecture Overview

## System Components

### Core Files

- **`src/scraper.py`** - Main scraping logic and orchestration
- **`src/transformers.py`** - Data cleaning and standardization functions
- **`src/validators.py`** - Data validation and quality checking
- **`requirements.txt`** - Python dependencies
- **`docs/ethics.md`** - Web scraping ethics and compliance

### Data Flow

```
1. Raw HTML Extraction

2. Data Transformation

3. Data Validation

4. Clean JSON Output
```

## Architecture Details

### 1. Raw HTML Extraction (`src/scraper.py`)

- **Target**: Cointelegraph crypto bonus airdrop page
- **Method**: HTTP requests using `requests` library
- **Parsing**: BeautifulSoup4 with CSS selectors
- **Rate Limiting**: 1-second delays between requests
- **Output**: Raw dictionary objects with HTML structure

### 2. Data Transformation (`src/transformers.py`)

- **Input**: Raw scraped dictionaries
- **Functions**:
  - `clean_text()` - Remove extra spaces and prefixes
  - `clean_project_name()` - Standardize project names
  - `extract_token_symbol()` - Find token symbols like $AITV
  - `extract_reward_amount()` - Parse USD amounts (returns null if none)
  - `standardize_categories()` - Clean category names
  - `get_action_type()` - Determine required action type
- **Output**: Standardized data objects

### 3. Data Validation (`src/validators.py`)

- **Input**: Transformed data objects
- **Functions**:
  - `validate_airdrop()` - Check individual records
  - `validate_batch()` - Process multiple records
  - `calculate_quality_score()` - Score from 0-100
  - `get_validation_summary()` - Human-readable summary
- **Output**: Validation results and quality metrics

### 4. Clean JSON Output

- **Format**: Array of standardized JSON objects
- **Fields**:
  - `project_name` - Clean project identifier
  - `task_title` - What needs to be done
  - `task_description` - Detailed instructions
  - `categories` - Standardized category tags
  - `reward_token` - Token symbol (if any)
  - `reward_amount` - USD value or null
  - `action_required` - Classification of action type
  - `geographic_scope` - Availability region
  - `labels` - Status indicators (new, hot)
  - `scraped_at` - Timestamp

## Technical Stack

### Dependencies

- **`requests`** - HTTP client for web scraping
- **`beautifulsoup4`** - HTML parsing and CSS selection
- **`lxml`** - Fast XML/HTML parser backend

### Python Features Used

- **Type hints** - Function signatures and return types
- **Regular expressions** - Pattern matching for data extraction
- **JSON serialization** - Standard library for output formatting
- **Error handling** - Try/catch blocks for robust operation

## Design Principles

### Modularity

- **Separation of concerns** - Each file has single responsibility
- **Reusable functions** - Transformers work independently
- **Clean interfaces** - Simple function signatures

### Data Pipeline

- **Sequential processing** - Scrape � Transform � Validate � Output
- **Immutable transformations** - Original data preserved
- **Quality gates** - Validation at each step

### Robustness

- **Error handling** - Graceful failure modes
- **Input validation** - Check data types and formats
- **Rate limiting** - Respect server resources
- **Logging** - Progress and status reporting

### Extension Points

- **Multi-site support** - Add new scraper classes
- **Database storage** - Replace JSON output
- **Parallel processing** - Async requests for speed
- **Configuration** - External settings files

## Usage Patterns

### Development Workflow

```bash
# Install dependencies
pip install -r requirements.txt

# Run scraper
python src/scraper.py

# View results
# JSON output printed to console
```
