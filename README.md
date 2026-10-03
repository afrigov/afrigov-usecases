# afrigov use cases

Real government websites rebuilt page for page on [afrigov](https://github.com/omoyolab/afrigov), to find out what breaks when the components meet real content, and to show the same site built accessibly next to the real one's audit score.

Live: https://omoyolab.github.io/afrigov-usecases/

| Use case | Rebuild | Real site, home page |
| --- | --- | --- |
| [fmcide.gov.ng](fmcide/), Nigeria | ![Rebuild score](https://omoyolab.github.io/afrigov-usecases/badges/fmcide-rebuild.svg) | ![Real site score](https://omoyolab.github.io/afrigov-usecases/badges/fmcide-real.svg) |
| [nia.gov.gh](nia-gh/), Ghana | ![Rebuild score](https://omoyolab.github.io/afrigov-usecases/badges/nia-gh-rebuild.svg) | ![Real site score](https://omoyolab.github.io/afrigov-usecases/badges/nia-gh-real.svg) |
| [moh.gov.gh](moh-gh/), Ghana | ![Rebuild score](https://omoyolab.github.io/afrigov-usecases/badges/moh-gh-rebuild.svg) | ![Real site score](https://omoyolab.github.io/afrigov-usecases/badges/moh-gh-real.svg) |

The badges come from [afrigov-audit](https://github.com/omoyolab/afrigov-audit) and update automatically every week. See [How the scores stay current](#how-the-scores-stay-current).

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

## How the scores stay current

`scripts/build.mjs` audits every rebuilt page and the real pages they are compared with, then writes `scores.json`, a badge per use case in `badges/`, and `index.html`. The Pages workflow runs it on every push, every Monday, and on demand, so the live index and the badges always show the last audit. A rebuild's badge is its lowest-scoring page. If a real site will not load, its last score is kept with the date it was taken.

```sh
npm install
npx playwright install chromium
npm run build            # audit, then write the index, scores and badges
npm run build:offline    # rebuild the index from scores.json without auditing
```

## Adding a use case

Add a folder with the rebuilt pages and an entry in `usecases.json` naming the real pages to compare. The build does the rest: the card, the badges and the scores table. Add the badge row to this README.
