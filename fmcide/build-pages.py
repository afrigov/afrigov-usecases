# Generates the rebuilt pages from one shell. Run: python3 build-pages.py
import os, html, re
CDN = os.environ.get("AFRIGOV_CDN", "https://cdn.jsdelivr.net/npm/afrigov@0.11/dist/")
NAV = [("index.html","Home"),("about.html","About"),("initiatives.html","Initiatives"),("media.html","Media"),("ict-hubs.html","ICT Hubs"),("project-bridge.html","Project BRIDGE"),("pebec.html","PEBEC")]

ORG = "Federal Ministry of Communications, Innovation and Digital Economy"

def describe(title, main):
    """One or two sentences for the description: the page's own lead paragraph, or its first paragraph."""
    m = re.search(r'<p class="ag-lead[^"]*">(.*?)</p>', main, flags=re.S) or re.search(r"<p>(.*?)</p>", main, flags=re.S)
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else title
    if len(text) > 158:
        text = text[:158].rsplit(" ", 1)[0].rstrip(",;:") + "…"
    return text

def shell(title, main, current=None, root="", extra_css="", breadcrumb=None):
    page_title = title if title == ORG else f"{title} – {ORG}"
    description = html.escape(describe(title, main), quote=True)
    r = root
    nav = "\n".join(f'            <li><a class="ag-nav__link" href="{r}{h}"{" aria-current=\"page\"" if label==current else ""}>{label}</a></li>' for h,label in NAV)
    crumb = ""
    if breadcrumb:
        items = "".join(f'<li><a href="{r}{h}">{t}</a></li>' for h,t in breadcrumb[:-1]) + f'<li><span aria-current="page">{breadcrumb[-1][1]}</span></li>'
        crumb = f'      <nav aria-label="Breadcrumb"><ol class="ag-breadcrumb">{items}</ol></nav>\n'
    return f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{html.escape(page_title)}</title>
    <meta name="description" content="{description}" />
    <!-- An unofficial rebuild stays out of search results, so it never competes with the ministry's own site. -->
    <meta name="robots" content="noindex" />
    <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin />
    <!-- Collapses the menu on phones from the first paint, so the page does not jump when the script arrives. -->
    <script>
      document.documentElement.classList.add("ag-js");
      addEventListener("load", function () {{
        if (!window.AfriGov) document.documentElement.classList.remove("ag-js");
      }});
    </script>
    <link rel="stylesheet" href="{CDN}core.min.css" />
    <link rel="stylesheet" href="{CDN}ng.min.css" />
  </head>
  <body>
    <a class="ag-skip-link" href="#main">Skip to main content</a>

    <section class="ag-banner" aria-label="Unofficial website notice">
      <div class="ag-container ag-banner__inner">
        <span class="ag-flag" aria-hidden="true"><span></span><span></span><span></span></span>
        <p class="ag-banner__text">An unofficial rebuild of a Federal Republic of Nigeria website</p>
        <details class="ag-banner__details">
          <summary>How you know this is unofficial</summary>
          <p>This is a demonstration built on afrigov. It is not run by the ministry. The real website is <a href="https://fmcide.gov.ng/">fmcide.gov.ng</a>.</p>
          <p>Official websites use .gov.ng. This one does not, and it carries no government seal.</p>
        </details>
      </div>
    </section>

    <header class="ag-header ag-header--stacked">
      <div class="ag-container ag-header__inner">
        <a class="ag-header__brand" href="{r}index.html">
          <img class="ag-header__logo ag-header__logo--lg" src="{r}assets/mark.svg" alt="" width="56" height="56" />
          <span>
            <span class="ag-header__org">Federal Ministry of Communications, Innovation and Digital Economy</span>
          </span>
        </a>
        <button class="ag-header__toggle" type="button" aria-expanded="false" aria-controls="nav" data-ag-toggle>Menu</button>
        <nav class="ag-header__nav" id="nav" aria-label="Main">
          <ul class="ag-nav">
{nav}
          </ul>
        </nav>
      </div>
    </header>

    <main class="ag-main ag-container" id="main" tabindex="-1">
{crumb}{main}
    </main>

    <footer class="ag-footer">
      <div class="ag-container">
        <div class="ag-footer__columns">
          <div>
            <h2 class="ag-footer__heading">Ministry</h2>
            <ul class="ag-footer__list">
              <li><a href="{r}about.html">About</a></li>
              <li><a href="{r}initiatives.html">Initiatives</a></li>
              <li><a href="{r}resources.html">Resources</a></li>
            </ul>
          </div>
          <div>
            <h2 class="ag-footer__heading">Media</h2>
            <ul class="ag-footer__list">
              <li><a href="{r}news.html">News</a></li>
              <li><a href="{r}events.html">Events</a></li>
              <li><a href="{r}articles.html">Articles</a></li>
              <li><a href="{r}gallery.html">Gallery</a></li>
            </ul>
          </div>
          <div>
            <h2 class="ag-footer__heading">Contact</h2>
            <address class="ag-footer__address">
              Federal Secretariat Complex Phase I,<br />
              Annex III, Shehu Shagari Way,<br />
              FCT Nigeria.<br />
              P.M.B. 12578
            </address>
            <ul class="ag-footer__list">
              <li><a href="mailto:info@fmcide.gov.ng">info@fmcide.gov.ng</a></li>
              <li><a href="{r}contact.html">Send a message</a></li>
            </ul>
            <ul class="ag-social">
              <li><a class="ag-social__link" href="https://www.facebook.com/FMoCDE"><svg class="ag-social__icon" aria-hidden="true" viewBox="0 0 24 24"><path d="M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z"/></svg>Facebook</a></li>
              <li><a class="ag-social__link" href="https://x.com/fmcidenigeria"><svg class="ag-social__icon" aria-hidden="true" viewBox="0 0 24 24"><path d="M14.234 10.162 22.977 0h-2.072l-7.591 8.824L7.251 0H.258l9.168 13.343L.258 24H2.33l8.016-9.318L16.749 24h6.993zm-2.837 3.299-.929-1.329L3.076 1.56h3.182l5.965 8.532.929 1.329 7.754 11.09h-3.182z"/></svg>X</a></li>
              <li><a class="ag-social__link" href="https://www.instagram.com/fmocde"><svg class="ag-social__icon" aria-hidden="true" viewBox="0 0 24 24"><path d="M7.0301.084c-1.2768.0602-2.1487.264-2.911.5634-.7888.3075-1.4575.72-2.1228 1.3877-.6652.6677-1.075 1.3368-1.3802 2.127-.2954.7638-.4956 1.6365-.552 2.914-.0564 1.2775-.0689 1.6882-.0626 4.947.0062 3.2586.0206 3.6671.0825 4.9473.061 1.2765.264 2.1482.5635 2.9107.308.7889.72 1.4573 1.388 2.1228.6679.6655 1.3365 1.0743 2.1285 1.38.7632.295 1.6361.4961 2.9134.552 1.2773.056 1.6884.069 4.9462.0627 3.2578-.0062 3.668-.0207 4.9478-.0814 1.28-.0607 2.147-.2652 2.9098-.5633.7889-.3086 1.4578-.72 2.1228-1.3881.665-.6682 1.0745-1.3378 1.3795-2.1284.2957-.7632.4966-1.636.552-2.9124.056-1.2809.0692-1.6898.063-4.948-.0063-3.2583-.021-3.6668-.0817-4.9465-.0607-1.2797-.264-2.1487-.5633-2.9117-.3084-.7889-.72-1.4568-1.3876-2.1228C21.2982 1.33 20.628.9208 19.8378.6165 19.074.321 18.2017.1197 16.9244.0645 15.6471.0093 15.236-.005 11.977.0014 8.718.0076 8.31.0215 7.0301.0839m.1402 21.6932c-1.17-.0509-1.8053-.2453-2.2287-.408-.5606-.216-.96-.4771-1.3819-.895-.422-.4178-.6811-.8186-.9-1.378-.1644-.4234-.3624-1.058-.4171-2.228-.0595-1.2645-.072-1.6442-.079-4.848-.007-3.2037.0053-3.583.0607-4.848.05-1.169.2456-1.805.408-2.2282.216-.5613.4762-.96.895-1.3816.4188-.4217.8184-.6814 1.3783-.9003.423-.1651 1.0575-.3614 2.227-.4171 1.2655-.06 1.6447-.072 4.848-.079 3.2033-.007 3.5835.005 4.8495.0608 1.169.0508 1.8053.2445 2.228.408.5608.216.96.4754 1.3816.895.4217.4194.6816.8176.9005 1.3787.1653.4217.3617 1.056.4169 2.2263.0602 1.2655.0739 1.645.0796 4.848.0058 3.203-.0055 3.5834-.061 4.848-.051 1.17-.245 1.8055-.408 2.2294-.216.5604-.4763.96-.8954 1.3814-.419.4215-.8181.6811-1.3783.9-.4224.1649-1.0577.3617-2.2262.4174-1.2656.0595-1.6448.072-4.8493.079-3.2045.007-3.5825-.006-4.848-.0608M16.953 5.5864A1.44 1.44 0 1 0 18.39 4.144a1.44 1.44 0 0 0-1.437 1.4424M5.8385 12.012c.0067 3.4032 2.7706 6.1557 6.173 6.1493 3.4026-.0065 6.157-2.7701 6.1506-6.1733-.0065-3.4032-2.771-6.1565-6.174-6.1498-3.403.0067-6.156 2.771-6.1496 6.1738M8 12.0077a4 4 0 1 1 4.008 3.9921A3.9996 3.9996 0 0 1 8 12.0077"/></svg>Instagram</a></li>
              <li><a class="ag-social__link" href="https://www.linkedin.com/company/fmcidenigeria/"><svg class="ag-social__icon" aria-hidden="true" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>LinkedIn</a></li>
            </ul>
          </div>
        </div>
        <div class="ag-footer__bar">
          <span class="ag-flag" aria-hidden="true"><span></span><span></span><span></span></span>
          <p>Unofficial rebuild of <a href="https://fmcide.gov.ng/">fmcide.gov.ng</a> on <a href="https://github.com/omoyolab/afrigov">afrigov</a>, for demonstration. The ministry and its agencies own their content and marks.</p>
        </div>
      </div>
    </footer>
{extra_css}
    <script src="{CDN}afrigov.iife.js"></script>
  </body>
