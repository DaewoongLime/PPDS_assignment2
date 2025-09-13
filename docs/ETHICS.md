## Purpose

This scraper is designed for **educational and research purposes** to collect publicly available airdrop information from Cointelegraph's crypto bonus section.

---

## Compliance with Cointelegraph Policies

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
- ✅ No modification or misrepresentation of collected content.  

### Data Handling
- Collects **only public airdrop listings**.  
- Does **not** collect personal data (e.g., user accounts, emails).  
- Processing and transformation are done locally.  
- Does not use cookies or track user behavior.  

### Technical Considerations
- Does not bypass access controls or paywalls.  
- Uses only standard HTTP requests.  
- Respects HTTP error codes; stops on failures.  
- Does not abuse caching mechanisms.  

---

## Legal Considerations

### Fair Use
- **Transformative**: Data is cleaned and restructured for analysis.  
- **Limited Scope**: Collects only a small portion of site content (airdrops only).  
- **No Commercial Impact**: Does not compete with or harm Cointelegraph’s business.  
- **Educational Purpose**: Used solely for learning data science and programming skills.  

### Data Protection
- No GDPR issues: only public business information is collected.  
- No sensitive or personally identifiable information.  
- Minimal data collection: only fields necessary for research.  

---
