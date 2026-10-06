# afrigov use case: fmcide.gov.ng rebuilt

An unofficial rebuild of the website of Nigeria's Federal Ministry of Communications, Innovation and Digital Economy, page for page, on [afrigov](https://github.com/afrigov/afrigov). It exists to find out what breaks when the components meet a real government site's content, and to show the same site built accessibly next to the real one's audit score.

It is not the ministry's website and says so on every page.

## Baseline

Scores from [afrigov-audit](https://github.com/afrigov/afrigov-audit) 0.1.1 on 2026-10-02.

| Real page | Score | Biggest problem |
| --- | ---: | --- |
| Home | 52, D | 9 links with no text, 11 of 29 tap targets under 44px, contrast on buttons |
| Initiatives | 73, C | image without alt text, small targets |
| News | 58, D | links with no text, small targets |

The rebuilt pages are audited the same way; see `FINDINGS.md`.

## Rules

- **Install like an agency would.** Two link tags from the CDN, the Nigeria pack, the optional script. No build step, no copying the source.
- **Structure and headings are the real site's.** Body text is condensed and rewritten, not copied. The one exception is the minister's message, which is quoted in full because it is a signed statement. No images from the site; the ministry's logo and photographs are theirs.
- **Every gap is a finding, not a workaround.** If a page needs a component or pattern afrigov does not have, or a component does not fit the content, it goes in `FINDINGS.md` and the page uses the nearest thing. Page-local CSS is allowed only in a marked block, and each block is a finding. Since afrigov 0.5 there is none left.
- **It should look like the finished site, and never be mistaken for it.** The layout, names and content are as on the real site. The banner at the top says it is an unofficial rebuild, with a disclosure that links to fmcide.gov.ng. The header carries a generic green mark, not the national coat of arms. Agency logos are shown as on the real site and belong to the agencies. The minister's message is quoted from the ministry's site and says so. Every page has `noindex`.
- **Audit every page** with `npx afrigov-audit` at the end and record the score next to the baseline.

## Page map

| Real page | Rebuilt file | Built from | Notes |
| --- | --- | --- | --- |
| Home | `index.html` | Service home template | Hero with an image slot, blueprint download link, initiatives as cards, dated news list, agencies |
| About | `about.html` | Content page | Mandate, minister and permanent secretary, departments, agencies |
| Initiatives | `initiatives.html` | Content page with cards | Seven initiatives, each a card to its own page |
| Project BRIDGE | `project-bridge.html` | Content page | One initiative in full: outcomes, progress, partners, questions, complaints |
| E-government | `initiatives/e-government.html` | Content page | The second initiative with its own page on the real site; the other five link out |
| News | `news.html` | Content page with list, pagination | Six per page, thumbnail, date and title; one rebuilt, the rest link to the real posts |
| A news article | `news/goalkeepers-champion.html` | Content page | One article in full, breadcrumb |
| Media | `media.html` | Section page | Replaces the dropdown: News, Events, Articles, Gallery |
| Events | `events.html` | Content page with list | |
| Articles | `articles.html` | Content page with list, thumbnails | |
| An article | `articles/learning-community.html` | Content page | One article in full, lead image |
| Gallery | `gallery.html` | Photo gallery pattern | One card per album with a cover frame |
| An album | `gallery/atu-conference.html` | Photo gallery pattern | Six captioned frames, each linking to the full-size placeholder |
| ICT Hubs | `ict-hubs.html` | Content page with cards | |
| PEBEC | `pebec.html` | Content page | Ease of doing business reforms |
| Resources | `resources.html` | Content page with table | Documents with type, size and date |
| Contact | `contact.html` | Question page | A working contact form, the real one is broken |
| 3MTT sign-up | `3mtt/start.html` and steps | Start, question, check answers, confirmation | The one real transactional journey |

### The 3MTT journey

The real sign-up is on a separate app. The rebuild follows what it asks, one question per page:

1. Start page: what the programme is, who can apply, what you need.
2. Are you applying as a fellow or a training provider? (radios)
3. Your name (text input)
4. Date of birth (date input)
5. Phone number (phone number component)
6. Email address (text input)
7. State and local government area (region selector)
8. Which track? (radios, twelve options)
9. Highest level of education (select)
10. Check your answers
11. Confirmation with a reference number

## Run it

Open `index.html`. Everything loads from the CDN. To audit a page from this folder:

```sh
npx afrigov-audit "file://$PWD/index.html"
```