</html>
'''

def write(path, content):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    open(path, "w").write(content)

P = {}
P["about.html"] = shell("About the ministry", '''      <div class="ag-prose">
        <h1 class="ag-heading-xl">About the ministry</h1>
        <p class="ag-lead">Pioneering Nigeria's digital future. The Federal Ministry of Communications, Innovation and Digital Economy was created in 2011 to drive economic growth through digital technology and innovation.</p>
        <p>Our mandate is to speed up the diversification of the Nigerian economy by raising productivity in its critical sectors.</p>

        <h2 id="journey">Our journey</h2>
        <p>The ministry was established in 2011 as the Ministry of Communication Technology, at a turning point in Nigeria's move towards a knowledge-based economy and an inclusive information society. It became the Federal Ministry of Communications, Innovation and Digital Economy in 2023, with a wider brief that covers innovation and the whole digital economy.</p>
        <p>From the start the work has rested on one belief: in the digital age, access to information and technology is a right, not a luxury. The first task was to close the divide between the country's cities and its rural communities, and it still is.</p>

        <h2 id="why">Why we exist</h2>
        <p>The ministry exists to use information and communication technology for three things: creating jobs, growing the economy, and making government transparent. ICT has been a cornerstone of the national development plan since the ministry's first day.</p>

        <h2 id="minister">Meet the minister</h2>
        <p>Dr 'Bosun Tijani is the Honourable Minister of Communications, Innovation and Digital Economy. He leads the ministry's strategic blueprint for the digital economy and the agencies that deliver it, with a view of Nigeria as a digital economy that drives progress, strengthens security and diversifies the economy.</p>
      </div>
      <section class="ag-statement" aria-labelledby="minister-message">
        <figure class="ag-figure ag-statement__media">
          <img class="ag-figure__image" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1 1'%3E%3Crect width='1' height='1' fill='%23dfe6ec'/%3E%3C/svg%3E" alt="" width="320" height="320" loading="lazy" />
          <figcaption class="ag-figure__caption">The minister's portrait goes here.</figcaption>
        </figure>
        <div class="ag-statement__body">
          <h3 class="ag-statement__title" id="minister-message">Message from the minister</h3>
          <p>I am truly honoured to serve our great nation in this capacity as Minister of Communications, Innovation and Digital Economy as we work towards actualising the Renewed Hope Agenda of President Bola Ahmed Tinubu, GCFR.</p>
          <p>As we stand on the cusp of a new era, characterised by rapid technological advancements, I believe it is our collective responsibility to harness the transformative power of innovation and technology, coupled with the ingenuity of the Nigerian people, young and old, to accelerate our development and position ourselves at the forefront of the global digital discourse.</p>
          <p>To achieve this, with the input of critical stakeholders, we have co-created a Strategic Blueprint which will serve as a framework to guide our activities and ensure that we deliver on set targets for the prosperity of all Nigerians.</p>
          <p>The Blueprint is a detailed and progressive framework that encompasses five key pillars: Knowledge, Policy, Infrastructure, Innovation, Entrepreneurship and Capital, and Trade.</p>
          <p>Each pillar is integral to our mission and interconnected with the others, forming the foundation of our strategy. Together, let us embark on this exciting journey towards a prosperous digital Nigeria.</p>
          <p>Yours sincerely,</p>
          <p class="ag-statement__by"><strong>Dr 'Bosun Tijani</strong>Honourable Minister for Communications, Innovation and Digital Economy, Federal Republic of Nigeria</p>
          <p>Quoted from the ministry's website, <a href="https://fmcide.gov.ng/">fmcide.gov.ng</a>.</p>
        </div>
      </section>
      <div class="ag-prose">
        <h2 id="mandate">Our mandate</h2>
        <p>The Federal Government has given the ministry four responsibilities.</p>
        <ol>
          <li><strong>Enable universal access.</strong> Widespread, seamless and affordable access to communications infrastructure across the whole country.</li>
          <li><strong>Advance ICT integration.</strong> ICT in every part of life, from digital content and home-grown software to public and private services delivered over the internet.</li>
          <li><strong>Grow the ICT industry.</strong> A larger ICT industry and a larger share of national output from it.</li>
          <li><strong>Drive transparency and efficiency.</strong> ICT that makes government open and public services better and cheaper to deliver.</li>
        </ol>

        <h2 id="pledge">Our pledge</h2>
        <p>We are your partners in building a digital Nigeria. This is what you can expect from us.</p>
        <ul>
          <li>Innovation at the heart of our work: the latest technology, used for prosperity and creativity.</li>
          <li>Transparent governance, with technology as the instrument of openness and accountability.</li>
          <li>A thriving economy built on ICT, with jobs and opportunity for all.</li>
          <li>Your safety and your data protected, through investment in cybersecurity.</li>
        </ul>

        <h2 id="vision">Vision and mission</h2>
        <dl class="ag-summary">
          <div class="ag-summary__row"><dt class="ag-summary__key">Vision</dt><dd class="ag-summary__value">A robust digital economy that enhances security, increases transparency and diversifies the Nigerian economy.</dd></div>
          <div class="ag-summary__row"><dt class="ag-summary__key">Mission</dt><dd class="ag-summary__value">Digital technologies for national economic development.</dd></div>
        </dl>

        <h2 id="agencies">Structure and agencies</h2>
        <p>The ministry supervises seven agencies: NITDA, the Nigeria Data Protection Commission, the Nigerian Communications Commission, Galaxy Backbone, NIGCOMSAT, NIPOST and the Universal Service Provision Fund. They are listed with links on the <a href="index.html">home page</a>. <a href="index.html#contact">Contact details</a> are there too.</p>
      </div>''', current="About", breadcrumb=[("index.html","Home"),("about.html","About")])

inits = [
 ("project-bridge","Project BRIDGE","A special purpose vehicle to lay at least 90,000 km of fibre optic cable as Nigeria's core connectivity infrastructure, under a public-private partnership.","project-bridge.html"),
 ("3mtt","3 Million Technical Talent","Building Nigeria's technical talent backbone to power the digital economy and make Nigeria a net exporter of talent. Applications are open.","3mtt/start.html"),
 ("ai-research","Nigeria Artificial Intelligence Research Scheme","Financial support, knowledge sharing and collaboration for a lasting AI ecosystem in Nigeria. Run by NITDA.","https://airg.nitda.gov.ng/"),
 ("ai","National Artificial Intelligence Strategy","Steering the AI revolution towards national goals: job creation, social inclusion and sustainable development.","https://www.linkedin.com/pulse/co-creating-national-artificial-intelligence-strategy-tijani/"),
 ("digital-nigeria","Digital Nigeria","A Federal Government programme giving innovators and entrepreneurs the skills to thrive in the emerging digital economy.","https://digitalnigeria.gov.ng/"),
 ("local-content","Local content and capacity","An ICT industry that contributes to national development targets and drives the production, sale and use of high-quality Nigerian IT products.",None),
 ("e-government","E-government","Four goals for e-government across all ministries, departments and agencies: connected government, informed citizenry, open data and open government partnership.","initiatives/e-government.html"),
]
cards = "".join(f'''
        <li class="ag-card" id="{i}">
          <h2 class="ag-card__title">{f'<a class="ag-card__link" href="{link}">{name}</a>' if link else name}</h2>
          <p class="ag-card__text">{desc}</p>
        </li>''' for i,name,desc,link in inits)
P["initiatives.html"] = shell("Initiatives", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Initiatives</h1>
        <p class="ag-lead">The programmes through which the ministry drives inclusive growth and the digital economy.</p>
      </div>
      <ul class="ag-cards">{cards}
      </ul>''', current="Initiatives", breadcrumb=[("index.html","Home"),("initiatives.html","Initiatives")])

