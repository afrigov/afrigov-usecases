# Findings

What was missing, what broke, and what felt wrong when afrigov met a fourth government site. Most of what this site needed was built for the third rebuild, so this one is mostly a check that those parts hold up on different content.

| # | Page | Needed | afrigov had | Done | Issue |
| --- | --- | --- | --- | --- | --- |
| 1 | Header | A one-row header with a long ministry name and eight items | One row, wrapping to a second row when the items do not fit | Between 1000 and about 1060 pixels wide, the brand and seven items did not fit, and the navigation dropped to a second row without warning. Agencies and resources moved into the About menu and the Home link went, since the brand already links home. One row at every width now | [afrigov#30](https://github.com/afrigov/afrigov/issues/30) |
| 2 | Videos | Play the ministry's MP4 files | The video component loads a player in a frame, made for YouTube and similar sites | It works: the frame opens the MP4 in the browser's own player. A `<video>` element with controls would be the right element for a file, with a place for a captions track | [afrigov#31](https://github.com/afrigov/afrigov/issues/31) |
| 3 | Videos | A transcript | The video page has a place for one | The real clips have none, so the page says a live service must add one | |
| 4 | Agencies | Seventeen agency logos | The card's logo slot | The real logos are 150 by 70 pixel thumbnails and some are cropped, so the cards have none. A card with a name, a short name and a website reads fine | |
| 5 | Departments, programs | Items with no page of their own | Cards with or without a link | Cards without a link, saying the real site has no page yet. Worked | |
| 6 | Home | The ministry's numbers under the hero | Key figures, from 0.9 | Worked: founded, departments, units, agencies | |
| 7 | Home | One programme given more room than a card | The feature block, from 0.9 | Worked, with a wordless drawing where the picture goes | |
| 8 | Youth programme | How the programme runs | Steps, from 0.9 | Worked. A first version used the confirmation panel to say applications were closed; the panel is for the end of a form, so it became an inset | |
| 9 | Events | An event with no date, no venue and no flyer | The "to be confirmed" date block and the event page, from 0.11 | Worked. The event page leaves the flyer out and says where it goes once there is one | |
| 10 | Management | Two leaders, then 18 directors | `ag-people--2` and `ag-people--4` | Worked. The two leaders sit at the four-column size, centred, as agreed in the third rebuild | |
| 11 | Resources | File sizes | The download link's meta | The real site gives none. The sizes here come from the ministry's server, so the 21 MB roadmap carries a warning | |
| 12 | Gallery | A gallery with nothing in it | The empty state | Worked | |
| 13 | Header, every page | Search. The real site has a search form in its header, and it is its one critical accessibility error | Nothing: afrigov had a pattern about search engines, but no search box | **Built in 0.14.0:** `ag-search`, the header search button, and the site search results pattern. Here the results come from a Pagefind index of the 40 content pages, built with the site, so there is no server. A search transfers about 73 KB, the header stays on one row at 1024px, and the results page scores 100 | |

Two things are open in afrigov from this rebuild, findings 1 and 2.

## What worked

- **The pack.** Nigeria's green from the pack carries the hero, the card edges, the event blocks and the footer, with no page CSS.
- **Video cards and the video page.** Two clips with no titles became two pages with a title, a source, a date, a length and a play button, and nothing downloads until someone presses play.
- **Pages only where there is content.** Thirteen department pages and four program pages, with the rest listed and marked.
- **Weight.** The rebuilt home page is 33 KB in 7 requests on a phone. The real one is 6.7 MB in 116.
- **The audit as a reviewer.** All 41 pages scored 100 on the first full run.
