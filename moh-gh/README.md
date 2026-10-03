# afrigov use case: moh.gov.gh rebuilt

An unofficial rebuild of the website of Ghana's Ministry of Health on [afrigov](https://github.com/omoyolab/afrigov). It is the third use case, and the first to use the section menus and the panel hero that afrigov 0.10 added for it.

It is not the ministry's website and says so on every page.

## Why this site

The first use case was a ministry in Nigeria, the second a service agency in Ghana. This is a ministry in Ghana, so the two Ghanaian rebuilds share a country pack and nothing else: the agency has a green header, a tinted hero and a light footer; the ministry has a white header with the flag stripe, a photograph with the title in a panel over it, and the dark footer.

The real site keeps its 37 pages behind six dropdown menus and opens with a photo slider. Those two things are what most government sites do, and afrigov had neither until this rebuild asked for them.

## Baseline

Scores from [afrigov-audit](https://github.com/omoyolab/afrigov-audit) 0.2.0 on 3 October 2026. The full results are in `baseline/`.

| Real page | Score | Biggest problems |
| --- | ---: | --- |
| Home | 17.5, F | Hidden slides that can still be tabbed to, controls inside controls, unsupported ARIA on the slider, small tap targets |
| The ministry | 98.5, A | No skip link |
| Policy documents | 89.5, B | Three small tap targets, no skip link |

The real site's inner pages are nearly fine. Its home page is where the slider, the carousel and the widgets are.

Every rebuilt page scores 100, A, on afrigov 0.10.1 from the CDN.

## Rules

- **Install like an agency would.** Two link tags from the CDN, the Ghana pack, the optional script. No build step beyond the page generator.
- **Structure and facts are the real site's.** The menu, the directorates, the programmes, the document lists, the leadership, the contact details and the agencies were taken from moh.gov.gh on 2 and 3 October 2026. The wording is condensed and rewritten.
- **Agency logos stay.** They are what the agencies page is, as on the first use case. They belong to the agencies. Partner logos are not reproduced; the partners are listed by name.
- **No photographs from the site.** The hero carries a wordless drawing where a photograph goes, and grey frames stand where portraits and news images go.
- **Nothing you type is sent.** The contact form submits nothing, and its fields have no `name` attribute.
- **Every gap is a finding.** It goes in `FINDINGS.md`, and the page uses the nearest thing. There is no page-local CSS.
- **It should look like the finished site, and never be mistaken for it.** The banner says it is an unofficial rebuild, with a disclosure that links to moh.gov.gh. The header carries a generic mark. Every page has `noindex`.

## Page map

| Real pages | Rebuilt | Notes |
| --- | --- | --- |
| Home | `index.html` | Panel hero on the free primary healthcare campaign, what the ministry does, news, leadership with portrait frames, the twelve agencies with logos, programmes, events on a green band, latest publications |
| About us, 4 pages | `about.html`, `chief-director.html`, `organogram.html`, `partners.html` | The organogram, one picture on the real site, is a text structure here |
| Agencies | `agencies.html` | Twelve logo cards |
| Directorates, 10 pages | `directorates.html` and `directorates/*.html` | An index, and one page per directorate with its units as a summary list |
| Publications, 9 categories | `publications.html` and `publications/*.html` | Download tables with name and year. The largest categories show their most recent twelve and link to the rest |
| Programmes, 4 pages | `programmes.html` and `programmes/*.html` | |
| Media, 5 pages | `news.html`, `news/free-primary-healthcare.html`, `press-releases.html`, `events.html`, `gallery.html`, `videos.html` | The gallery and video pages are empty on the real site, so they are empty states |
| Tenders | `tenders.html` | An empty state: the newest notices are from 2017 |
| Contact us, useful links | `contact.html`, `contact-sent.html`, `useful-links.html` | |

42 pages. The real site's single news articles, agency pages and the QualityRights project page are not rebuilt; the lists link to them.

## Things about the real site worth knowing

- The site's firewall blocks visitors it takes for automated after a few dozen requests. Three pages and every article came back as a block page on the first pass; the texts were taken on a second pass at a slower rate.
- News, press releases and events are listed without dates. The lists here say what each item is instead.
- Headlines on the home page are typed in bold mathematical symbols, which screen readers read letter by letter or skip. They are plain text here.
- 33 of the 35 images on the home page have no description.
- The footer reads "0 Fans, 0 Followers", and a box of health posts dates from 2017.
- Every document page ends with a comment form.
- No file sizes are given for the 165 PDFs.

## Run it

```sh
python3 build-pages.py                                   # writes the 42 pages
AFRIGOV_CDN=http://localhost:8080/dist/ python3 build-pages.py   # against a local afrigov
```