P["index.html"] = shell("Federal Ministry of Communications, Innovation and Digital Economy", f'''      <div class="ag-hero ag-hero--image">
        <div class="ag-hero__inner">
          <div>
            <h1 class="ag-heading-xl ag-hero__title">Driving economic growth through digital technology and innovation</h1>
            <p class="ag-lead ag-hero__lead">
              The ministry leads Nigeria's digital economy: connectivity, technical talent, data, innovation and the
              digital transformation of government.
            </p>
            <div class="ag-button-group ag-hero__actions">
              <a class="ag-button ag-button--start" href="initiatives.html">Our initiatives</a>
            </div>
          </div>
          <figure class="ag-figure ag-hero__media">
            <img class="ag-figure__image" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 4 3'%3E%3Crect width='4' height='3' fill='%23dfe6ec'/%3E%3C/svg%3E" alt="" width="800" height="600" />
            <figcaption class="ag-figure__caption">
              A photograph of the ministry's work goes here: fibre being laid, 3MTT fellows, a data centre.
            </figcaption>
          </figure>
        </div>
      </div>

      <section class="ag-statement" aria-labelledby="minister-message">
        <figure class="ag-figure ag-statement__media">
          <img class="ag-figure__image" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1 1'%3E%3Crect width='1' height='1' fill='%23dfe6ec'/%3E%3C/svg%3E" alt="" width="320" height="320" loading="lazy" />
          <figcaption class="ag-figure__caption">The minister's portrait goes here.</figcaption>
        </figure>
        <div class="ag-statement__body">
          <h2 class="ag-statement__title" id="minister-message">A message from the Minister</h2>
          <p>It is an honour to serve Nigeria in this role as we work towards the Renewed Hope Agenda. We are at the start of a new era of rapid technological change, and it is our shared responsibility to put innovation, technology and the ingenuity of Nigerians, young and old, to work for the country's development.</p>
          <p>With the input of stakeholders across the sector we have co-created a strategic blueprint for the digital economy. It is the plan this ministry is delivering.</p>
          <p class="ag-statement__by"><strong>Dr 'Bosun Tijani</strong>Honourable Minister of Communications, Innovation and Digital Economy</p>
          <p><a href="about.html#minister">Read the full message</a>. Drawn from the minister's welcome on the ministry's website.</p>
        </div>
      </section>

      <div class="ag-alert" role="status">
        <h2 class="ag-alert__title">Strategic blueprint</h2>
        <p>
          The ministry's plan for the digital economy, in five pillars.
          <a class="ag-download" href="https://fmcide.gov.ng/wp-content/uploads/2023/11/blueprint.pdf">Read the strategic blueprint <span class="ag-download__meta">(PDF, 4.1 MB)</span></a>
        </p>
      </div>

      <h2>Initiatives</h2>
      <ul class="ag-cards">{cards}
      </ul>
      <p><a href="initiatives.html">All initiatives</a></p>

      <h2 id="news">News</h2>
      <ul class="ag-list">
        <li class="ag-list__item">
          <a class="ag-list__link" href="news/goalkeepers-champion.html">Minister named 2026 Gates Foundation Goalkeepers Champion</a>
          <span class="ag-list__meta">18 September 2026</span>
        </li>
        <li class="ag-list__item">
          <a class="ag-list__link" href="news.html">Minister commissions Nigeria Data Protection Commission headquarters</a>
          <span class="ag-list__meta">15 September 2026</span>
        </li>
        <li class="ag-list__item">
          <a class="ag-list__link" href="news.html">Federal Government unveils National Digital Cloud Policy</a>
          <span class="ag-list__meta">17 August 2026</span>
        </li>
        <li class="ag-list__item">
          <a class="ag-list__link" href="news.html">ATU Conference of Plenipotentiaries concludes in Abuja</a>
          <span class="ag-list__meta">25 July 2026</span>
        </li>
        <li class="ag-list__item">
          <a class="ag-list__link" href="news.html">ATU Plenipotentiary Conference opens in Abuja</a>
          <span class="ag-list__meta">23 July 2026</span>
        </li>
      </ul>
      <p><a href="news.html">All news</a></p>

      <h2>Agencies</h2>
      <p class="ag-prose">The ministry supervises seven agencies.</p>
      <ul class="ag-cards">
        <li class="ag-card"><div class="ag-card__logo"><img src="assets/agencies/nitda.webp" alt="" width="252" height="112" loading="lazy" /></div><h3 class="ag-card__title"><a class="ag-card__link" href="https://nitda.gov.ng/">NITDA</a></h3><p class="ag-card__text">National Information Technology Development Agency</p></li>
        <li class="ag-card"><div class="ag-card__logo"><img src="assets/agencies/ndpc.webp" alt="" width="343" height="112" loading="lazy" /></div><h3 class="ag-card__title"><a class="ag-card__link" href="https://ndpc.gov.ng/">NDPC</a></h3><p class="ag-card__text">Nigeria Data Protection Commission</p></li>
        <li class="ag-card"><div class="ag-card__logo"><img src="assets/agencies/ncc.webp" alt="" width="159" height="112" loading="lazy" /></div><h3 class="ag-card__title"><a class="ag-card__link" href="https://ncc.gov.ng/">NCC</a></h3><p class="ag-card__text">Nigerian Communications Commission</p></li>
        <li class="ag-card"><div class="ag-card__logo"><img src="assets/agencies/galaxy.webp" alt="" width="171" height="112" loading="lazy" /></div><h3 class="ag-card__title"><a class="ag-card__link" href="https://galaxybackbone.com.ng/">Galaxy Backbone</a></h3><p class="ag-card__text">Government network and data centre operator</p></li>
        <li class="ag-card"><div class="ag-card__logo"><img src="assets/agencies/comsat.webp" alt="" width="200" height="112" loading="lazy" /></div><h3 class="ag-card__title"><a class="ag-card__link" href="https://nigcomsat.gov.ng/">NIGCOMSAT</a></h3><p class="ag-card__text">Nigerian Communications Satellite</p></li>
        <li class="ag-card"><div class="ag-card__logo"><img src="assets/agencies/nipost.webp" alt="" width="131" height="112" loading="lazy" /></div><h3 class="ag-card__title"><a class="ag-card__link" href="https://nipost.gov.ng/">NIPOST</a></h3><p class="ag-card__text">Nigerian Postal Service</p></li>
        <li class="ag-card"><div class="ag-card__logo"><img src="assets/agencies/uspf.webp" alt="" width="112" height="112" loading="lazy" /></div><h3 class="ag-card__title"><a class="ag-card__link" href="https://uspf.gov.ng/">USPF</a></h3><p class="ag-card__text">Universal Service Provision Fund</p></li>
      </ul>

      <div class="ag-prose">
        <h2 id="contact">Contact</h2>
        <address>
          Federal Secretariat Complex Phase I,<br />
          Annex III, Shehu Shagari Way,<br />
          FCT Nigeria.<br />
          P.M.B. 12578
        </address>
        <p>Email <a href="mailto:info@fmcide.gov.ng">info@fmcide.gov.ng</a>, or <a href="contact.html">send a message</a>.</p>
      </div>''', current="Home")

