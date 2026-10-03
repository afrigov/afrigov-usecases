// Audits every rebuilt page and the real pages they are compared with, then writes
// scores.json, a badge per use case, and index.html.
//
//   node scripts/build.mjs            audit, then write everything
//   node scripts/build.mjs --offline  skip the audits and rebuild the index from scores.json
import { createServer } from "node:http";
import { readFileSync, writeFileSync, mkdirSync, readdirSync, statSync, existsSync } from "node:fs";
import { dirname, extname, join, relative } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const OFFLINE = process.argv.includes("--offline");
const usecases = JSON.parse(readFileSync(join(ROOT, "usecases.json"), "utf8"));
const previous = existsSync(join(ROOT, "scores.json"))
  ? JSON.parse(readFileSync(join(ROOT, "scores.json"), "utf8"))
  : { usecases: {} };

const TYPES = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".svg": "image/svg+xml", ".png": "image/png", ".webp": "image/webp", ".json": "application/json" };

function serve() {
  const server = createServer((req, res) => {
    const path = join(ROOT, decodeURIComponent(new URL(req.url, "http://x").pathname));
    const file = existsSync(path) && statSync(path).isDirectory() ? join(path, "index.html") : path;
    if (!file.startsWith(ROOT) || !existsSync(file)) {
      res.writeHead(404).end();
      return;
    }
    res.writeHead(200, { "content-type": TYPES[extname(file)] ?? "application/octet-stream" });
    res.end(readFileSync(file));
  });
  return new Promise((resolve) => server.listen(0, "127.0.0.1", () => resolve(server)));
}

function htmlFiles(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((entry) =>
    entry.isDirectory()
      ? htmlFiles(join(dir, entry.name))
      : entry.name.endsWith(".html")
        ? [join(dir, entry.name)]
        : [],
  );
}

const gradeOf = (score) => (score >= 90 ? "A" : score >= 75 ? "B" : score >= 60 ? "C" : score >= 40 ? "D" : "F");

async function run() {
  const scores = { checkedAt: new Date().toISOString().slice(0, 10), tool: previous.tool ?? null, usecases: {} };
  let audit, badgeSvg, version;
  if (!OFFLINE) ({ audit, badgeSvg, version } = await import("afrigov-audit"));
  else ({ badgeSvg } = await import("afrigov-audit").catch(() => ({ badgeSvg: null })));
  if (!OFFLINE) scores.tool = `afrigov-audit ${version}`;
  else scores.checkedAt = previous.checkedAt ?? scores.checkedAt;

  const server = OFFLINE ? null : await serve();
  const base = server ? `http://127.0.0.1:${server.address().port}/` : "";

  for (const uc of usecases) {
    const before = previous.usecases?.[uc.slug];
    if (OFFLINE) {
      if (!before) throw new Error(`No saved scores for ${uc.slug}; run without --offline first.`);
      scores.usecases[uc.slug] = before;
      continue;
    }
    // Every rebuilt page. The use case's score is its worst page.
    const files = htmlFiles(join(ROOT, uc.slug)).map((f) => relative(ROOT, f).split("\\").join("/"));
    const rebuilt = {};
    for (const file of files) {
      const r = await audit(base + file);
      rebuilt[file] = { score: r.score, grade: r.grade };
      console.log(`${uc.slug}  rebuild  ${r.grade} ${r.score}  ${file}`);
    }
    const worst = Math.min(...Object.values(rebuilt).map((r) => r.score));
    // The real pages. A site that will not load keeps its last score, marked with the date it was taken.
    const compare = [];
    for (const page of uc.compare) {
      const last = before?.compare?.find((p) => p.label === page.label)?.real;
      let real;
      try {
        const r = await audit(page.real, { timeout: 45000 });
        real = { score: r.score, grade: r.grade, checkedAt: scores.checkedAt };
        console.log(`${uc.slug}  real     ${r.grade} ${r.score}  ${page.real}`);
      } catch (err) {
        real = last ?? null;
        console.log(`${uc.slug}  real     could not load ${page.real}: ${err.message}. Keeping ${last ? `${last.grade} ${last.score} from ${last.checkedAt}` : "nothing"}.`);
      }
      compare.push({ label: page.label, url: page.real, real, rebuild: rebuilt[page.rebuild] });
    }
    scores.usecases[uc.slug] = {
      pages: files.length,
      rebuild: { score: worst, grade: gradeOf(worst) },
      real: compare[0]?.real ?? null,
      compare,
    };
  }
  server?.close();

  writeFileSync(join(ROOT, "scores.json"), JSON.stringify(scores, null, 2) + "\n");
  mkdirSync(join(ROOT, "badges"), { recursive: true });
  if (badgeSvg) {
    for (const uc of usecases) {
      const s = scores.usecases[uc.slug];
      writeFileSync(join(ROOT, "badges", `${uc.slug}-rebuild.svg`), badgeSvg(s.rebuild, { label: "rebuild" }));
      if (s.real) writeFileSync(join(ROOT, "badges", `${uc.slug}-real.svg`), badgeSvg(s.real, { label: "real site" }));
    }
  }
  writeFileSync(join(ROOT, "index.html"), index(scores));
  console.log(`index.html, scores.json and badges written (${scores.checkedAt}).`);
}

const esc = (t) => String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const cell = (s) => (s ? `${s.score}, ${s.grade}` : "could not be checked");

