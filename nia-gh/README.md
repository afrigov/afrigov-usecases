# afrigov use case: nia.gov.gh rebuilt

An unofficial rebuild of the website of Ghana's National Identification Authority, the agency that issues the Ghana Card, on [afrigov](https://github.com/afrigov/afrigov). It exists to find out what breaks when the components meet a service site, and to show the same site built accessibly next to the real one's audit score.

It is not the authority's website and says so on every page.

## Why this site

The first use case, fmcide.gov.ng, is a ministry: news, initiatives and documents. This one is a service agency. People come to it to do something: get a card, replace one, change their details, find an office, check a fee. The real home page has 252 links and is about eight screens tall. The rebuild's home page leads with six tasks.

It is also a different country and a different look. It uses the Ghana pack with the flag stripe under the header, a header in the primary colour, full-width bands including one in Ghana's gold, and a light footer, where the first use case has a white header, an image hero and a dark footer.

## Baseline

Scores from [afrigov-audit](https://github.com/afrigov/afrigov-audit) 0.2.0 on 2 October 2026. The full results are in `baseline/`.

| Real page | Score | Biggest problems |
| --- | ---: | --- |
| Home | 38.5, F | 23 texts with low contrast, 20 controls too small to tap on a phone, 14 links with no name, no skip link |
| Card replacement | 68.5, C | Low contrast, links with no name, no skip link |
| Fees and charges | 65.5, C | Low contrast, links with no name, no skip link |

Every rebuilt page scores 100, A, on afrigov 0.9.0 from the CDN.

## Rules

- **Install like an agency would.** Two link tags from the CDN, the Ghana pack, the optional script. No build step beyond the page generator.
- **Structure and facts are the real site's.** Fees, steps, requirements, names and phone numbers were taken from nia.gov.gh on 2 October 2026. The wording is condensed and rewritten. Nothing is quoted at length.
- **No images from the site.** No photographs, no logo, no picture of a real Ghana Card. The header carries a generic mark, a grey frame stands where a portrait would go, and the card on the home page is a simplified drawing.
- **Nothing that could be used to defraud.** The authority's bank account details are left out and the page that would carry them says where to find the real ones. Every link to pay, apply or download goes to nia.gov.gh.
- **Nothing you type is sent.** The contact form and the replacement journey submit nothing. Fields for personal details have no `name` attribute, so the browser leaves them out of the request.
- **Every gap is a finding.** If a page needs something afrigov does not have, it goes in `FINDINGS.md` and the page uses the nearest thing. Page-local CSS is allowed only in a marked block. Since afrigov 0.9 there is none.
- **It should look like the finished site, and never be mistaken for it.** The banner at the top says it is an unofficial rebuild, with a disclosure that links to nia.gov.gh. Every page has `noindex`.

## Page map

| Real page | Rebuilt file | Notes |
| --- | --- | --- |
| Home | `index.html` | Hero on a tinted band, six tasks as cards, the card described beside a drawing, news, key figures, the Executive Secretary, a call to organisations on an accent band |
| Services | `services.html` | The seven services in four groups |
| Registration of Ghanaians in Ghana | `services/register-in-ghana.html` | Who, what to bring, steps, cost, questions |
| Registration of Ghanaians living abroad | `services/register-abroad.html` | Steps and fees by region of the world |
| Foreigner Identification Management System | `services/non-citizen-card.html` | Exemptions, documents, steps, fees |
| Card replacement | `services/replace-card.html` | Documents, steps, fees, questions |
| Personal information update | `services/update-details.html` | Documents, steps, fees, questions |
| Identity verification | `services/verification.html` | The new rule on biometric checks, how an organisation joins |
| Institutional and household registration | `services/mobile-registration.html` | Survey, fees by distance, how to apply. Bank details left out |
| Fees and charges | `fees.html` | Six tables |
| Regional and district offices | `offices.html` | Head office, seven regional offices and 27 district offices, of 307 |
| Registration centres, ages 6 to 14 | `centres-6-14.html` | An empty state, as the real list had no entries |
| FAQs | `questions.html` | 37 of the 70 answers, in seven groups |
| Scam alert | `scam-alert.html` | |
| About, and the Executive Secretary's profile | `about.html` | Mandate, vision and mission, the identification system, the technical partner |
| Governing board and management | `board.html` | People with portrait frames: the chairman and the Executive Secretary in two columns, the members in four, management as rows |
| User agencies | `user-agencies.html` | The first 25 private institutions |
| Registration statistics | `statistics.html` | Six figures as a table |
| News | `news.html` | Eight headlines. One is rebuilt, the rest link to the real posts |
| A press release | `news/biometric-verification.html` | Rewritten in full |
| Forms, reports, laws | `documents.html` | Three real pages in one, with file sizes |
| Careers | `careers.html` | An empty state |
| Contact | `contact.html`, `contact-sent.html` | The real form's fields. Sends nothing |
| No real equivalent | `replace/start.html` and seven steps | How the first part of a card replacement could be done online |

The real site also has a gallery, videos, audio and a right to information page. They are not rebuilt.

### The replacement journey

Replacing a card is done in person today. The journey shows how the request could start online, one question per page, and says on its first page that it is a demonstration.

1. Start page: what you need, how long it takes, what it costs.
2. What happened to your card? (radios)
3. Do you have a police extract? (radios)
4. Your Ghana Card number (the national ID input, with the pack's pattern and length)
5. Your phone number (phone number component)
6. Where will you collect the card? (region and district office)
7. Check your answers (summary list with change links)
8. Confirmation, with what happens next

## Things about the real site worth knowing

- The registration counters on the home page were empty, the search for registration centres returned nothing, and the news section showed a grid of blank boxes from a social media feed.
- The fee for a first card is stated three ways. The scam alert and the registration page say it is free. The fees table from January 2026 says it is free under 25 and GH₵30 from 25. The rebuild follows the fees table.
- A replacement non-citizen card is US$75 on its service page and US$78 in the fees table. The rebuild follows the fees table.
- The page for institutional registration publishes two bank account numbers in a table.

## Run it

```sh
python3 build-pages.py                                   # writes the 32 pages
AFRIGOV_CDN=http://localhost:8080/dist/ python3 build-pages.py   # against a local afrigov
```