P["project-bridge.html"] = shell("Project BRIDGE", '''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Project BRIDGE</h1>
        <p class="ag-lead">Building Resilient Digital Infrastructure for Growth: at least 90,000 km of fibre optic cable as Nigeria's national backbone, delivered through a public-private partnership.</p>

        <h2 id="what">What it is</h2>
        <p>A special purpose vehicle, owned jointly by government and private investors, will lay at least 90,000 km of fibre optic cable as the core connectivity infrastructure for universal access to ICT across Nigeria. It completes the national target of 120,000 km set in the National Broadband Plan 2020 to 2025.</p>
        <p>The total cost is estimated at $2 billion, funded by sovereign loans from development finance institutions, including the World Bank and the African Development Bank, and equity from private companies. The Nigerian government will hold between 25% and 49%. The vehicle is run independently as a limited liability company with a board and management drawn from telecommunications and related industries.</p>

        <h2 id="outcomes">Expected outcomes</h2>
      </div>
      <dl class="ag-summary">
        <div class="ag-summary__row"><dt class="ag-summary__key">Connectivity and access</dt><dd class="ag-summary__value">Faster, more reliable internet across the country, penetration above 70%, and access for millions of households, businesses, schools and hospitals, especially in underserved regions.</dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Economic development</dt><dd class="ag-summary__value">Up to 20,000 direct and 150,000 indirect jobs, and up to 1.5% growth in GDP per person, taking GDP from about $472.6 billion to about $502 billion in four years.</dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Skills</dt><dd class="ag-summary__value">5,000 young Nigerians trained through the Digital Bridge Institute, to roll out the network and maintain it afterwards.</dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Local manufacturing</dt><dd class="ag-summary__value">International fibre manufacturers are working with Nigerian cable companies, so that cables and components are made here and exported to West Africa.</dd></div>
      </dl>
      <div class="ag-prose">
        <h2 id="progress">Progress</h2>
        <ol>
          <li>The Federal Executive Council has approved the special purpose vehicle, as a public-private partnership, to own and deliver the project.</li>
          <li>Eleven development finance institutions have shown interest, including AfDB, AFC, AFD, DFC, the EU, IFC, EIB, IsDB, the World Bank Group, BII and EBRD. $845 million in funding commitments is secured from the World Bank Group, AfDB, AFC and the EU. Talks with the others continue.</li>
          <li>Preliminary technical, commercial and regulatory studies have begun.</li>
          <li>A dedicated project team of professionals from the private and public sectors oversees the preparatory work.</li>
          <li>The National Broadband Alliance for Nigeria brings government, private companies and civil society together to use broadband for development.</li>
          <li>A public consultation with the private sector drew 30 companies formally registering to invest.</li>
          <li>An environmental and social management plan is being prepared.</li>
        </ol>
        <h3>Notices</h3>
        <ul class="ag-list">
          <li class="ag-list__item"><a class="ag-list__link" href="https://fmcide.gov.ng/project-bridge-preparation-of-low-level-designs-for-the-rollout-of-40000-km-of-fibre-optic-networks/">Preparation of low-level designs for the rollout of 40,000 km of fibre optic networks</a><span class="ag-list__meta">Procurement notice</span></li>
          <li class="ag-list__item"><a class="ag-list__link" href="https://fmcide.gov.ng/general-procurement-notice-nigeria-sovereign-fibre-bridge-project/">General procurement notice: Nigeria Sovereign Fibre (BRIDGE) Project</a><span class="ag-list__meta">Procurement notice</span></li>
        </ul>

        <h2 id="partners">Committed partners</h2>
      </div>
      <div class="ag-table-wrap" role="region" aria-label="Committed partners" tabindex="0">
        <table class="ag-table">
          <caption>Committed funding</caption>
          <thead><tr><th scope="col">Partner</th><th scope="col" class="ag-table__numeric">Commitment</th></tr></thead>
          <tbody>
            <tr><th scope="row"><a href="https://projects.worldbank.org/en/projects-operations/project-detail/P508383">World Bank</a></th><td class="ag-table__numeric">$500 million</td></tr>
            <tr><th scope="row">African Development Bank</th><td class="ag-table__numeric">$200 million</td></tr>
            <tr><th scope="row">European Bank for Reconstruction and Development</th><td class="ag-table__numeric">$100 million</td></tr>
          </tbody>
        </table>
      </div>
      <div class="ag-prose">
        <h2 id="everyday">What it means for everyday Nigerians</h2>
        <p>About 216,871 schools, tertiary institutions, health centres and social institutions cannot get online reliably or use the internet for their work. With policies for digital inclusion, a growing startup scene and more smartphones every year, demand for infrastructure has never been higher.</p>
        <ul>
          <li>Connected primary, secondary and tertiary schools, which improves what students learn and builds digital literacy from an early age.</li>
          <li>Connected hospitals and clinics, with real-time data, more accurate diagnosis and faster service.</li>
        </ul>

        <h2 id="questions">Questions</h2>
      </div>
      <div class="ag-accordion">
        <details class="ag-accordion__item"><summary class="ag-accordion__summary">What is Project BRIDGE?</summary><div class="ag-accordion__body"><p>A project to lay a 90,000 km national fibre backbone and expand Nigeria's digital infrastructure.</p></div></details>
        <details class="ag-accordion__item"><summary class="ag-accordion__summary">What is the goal?</summary><div class="ag-accordion__body"><p>More than 33 million Nigerians are still offline. The project is for inclusion, access to education and financial services, growth, jobs, digital literacy, opportunities for young Nigerians and national security.</p></div></details>
        <details class="ag-accordion__item"><summary class="ag-accordion__summary">Why 90,000 km?</summary><div class="ag-accordion__body"><p>It is the amount left to reach the 120,000 km target in the <a href="https://digitalrightslawyers.org/wp-content/uploads/2021/01/Nigerian_National_Broadband_Plan_2020-2025.pdf">National Broadband Plan 2020 to 2025 <span class="ag-download__meta">(PDF)</span></a>.</p></div></details>
        <details class="ag-accordion__item"><summary class="ag-accordion__summary">What is the timeline?</summary><div class="ag-accordion__body"><p>Rollout runs over five years, starting with 30,000 km in the first year. The special purpose vehicle was to be incorporated in the third quarter of 2025 to lead delivery. Phase timelines and milestones are published here as they are settled.</p></div></details>
        <details class="ag-accordion__item"><summary class="ag-accordion__summary">How is it funded?</summary><div class="ag-accordion__body"><p>Sovereign loans from development finance institutions, including the World Bank Group and the African Development Bank, plus equity from private companies.</p></div></details>
        <details class="ag-accordion__item"><summary class="ag-accordion__summary">How can I get involved?</summary><div class="ag-accordion__body"><p>Vendor opportunities and public engagement forums are announced on this website. Check back regularly.</p></div></details>
        <details class="ag-accordion__item"><summary class="ag-accordion__summary">Who can I contact?</summary><div class="ag-accordion__body"><p>Email <a href="mailto:projectbridge@fmcide.gov.ng">projectbridge@fmcide.gov.ng</a>.</p></div></details>
      </div>
      <div class="ag-prose">
        <h2 id="grievance">Complaints about the project</h2>
        <p>The project's grievance mechanism is a simple, safe way for communities, people affected by the works, workers and other stakeholders to raise a complaint or concern. Every complaint is received, recorded, assessed and answered fairly within the published timelines, in confidence where needed.</p>
        <p>It is for project-related complaints only, not general enquiries.</p>
        <p><a class="ag-button ag-button--secondary" href="https://docs.google.com/forms/d/e/1FAIpQLSfAAZyyAGQJEwzJiTmV5WipThk4MJikM0YwYWcuXgF2Fj9T3A/viewform">Submit a complaint</a></p>
        <p>Or email <a href="mailto:projectbridge.complaints@gmail.com">projectbridge.complaints@gmail.com</a>.</p>
      </div>''', current="Project BRIDGE", breadcrumb=[("index.html","Home"),("initiatives.html","Initiatives"),("project-bridge.html","Project BRIDGE")])

P["initiatives/e-government.html"] = shell("E-government", '''      <div class="ag-prose">
        <h1 class="ag-heading-xl">E-government</h1>
        <p class="ag-lead">Four goals for e-government across every ministry, department and agency: connected government, an informed citizenry, open data and open government partnership.</p>
        <p>The ministry runs projects that give citizens and businesses easy access to government services. Each is chosen to spread e-government across the MDAs, which improves service delivery and drives transparency, accountability and good governance.</p>
        <h2>Programmes run by the E-Government department</h2>
        <dl class="ag-summary">
          <div class="ag-summary__row"><dt class="ag-summary__key">National E-Government Master Plan</dt><dd class="ag-summary__value">A roadmap for e-government across all federal MDAs, developed with the Government of Korea. The department leads its rollout: simpler services, better experience for citizens and businesses, more engagement, more transparency.</dd></div>
          <div class="ag-summary__row"><dt class="ag-summary__key">Government Service Portal</dt><dd class="ag-summary__value">One portal, <a href="https://services.gov.ng/">services.gov.ng</a>, for citizens, businesses and visitors to reach government services at any hour without travelling to an office.</dd></div>
          <div class="ag-summary__row"><dt class="ag-summary__key">Government Contact Centre</dt><dd class="ag-summary__value">Government services and information by phone, for anyone regardless of location, literacy or language. It has created jobs and gives citizens a way to send ideas and feedback.</dd></div>
          <div class="ag-summary__row"><dt class="ag-summary__key">Open Data Portal</dt><dd class="ag-summary__value"><a href="https://data.gov.ng/">data.gov.ng</a>, where MDAs publish non-sensitive data sets for the public, so citizens and businesses can use them in their decisions.</dd></div>
          <div class="ag-summary__row"><dt class="ag-summary__key">Electronic Document Management System</dt><dd class="ag-summary__value">Government documents moved online: better information security, lower cost, automated processes and easier access.</dd></div>
          <div class="ag-summary__row"><dt class="ag-summary__key">E-Government Capacity Building Programme</dt><dd class="ag-summary__value">Continuous service-wide training in e-governance. More than 2,000 public servants trained at federal and regional level.</dd></div>
          <div class="ag-summary__row"><dt class="ag-summary__key">National E-Health Strategic Framework</dt><dd class="ag-summary__value">Developed with the Federal Ministry of Health: ICT for better care, lower administrative cost, faster access to health information and more productive health workers.</dd></div>
        </dl>
        <p><a href="../initiatives.html">All initiatives</a></p>
      </div>''', current="Initiatives", root="../", breadcrumb=[("index.html","Home"),("initiatives.html","Initiatives"),("initiatives/e-government.html","E-government")])