function index(scores) {
  const cards = usecases
    .map((uc) => {
      const s = scores.usecases[uc.slug];
      const real = s.real
        ? `<img src="badges/${uc.slug}-real.svg" alt="Real site home page: ${s.real.grade} ${s.real.score}" height="20" />`
        : "";
      return `
        <li class="ag-card">
          <h3 class="ag-card__title"><a class="ag-card__link" href="${uc.slug}/index.html">${esc(uc.name)}</a></h3>
          <p class="ag-card__text">${esc(uc.country)} · ${esc(uc.site)} · ${s.pages} pages, ${esc(uc.note)}</p>
          <p class="ag-card__meta"><img src="badges/${uc.slug}-rebuild.svg" alt="Rebuild: ${s.rebuild.grade} ${s.rebuild.score}" height="20" /> ${real}</p>
        </li>`;
    })
    .join("");
  const rows = usecases
    .map((uc) => {
      const s = scores.usecases[uc.slug];
      return s.compare
        .map(
          (p, i) =>
            `<tr>${i === 0 ? `<th scope="row" rowspan="${s.compare.length}">${esc(uc.site)}</th>` : ""}<td>${esc(p.label)}</td><td class="ag-table__numeric">${cell(p.real)}</td><td class="ag-table__numeric">${cell(p.rebuild)}</td></tr>`,
        )
        .join("\n            ");
    })
    .join("\n            ");
  return `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>afrigov use cases</title>
    <meta name="description" content="Real government websites rebuilt on afrigov, with the accessibility score of the real site beside the rebuild." />
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/afrigov@0.10/dist/core.min.css" />
  </head>
  <body>
    <!-- Generated by scripts/build.mjs from usecases.json and the audit results. Do not edit by hand. -->
    <a class="ag-skip-link" href="#main">Skip to main content</a>

    <section class="ag-banner" aria-label="About this site">
      <div class="ag-container ag-banner__inner">
        <p class="ag-banner__text">These are unofficial rebuilds for demonstration. None of them is a government website.</p>
      </div>
    </section>

    <header class="ag-header">
      <div class="ag-container ag-header__inner">
        <a class="ag-header__brand" href="index.html">
          <span>
            <span class="ag-header__org">afrigov use cases</span>
            <span class="ag-header__sub">Real government websites, rebuilt on afrigov</span>
          </span>
        </a>
      </div>
    </header>

    <main class="ag-main ag-container" id="main" tabindex="-1">
      <div class="ag-prose">
        <h1 class="ag-heading-xl">Use cases</h1>
        <p class="ag-lead">Real government websites rebuilt page for page on afrigov, to find out what breaks when the components meet real content, and to show the same site built accessibly.</p>
        <p>Each rebuild keeps the real site's structure and content, installs afrigov from the CDN the way an agency would, and is checked on every page with <a href="https://github.com/omoyolab/afrigov-audit">afrigov-audit</a>. Every gap found goes back into afrigov; the findings are in each folder.</p>
      </div>

      <h2>Rebuilds</h2>
      <ul class="ag-cards ag-cards--wide">${cards}
      </ul>

      <div class="ag-prose">
        <h2>Scores</h2>
      </div>
      <div class="ag-table-wrap" role="region" aria-label="Scores" tabindex="0">
        <table class="ag-table">
          <caption>Accessibility score out of 100, real site and rebuild</caption>
          <thead>
            <tr><th scope="col">Site</th><th scope="col">Page</th><th scope="col" class="ag-table__numeric">Real site</th><th scope="col" class="ag-table__numeric">Rebuild</th></tr>
          </thead>
          <tbody>
            ${rows}
          </tbody>
        </table>
      </div>
      <div class="ag-prose">
        <p>Last checked <time datetime="${scores.checkedAt}">${scores.checkedAt}</time> with ${esc(scores.tool ?? "afrigov-audit")}, at phone and desktop widths. The badges and this table come from the audit and update automatically every week. A rebuild's badge is its lowest-scoring page. Automated checks find about a third of real accessibility problems; a score of 100 means the automated checks pass. Testing with a screen reader still has to be done by a person.</p>
        <h2>What the rebuilds changed in afrigov</h2>
        <p>The first rebuild logged 17 findings. They became the back link, dated list, image and figure, download link, empty state, hero, statement, social links, band and the photo gallery pattern, released as afrigov 0.5 to 0.8. <a href="https://github.com/omoyolab/afrigov-usecases/blob/main/fmcide/FINDINGS.md">Read the findings</a>.</p>
        <p>The second rebuild, a service agency in another country, logged 15. They became the flag stripe, the accent band, feature, people, steps and key figures, released as afrigov 0.9. Two are open issues: a contents list, and finding an entry in a long list. <a href="https://github.com/omoyolab/afrigov-usecases/blob/main/nia-gh/FINDINGS.md">Read the findings</a>.</p>
        <p>The third rebuild, a ministry in Ghana, needed what most government sites have and afrigov did not: dropdown menus and a photograph with the title over it. Both went into afrigov 0.10 as section menus and the panel hero. <a href="https://github.com/omoyolab/afrigov-usecases/blob/main/moh-gh/FINDINGS.md">Read the findings</a>.</p>
      </div>
    </main>

    <footer class="ag-footer">
      <div class="ag-container">
        <div class="ag-footer__bar">
          <p>Unofficial rebuilds on <a href="https://github.com/omoyolab/afrigov">afrigov</a>. Each government and its agencies own their content and marks. <a href="https://github.com/omoyolab/afrigov-usecases">Source</a>.</p>
        </div>
      </div>
    </footer>
  </body>
</html>
`;
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
