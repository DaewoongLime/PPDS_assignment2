# AI Usage Documentation

## 1. Prompts Used

Below is the full list of prompts that were used with AI tools during the development of this project:

- "Please make a python scraper to collect the raw data from the site and then we'll parse it"
- "Here is the raw HTML, parse it so that we can have clean returns. no longer return as a file, return an array of json objects"
- "Ok let's break it down into the relevant files of transformers.py and validators.py, please provide notes where needed"
- "Clean up the requirements and gitignore"
- "Fill out the architecture with main bullets, very simply and easy to follow but robust"
- "Let's have the scraper go one level deeper to the individual offering pages themselves to get the second level data"
- "Let's also set max response to 10 items"
- "Let's install the progress bar library for py and update the requirements with such"
- "https://cointelegraph.com/crypto-bonus/bonus-page/engage-with-aitv-agents-to-earn-the-aitv-airdrop/"
- "Ok now let's get the time left from this"
- "the project links"
- "time to complete"
- "the number of steps"
- "risk"
- "these are 1 page in so get these"
- "keep in mind the time is JS so we need to delay"
- "can we update it to save ot sample_output.json instead in the data folder of
  console it"
- "We already have our scraper, right?"
- "Ok the code works. Explain how to use the validator and transformer as well."
- "ok let's go to respectful scraping now and implement exponential backoff and retry
  limits very simply

---

## 2. AI-Generated vs Human-Written Code

- **AI-Generated (initial drafts):**

  - Skeleton of `scraper.py` (requests + BeautifulSoup loop, retry/backoff pattern)
  - Transformer skeleton, `clean_text()` and `extract_reward_amount()` in `transformers.py`
  - Validator skeleton (`validate_airdrop`, `validate_batch`) in `validators.py`
  - `requirements.txt` and initial `README` template
  - Almost all the code was written with AI using either ChatGPT or Claude Code

- **Human-Written or Heavily Edited:**
  - Validation refinements and alignment with project schema
  - Business_case, ethics, and architecture documentation
  - Final `README.md`, `AI_USAGE.md`, and `ETHICS.md`
  - Again, each file was read through and refined. Adjustments made where needed.
  - A lot of the ethics and other files were human written as well.

---

## 3. Bugs Found in AI Suggestions & Fixes

- **Bug:** AI suggested `from transformers import clean_text` which conflicted with the HuggingFace library `transformers`.

  - **Fix:** Renamed to local module `transformers.py` in repo.

- **Bug:** AI output initially saved directly to file objects; repo requirement was to export JSON array.

  - **Fix:** Updated to collect dicts in list, then `json.dump` at once.

- **Bug:** Progress bar dependency was omitted from requirements.

  - **Fix:** Added `tqdm` to `requirements.txt`.

- **Bug:** AI didn’t implement robots.txt check or ethics notes.

  - **Fix:** ETHICS.md written manually, scraper constrained to public bonus pages only.

---

## 4. Performance & Productivity Notes

- **Development speed:** Initial AI-generated code got us to a working prototype; manually writing would have taken several hours.
- **Bug fixing time:** AI suggestions introduced 3–4 bugs which required ~1 hour of human debugging.
- **Runtime performance:**
  - ~10 pages scraped in <30s (including politeness delay).
  - Error rate low (<5%) due to retry/backoff.
- **Overall impact:** LLM assistance accelerated prototyping significantly, but human intervention was essential for correctness, ethical compliance, and alignment with project requirements.