P["media.html"] = shell("Media", '''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Media</h1>
        <p class="ag-lead">News, events, articles and photographs from the ministry.</p>
      </div>
      <ul class="ag-cards">
        <li class="ag-card"><h2 class="ag-card__title"><a class="ag-card__link" href="news.html">News</a></h2><p class="ag-card__text">Press releases and announcements.</p></li>
        <li class="ag-card"><h2 class="ag-card__title"><a class="ag-card__link" href="events.html">Events</a></h2><p class="ag-card__text">Conferences, launches and public engagements.</p></li>
        <li class="ag-card"><h2 class="ag-card__title"><a class="ag-card__link" href="articles.html">Articles</a></h2><p class="ag-card__text">Longer pieces on policy and strategy.</p></li>
        <li class="ag-card"><h2 class="ag-card__title"><a class="ag-card__link" href="gallery.html">Gallery</a></h2><p class="ag-card__text">Photographs from ministry events.</p></li>
      </ul>''', current="Media", breadcrumb=[("index.html","Home"),("media.html","Media")])

news = [
 ("news/goalkeepers-champion.html","Minister named 2026 Gates Foundation Goalkeepers Champion","18 September 2026"),
 ("https://fmcide.gov.ng/honourable-minister-dr-bosun-tijani-commissions-nigeria-data-protection-commission-headquarters-extols-president-bola-ahmed-tinubu-visionary-leadership/","Minister commissions Nigeria Data Protection Commission headquarters","15 September 2026"),
 ("https://fmcide.gov.ng/federal-government-unveils-national-digital-cloud-policy-to-drive-investment-digital-sovereignty-and-government-transformation/","Federal Government unveils National Digital Cloud Policy","17 August 2026"),
 ("https://fmcide.gov.ng/dr-tijani-calls-for-deeper-cooperation-among-member-states-as-atu-conference-of-plenipotentiaries-concludes-in-abuja/","ATU Conference of Plenipotentiaries concludes in Abuja","25 July 2026"),
 ("https://fmcide.gov.ng/atu-plenipotentiary-conference-kicks-off-in-abuja-with-vice-president-kashim-shettima-as-special-guest-of-honour/","ATU Plenipotentiary Conference opens in Abuja","23 July 2026"),
 ("https://fmcide.gov.ng/nigeria-set-to-host-africas-ict-ministers-as-atu-conference-of-plenipotentiaries-convenes-in-abuja/","Nigeria to host Africa's ICT ministers for the ATU conference","10 July 2026"),
]
THUMB = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 3 2'%3E%3Crect width='3' height='2' fill='%23dfe6ec'/%3E%3C/svg%3E"
def thumb_item(h,t,d):
    return f'\n        <li class="ag-list__item ag-list__item--media"><div class="ag-list__media"><img src="{THUMB}" alt="" width="240" height="160" loading="lazy" /></div><div class="ag-list__body"><a class="ag-list__link" href="{h}">{t}</a><span class="ag-list__meta">{d}</span></div></li>'
