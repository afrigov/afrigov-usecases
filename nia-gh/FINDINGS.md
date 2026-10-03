# Findings

What broke, what was missing, and what felt wrong when afrigov 0.8 met a service agency's content, and what became of each. The rebuild was first built on 0.8 with workarounds; the fixes shipped in afrigov 0.9.0 and the workarounds were removed.

| # | Page | Needed | afrigov had | Done | Issue |
| --- | --- | --- | --- | --- | --- |
| 1 | Home | A band directly under the header, and one directly above the footer | `.ag-main` has padding at both ends, which shows as a white strip between the header and the first band, and between the last band and the footer | One page-local rule at first. **Fixed in 0.9.0:** `ag-main--flush`. The rebuild has no page-local CSS | [#22](https://github.com/omoyolab/afrigov/issues/22) |
| 2 | Every service page, the confirmation page | The numbered steps of a process. The real site sets out "Step 1" to "Step 6" on every service | No steps component | An ordered list in prose at first. **Fixed in 0.9.0:** `ag-steps`, used on every service page and the confirmation page | [#23](https://github.com/omoyolab/afrigov/issues/23) |
| 3 | Home, statistics | A few headline numbers: people enrolled, cards issued | Nothing for figures | Plain cards at first. **Fixed in 0.9.0:** `ag-stats` on the home page, with the accent colour beside each figure | [#24](https://github.com/omoyolab/afrigov/issues/24) |
| 4 | Home | Two actions in the green hero, one more important than the other | On a primary or dark band every button becomes white, so a start button and a secondary button look the same | **Fixed in 0.9.0.** A secondary button on a coloured band is an outline in the band's text colour | [#25](https://github.com/omoyolab/afrigov/issues/25) |
| 5 | Fees, service pages, board | Tables with two columns, such as a service and its fee | A table takes the full width, so the two columns sit about 700px apart | Two-column tables are wrapped in `ag-prose`. **Documented in 0.9.0** on the Table page | [#26](https://github.com/omoyolab/afrigov/issues/26) |
| 6 | Offices | To find one office among 307, by region or by name | Tables and pagination, and a search pattern for whole sites. Nothing for narrowing a long list | A sample of offices in two tables, and a link to the full list | [#27](https://github.com/omoyolab/afrigov/issues/27) |
| 7 | Journey, office step | Ghana's sixteen regions | The Ghana pack lists six | The page supplies its own list. **Fixed in 0.9.0:** the pack has all sixteen | [#28](https://github.com/omoyolab/afrigov/issues/28) |
| 8 | Questions, fees, service pages | Links to the sections of a long page | Nothing. Proposed during the first use case and not built | A plain list of links on the questions page, nothing elsewhere | [#29](https://github.com/omoyolab/afrigov/issues/29) |
| 9 | Header | The real menu has six items with dropdowns and about forty links | Flat navigation, no dropdown by design | Seven flat links. Everything else is on the Services page and in the footer. The same finding as on fmcide, and the same answer worked | |
| 10 | Journey, card number step | The Ghana Card number's pattern and length | The pack publishes both in `gh.json`. Putting them on the input is done by hand | `maxlength` and `pattern` copied from the pack. The documentation says to do this, and it took a minute | |
| 11 | Forms | A form that shows the components and sends nothing | Not afrigov's concern | Personal fields have no `name` attribute, so the browser leaves them out of the request | |

Eight findings have issues. Six were fixed in afrigov 0.9.0; the contents list and the long-list pattern stay open.

## What the user noticed

Three things came from looking at the finished rebuild beside the first one, and all three became part of 0.9.0.

| # | Where | Noticed | afrigov had | Done |
| --- | --- | --- | --- | --- |
| 12 | Every page | Only green and white. No Ghana colours, when the pack has gold and red | Every pack defines an accent colour and its flag colours, and no component used the accent. Five of the seven packs have a green primary, so their sites all looked alike | **0.9.0:** the flag stripe under the header, an accent band, and the accent colour on card edges and key figures. The header carries the stripe, the organisations call is a gold band, and the "Before you go" cards have gold edges |
| 13 | Board | Names in a table, where the real page has a portrait for each person | Photo cards, built for news | **0.9.0:** `ag-people`, a grid for the board and rows for management, with grey frames where the portraits go |
| 14 | Home | A green header followed by a green hero, which ran together | Neutral options already existed: a plain hero, or a hero on a tinted band | The hero is on a tinted band, with the stripe between it and the header. The Hero page now says not to put a primary hero under a primary header |
| 15 | Home | Nothing shows what the card looks like, where the real page describes it beside a picture | Hero with image, which is for the top of a page | **0.9.0:** `ag-feature`, a picture beside a name and main points. The picture is a simplified drawing, since the real card is a security document |

## What worked

- **Variants did their job.** A header in the primary colour, bands, plain cards and a light footer give a site that does not look like the fmcide rebuild. Since 0.9.0 there is no page-local CSS at all.
- **Cards with a badge.** "Free under 25", "From GH₵200" and "For organisations" on the task cards answer the first question people have before they click.
- **The accordion.** Thirty-seven answers in seven groups stay readable, and each one opens without JavaScript.
- **Alert and inset text.** The scam warning, the note about bank details and the "this is a demonstration" notice each found the right weight.
- **The empty state.** Two real pages had nothing to list: no registration centres and no vacancies. Both are clearer with a sentence saying so than with an empty table.
- **Download links with a size.** The real site gives file sizes, so every form and report says what it is and how big.
- **The question pages.** The eight-step journey was built from the same pieces as the 3MTT journey with no new markup.
- **The header test.** Seven links stay on one row at 1024px in a wide font.
