# Findings

What broke, what was missing, and what felt wrong when afrigov 0.8 met a service agency's content. Each entry names the page, what the content needed, what afrigov offered, and what was done. Findings that point to a change in afrigov have an issue there.

| # | Page | Needed | afrigov had | Done | Issue |
| --- | --- | --- | --- | --- | --- |
| 1 | Home | A band directly under the header, and one directly above the footer | `.ag-main` has padding at both ends, which shows as a white strip between the header and the first band, and between the last band and the footer | One page-local rule on the home page, in a marked block: `.ag-main { padding-block: 0; }` | [#22](https://github.com/omoyolab/afrigov/issues/22) |
| 2 | Every service page, the confirmation page | The numbered steps of a process. The real site sets out "Step 1" to "Step 6" on every service | No steps component | An ordered list in prose. It reads correctly and has no more weight than any other list | [#23](https://github.com/omoyolab/afrigov/issues/23) |
| 3 | Home, statistics | A few headline numbers: people enrolled, cards issued | Nothing for figures | Plain cards with the number as the title on the home page, a table on the statistics page | [#24](https://github.com/omoyolab/afrigov/issues/24) |
| 4 | Home | Two actions in the green hero, one more important than the other | On a primary or dark band every button becomes white, so a start button and a secondary button look the same | Left as it is | [#25](https://github.com/omoyolab/afrigov/issues/25) |
| 5 | Fees, service pages, board | Tables with two columns, such as a service and its fee | A table takes the full width, so the two columns sit about 700px apart | Two-column tables are wrapped in `ag-prose` to hold them to the reading width | [#26](https://github.com/omoyolab/afrigov/issues/26) |
| 6 | Offices | To find one office among 307, by region or by name | Tables and pagination, and a search pattern for whole sites. Nothing for narrowing a long list | A sample of offices in two tables, and a link to the full list | [#27](https://github.com/omoyolab/afrigov/issues/27) |
| 7 | Journey, office step | Ghana's sixteen regions | The Ghana pack lists six | The page supplies its own list | [#28](https://github.com/omoyolab/afrigov/issues/28) |
| 8 | Questions, fees, service pages | Links to the sections of a long page | Nothing. Proposed during the first use case and not built | A plain list of links on the questions page, nothing elsewhere | [#29](https://github.com/omoyolab/afrigov/issues/29) |
| 9 | Header | The real menu has six items with dropdowns and about forty links | Flat navigation, no dropdown by design | Seven flat links. Everything else is on the Services page and in the footer. The same finding as on fmcide, and the same answer worked | |
| 10 | Journey, card number step | The Ghana Card number's pattern and length | The pack publishes both in `gh.json`. Putting them on the input is done by hand | `maxlength` and `pattern` copied from the pack. The documentation says to do this, and it took a minute | |
| 11 | Forms | A form that shows the components and sends nothing | Not afrigov's concern | Personal fields have no `name` attribute, so the browser leaves them out of the request | |

Eight findings have issues. None is fixed yet; this rebuild is on afrigov 0.8.

## What worked

- **Variants did their job.** A header in the primary colour, bands, plain cards and a light footer give a site that does not look like the fmcide rebuild, with no page-local CSS beyond finding 1.
- **Cards with a badge.** "Free under 25", "From GH₵200" and "For organisations" on the task cards answer the first question people have before they click.
- **The accordion.** Thirty-seven answers in seven groups stay readable, and each one opens without JavaScript.
- **Alert and inset text.** The scam warning, the note about bank details and the "this is a demonstration" notice each found the right weight.
- **The empty state.** Two real pages had nothing to list: no registration centres and no vacancies. Both are clearer with a sentence saying so than with an empty table.
- **Download links with a size.** The real site gives file sizes, so every form and report says what it is and how big.
- **The question pages.** The eight-step journey was built from the same pieces as the 3MTT journey with no new markup.
- **The header test.** Seven links stay on one row at 1024px in a wide font.