items = "".join(thumb_item(h,t,d) for h,t,d in news)
P["news.html"] = shell("News", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">News</h1>
      </div>
      <ul class="ag-list">{items}
      </ul>
      <nav aria-label="Pagination">
        <ul class="ag-pagination">
          <li><a class="ag-pagination__link" href="news.html" aria-current="page">1</a></li>
          <li><a class="ag-pagination__link" href="news.html">2</a></li>
          <li><a class="ag-pagination__link" href="news.html">3</a></li>
          <li><span class="ag-pagination__ellipsis" aria-hidden="true">…</span></li>
          <li><a class="ag-pagination__link" href="news.html">6</a></li>
          <li><a class="ag-pagination__link" href="news.html" rel="next">Next</a></li>
        </ul>
      </nav>''', current="Media", breadcrumb=[("index.html","Home"),("media.html","Media"),("news.html","News")])

P["news/goalkeepers-champion.html"] = shell("Minister named 2026 Gates Foundation Goalkeepers Champion", '''      <div class="ag-prose">
        <p class="ag-caption">News · 18 September 2026</p>
        <h1 class="ag-heading-xl">Minister named 2026 Gates Foundation Goalkeepers Champion</h1>
        <p class="ag-lead">The Gates Foundation has recognised Dr 'Bosun Tijani for his work on artificial intelligence and digital transformation in Africa.</p>
      </div>
      <figure class="ag-figure ag-figure--16-9" style="max-width: 48rem">
        <img class="ag-figure__image" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 9'%3E%3Crect width='16' height='9' fill='%23dfe6ec'/%3E%3C/svg%3E" alt="" width="1200" height="675" />
        <figcaption class="ag-figure__caption">Dr 'Bosun Tijani at the Goalkeepers event in New York. The photograph goes here; the ministry's photographs are not reproduced in this rebuild.</figcaption>
      </figure>
      <div class="ag-prose">
        <p>Goalkeepers Champions are people whose work, in the foundation's words, is helping shape a future where artificial intelligence expands opportunity rather than deepens inequality.</p>
        <p>Under the minister's leadership, Nigeria has published a National Artificial Intelligence Strategy, built N-ATLAS, a language model for Nigerian languages, and set up the National AI Trust.</p>
        <p>The recognition ceremony takes place in New York on 21 September 2026.</p>
        <div class="ag-inset"><p>Media enquiries: <a href="mailto:info@fmcide.gov.ng">info@fmcide.gov.ng</a></p></div>
      </div>''', current="Media", root="../", breadcrumb=[("index.html","Home"),("media.html","Media"),("news.html","News"),("news/goalkeepers-champion.html","Goalkeepers Champion")])

P["events.html"] = shell("Events", '''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Events</h1>
        <p class="ag-lead">Conferences, launches and public engagements run or hosted by the ministry.</p>
        <div class="ag-empty"><h2 class="ag-empty__title">No events are scheduled</h2><p>New events are announced here and in the <a href="news.html">news</a>. Past events are listed below.</p></div>
        <h2>Past events</h2>
      </div>
      <ul class="ag-list">
        <li class="ag-list__item"><a class="ag-list__link" href="news.html">National Digital Cloud Policy launch</a><span class="ag-list__meta">17 August 2026 · Abuja</span></li>
        <li class="ag-list__item"><a class="ag-list__link" href="news.html">ATU Conference of Plenipotentiaries</a><span class="ag-list__meta">21 to 25 July 2026 · Abuja</span></li>
      </ul>''', current="Media", breadcrumb=[("index.html","Home"),("media.html","Media"),("events.html","Events")])

arts = [
 ("articles/learning-community.html","Ministry launches 3MTT learning community with IHS Nigeria","23 October 2023"),
 ("articles.html","Strategic blueprint unveiled: three million young people for talent development","4 October 2023"),
 ("https://fmcide.gov.ng/nigeria-has-digital-capacity-to-compete-favourably-with-other-nations-bosun-tijani/","Nigeria has the digital capacity to compete with any nation","22 August 2023"),
 ("https://fmcide.gov.ng/dr-william-alo-inaugurates-teams-to-drive-pms-inplementation-in-communications-ministry-and-its-agencies-charges-members-to-be-committed/","Teams inaugurated to drive performance management across the ministry and its agencies","8 March 2023"),
 ("https://fmcide.gov.ng/pantami-sets-vision-for-accelerating-the-implementation-of-wsis-action-lines/","A vision for accelerating the WSIS action lines","2 June 2022"),
 ("https://fmcide.gov.ng/nigerias-digital-economy-minister-chairs-wsis-forum-2022-calls-for-high-level-multistakeholder-advisory-council/","Nigeria chairs WSIS Forum 2022, calls for a multistakeholder advisory council","31 May 2022"),
]
P["articles.html"] = shell("Articles", '''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Articles</h1>
        <p class="ag-lead">Longer pieces on policy and strategy from the ministry and its leadership.</p>
      </div>
      <ul class="ag-list">''' + "".join(thumb_item(h,t,d) for h,t,d in arts) + '''
      </ul>''', current="Media", breadcrumb=[("index.html","Home"),("media.html","Media"),("articles.html","Articles")])

P["articles/learning-community.html"] = shell("Ministry launches 3MTT learning community with IHS Nigeria", '''      <div class="ag-prose">
        <p class="ag-caption">Article · 23 October 2023</p>
        <h1 class="ag-heading-xl">Ministry launches 3MTT learning community with IHS Nigeria</h1>
        <p class="ag-lead">A three-year partnership will set up learning communities in all 36 states and the FCT, where 3MTT participants meet every week to learn, work together and build.</p>
      </div>
      <figure class="ag-figure ag-figure--16-9" style="max-width: 48rem">
        <img class="ag-figure__image" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 9'%3E%3Crect width='16' height='9' fill='%23dfe6ec'/%3E%3C/svg%3E" alt="" width="1200" height="675" />
        <figcaption class="ag-figure__caption">The minister and IHS Nigeria's chief executive at the launch. The photograph goes here; the ministry's photographs are not reproduced in this rebuild.</figcaption>
      </figure>
      <div class="ag-prose">
        <p>In support of the Three Million Technical Talent programme, the ministry has announced a three-year partnership with IHS Nigeria to establish the 3MTT Learning Community, a nationwide initiative to give Nigerians critical digital skills.</p>
        <p>The partnership sets up learning communities in every state and the FCT, with dedicated training spaces where participants gather weekly. The communities are also meant to strengthen local innovation ecosystems across the country.</p>
        <p>IHS Nigeria provides funding and industry expertise. It has committed to paying the salaries of the 37 learning community managers and to providing a learning platform for the programme.</p>
        <p>The Honourable Minister, Dr 'Bosun Tijani, said the funding is a significant commitment to the ministry's effort to build a pipeline of technical talent for the Renewed Hope Agenda.</p>
        <div class="ag-inset"><p>"Our journey towards a national digital transformation requires significant collaboration between the public and private sectors, and this is the first in a number of partnerships that we intend to secure to achieve our goals as outlined in our Strategic Blueprint."</p></div>
        <p>Mohamad Darwish, chief executive of IHS Nigeria, said the company takes pride in giving back to the communities where it operates, shares the government's commitment to Nigeria's economic growth, and hopes the initiative will feed into the President's agenda on job creation.</p>
        <p>The learning community is part of the overall 3MTT programme. <a href="../3mtt/start.html">Apply to 3MTT</a>.</p>
        <p class="ag-caption">Ekaete Umo, Head, Press and Public Relations</p>
      </div>''', current="Media", root="../", breadcrumb=[("index.html","Home"),("media.html","Media"),("articles.html","Articles"),("articles/learning-community.html","3MTT learning community")])

P["gallery.html"] = shell("Gallery", '''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Gallery</h1>
        <p class="ag-lead">Photographs from ministry events, one album per event. The ministry's photographs are not reproduced in this rebuild; the frames show where they go and how each is described.</p>
      </div>
      <ul class="ag-cards">
        <li class="ag-card">
          <div class="ag-card__image"><img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 3 2'%3E%3Crect width='3' height='2' fill='%23dfe6ec'/%3E%3C/svg%3E" alt="" width="600" height="400" loading="lazy" /></div>
          <h2 class="ag-card__title"><a class="ag-card__link" href="gallery/atu-conference.html">ATU Conference of Plenipotentiaries</a></h2>
          <p class="ag-card__text">21 to 25 July 2026 · 6 photos</p>
        </li>
        <li class="ag-card">
          <div class="ag-card__image"><img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 3 2'%3E%3Crect width='3' height='2' fill='%23dfe6ec'/%3E%3C/svg%3E" alt="" width="600" height="400" loading="lazy" /></div>
          <h2 class="ag-card__title"><a class="ag-card__link" href="gallery/atu-conference.html">Commissioning of the NDPC headquarters</a></h2>
          <p class="ag-card__text">15 September 2026 · 9 photos</p>
        </li>
        <li class="ag-card">
          <div class="ag-card__image"><img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 3 2'%3E%3Crect width='3' height='2' fill='%23dfe6ec'/%3E%3C/svg%3E" alt="" width="600" height="400" loading="lazy" /></div>
          <h2 class="ag-card__title"><a class="ag-card__link" href="gallery/atu-conference.html">3MTT learning community session</a></h2>
          <p class="ag-card__text">23 October 2023 · 12 photos</p>
        </li>
        <li class="ag-card">
          <div class="ag-card__image"><img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 3 2'%3E%3Crect width='3' height='2' fill='%23dfe6ec'/%3E%3C/svg%3E" alt="" width="600" height="400" loading="lazy" /></div>
          <h2 class="ag-card__title"><a class="ag-card__link" href="gallery/atu-conference.html">Launch of the National Digital Cloud Policy</a></h2>
          <p class="ag-card__text">17 August 2026 · 8 photos</p>
        </li>
      </ul>''', current="Media", breadcrumb=[("index.html","Home"),("media.html","Media"),("gallery.html","Gallery")])

P["gallery/atu-conference.html"] = shell("ATU Conference of Plenipotentiaries, July 2026", '''      <div class="ag-prose">
        <h1 class="ag-heading-xl">ATU Conference of Plenipotentiaries</h1>
        <p class="ag-lead">21 to 25 July 2026, Abuja. Nigeria hosted Africa's ICT ministers for the African Telecommunications Union's conference, opened by the Vice President.</p>
        <p>Tap a photograph to see it at full size. <a href="../news.html">Read the news from the conference</a>.</p>
      </div>
      <ul class="ag-gallery ag-gallery--2">
        <li>
          <figure class="ag-figure ag-figure--3-2">
            <a href="../assets/photos/placeholder.svg" aria-labelledby="photo-1-caption"><img class="ag-figure__image" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 3 2'%3E%3Crect width='3' height='2' fill='%23dfe6ec'/%3E%3C/svg%3E" alt="" width="600" height="400" loading="lazy" /></a>
            <figcaption class="ag-figure__caption" id="photo-1-caption">The Vice President, Kashim Shettima, opens the conference as special guest of honour.</figcaption>
          </figure>
        </li>
        <li>
          <figure class="ag-figure ag-figure--3-2">
            <a href="../assets/photos/placeholder.svg" aria-labelledby="photo-2-caption"><img class="ag-figure__image" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 3 2'%3E%3Crect width='3' height='2' fill='%23dfe6ec'/%3E%3C/svg%3E" alt="" width="600" height="400" loading="lazy" /></a>
            <figcaption class="ag-figure__caption" id="photo-2-caption">The minister welcomes delegates from 44 member states.</figcaption>
          </figure>
        </li>
        <li>
          <figure class="ag-figure ag-figure--3-2">
            <a href="../assets/photos/placeholder.svg" aria-labelledby="photo-3-caption"><img class="ag-figure__image" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 3 2'%3E%3Crect width='3' height='2' fill='%23dfe6ec'/%3E%3C/svg%3E" alt="" width="600" height="400" loading="lazy" /></a>
            <figcaption class="ag-figure__caption" id="photo-3-caption">Ministers in session on day two.</figcaption>
          </figure>
        </li>
        <li>
          <figure class="ag-figure ag-figure--3-2">
            <a href="../assets/photos/placeholder.svg" aria-labelledby="photo-4-caption"><img class="ag-figure__image" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 3 2'%3E%3Crect width='3' height='2' fill='%23dfe6ec'/%3E%3C/svg%3E" alt="" width="600" height="400" loading="lazy" /></a>
            <figcaption class="ag-figure__caption" id="photo-4-caption">The Nigerian delegation at the plenary.</figcaption>
          </figure>
        </li>
        <li>
          <figure class="ag-figure ag-figure--3-2">
            <a href="../assets/photos/placeholder.svg" aria-labelledby="photo-5-caption"><img class="ag-figure__image" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 3 2'%3E%3Crect width='3' height='2' fill='%23dfe6ec'/%3E%3C/svg%3E" alt="" width="600" height="400" loading="lazy" /></a>
            <figcaption class="ag-figure__caption" id="photo-5-caption">A side event on spectrum policy.</figcaption>
          </figure>
        </li>
        <li>
          <figure class="ag-figure ag-figure--3-2">
            <a href="../assets/photos/placeholder.svg" aria-labelledby="photo-6-caption"><img class="ag-figure__image" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 3 2'%3E%3Crect width='3' height='2' fill='%23dfe6ec'/%3E%3C/svg%3E" alt="" width="600" height="400" loading="lazy" /></a>
            <figcaption class="ag-figure__caption" id="photo-6-caption">The closing communiqué is signed.</figcaption>
          </figure>
        </li>
      </ul>
      <p><a href="../gallery.html">All albums</a></p>''', current="Media", root="../", breadcrumb=[("index.html","Home"),("media.html","Media"),("gallery.html","Gallery"),("gallery/atu-conference.html","ATU Conference")])

P["pebec.html"] = shell("PEBEC reforms", '''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Ease of doing business reforms</h1>
        <p class="ag-lead">The ministry's part in the Presidential Enabling Business Environment Council's reforms: making it faster and cheaper to build and run digital businesses in Nigeria.</p>
        <h2>What the ministry is responsible for</h2>
        <ul>
          <li>Harmonising right-of-way charges for fibre across states, so laying cable costs the same everywhere.</li>
          <li>Faster approvals for telecommunications infrastructure.</li>
          <li>Open, published service standards for the ministry's own processes.</li>
        </ul>
        <h2>Report a problem</h2>
        <p>If a ministry process is slower or costlier than its published standard, report it through PEBEC's <a href="https://pebec.gov.ng/">ReportGov</a> channel or <a href="contact.html">contact the ministry</a>.</p>
      </div>''', current="PEBEC", breadcrumb=[("index.html","Home"),("pebec.html","PEBEC")])

docs = {
 "Policies": [("National Digital Economy and E-Governance Bill 2024","Draft policy","PDF","2024"),("National Policy on 5G Networks","Policy","PDF","2022"),("National Blockchain Policy","Policy","PDF","2023")],
 "Reports": [("Nigeria E-Government Master Plan","Report","PDF","2019"),("Nigeria ICT Roadmap 2017 to 2020","Report","PDF","2017"),("National Broadband Plan 2013 to 2018","Report","PDF","2013"),("Right of Way Harmonisation","Report","PDF","June 2017"),("Nigeria Internet Governance Forum communiqué","Report","PDF","2018")],
 "Forms": [("Service and needs assessment form","Form","PDF","2024"),("Radio frequency licence application (DSS-FC-1)","Form","PDF","2023")],
 "Media kit": [("Ministry logo","Image","PNG","2023"),("Profile of the minister","Document","PDF","2023")],
}
tables = ""
for group, rows in docs.items():
    body = "".join(f'<tr><th scope="row"><a class="ag-download" href="resources.html">{t} <span class="ag-download__meta">({f})</span></a></th><td>{k}</td><td>{d}</td></tr>' for t,k,f,d in rows)
    tables += f'''
      <h2>{group}</h2>
      <div class="ag-table-wrap" role="region" aria-label="{group}" tabindex="0">
        <table class="ag-table"><caption class="ag-visually-hidden">{group}</caption><thead><tr><th scope="col">Document</th><th scope="col">Type</th><th scope="col">Year</th></tr></thead><tbody>{body}</tbody></table>
      </div>'''
P["resources.html"] = shell("Resources", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Resources</h1>
        <p class="ag-lead">Policies, reports, forms and media files published by the ministry. Each link says the file format. The real site does not state file sizes, so they are missing here too; a live service must add them.</p>
      </div>{tables}''', breadcrumb=[("index.html","Home"),("resources.html","Resources")])

