# afrigov use cases

Real government websites rebuilt page for page on [afrigov](https://github.com/omoyolab/afrigov), to find out what breaks when the components meet real content, and to show the same site built accessibly next to the real one's audit score.

Live: https://omoyolab.github.io/afrigov-usecases/

| Use case | Real site | Folder | Pages | Real home page | Rebuild |
| --- | --- | --- | ---: | ---: | ---: |
| Federal Ministry of Communications, Innovation and Digital Economy, Nigeria | fmcide.gov.ng | [`fmcide/`](fmcide/) | 29 | 52, D | 100, A |

## What these are, and are not

- **Unofficial.** None of these is a government website. Every page says so in the banner at the top and carries `noindex`.
- **No national seals.** Headers use a generic mark. Agency logos appear where the real site shows them and belong to the agencies.
- **Content belongs to the governments.** Structure and facts are the real site's; wording is condensed and rewritten, except signed statements, which are quoted and attributed.
- **The code is MIT**, like afrigov. The content and marks are not ours to license.

If you speak for one of these organisations and want something changed or removed, open an issue or write to xanderabim@gmail.com.

## How a use case is built

1. Map the real site's pages and audit them with `npx afrigov-audit` for a baseline.
2. Rebuild each page with afrigov from the CDN: two link tags, the country pack, the optional script. No build step beyond the page generator in the folder.
3. Log every gap in `FINDINGS.md`. A gap that needs a change in afrigov becomes an issue there.
4. Audit every rebuilt page and record the score beside the baseline.

Each folder has its own README with the page map and its own findings.

## Adding a use case

Add a folder, add a row to the table above and a card on `index.html`. Pages publishes the whole repository on every push to `main`.
