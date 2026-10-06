# afrigov use case: scienceandtech.gov.ng rebuilt

An unofficial rebuild of the website of Nigeria's Federal Ministry of Innovation, Science and Technology on [afrigov](https://github.com/afrigov/afrigov). It is the fourth use case, and the first to use the video components and the people grid on a Nigerian site.

It is not the ministry's website and says so on every page.

## Why this site

The first use case was also a Nigerian ministry, so the two share a country pack and nothing else. The communications ministry has a stacked header and a photograph beside its title. This one has a one-row white header with three menus, a solid green hero with the key figures under it, and a plain footer.

The real site is built with WordPress and Elementor. It opens with a slider, holds its mandate and objectives in hidden tabs, and has a video page, a gallery, 15 departments and 17 agencies. That made it a test of the components afrigov added in 0.11 and 0.12: events, video cards, the video page, the feature block, steps and key figures.

## Baseline

Scores from [afrigov-audit](https://github.com/afrigov/afrigov-audit) 0.3.0 on 3 October 2026. The full results are in `baseline/`.

| Real page | Score | Weight on a phone | Biggest problems |
| --- | ---: | ---: | --- |
| Home | 44.5, D | 6.7 MB, 116 requests | A search form with broken ARIA, unnamed links, 31 of 35 tap targets under 44 pixels, no skip link |
| Management | 59.5, D | 4.5 MB | The same, and 20 top-level headings |
| Contact | 65.5, C | 3.1 MB | The same, and a form that shows as raw code |
| A news article | 47.5, D | 2.6 MB | The same, and low contrast |

Every rebuilt page scores 100, A, on afrigov 0.13 from the CDN. The rebuilt home page is 33 KB in 7 requests on a phone.

## Rules

- **Install like an agency would.** Two link tags from the CDN, the Nigeria pack, the optional script. No build step beyond the page generator.
- **Structure and facts are the real site's.** The departments, programs, services, leadership, agencies, documents, news and contact details were taken from scienceandtech.gov.ng on 3 October 2026. The wording is condensed and rewritten.
- **A page only where the real site has content.** Thirteen departments and four programs have a page. The ones whose links go nowhere are listed without a link, and say so.
- **No agency logos.** The real logos are 150 by 70 pixel thumbnails, and some are cropped. The agency cards carry the name, the short name and the website instead.
- **No photographs from the site.** Grey frames stand where portraits and news photographs go, and wordless drawings where a picture or a video's first frame goes.
- **Videos play from the ministry's site.** The two clips are linked, not copied. Nothing loads until someone presses play.
- **Nothing you type is sent.** The contact form submits nothing, and its fields have no `name` attribute.
- **Every gap is a finding.** It goes in `FINDINGS.md`, and the page uses the nearest thing. There is no page-local CSS.
- **It should look like the finished site, and never be mistaken for it.** The banner says it is an unofficial rebuild, with a disclosure that links to scienceandtech.gov.ng. The header carries a generic mark. Every page has `noindex`.

## Page map

| Real pages | Rebuilt | Notes |
| --- | --- | --- |
| Home | `index.html` | Green hero, key figures, three services, the youth programme as a feature block, events, the two leaders, news, video cards |
| Mandate and vision | `about.html` | The mandate and objectives from the hidden tabs, as text on the page |
| Management, 2 profiles | `management.html`, `minister.html`, `permanent-secretary.html` | Two leaders, then 18 directors and heads in a four-column grid |
| Departments, 13 pages | `departments.html` and `departments/*.html` | 15 departments and 3 units. Each page has the director, the divisions and what the department does |
| Programs, 4 pages | `programs.html` and `programs/*.html` | Eight programs. Four have pages |
| Youth and Students in Innovation | `ysi.html` | Steps for how it works, and the eight tracks. Applications closed on 14 September |
| What We Do, on the home page | `services.html` | Five services, each with the agency that handles it |
| None | `events.html`, `events/technology-innovation-expo.html` | The real site has no events page. The Expo is set for the third week of October, with no date announced |
| News | `news.html` and `news/*.html` | Ten dated releases, four rebuilt |
| Videos | `videos.html` and `videos/*.html` | Two clips with titles, lengths and a video page each |
| Gallery | `gallery.html` | Empty on the real site, so an empty state |
| Agencies | `agencies.html` | Seventeen cards |
| Resources | `resources.html` | Five documents with their type and size |
| Contact | `contact.html`, `contact-sent.html` | |
| Search, in the header of every page | `search.html` | Added with afrigov 0.14. The real site's search form is its one critical accessibility error. Results come from a Pagefind index of the other pages, built with the site; there is no server |

42 pages.

## Things about the real site worth knowing

- Four program links go to test.joyhomeapartments.com, a test domain that no longer exists. The Grand Challenges Nigeria link goes to the PSCII address, which shows the Grand Challenges page.
- The Bioresources Technology link is a WordPress preview address. Health and Biomedical Sciences sits at the address meant for Science and Technology Promotion. Four departments and units have no page, and the Legal unit's link returns "page not found".
- The contact page shows `[wpforms id="7"]` where the form should be.
- The About page still describes the previous Permanent Secretary, who left in April 2026.
- The home page says "the call is open" for the youth programme, whose applications closed on 14 September 2026.
- The National Council page opens with the paragraph about the 774 YONSPA competition.
- The agencies page uses the biotechnology agency's old name, NABDA. Its logo and website use the current name, NBRDA.
- The gallery has filters and no photographs. The two videos are WhatsApp exports with no title, poster, captions or transcript.
- The resources list has a performance report with no file, and gives no file sizes. The roadmap is a 21 MB PDF.
- The management page makes every person a top-level heading, 20 in all. The email address and phone number are headings on every page.
- A permanent secretary photograph of 1 MB is shown 250 pixels wide. About 3.3 MB of the home page's images could be saved.
- The footer says 2025.

## Run it

```sh
python3 build-pages.py                                   # writes the 42 pages
npx pagefind@1.5.2 --site .                              # builds the search index in pagefind/
AFRIGOV_CDN=http://localhost:8080/dist/ python3 build-pages.py   # against a local afrigov
```