P["contact.html"] = shell("Contact the ministry", '''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Contact the ministry</h1>
        <p class="ag-lead">Send a message and we will reply by email within five working days.</p>
      </div>
      <form action="contact-sent.html" method="get" novalidate>
        <div class="ag-field">
          <label class="ag-label" for="name">Your name</label>
          <input class="ag-input" id="name" name="name" type="text" autocomplete="name" />
        </div>
        <div class="ag-field">
          <label class="ag-label" for="email">Email address</label>
          <span class="ag-hint" id="email-hint">We will reply to this address</span>
          <input class="ag-input" id="email" name="email" type="email" autocomplete="email" aria-describedby="email-hint" />
        </div>
        <div class="ag-field">
          <label class="ag-label" for="subject">What is it about?</label>
          <select class="ag-select" id="subject" name="subject">
            <option value="">Choose a subject</option>
            <option>A ministry service</option>
            <option>Project BRIDGE</option>
            <option>3MTT</option>
            <option>Media enquiry</option>
            <option>Something else</option>
          </select>
        </div>
        <div class="ag-field" data-ag-char-count>
          <label class="ag-label" for="message">Your message</label>
          <span class="ag-hint" id="message-hint">Up to 500 characters. Do not include your NIN or bank details.</span>
          <textarea class="ag-textarea" id="message" name="message" rows="6" data-ag-max="500" aria-describedby="message-hint message-count"></textarea>
          <span class="ag-char-count__message" id="message-count"></span>
        </div>
        <button class="ag-button" type="submit">Send message</button>
      </form>
      <div class="ag-prose">
        <h2>Other ways to reach us</h2>
        <p>Federal Secretariat Complex, Shehu Shagari Way, Abuja. Email <a href="mailto:info@fmcide.gov.ng">info@fmcide.gov.ng</a>.</p>
      </div>''', breadcrumb=[("index.html","Home"),("contact.html","Contact")])
P["contact-sent.html"] = shell("Message sent", '''      <div class="ag-panel"><h1 class="ag-panel__title">Message sent</h1><p class="ag-panel__body">Your reference <span class="ag-panel__ref">FM-2026-10842</span></p></div>
      <div class="ag-prose"><p>We will reply by email within five working days. Quote the reference if you need to follow up.</p><p><a href="index.html">Return to the home page</a></p></div>''')

# ---- 3MTT journey ----
def q(title, body, back, action, extra_fields=""):
    return shell(title, f'''      <a class="ag-back-link" href="{back}">Back</a>
      <form action="{action}" method="get" novalidate>
{body}
        <button class="ag-button" type="submit">Continue</button>
      </form>''', current="Initiatives", root="../")
def legend(text, hint=None, hid="q-hint"):
    h = f'\n          <span class="ag-hint" id="{hid}">{hint}</span>' if hint else ""
    return f'<legend class="ag-legend ag-legend--xl"><h1 class="ag-heading-legend">{text}</h1></legend>{h}'

P["3mtt/start.html"] = shell("Apply to the 3 Million Technical Talent programme", '''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Apply to the 3 Million Technical Talent programme</h1>
        <p class="ag-lead">Free training in one of twelve technical skills, online and in person, over about three months. For Nigerians building a career in the digital economy, and for organisations that train them.</p>
        <h2>Who can apply</h2>
        <ul>
          <li><strong>Fellows:</strong> Nigerians aged 18 or over who want technical skills. There is no fee and no qualification required; an entry assessment places you at the right level.</li>
          <li><strong>Training providers:</strong> registered organisations with access to a training facility.</li>
        </ul>
        <h2>Before you start</h2>
        <p>You will need your phone number, an email address, and your state and local government area. It takes about five minutes.</p>
        <div class="ag-button-group"><a class="ag-button ag-button--start" href="role.html">Start now</a></div>
        <details class="ag-details"><summary class="ag-details__summary">The twelve tracks</summary><div class="ag-details__body"><p>AI and machine learning, animation, cloud computing, cybersecurity, data analysis and visualisation, data science, DevOps, game development, product management, quality assurance, software development, UI and UX design.</p></div></details>
      </div>''', current="Initiatives", root="../", breadcrumb=[("index.html","Home"),("initiatives.html","Initiatives"),("3mtt/start.html","3 Million Technical Talent")])

P["3mtt/role.html"] = q("Are you applying as a fellow or a training provider?", f'''        <fieldset class="ag-field">
          {legend("Are you applying as a fellow or a training provider?")}
          <div class="ag-choices">
            <label class="ag-radio"><input type="radio" name="role" value="fellow" /><span class="ag-radio__label">Fellow <span class="ag-radio__hint">I want to be trained</span></span></label>
            <label class="ag-radio"><input type="radio" name="role" value="provider" /><span class="ag-radio__label">Training provider <span class="ag-radio__hint">My organisation trains people</span></span></label>
          </div>
        </fieldset>''', "start.html", "name.html")
P["3mtt/name.html"] = q("What is your name?", '''        <div class="ag-prose"><h1 class="ag-heading-xl">What is your name?</h1></div>
        <div class="ag-field"><label class="ag-label" for="first">First name</label><input class="ag-input ag-input--width-20" id="first" name="first" type="text" autocomplete="given-name" /></div>
        <div class="ag-field"><label class="ag-label" for="last">Surname</label><input class="ag-input ag-input--width-20" id="last" name="last" type="text" autocomplete="family-name" /></div>''', "role.html", "date-of-birth.html")
