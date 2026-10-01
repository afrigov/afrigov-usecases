# Findings

What broke, what was missing, and what felt wrong when afrigov met the real content. Each entry names the page, what the content needed, what afrigov offered, and what was done. Findings that point to a change in afrigov get an issue there and are linked.

| # | Page | Needed | afrigov had | Done | Issue |
| --- | --- | --- | --- | --- | --- |
| 1 | Home | A dated list of links (news headlines with dates) | Stack utility, caption style; no list component | Page-local CSS at first. afrigov 0.5 shipped the dated list (`.ag-list`) and the pages use it. | [#18](https://github.com/omoyolab/afrigov/issues/18) |
| 2 | Home | A grid of agency logos | Service cards | Cards with the acronym as the link and the full name as text; no logos, which is also better for screen readers | |
| 3 | Header | A dropdown menu (Media Center with News, Events, Articles, Gallery) | Flat navigation, no dropdown by design | A Media section page that lists the four; the four also in the footer. Candidate for a section-page pattern in afrigov. | |
| 4 | Header | Eight top-level items plus a dropdown | Header guidance says six links | Seven in the nav (Home, About, Initiatives, Media, ICT Hubs, Project BRIDGE, PEBEC); Resources and Contact in the footer. Check the wrap at 1024px. | |
| 5 | Header | The national coat of arms as the brand mark | `ag-header__logo` slot for an agency's own image; flags ship in packs, coats of arms do not | A generic green mark is used here because use of the coat of arms needs government permission. afrigov docs should say where a crest goes and why it is not shipped. | |
| 6 | Question pages, check answers | A back link at the top of every step | Nothing; the page templates carry one as page-local CSS | Page-local `.fm-back` at first. afrigov 0.5 shipped `.ag-back-link`. | [#17](https://github.com/omoyolab/afrigov/issues/17) |
| 7 | Gallery | A grid of captioned photographs | Grid utility; no figure or image pattern, no guidance on captions and alt text | Page-local figure styles at first. afrigov 0.5 shipped image, figure and gallery with alt and caption rules; the gallery uses them with placeholder frames. | [#19](https://github.com/omoyolab/afrigov/issues/19) |
| 8 | Resources | Document links that say format and size | Table | afrigov 0.5 shipped the download link. The blueprint on the home page states its size (4.1 MB, from the file's headers); the resources table still lacks sizes because the real site does not state them. | [#20](https://github.com/omoyolab/afrigov/issues/20) |
| 9 | Events | A listing with nothing to list | Alert | An alert at first. afrigov 0.5 shipped the empty state and the page uses it. | [#21](https://github.com/omoyolab/afrigov/issues/21) |
| 10 | Resources | Links inside table header cells flagged as small tap targets | afrigov-audit exempted td but not th | Fixed in afrigov-audit 0.1.2; score is 97 under 0.1.1 and 100 after. | |
| 11 | Contact | A working contact form; the real one shows "Contact form not found" | Text input, select, textarea with character count, button | Built as the question-page pattern. Server side is out of scope. | |
| 12 | ICT Hubs | The real registry subdomain has an expired TLS certificate | Not a design-system matter | Noted on the rebuilt page. Should be reported to the ministry with the courtesy notice. | |
| 13 | 3MTT location | Local government areas for all 36 states and the FCT | Region selector with sample divisions in the pack | Five states have sample areas; a real service supplies all 774. The pack format works; the data needs a maintained source. | |
| 14 | Home | A photograph of the minister, as on the real home page | No image component and no hero | afrigov 0.5 shipped the hero with an image slot. The portrait then moved out of the hero into the statement component (0.6), under the hero, as a message from the minister; the About page carries the full message. | shipped in 0.5.0, 0.6.0 |
| 15 | Footer, all pages | Links to the ministry's Facebook, X, Instagram and LinkedIn | Nothing; the footer list takes plain links | afrigov 0.6 shipped social links; the footer's Contact column has the four accounts. | shipped in 0.6.0 |
| 16 | Footer, home, contact | A postal address | Nothing; the footer has heading, list and bar slots only, and the base styles leave `address` italic | afrigov 0.6 shipped `ag-footer__address` and the italic reset. | shipped in 0.6.0 |
| 17 | Media, short pages | The footer at the bottom of the screen on a page with little content | Nothing: the footer followed the content and left blank space under it | afrigov 0.8.3 makes the body a column with the main area filling the viewport. | shipped in 0.8.3 |

## Scores

Each rebuilt page, audited with afrigov-audit at phone and desktop width, next to the real page's baseline. Audited 2026-10-02 with afrigov-audit 0.1.1.

| Page | Real site | Rebuild | Notes |
| --- | ---: | ---: | --- |
| Home | 52, D | 100, A | |
| Initiatives | 73, C | 100, A | |
| News | 58, D | 100, A | |
| About | not audited | 100, A | |
| Project BRIDGE | not audited | 100, A | Everything on the real page, including the seven questions and the grievance mechanism |
| E-government | not audited | 100, A | |
| Media, Events, Articles, Gallery | not audited | 100, A each | News and Articles with thumbnails; one article rebuilt in full |
| ICT Hubs | could not load, expired certificate | 100, A | |
| PEBEC | not audited | 100, A | |
| Resources | not audited | 100, A | Finding 10; 97 under afrigov-audit 0.1.1 |
| Contact, Message sent | real form is broken | 100, A each | |
| 3MTT journey, 11 pages | separate app, not audited | 100, A each | |

Final run on 2026-10-02: 28 pages against afrigov 0.7.0 from the CDN, afrigov-audit 0.1.2, every page 100, A.
