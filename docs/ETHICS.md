## Purpose

This scraper is designed for **educational and research purposes** to collect publicly available airdrop information from Cointelegraph's crypto bonus section.

---

## Ethical & Legal Analysis:

### Robots.txt Compliance

- ✅ Allowed Access: Targets `/crypto-bonus/`, not disallowed in robots.txt.
- ✅ Avoided Paths: Does not access disallowed areas such as:
  - `/api/` endpoints
  - Search queries (`/search?query=*`)
  - Private areas (`/profile`, `/contacts`)
  - AMP pages (`/amp*`)
  - Admin areas (`/wp-admin/`)
  - URLs with tracking parameters (`*_token=`, `*fbclid`, etc.)

### Terms of Service Compliance

- ✅ Scraping data does not explicitly violate Cointelegraph’s Terms of Service.
- ✅ Used only for **personal and academic purposes**.
- ✅ Attribution: All content remains property of Cointelegraph.
- ✅ No misrepresentation of collected content.

### Ethical Framework

Based off of the above analysis and our review, we feel that this project is in line with the ethics outlined in the assignment. In the README.md we also added extra information about how we took ethics seriously. Our scraper will only take the first 30 of the results and only scrape the first 5 of the sub pages. Again, this is easy to increase on a technical level, but this was a choice of ours to remain ethical. Based on all this, we feel we've considered the ethics and came to a strong conclusion.

### Permission

We received the permission of Professor Grewell to do this project.

# Privacy considerations for scraped data

- Collects **only public airdrop listings**.
- Does **not** collect personal data (e.g., user accounts, emails).
- Processing and transformation are done locally.
- Does not use cookies or track user behavior.

There's really not many areas where we're dealing with sensitive data, so we should largely be in the clear in regards to this.

# Alternative approaches considered

We could try doing crowd sourcing for some of the airdrops and using an upvote system. The one issue with this is that oftentimes in crypto people use upvotes as a method of providing false security for scam projects so this actually might be a potential downside and lead to more scams where bad actors can promote. It's better to scrape from pre-vetted lits. This is likely one of the best methods. Another option might be introducing an elo system for the people that contribute to a potential list, but again there are situations where someone might exit scam.

# Legal analysis with specific law citations

### Technical Considerations

- Does not bypass access controls or paywalls.
- Uses only standard HTTP requests.
- Respects HTTP error codes; stops on failures.
- Does not abuse caching mechanisms.

### Fair Use (U.S.)

- **17 U.S.C. §107**: Transformative, educational use; small subset of content only.
- _Authors Guild v. Google (2015)_ supports scraping for analysis when outputs are transformative.

### CFAA (U.S.)

- **18 U.S.C. §1030**: Bars unauthorized access.
- _hiQ Labs v. LinkedIn (2022)_ confirms scraping **public pages** is not a CFAA violation.

### GDPR (EU)

- **Regulation (EU) 2016/679**: Applies to personal data of natural persons.
- Recital 14 excludes legal/business data → our scraping avoids PII.

### CCPA (California)

- **Cal. Civ. Code §1798.100 et seq.**: Protects personal/household data.
- No personal data collected → not applicable.

### Robots.txt & ToS

- Robots.txt is advisory, not law.
- We respect site load with backoff/retry limits.
- _eBay v. Bidder’s Edge (2000)_ shows issues arise only with abusive scraping.

# Impact on website operations

With this minimal amount of scraping and the ethics we've put in place it is extremely unlikely this would have any actual impact on Cointelegraph's servers since they get over 7 million visitors per month.