P["3mtt/date-of-birth.html"] = q("What is your date of birth?", f'''        <fieldset class="ag-field" aria-describedby="dob-hint">
          {legend("What is your date of birth?", "For example, 27 3 1990. You must be 18 or over.", "dob-hint")}
          <div class="ag-date-input">
            <div class="ag-date-input__item"><label class="ag-date-input__label" for="dob-day">Day</label><input class="ag-input" id="dob-day" name="dob-day" type="text" inputmode="numeric" autocomplete="bday-day" /></div>
            <div class="ag-date-input__item"><label class="ag-date-input__label" for="dob-month">Month</label><input class="ag-input" id="dob-month" name="dob-month" type="text" inputmode="numeric" autocomplete="bday-month" /></div>
            <div class="ag-date-input__item ag-date-input__item--year"><label class="ag-date-input__label" for="dob-year">Year</label><input class="ag-input" id="dob-year" name="dob-year" type="text" inputmode="numeric" autocomplete="bday-year" /></div>
          </div>
        </fieldset>''', "name.html", "phone.html")
P["3mtt/phone.html"] = q("What is your phone number?", f'''        <fieldset class="ag-field" aria-describedby="ph-hint">
          {legend("What is your phone number?", "We will send a code by SMS. For example, 0803 000 0000", "ph-hint")}
          <div class="ag-phone">
            <div class="ag-phone__item ag-phone__item--code"><label class="ag-phone__label" for="code">Country code</label><select class="ag-select" id="code" name="code" autocomplete="tel-country-code"><option value="+234" selected>+234 Nigeria</option></select></div>
            <div class="ag-phone__item ag-phone__item--number"><label class="ag-phone__label" for="phone">Number</label><input class="ag-input" id="phone" name="phone" type="tel" inputmode="tel" autocomplete="tel-national" /></div>
          </div>
        </fieldset>''', "date-of-birth.html", "email.html")
P["3mtt/email.html"] = q("What is your email address?", '''        <div class="ag-prose"><h1 class="ag-heading-xl">What is your email address?</h1></div>
        <div class="ag-field"><label class="ag-label" for="email">Email address</label><span class="ag-hint" id="email-hint">We will send your assessment link here</span><input class="ag-input" id="email" name="email" type="email" autocomplete="email" aria-describedby="email-hint" /></div>''', "phone.html", "location.html")
states = ["Abia","Adamawa","Akwa Ibom","Anambra","Bauchi","Bayelsa","Benue","Borno","Cross River","Delta","Ebonyi","Edo","Ekiti","Enugu","FCT Abuja","Gombe","Imo","Jigawa","Kaduna","Kano","Katsina","Kebbi","Kogi","Kwara","Lagos","Nasarawa","Niger","Ogun","Ondo","Osun","Oyo","Plateau","Rivers","Sokoto","Taraba","Yobe","Zamfara"]
lgas = {"Lagos":["Ikeja","Surulere","Eti-Osa","Alimosho","Ikorodu"],"Kano":["Nassarawa","Dala","Fagge","Tarauni"],"FCT Abuja":["Abuja Municipal","Bwari","Gwagwalada","Kuje"],"Rivers":["Port Harcourt","Obio-Akpor"],"Oyo":["Ibadan North","Ibadan South-West"]}
opts = "".join(f'<option>{s}</option>' for s in states)
groups = "".join(f'<optgroup label="{s}">' + "".join(f'<option>{l}</option>' for l in ls) + '</optgroup>' for s,ls in lgas.items())
P["3mtt/location.html"] = q("Where do you live?", f'''        <div class="ag-prose"><h1 class="ag-heading-xl">Where do you live?</h1><p>Training is matched to your local government area where possible.</p></div>
        <div class="ag-field"><label class="ag-label" for="state">State</label><select class="ag-select" id="state" name="state" data-ag-region-for="lga"><option value="">Choose a state</option>{opts}</select></div>
        <div class="ag-field"><label class="ag-label" for="lga">Local government area</label><span class="ag-hint" id="lga-hint">Choose a state first. This rebuild lists a few areas per state.</span><select class="ag-select" id="lga" name="lga" aria-describedby="lga-hint"><option value="">Choose a local government area</option>{groups}</select></div>''', "email.html", "track.html")
tracks = ["AI and machine learning","Animation","Cloud computing","Cybersecurity","Data analysis and visualisation","Data science","DevOps","Game development","Product management","Quality assurance","Software development","UI and UX design"]
radios = "".join(f'\n            <label class="ag-radio"><input type="radio" name="track" value="{t}" /><span class="ag-radio__label">{t}</span></label>' for t in tracks)
P["3mtt/track.html"] = q("Which track do you want to train in?", f'''        <fieldset class="ag-field" aria-describedby="track-hint">
          {legend("Which track do you want to train in?", "Choose one. You can change it after the assessment.", "track-hint")}
          <div class="ag-choices">{radios}
          </div>
        </fieldset>''', "location.html", "education.html")
P["3mtt/education.html"] = q("What is your highest level of education?", '''        <div class="ag-prose"><h1 class="ag-heading-xl">What is your highest level of education?</h1></div>
        <div class="ag-field"><label class="ag-label" for="edu">Highest level completed</label><span class="ag-hint" id="edu-hint">No qualification is required to apply</span><select class="ag-select" id="edu" name="edu" aria-describedby="edu-hint"><option value="">Choose a level</option><option>Primary</option><option>Secondary (SSCE or equivalent)</option><option>OND or NCE</option><option>HND or Bachelor's degree</option><option>Master's degree or above</option><option>Prefer not to say</option></select></div>''', "track.html", "check-answers.html")
rows = [("Applying as","Fellow","role.html"),("Name","Amina Bello","name.html"),("Date of birth","27 March 1990","date-of-birth.html"),("Phone number","0803 000 0000","phone.html"),("Email address","amina@example.com","email.html"),("State and local government area","Lagos, Ikeja","location.html"),("Track","Data analysis and visualisation","track.html"),("Highest level of education","HND or Bachelor's degree","education.html")]
summary = "".join(f'\n        <div class="ag-summary__row"><dt class="ag-summary__key">{k}</dt><dd class="ag-summary__value">{v}</dd><dd class="ag-summary__action"><a href="{h}">Change<span class="ag-visually-hidden"> {k.lower()}</span></a></dd></div>' for k,v,h in rows)
P["3mtt/check-answers.html"] = shell("Check your answers", f'''      <a class="ag-back-link" href="education.html">Back</a>
      <div class="ag-prose"><h1 class="ag-heading-xl">Check your answers before sending your application</h1></div>
      <dl class="ag-summary">{summary}
      </dl>
      <form action="confirmation.html" method="get">
        <div class="ag-prose"><h2>Now send your application</h2><p>By sending this application you confirm that the details are correct and that you are 18 or over.</p></div>
        <div class="ag-field"><label class="ag-checkbox"><input type="checkbox" name="declare" value="yes" /><span class="ag-checkbox__label">I confirm the details above are correct</span></label></div>
        <button class="ag-button" type="submit">Accept and send</button>
      </form>''', current="Initiatives", root="../")
P["3mtt/confirmation.html"] = shell("Application sent", '''      <div class="ag-panel"><h1 class="ag-panel__title">Application sent</h1><p class="ag-panel__body">Your reference number <span class="ag-panel__ref">3MTT-2026-7K4Q2</span></p></div>
      <div class="ag-prose">
        <p>We have sent a confirmation by SMS to 0803 000 0000 and by email.</p>
        <h2>What happens next</h2>
        <p>Within 7 days you will receive a link to the entry assessment. It takes about 45 minutes and places you at the right level for your track. Training starts in the next cohort after your assessment.</p>
        <h2>If you do not hear from us</h2>
        <p>Check your SMS and email after 7 days. If nothing has arrived, <a href="../contact.html">contact the ministry</a> and quote your reference number.</p>
        <p><a href="../initiatives.html">Return to initiatives</a></p>
      </div>''', current="Initiatives", root="../")

P["ict-hubs.html"] = shell("ICT Hubs", '''      <div class="ag-prose">
        <h1 class="ag-heading-xl">ICT Hubs</h1>
        <p class="ag-lead">A national registry of technology hubs, innovation centres and co-working spaces, so the ministry and its partners can find, support and work with them.</p>
        <h2>Who it is for</h2>
        <p>Hubs, incubators, accelerators, maker spaces and training centres anywhere in Nigeria. Registration is free and takes about ten minutes.</p>
        <h2>What registered hubs get</h2>
        <ul>
          <li>A listing in the national registry, visible to investors, partners and the public.</li>
          <li>Early notice of ministry programmes, grants and calls for partners.</li>
          <li>A say in how the ministry supports the innovation ecosystem.</li>
        </ul>
        <div class="ag-button-group"><a class="ag-button ag-button--start" href="contact.html">Register a hub</a></div>
        <div class="ag-inset"><p>The real registry is at ict-hubs.fmcide.gov.ng. Its security certificate had expired when this rebuild was made, so browsers warn before opening it; that is logged as a finding.</p></div>
      </div>''', current="ICT Hubs", breadcrumb=[("index.html","Home"),("ict-hubs.html","ICT Hubs")])

for path, content in P.items():
    write(path, content)
print(f"wrote {len(P)} pages")
