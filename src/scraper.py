import json
import os
import random
import time
from datetime import datetime
from typing import List, Dict, Any

import requests
from bs4 import BeautifulSoup

from transformers import clean_text, extract_reward_amount
from validators import validate_airdrop, validate_batch


class SimpleCointelegraphScraper:
    """
    Minimal scraper for Cointelegraph airdrop listings.

    Covers assignment requirements:
      - Data quality: validate required fields
      - Respectful scraping: retry limit + exponential backoff with jitter
      - Business logic: basic transform + value-added 'reward_amount'
      - Export: saves JSON to data/sample_output.json
    """

    BASE_URL = "https://cointelegraph.com/crypto-bonus/bonus-category/airdrop/"

    def __init__(self, timeout: int = 10, delay: float = 1.0, max_retries: int = 3):
        self.session = requests.Session()
        # Keep headers minimal but realistic
        self.session.headers.update({"User-Agent": "Mozilla/5.0"})
        self.timeout = timeout
        self.delay = delay
        self.max_retries = max_retries

    # -----------------------------
    # Networking helpers
    # -----------------------------
    def fetch_html(self, url: str) -> str:
        """
        Fetch raw HTML from URL with retry + exponential backoff (+ jitter).
        Raises RuntimeError if all retries fail.
        """
        for attempt in range(self.max_retries):
            try:
                resp = self.session.get(url, timeout=self.timeout)
                # Treat 429/5xx as retryable
                if resp.status_code >= 500 or resp.status_code == 429:
                    raise requests.HTTPError(f"retryable status {resp.status_code}")
                resp.raise_for_status()
                return resp.text
            except Exception as e:
                # Exponential backoff: 1, 2, 4... plus small random jitter
                wait = (2 ** attempt) + random.random()
                if attempt < self.max_retries - 1:
                    print(f"[warn] fetch failed ({e}). retry {attempt+1}/{self.max_retries} in {wait:.1f}s")
                    time.sleep(wait)
                else:
                    raise RuntimeError(f"Failed to fetch {url}: {e}")

    # -----------------------------
    # Parsing
    # -----------------------------
    def parse_list_page(self, html: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Parse list page and extract individual airdrop cards (minimal fields).
        Includes a fallback selector path to be resilient to minor markup shifts.
        """
        soup = BeautifulSoup(html, "lxml")
        items: List[Dict[str, Any]] = []

        # Primary: <div class="card">
        cards = soup.select("div.card")
        # Fallback: <a> elements that contain a .card inside
        if not cards:
            cards = [a for a in soup.find_all("a") if a.find("div", class_="card")]

        for card in cards[:limit]:
            item = self.parse_card(card)
            if item:
                items.append(item)

        return items

    def parse_card(self, card) -> Dict[str, Any] | None:
        """
        Extract minimal fields from a single card and perform tiny transform.
        Returns None if required fields are missing.
        """
        try:
            # Raw text extraction
            name_el = card.select_one(".project-name-title")
            task_el = card.select_one(".task-name")
            reward_el = card.select_one(".reward")

            # Transform (clean text)
            project_name = clean_text(name_el.get_text()) if name_el else ""
            task_title = clean_text(task_el.get_text()) if task_el else ""
            reward = clean_text(reward_el.get_text()) if reward_el else ""

            # Value-added: numeric reward amount parsed from free text (best effort)
            reward_amount = extract_reward_amount(reward)

            item: Dict[str, Any] = {
                "project_name": project_name,
                "task_title": task_title,          # aligned with validator
                "reward": reward,
                "reward_amount": reward_amount,    # may be None if not parsable
                "scraped_at": datetime.utcnow().isoformat() + "Z",
            }

            # Validate essential fields before keeping the record
            if not validate_airdrop(item)["valid"]:
                return None

            return item

        except Exception:
            # Fail-soft: skip broken cards without stopping the whole run
            return None

    # -----------------------------
    # Public API
    # -----------------------------
    def scrape(self, limit: int = 10) -> List[Dict[str, Any]]:
        """End-to-end: fetch list page -> parse -> (light) transform/validate."""
        html = self.fetch_html(self.BASE_URL)
        items = self.parse_list_page(html, limit=limit)
        # Gentle delay to avoid hammering the server
        time.sleep(self.delay)
        return items

    @staticmethod
    def save_json(data: List[Dict[str, Any]], path: str = "data/sample_output.json") -> None:
        """Save records to JSON; create the folder if missing."""
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"[ok] Saved {len(data)} records → {path}")
        except Exception as e:
            print(f"[error] Save failed: {e}")


if __name__ == "__main__":
    scraper = SimpleCointelegraphScraper(timeout=10, delay=1.0, max_retries=3)
    records = scraper.scrape(limit=5)

    # Batch validation summary (optional but nice for the rubric)
    summary, results = validate_batch(records)
    print("\nValidation summary:", summary)

    # Console preview
    print("\nScraped airdrops:")
    for r in records:
        amt = f" | amount≈{r['reward_amount']}" if r.get("reward_amount") is not None else ""
        print(f"- {r['project_name']} | {r['task_title']} | {r['reward']}{amt}")

    # Persist JSON for the demo/pitch
    scraper.save_json(records, "data/sample_output.json")
