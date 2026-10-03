# Findings

What was missing, what broke, and what felt wrong when afrigov met a ministry's content for the second time, in a second country. Two of the three things this site needed were built into afrigov before the rebuild began, after the second use case made the same point; the rest came out during the build.

| # | Page | Needed | afrigov had | Done | Issue |
| --- | --- | --- | --- | --- | --- |
| 1 | Header | Six dropdown menus holding 37 pages | Flat navigation. Both earlier rebuilds worked around it with section pages | **Built first, in 0.10.0:** section menus, a native disclosure that opens on click. Six menus and three plain links here, on a stacked header, one row at 1024px | |
| 2 | Home | A photograph across the top with the title over it, as the real site and most ministry sites have | The hero put the image beside the text, and the rule said never over it | **Built first, in 0.10.0:** the cover hero, with the text in a solid panel over the photograph. The contrast is between text and panel | |
| 3 | Home | Upcoming events as a dated list on the green band | The list's meta line kept its grey, which failed contrast on green. The audit caught it | **Fixed in 0.10.1.** On a coloured band the meta line and the hairlines take the band's colour | |
| 4 | Header | Nine items across: home, six menus, tenders, contact | Six links beside the brand, by the guidance | `ag-header--stacked`, which puts the navigation on its own row. Nine items fit at 1024px with the wide font the header test uses | |
| 5 | Organogram | The ministry's structure | The real page is one picture, which cannot be read aloud, searched or resized | Lists of the leadership, the directorates and the agencies, with links | |
| 6 | Publications | Download links with the file size | The real site gives none for its 165 PDFs | The tables give the document and its year. The same finding as on fmcide; a live service must add sizes | |
| 7 | News, press | Dates for the dated list | The real lists give no dates | The meta line says what the item is. A dated list without dates is a plain list; the component copes but the guidance could say so | |
| 8 | Agencies | Twelve logos in a grid, linking to the agencies | The card's logo slot, from 0.6 | Worked. The real site links each agency to a page on the ministry's site, so the cards do too | |
| 9 | Home | Three leaders with portraits | `ag-people--3`, from 0.9 | Worked, with grey frames where the portraits go | |
| 10 | Home | A photograph for the cover hero | Not afrigov's concern | A wordless drawing stands in. The hero reads correctly without it, since the title is text in the panel | |
| 11 | Everywhere | The site's content | The site's firewall blocked the crawl after a few dozen requests | The texts were collected over two passes at a slower rate. One article is rebuilt from its summary only | |
| 12 | Home, events | Events with a date people see at a glance, and a page for one event | A dated list, which shows a date as a line of text, and no event page. The user asked for the square date block most sites use | **Built in 0.11.0:** `ag-events` with a date block, a "to be confirmed" block and a past state, and an event page template. The events page here uses all three; the African Union summit has its own page | |
| 13 | Programmes, footer | Somewhere for the third flag colour. Only the stripe under the header carried Ghana's red | The pack exposes every official colour, but components have roles for two: primary and accent. Red on its own would read as an error | **Built in 0.11.0:** `ag-card--flag` and `ag-footer--striped`, the flag's three colours as an edge. On the four programme cards and the footer here | |
| 14 | Events | Dates for the events | Each event on the real site is a picture of a flyer, with no text and no date | The dates were read from the flyers. Three flyers give none, and the block says so. An event's details should be text on the page, for people and for machines | |

Nothing is open in afrigov from this rebuild. Findings 12 and 13 came from the user's review of the finished site and were built the same day. Finding 7 is a line of guidance to add when the dated list page is next touched.

## What worked

- **Section menus.** Nine items and 33 links in the header, every page reachable, and the whole thing works with the script turned off. One menu open at a time, Escape closes it.
- **The stacked header.** The ministry's name, the mark and nine items, on two rows on purpose, with the flag stripe under them.
- **The cover hero.** The look of the real site's slider, with one picture and text that can be read.
- **The summary list for directorate units.** Ten directorates with up to seven units each read as a list of terms and descriptions, which is what they are.
- **The empty state**, four times: the gallery, the videos, the tenders and the partner logos all had nothing or nothing current to show.
- **Download tables.** 69 documents across eight categories from one function.
- **The audit as a reviewer.** It caught the one contrast failure, on the green band, before anyone saw the page.
