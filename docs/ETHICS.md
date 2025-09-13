## Purpose

This scraper is designed for educational and research purposes to collect publicly available airdrop information from Cointelegraph's crypto bonus section.

## Compliance with Cointelegraph Policies

### Robots.txt Compliance

- ✅ **Allowed Access**: The scraper targets `/crypto-bonus/` which is not explicitly disallowed in robots.txt
- ✅ **Avoided Paths**: We do not access any disallowed paths including:
  - `/api/` endpoints
  - Search queries (`/search?query=*`)
  - Private areas (`/profile`, `/contacts`)
  - AMP pages (`/amp*`)
  - Admin areas (`/wp-admin/`)
  - URLs with tracking parameters (`*_token=`, `*fbclid`, etc.)

### Terms of Service Compliance

- ✅ **ToS**: Scraping data from Cointelegraph does not explicitly violate their Terms of Service
- ✅ **Personal Use**: The scraper is used for personal and school uses for the sake of this project
- ✅ **Attribution**: All content remains property of Cointelegraph as stated in their ToS
- ✅ **No Modification**: We collect data as-is without misrepresentation

### Data Handling

- **Public Data Only**: Only collects publicly visible airdrop listings
- **No Personal Data**: Does not collect user accounts, emails, or personal information
- **Local Processing**: All data transformation happens locally
- **No Tracking**: Does not use cookies or track user behavior

### Technical Considerations - Following the Rules

- **No Circumvention**: Does not bypass any access controls or paywalls
- **Standard HTTP**: Uses only standard HTTP requests, no advanced techniques
- **Error Handling**: Respects HTTP error codes and stops on failures
- **No Caching Abuse**: Does not exploit caching mechanisms

## Legal Considerations

### Fair Use

This scraper operates under fair use principles:

- **Transformative**: Data is cleaned and restructured for analysis
- **Limited Scope**: Small portion of total site content, only airdrops
- **No Commercial Impact**: Does not compete with or harm Cointelegraph's business
- **Educational Purpose**: Used for learning data science and programming skills

### Data Protection

- **No GDPR Issues**: Only collects public business information, not personal data
- **No Sensitive Data**: Avoids any personally identifiable information
- **Minimal Collection**: Only collects necessary fields for research purposes
