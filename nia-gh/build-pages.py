# Generates the rebuilt pages from one shell. Run: python3 build-pages.py
import os, html, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
CDN = os.environ.get("AFRIGOV_CDN", "https://cdn.jsdelivr.net/npm/afrigov@0.11/dist/")
REAL = "https://nia.gov.gh/"
ORG = "National Identification Authority"
ICONS = json.load(open(os.path.join(HERE, "assets", "social-icons.json")))

NAV = [
    ("index.html", "Home"),
    ("services.html", "Services"),
    ("fees.html", "Fees"),
    ("offices.html", "Offices"),
    ("questions.html", "Questions"),
    ("news.html", "News"),
    ("about.html", "About"),
]

SOCIAL = [
    ("Facebook", "https://www.facebook.com/officialNIAGH"),
    ("X", "https://www.x.com/officialNIAGH"),
    ("Instagram", "https://www.instagram.com/officialNIAGH"),
    ("YouTube", "https://www.youtube.com/channel/UCmN_K4T06P22xy03eC4SC0g"),
]

PORTRAIT = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1 1'%3E%3Crect width='1' height='1' fill='%23dfe6ec'/%3E%3C/svg%3E"


def describe(title, main):
    """One or two sentences for the description: the page's own lead paragraph, or its first paragraph."""
    m = re.search(r'<p class="ag-lead[^"]*">(.*?)</p>', main, flags=re.S) or re.search(r"<p>(.*?)</p>", main, flags=re.S)
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else title
    if len(text) > 158:
        text = text[:158].rsplit(" ", 1)[0].rstrip(",;:") + "…"
    return text


def shell(title, main, current=None, root="", breadcrumb=None, wide=False):
    """One page. `wide` leaves the main element without a container, for pages built from full-width bands."""
    page_title = ORG if title == ORG else f"{title} – {ORG}"
    description = html.escape(describe(title, main), quote=True)
    r = root
    nav = "\n".join(
        f'            <li><a class="ag-nav__link" href="{r}{h}"{" aria-current=\"page\"" if label == current else ""}>{label}</a></li>'
        for h, label in NAV
    )
    crumb = ""
    if breadcrumb:
        items = "".join(f'<li><a href="{r}{h}">{t}</a></li>' for h, t in breadcrumb[:-1])
        items += f'<li><span aria-current="page">{breadcrumb[-1][1]}</span></li>'
        crumb = f'      <nav aria-label="Breadcrumb"><ol class="ag-breadcrumb">{items}</ol></nav>\n'
    social = "\n".join(
        f'              <li><a class="ag-social__link" href="{url}"><svg class="ag-social__icon" aria-hidden="true" viewBox="0 0 24 24"><path d="{ICONS[name]}"/></svg>{name}</a></li>'
        for name, url in SOCIAL
    )
    main_class = "ag-main ag-main--flush" if wide else "ag-main ag-container"
    return f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{html.escape(page_title)}</title>
    <meta name="description" content="{description}" />
    <!-- An unofficial rebuild stays out of search results, so it never competes with the authority's own site. -->
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
    <link rel="stylesheet" href="{CDN}gh.min.css" />
  </head>
  <body>
    <a class="ag-skip-link" href="#main">Skip to main content</a>

    <section class="ag-banner" aria-label="Unofficial website notice">
      <div class="ag-container ag-banner__inner">
        <span class="ag-flag" aria-hidden="true"><span></span><span></span><span></span></span>
        <p class="ag-banner__text">An unofficial rebuild of a Government of Ghana website</p>
        <details class="ag-banner__details">
          <summary>How you know this is unofficial</summary>
          <p>This is a demonstration built on afrigov. It is not run by the National Identification Authority. The real website is <a href="{REAL}">nia.gov.gh</a>.</p>
          <p>Official websites use .gov.gh. This one does not, and it carries no government seal. Nothing you type here is sent to the authority.</p>
        </details>
      </div>
    </section>

    <header class="ag-header ag-header--primary ag-header--striped">
      <div class="ag-container ag-header__inner">
        <a class="ag-header__brand" href="{r}index.html">
          <img class="ag-header__logo" src="{r}assets/mark.svg" alt="" width="40" height="40" />
          <span>
            <span class="ag-header__org">National Identification Authority</span>
            <span class="ag-header__sub">Ghana Card</span>
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

    <main class="{main_class}" id="main" tabindex="-1">
{crumb}{main}
    </main>

    <footer class="ag-footer ag-footer--light">
      <div class="ag-container">
        <div class="ag-footer__columns">
          <div>
            <h2 class="ag-footer__heading">Services</h2>
            <ul class="ag-footer__list">
              <li><a href="{r}services/register-in-ghana.html">Register in Ghana</a></li>
              <li><a href="{r}services/register-abroad.html">Register from abroad</a></li>
              <li><a href="{r}services/replace-card.html">Replace a card</a></li>
              <li><a href="{r}services/update-details.html">Update your details</a></li>
              <li><a href="{r}services/non-citizen-card.html">Non-citizen card</a></li>
              <li><a href="{r}services/mobile-registration.html">Registration at your premises</a></li>
              <li><a href="{r}services/verification.html">Identity verification</a></li>
            </ul>
          </div>
          <div>
            <h2 class="ag-footer__heading">Information</h2>
            <ul class="ag-footer__list">
              <li><a href="{r}fees.html">Fees and charges</a></li>
              <li><a href="{r}offices.html">Offices</a></li>
              <li><a href="{r}centres-6-14.html">Centres for ages 6 to 14</a></li>
              <li><a href="{r}questions.html">Questions and answers</a></li>
              <li><a href="{r}documents.html">Forms, reports and laws</a></li>
              <li><a href="{r}scam-alert.html">Scam alert</a></li>
            </ul>
          </div>
          <div>
            <h2 class="ag-footer__heading">The authority</h2>
            <ul class="ag-footer__list">
              <li><a href="{r}about.html">About</a></li>
              <li><a href="{r}board.html">Board and management</a></li>
              <li><a href="{r}statistics.html">Registration statistics</a></li>
              <li><a href="{r}user-agencies.html">User agencies</a></li>
              <li><a href="{r}news.html">News</a></li>
              <li><a href="{r}careers.html">Careers</a></li>
            </ul>
          </div>
          <div>
            <h2 class="ag-footer__heading">Contact</h2>
            <address class="ag-footer__address">
              No. 8 Nelson Mandela Avenue,<br />
              South Legon, Accra.<br />
              Digital address GA-237-1033
            </address>
            <ul class="ag-footer__list">
              <li><a href="tel:+233302999306">0302 999 306</a></li>
              <li><a href="mailto:info@nia.gov.gh">info@nia.gov.gh</a></li>
              <li><a href="{r}contact.html">Send a message</a></li>
            </ul>
            <ul class="ag-social">
{social}
            </ul>
          </div>
        </div>
        <div class="ag-footer__bar">
          <span class="ag-flag" aria-hidden="true"><span></span><span></span><span></span></span>
          <p>Unofficial rebuild of <a href="{REAL}">nia.gov.gh</a> on <a href="https://github.com/omoyolab/afrigov">afrigov</a>, for demonstration. The authority owns its content and marks.</p>
        </div>
      </div>
    </footer>

    <script src="{CDN}afrigov.iife.js"></script>
  </body>
</html>
'''


def write(path, content):
    full = os.path.join(HERE, path)
    os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
    open(full, "w").write(content)


def crumbs(*pairs):
    return [("index.html", "Home"), *pairs]


def table(caption, head, rows, numeric=(), striped=True, hide_caption=False, narrow=None):
    """A table in its scrolling wrapper. The first cell of each row is the row header.
    A two-column table is kept to the reading width, so the eye does not have to cross the page."""
    if narrow is None:
        narrow = len(head) == 2
    cap = f'<caption class="ag-visually-hidden">{caption}</caption>' if hide_caption else f"<caption>{caption}</caption>"
    th = "".join(
        f'<th scope="col"{" class=\"ag-table__numeric\"" if i in numeric else ""}>{h}</th>' for i, h in enumerate(head)
    )
    body = ""
    for row in rows:
        cells = f'<th scope="row">{row[0]}</th>'
        cells += "".join(
            f'<td{" class=\"ag-table__numeric\"" if i in numeric else ""}>{c}</td>' for i, c in enumerate(row[1:], start=1)
        )
        body += f"<tr>{cells}</tr>"
    cls = "ag-table ag-table--striped" if striped else "ag-table"
    label = html.escape(re.sub(r"<[^>]+>", "", caption), quote=True)
    wrap = f'''
      <div class="ag-table-wrap" role="region" aria-label="{label}" tabindex="0">
        <table class="{cls}">{cap}<thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>
      </div>'''
    return f'''
      <div class="ag-prose">{wrap}
      </div>''' if narrow else wrap


def accordion(pairs):
    items = "".join(
        f'''
        <details class="ag-accordion__item">
          <summary class="ag-accordion__summary">{q}</summary>
          <div class="ag-accordion__body"><p>{a}</p></div>
        </details>'''
        for q, a in pairs
    )
    return f'      <div class="ag-accordion">{items}\n      </div>'


def cards(items, level="h2", variant="", wide=False):
    """items: (title, text, href or None, badge or None). A card with no href has a plain title."""
    out = ""
    for title, text, href, badge in items:
        heading = f'<a class="ag-card__link" href="{href}">{title}</a>' if href else title
        meta = f'\n          <p class="ag-card__meta">{badge}</p>' if badge else ""
        out += f'''
        <li class="ag-card{(" " + variant) if variant else ""}">
          <{level} class="ag-card__title">{heading}</{level}>
          <p class="ag-card__text">{text}</p>{meta}
        </li>'''
    return f'      <ul class="ag-cards{" ag-cards--wide" if wide else ""}">{out}\n      </ul>'


def steps(items):
    """The numbered steps of a process."""
    return '        <ol class="ag-steps">\n' + "".join(f'          <li class="ag-steps__item">{s}</li>\n' for s in items) + "        </ol>"


def badge(text, kind="neutral"):
    return f'<span class="ag-badge ag-badge--{kind}">{text}</span>'


P = {}

# ---------------------------------------------------------------- home

TASKS = [
    ("Register for a Ghana Card", "For Ghanaians living in Ghana, at any age. What to bring and what happens at the centre.", "services/register-in-ghana.html", badge("Free under 25", "success")),
    ("Replace a lost or damaged card", "Report it to the police first, then visit a registration office with the police extract.", "services/replace-card.html", badge("From GH₵200")),
    ("Update your details", "A change of name, address or other details must be reported within 30 days.", "services/update-details.html", badge("Free without a new card", "success")),
    ("Register from abroad", "For Ghanaians living outside Ghana. Apply online, then attend an interview at a Ghana Mission.", "services/register-abroad.html", badge("From US$55")),
    ("Get a non-citizen card", "For foreign nationals who have lived in Ghana for 90 days or more.", "services/non-citizen-card.html", badge("US$120")),
    ("Verify identities", "For banks, agencies and businesses that must confirm who they are dealing with.", "services/verification.html", badge("For organisations", "info")),
]

NEWS = [
    ("news/biometric-verification.html", "Biometric verification becomes mandatory for checking a Ghana Card", "16 July 2026"),
    (REAL + "nia-in-partnership-with-iom-commences-special-registration-for-the-ghana-card-in-sissala-west-lambussie-and-kassena-nankana-west-districts/", "Special registration begins in Sissala West, Lambussie and Kassena-Nankana West, with IOM", "9 July 2026"),
    (REAL + "guidelines-for-user-agencies-on-the-security-storage-and-retention-of-personal-information-obtained-from-the-national-identification-register-nir/", "Guidelines for user agencies on keeping personal information from the register secure", "19 March 2026"),
    (REAL + "public-announcement-temporary-recruitment/", "Temporary recruitment for the registration of children aged 6 to 14", "19 March 2026"),
    (REAL + "nia-management-engages-former-executive-secretaries-to-strengthen-ghanas-national-identity-system-2/", "Management meets former Executive Secretaries on strengthening the identity system", "24 September 2025"),
    (REAL + "nia-begins-registration-of-ghanaians-aged-6-14-years-old-at-its-premium-centres/", "Registration of Ghanaians aged 6 to 14 begins at Premium Centres", "10 September 2025"),
    (REAL + "institutions-urged-to-use-nia-ivsp-for-authentic-ghana-card-verification/", "Institutions urged to verify Ghana Cards through the verification platform", "16 July 2025"),
    (REAL + "strike-action-by-the-nia-division-of-the-public-services-workers-union-pswu-suspended/", "Strike by the NIA division of the Public Services Workers' Union suspended", "29 June 2025"),
]


def news_items(rows, root=""):
    return "".join(
        f'''
        <li class="ag-list__item">
          <a class="ag-list__link" href="{h if h.startswith("http") else root + h}">{t}</a>
          <span class="ag-list__meta">{d}</span>
        </li>'''
        for h, t, d in rows
    )


FIGURES = [
    ("20,146,876", "Ghanaians enrolled"),
    ("19,161,930", "Ghana Cards issued"),
    ("238,263", "Non-citizens enrolled"),
]

P["index.html"] = shell(ORG, f'''      <div class="ag-band ag-band--tint">
        <div class="ag-hero">
          <div class="ag-container ag-hero__inner">
            <div>
              <h1 class="ag-heading-xl ag-hero__title">Get, replace or update your Ghana Card</h1>
              <p class="ag-lead ag-hero__lead">The National Identification Authority registers Ghanaians at home and abroad, and foreign nationals who live in Ghana, and issues each of them a Ghana Card.</p>
              <div class="ag-button-group ag-hero__actions">
                <a class="ag-button ag-button--start" href="services/register-in-ghana.html">Register for a Ghana Card</a>
                <a class="ag-button ag-button--secondary" href="offices.html">Find an office</a>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="ag-container">
        <div class="ag-alert ag-alert--warning" role="status">
          <h2 class="ag-alert__title">A first Ghana Card is free for under-25s at district offices</h2>
          <p>It is GH₵30 if you are 25 or over. Only Premium Centres charge more, and fees are paid to the bank, never to a person. <a href="scam-alert.html">How to spot and report a scam</a>.</p>
        </div>

        <h2>What do you need to do?</h2>
{cards(TASKS, level="h3")}
        <p><a href="services.html">All services</a></p>
      </div>

      <div class="ag-band ag-band--dark">
        <div class="ag-container">
          <div class="ag-feature ag-mb-0">
            <figure class="ag-figure ag-feature__media">
              <img class="ag-figure__image" src="assets/card.svg" alt="A simplified drawing of a Ghana Card: a green band with the flag's gold and red lines across the top, a photograph on the left, a gold chip, lines of printed details, and a machine-readable strip along the bottom." width="320" height="200" loading="lazy" />
            </figure>
            <div class="ag-feature__body">
              <h2 class="ag-feature__title">The Ghana Card</h2>
              <p>The national identity card, with the features of an e-passport. It lasts ten years.</p>
              <ul class="ag-feature__list">
                <li>Your photograph, name, date of birth and personal identification number</li>
                <li>A chip that holds your fingerprints and other biometrics</li>
                <li>An aluminium watermark and ultraviolet printing</li>
                <li>Raised marks so people who cannot see can tell it apart</li>
                <li>The ECOWAS logo and a machine-readable zone, for travel in the region</li>
              </ul>
              <p><a href="questions.html#system">More about the card</a></p>
            </div>
          </div>
        </div>
      </div>

      <div class="ag-container">
        <h2>Before you go</h2>
{cards([
    ("Fees and charges", "What each service costs at a district office, at a Premium Centre and abroad.", "fees.html", None),
    ("Find an office", "The head office, regional offices and district offices, with phone numbers and opening hours.", "offices.html", None),
    ("Questions and answers", "Who can register, what to bring, and what to do when your details change.", "questions.html", None),
], level="h3", variant="ag-card--accent")}

        <h2 id="news">News</h2>
        <ul class="ag-list">{news_items(NEWS[:5])}
        </ul>
        <p><a href="news.html">All news</a></p>

        <h2>Registration so far</h2>
        <dl class="ag-stats">{"".join(f'<div class="ag-stats__item"><dt class="ag-stats__label">{label}</dt><dd class="ag-stats__value">{n}</dd></div>' for n, label in FIGURES)}
        </dl>
        <p class="ag-caption">Figures as at 17 August 2026. <a href="statistics.html">More registration statistics</a>.</p>

        <section class="ag-statement" aria-labelledby="executive-secretary">
          <figure class="ag-figure ag-statement__media">
            <img class="ag-figure__image" src="{PORTRAIT}" alt="" width="320" height="320" loading="lazy" />
            <figcaption class="ag-figure__caption">The Executive Secretary's portrait goes here.</figcaption>
          </figure>
          <div class="ag-statement__body">
            <h2 class="ag-statement__title" id="executive-secretary">Meet the Executive Secretary</h2>
            <p>Mr Wisdom Kwaku Deku leads the authority. He has more than 15 years in cybersecurity, systems analysis and IT strategy, and was Head of Systems Administration at the authority when the National Identification System was put in place.</p>
            <p class="ag-statement__by"><strong>Mr Wisdom Kwaku Deku</strong>Executive Secretary, National Identification Authority</p>
            <p><a href="about.html#executive-secretary">Read his profile</a>, or see the <a href="board.html">board and management</a>.</p>
          </div>
        </section>
      </div>

      <div class="ag-band ag-band--accent ag-mb-0">
        <div class="ag-container">
          <h2 class="ag-mt-0">Does your organisation need to confirm who people are?</h2>
          <p class="ag-lead">Since June 2026 a Ghana Card must be checked against the register, with the holder's fingerprint or face. Looking at the card, or photocopying it, is no longer enough.</p>
          <div class="ag-button-group">
            <a class="ag-button" href="services/verification.html">Join the verification platform</a>
            <a class="ag-button ag-button--secondary" href="news/biometric-verification.html">Read the announcement</a>
          </div>
        </div>
      </div>''', current="Home", wide=True)

# ---------------------------------------------------------------- services

P["services.html"] = shell("Services", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Services</h1>
        <p class="ag-lead">Registration for the Ghana Card, replacing a card, keeping your details up to date, and identity verification for organisations.</p>
      </div>

      <h2>Registration</h2>
{cards([
    ("Register in Ghana", "For Ghanaians living in Ghana, at any age.", "services/register-in-ghana.html", badge("Free under 25", "success")),
    ("Register from abroad", "For Ghanaians living outside Ghana, at a Ghana Mission.", "services/register-abroad.html", badge("From US$55")),
    ("Get a non-citizen card", "For foreign nationals who live in Ghana.", "services/non-citizen-card.html", badge("US$120")),
], level="h3")}

      <h2>At your premises</h2>
{cards([
    ("Registration for institutions and households", "Officers come to your office, home or chosen place to register seven or more people.", "services/mobile-registration.html", badge("GH₵410 a person")),
], level="h3")}

      <h2>Updates and replacements</h2>
{cards([
    ("Replace a card", "For a card that is lost, stolen, damaged or defaced.", "services/replace-card.html", badge("From GH₵200")),
    ("Update your details", "When your name, address or other details change, or were recorded wrongly.", "services/update-details.html", badge("Free without a new card", "success")),
], level="h3")}

      <h2>For organisations</h2>
{cards([
    ("Identity verification", "Check a person's identity against the National Identity Register in real time.", "services/verification.html", badge("For organisations", "info")),
], level="h3")}''', current="Services", breadcrumb=crumbs(("services.html", "Services")))

VOUCHERS = '''        <details class="ag-details">
          <summary class="ag-details__summary">Who can vouch for you</summary>
          <div class="ag-details__body">
            <p>If you have none of the documents above, a relative aged 18 or over who already holds a Ghana Card can vouch for you. If no relative can, two cardholders aged 18 or over can do so before a Commissioner for Oaths. The people who may vouch are:</p>
            <ul>
              <li>a practising or retired teacher, including heads of schools</li>
              <li>a gazetted chief</li>
              <li>a practising or retired magistrate or judge</li>
              <li>a licensed professional, such as a doctor, nurse, lawyer, accountant, engineer or architect</li>
              <li>a serving or retired civil or public servant</li>
              <li>a serving or retired clergyman, an imam or a catechist</li>
              <li>a serving or retired member of the security services</li>
              <li>a current or past Member of Parliament, or member of an Assembly or Unit Committee</li>
            </ul>
          </div>
        </details>'''

OTHER_CARDS = '''        <details class="ag-details">
          <summary class="ag-details__summary">Other government cards to bring if you have them</summary>
          <div class="ag-details__body">
            <p>These do not decide whether you can register. They let the authority link your records.</p>
            <ul>
              <li>SSNIT card</li>
              <li>Tax Identification Number</li>
              <li>driver's licence</li>
              <li>voter ID card</li>
              <li>NHIS card</li>
            </ul>
          </div>
        </details>'''

PAY = "at a CalBank branch, with the CalBank app, or by dialling *771#"


def service(title, lead, body, slug, short):
    return shell(title, f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">{title}</h1>
        <p class="ag-lead">{lead}</p>
{body}
      </div>''', current="Services", root="../", breadcrumb=crumbs(("services.html", "Services"), (f"services/{slug}.html", short)))


P["services/register-in-ghana.html"] = service(
    "Register for a Ghana Card in Ghana",
    "Every Ghanaian living in Ghana can register, from birth. At a district office a first card is free if you are under 25, and GH₵30 if you are older.",
    f'''        <h2 id="who">Who can register</h2>
        <ul>
          <li>Ghanaian citizens of any age who live in Ghana.</li>
          <li>Ghanaian citizens of any age who live abroad. <a href="register-abroad.html">Register from abroad</a>.</li>
          <li>Foreign nationals who live in Ghana legally and permanently. <a href="non-citizen-card.html">Get a non-citizen card</a>.</li>
        </ul>

        <h2 id="bring">What to bring</h2>
        <p>One of these, to show you are Ghanaian:</p>
        <ul>
          <li>a birth certificate from the Births and Deaths Registry of Ghana</li>
          <li>a valid Ghana passport</li>
          <li>a certificate of naturalisation or registration as a citizen</li>
          <li>an Oath of Identity form, if someone is vouching for you</li>
        </ul>
        <p>And the digital address code of the place where you live.</p>
{OTHER_CARDS}
{VOUCHERS}

        <h2 id="steps">What happens at the centre</h2>
        <p>A registration officer checks your documents, then:</p>
{steps([
    "Interviews you and helps you fill in the application form.",
    "Enters the details from your form in the National Identity Register.",
    "Takes your ten fingerprints, a scan of your irises, your photograph and your signature.",
    "Prints your details for you to check and sign or thumbprint. If anything is wrong, say so now. Corrections after this point are charged for.",
    "Prints your Ghana Card and hands it to you.",
])}
        <div class="ag-inset">
          <p>At a Premium Centre a first card is GH₵410, paid {PAY}. <a href="../fees.html">All fees</a>.</p>
        </div>
        <div class="ag-button-group"><a class="ag-button" href="../offices.html">Find a registration office</a></div>

        <h2 id="questions">Questions</h2>
      </div>
{accordion([
    ("What is the Ghana Card?", "The national identity card. The authority issues it to Ghanaian citizens in Ghana and abroad, and to foreign nationals who live in Ghana legally and permanently."),
    ("How long does it take to get the card?", "If you are 15 or over, the card is printed and given to you on the day, where there is power and a network connection. Where there is not, the officer tells you when and where to collect it."),
    ("Can I register without any of the documents?", "Yes. A relative aged 18 or over who holds a Ghana Card can vouch for you. Without a relative, two cardholders aged 18 or over can vouch for you before a Commissioner for Oaths."),
    ("Can someone register for me?", "No. Every applicant must come in person."),
])}
      <div class="ag-prose">
        <p><a href="../questions.html">All questions and answers</a></p>''',
    "register-in-ghana", "Register in Ghana")

P["services/register-abroad.html"] = service(
    "Register for a Ghana Card from abroad",
    "Ghanaians living outside Ghana register at a Ghana Mission. You apply online first, pay when you book, and attend an interview.",
    f'''        <h2 id="bring">What to bring</h2>
        <p>One of these, as the original document:</p>
        <ul>
          <li>a birth certificate from the Births and Deaths Registry of Ghana</li>
          <li>a valid Ghana passport</li>
          <li>a certificate of naturalisation or registration as a citizen</li>
          <li>an Oath of Identity form, if someone is vouching for you</li>
        </ul>
        <p>You will be asked for the address where you live and its post code or zip code.</p>
{OTHER_CARDS}
{VOUCHERS}

        <h2 id="steps">What happens at the interview</h2>
        <p>A registration officer checks your documents, then:</p>
{steps([
    "Reviews the application form you completed online.",
    "Enters your details in the National Identity Register.",
    "Takes your ten fingerprints, a scan of your irises, your photograph and your signature.",
    "Prints your details for you to check and sign or thumbprint. If anything is wrong, say so now.",
    "Prints your Ghana Card and hands it to you.",
])}

        <h2 id="cost">What it costs</h2>
        <p>The fee is paid when you book the interview. It is the cedi equivalent of the amounts below.</p>
      </div>
{table("First registration outside Ghana", ["Where you live", "Fee"], [
    ("An ECOWAS country", "US$55"),
    ("The rest of Africa", "US$75"),
    ("The rest of the world", "US$115"),
], numeric=(1,))}
      <div class="ag-prose">
        <p>Ghanaians who live abroad can also register while visiting Ghana. <a href="register-in-ghana.html">Register in Ghana</a>.</p>
        <div class="ag-inset"><p>The online application is on the authority's own website. This rebuild does not take applications. <a href="{REAL}service/registration-of-ghanaians-in-diaspora/">Start on nia.gov.gh</a>.</p></div>''',
    "register-abroad", "Register from abroad")

P["services/non-citizen-card.html"] = service(
    "Get a non-citizen identity card",
    "A foreign national who has lived in Ghana for 90 days or more in total can apply for a Non-Citizen Ghana Card. It is renewed every year.",
    f'''        <h2 id="who">Who does not need one</h2>
        <ul>
          <li>Diplomats, and people employed by a diplomatic or consular mission.</li>
          <li>People employed by the United Nations or one of its agencies.</li>
          <li>The spouse or dependant of any of the above.</li>
          <li>Visitors staying less than 90 days.</li>
        </ul>

        <h2 id="bring">What to bring</h2>
        <ul>
          <li>a valid passport</li>
          <li>a residence permit</li>
          <li>a birth certificate certified by your country's embassy</li>
          <li>an Oath of Identity form, sworn before a Commissioner for Oaths, if someone is vouching for you</li>
        </ul>

        <h2 id="steps">What happens at the centre</h2>
{steps([
    "Buy a scratch card at a CalBank or Access Bank branch, with the CalBank app, or by USSD.",
    "A registration officer interviews you and you complete the application form.",
    "A data entry officer checks the PIN on your scratch card, takes your fingerprints, portrait, iris scan and signature, and enters your form.",
    "You check the details that were entered. If anything is wrong, say so now.",
    "You collect your card from the issuance desk.",
])}

        <h2 id="cost">What it costs</h2>
        <p>Fees are per person and paid in cedis at the equivalent of the amounts below.</p>
      </div>
{table("Non-citizen identity card fees", ["Service", "Fee"], [
    ("First card", "US$120"),
    ("Renewal, every year", "US$78"),
    ("Replacement card", "US$78"),
    ("Update of records with a new card", "US$70"),
    ("Update of records only", "Free"),
], numeric=(1,))}
      <div class="ag-prose">
        <p>A non-citizen card has NON-CITIZEN IDENTITY CARD printed in red on the front. Refugees are issued a card marked REFUGEE, at US$15 a person.</p>''',
    "non-citizen-card", "Non-citizen card")

P["services/replace-card.html"] = service(
    "Replace a Ghana Card",
    "If your card is lost, stolen, damaged or defaced, report it to the police, then visit a regional or district office for a new one.",
    f'''        <h2 id="bring">What to bring</h2>
        <ul>
          <li><strong>Lost or stolen:</strong> the original police report or police extract. A photocopy is not accepted.</li>
          <li><strong>Damaged or defaced:</strong> the police extract and the damaged card.</li>
        </ul>

        <h2 id="steps">What happens at the office</h2>
{steps([
    "A registration officer reviews your police extract and, if the card is damaged, the card itself.",
    "The officer helps you complete and sign or mark the electronic request form, and submits it for you.",
    "An approval officer reviews the request. If it is declined you are told why.",
    f"Once it is approved, you pay {PAY}. A damaged card is taken from you.",
    "The officer enters the serial number and PIN from your payment, and takes your fingerprints, iris scan, photograph and signature.",
    "Your new Ghana Card is printed and handed to you.",
])}

        <h2 id="cost">What it costs</h2>
      </div>
{table("Card replacement fees", ["Where", "Fee"], [
    ("NIA district office", "GH₵200"),
    ("NIA Premium Centre", "GH₵520"),
    ("An ECOWAS country", "US$55"),
    ("The rest of Africa", "US$75"),
    ("The rest of the world", "US$115"),
], numeric=(1,))}
      <div class="ag-prose">
        <div class="ag-button-group">
          <a class="ag-button ag-button--start" href="../replace/start.html">See how an online request could work</a>
          <a class="ag-button ag-button--secondary" href="../offices.html">Find an office</a>
        </div>

        <h2 id="questions">Questions</h2>
      </div>
{accordion([
    ("Can I ask for a replacement without the request form?", "No. Every request must be signed or thumbprinted by the applicant. If you signed your registration form, you sign the request form too."),
    ("Is a photocopy of the police extract accepted?", "No. Bring the original. The officer scans it into the register and gives it back to you."),
    ("What documents are needed for a damaged or defaced card?", "The police extract and the damaged card itself."),
])}
      <div class="ag-prose">
        <p><a href="../questions.html#updates">All questions about updates and replacements</a></p>''',
    "replace-card", "Replace a card")

P["services/update-details.html"] = service(
    "Update your details",
    "The law requires you to tell the authority within 30 days when your details change, or when you find an error in them.",
    f'''        <p>That covers a change of name, address or other circumstances, and information that is incomplete, wrong or out of date. Not doing so without good reason can lead to a fine, a prison term, or both.</p>

        <h2 id="bring">What to bring</h2>
        <ul>
          <li>Your Ghana Card. The officer reads it to find your record, and takes it back if a new one is printed.</li>
          <li>The document that supports the change, where one exists. A change of name must be gazetted. A marriage certificate, an affidavit or an Assembly Press receipt is not enough.</li>
        </ul>

        <h2 id="steps">What happens at the office</h2>
{steps([
    "A registration officer reviews the documents that support your request.",
    "The officer helps you complete and sign or mark the electronic request form, and submits it for you.",
    "An approval officer reviews the request. You are told whether it is approved, and why if it is not.",
    f"Once it is approved, you pay {PAY}. If the update needs a new card, your old one is taken from you.",
    "The officer enters the serial number and PIN from your payment, and takes your fingerprints, iris scan, photograph and signature.",
    "The officer enters the new details and prints them for you to check and sign or thumbprint. If anything is wrong, say so now.",
    "Your new Ghana Card is printed and handed to you.",
])}
        <div class="ag-inset"><p>Not every request can be completed on the day. You are told when a decision has been made.</p></div>

        <h2 id="cost">What it costs</h2>
      </div>
{table("Fees for updating your details", ["Service", "Fee"], [
    ("Record update only, at a district office", "Free"),
    ("Record update with a new card, at a district office", "GH₵200"),
    ("Record update only, at a Premium Centre", "GH₵165"),
    ("Record update with a new card, at a Premium Centre", "GH₵410"),
    ("Nationality update, at a district office", "GH₵200"),
    ("Nationality update, at a Premium Centre", "GH₵410"),
    ("Record update only, outside Ghana", "Free"),
], numeric=(1,))}
      <div class="ag-prose">
        <p><a href="../fees.html">All fees</a></p>

        <h2 id="questions">Questions</h2>
      </div>
{accordion([
    ("An officer spelt my name wrongly. Do I still pay?", "Yes. At registration you were given a printout to check and sign. Once you confirmed it, a correction is charged for."),
    ("Can I change my date of birth?", "No. It can be corrected only if the officer entered a date different from the one on the document you presented or on your application form."),
    ("Why is a marriage certificate not accepted for a change of name?", "Marriage does not change a name by itself, and the certificate states the names of the two people as they were. To take a spouse's name, the change must be gazetted."),
    ("Can I update the photograph on my card?", "Yes, if the photograph is of poor quality or does not meet the standard. Check with the registration office first, and bring a reason for the request."),
])}
      <div class="ag-prose">
        <p><a href="../questions.html#updates">All questions about updates and replacements</a></p>''',
    "update-details", "Update your details")

P["services/verification.html"] = service(
    "Identity verification for organisations",
    "Organisations that must confirm a person's identity check it against the National Identity Register through the authority's verification platform.",
    f'''        <div class="ag-alert ag-alert--warning" role="status">
          <h2 class="ag-alert__title">Checking the card by eye is no longer enough</h2>
          <p>Since 9 June 2026, identity must be verified in real time with the holder's biometrics. Organisations must not photocopy, scan or keep copies of a Ghana Card to verify identity, unless the law allows it. <a href="../news/biometric-verification.html">Read the announcement</a>.</p>
        </div>

        <h2 id="when">When a Ghana Card must be used</h2>
        <p>The National Identity Register Regulations require the card wherever identification is needed for:</p>
        <ul>
          <li>applying for a passport or a driver's licence</li>
          <li>opening a personal bank account</li>
          <li>buying an insurance policy</li>
          <li>buying, transferring or registering land</li>
          <li>pensions, social security and the National Health Insurance Scheme</li>
          <li>consumer credit</li>
        </ul>

        <h2 id="steps">How an organisation joins</h2>
{steps([
    'Complete the request form and email it to <a href="mailto:idverification@nia.gov.gh">idverification@nia.gov.gh</a>.',
    "The authority replies with a list of documents it needs.",
    "Send the documents.",
    "The authority reviews them and arranges a meeting.",
    "Access is granted once your systems are set up and a contract is signed.",
])}

        <h2 id="documents">Documents the authority asks for</h2>
        <ul>
          <li>business registration certificate, where it applies</li>
          <li>the licence from your regulator</li>
          <li>the law that allows you to collect personal data</li>
          <li>a valid data protection certificate</li>
          <li>your SSNIT certificate</li>
          <li>a summary of your business, of how you will use the Ghana Card, and of the data you need</li>
        </ul>
        <p><a class="ag-download" href="{REAL}wp-content/uploads/IVSP-User-Request-Form_v2.225F.pdf">Identity verification request form <span class="ag-download__meta">(PDF, 487 KB)</span></a></p>
        <p><a href="../user-agencies.html">Organisations that already have access</a></p>''',
    "verification", "Identity verification")

P["services/mobile-registration.html"] = service(
    "Registration at your premises",
    "For institutions, organisations, households and groups of seven or more Ghanaian applicants. Officers come to your office, home or chosen place.",
    f'''        <p>The visit covers first registration, card replacement, updates to personal details and nationality updates.</p>

        <h2 id="before">Before the day</h2>
        <p>The authority surveys the place to check three things:</p>
        <ul>
          <li><strong>Signal:</strong> that the network there is strong and steady enough to register without interruption.</li>
          <li><strong>Space:</strong> that the room and what is provided in it are suitable.</li>
          <li><strong>List:</strong> that the list of applicants you sent is correct.</li>
        </ul>

        <h2 id="bring">What each applicant brings</h2>
        <p>The same documents as for <a href="register-in-ghana.html#bring">registering in Ghana</a>: a birth certificate, a valid Ghana passport or proof of acquired citizenship, and the digital address code of their home.</p>

        <h2 id="cost">What it costs</h2>
        <ul>
          <li>GH₵410 a person for the registration.</li>
          <li>The PIN for an update or replacement is bought separately, {PAY}.</li>
          <li>A logistics fee for the survey and for moving officers and equipment, by distance from the head office in South Legon, Accra.</li>
        </ul>
      </div>
{table("Logistics fee by distance from the head office", ["Distance", "Fee"], [
    ("1 to 10 km", "GH₵451"), ("11 to 20 km", "GH₵550"), ("21 to 30 km", "GH₵654"), ("31 to 40 km", "GH₵760"), ("41 to 50 km", "GH₵823"),
    ("51 to 60 km", "GH₵930"), ("61 to 70 km", "GH₵964"), ("71 to 80 km", "GH₵1,064"), ("81 to 90 km", "GH₵1,180"), ("91 to 100 km", "GH₵1,244"),
], numeric=(1,))}
      <div class="ag-prose">
        <p>Beyond 100 km, GH₵500 is added for every further 50 km. Distances are measured from the head office on Nelson Mandela Avenue.</p>
        <div class="ag-inset">
          <p>Payments are not refunded. Additions to the list on the day must be asked for, and paid for, before 12 noon.</p>
        </div>
        <div class="ag-alert" role="status">
          <h2 class="ag-alert__title">Bank details are not shown here</h2>
          <p>This is an unofficial rebuild, so it does not repeat the authority's bank account details. Take them only from <a href="{REAL}service/institutions-registration/">the authority's own page</a>.</p>
        </div>

        <h2 id="after">After the day</h2>
        <p>Cards are printed on the day where possible. If a card cannot be printed, the authority arranges a later date with your contact person. You are asked to complete a satisfaction survey, and the authority sends your contact person a report on the exercise.</p>

        <h2 id="apply">How to apply</h2>
        <p>Download the request form, fill it in, and email it with the list of applicants to <a href="mailto:mobileregistration@nia.gov.gh">mobileregistration@nia.gov.gh</a>.</p>
        <p><a class="ag-download" href="{REAL}wp-content/uploads/Mobile-Registration-Request-Form_fillable.pdf">Mobile registration request form <span class="ag-download__meta">(PDF, 85 KB)</span></a></p>''',
    "mobile-registration", "Registration at your premises")

# ---------------------------------------------------------------- fees

FEES = [
    ("First registration", [
        ("At a district office, under 25", "Free"),
        ("At a district office, 25 and over", "GH₵30"),
        ("At a Premium Centre", "GH₵410"),
        ("In an ECOWAS country", "US$55"),
        ("In the rest of Africa", "US$75"),
        ("In the rest of the world", "US$115"),
    ]),
    ("Card replacement", [
        ("At a district office", "GH₵200"),
        ("At a Premium Centre", "GH₵520"),
        ("In an ECOWAS country", "US$55"),
        ("In the rest of Africa", "US$75"),
        ("In the rest of the world", "US$115"),
    ]),
    ("Updating your details", [
        ("Record update only, at a district office", "Free"),
        ("Record update with a new card, at a district office", "GH₵200"),
        ("Record update only, at a Premium Centre", "GH₵165"),
        ("Record update with a new card, at a Premium Centre", "GH₵410"),
        ("Nationality update, at a district office", "GH₵200"),
        ("Nationality update, at a Premium Centre", "GH₵410"),
        ("Record update only, outside Ghana", "Free"),
        ("Update with a new card, in an ECOWAS country", "US$55"),
        ("Update with a new card, in the rest of Africa", "US$75"),
        ("Update with a new card, in the rest of the world", "US$115"),
    ]),
    ("Non-citizen identity card", [
        ("First card", "US$120"),
        ("Renewal, every year", "US$78"),
        ("Replacement card", "US$78"),
        ("Update of records only", "Free"),
        ("Update of records with a new card", "US$70"),
    ]),
    ("Refugees, per person", [
        ("First registration", "US$15"),
        ("Renewal of card", "US$15"),
        ("Replacement of card", "US$15"),
        ("Update of records with a new card", "US$15"),
        ("Update of records only", "Free"),
    ]),
    ("Registration at your premises, per person", [
        ("First registration", "GH₵410"),
        ("Card replacement", "GH₵440"),
        ("Update of personal details", "GH₵410"),
        ("Nationality update", "GH₵410"),
        ("Update of records only", "GH₵200"),
    ]),
]

fee_tables = "".join(
    f'''
      <h2 id="{re.sub(r"[^a-z]+", "-", name.lower()).strip("-")}">{name}</h2>{table(name, ["Service", "Fee"], rows, numeric=(1,), hide_caption=True)}'''
    for name, rows in FEES
)

P["fees.html"] = shell("Fees and charges", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Fees and charges</h1>
        <p class="ag-lead">What each service costs from January 2026. Fees in US dollars are paid in cedis at the day's rate.</p>
        <div class="ag-inset"><p>Fees are paid at a CalBank branch, with the CalBank app or by dialling *771#, never to a person. <a href="scam-alert.html">Scam alert</a>.</p></div>
      </div>{fee_tables}
      <div class="ag-prose">
        <p>For registration at your premises there is also a logistics fee by distance. <a href="services/mobile-registration.html#cost">See the distances</a>.</p>
        <p><a class="ag-download" href="{REAL}wp-content/uploads/January-2026-New-Fees-and-Charges-For-Website.pdf">Approved fees and charges, January 2026 <span class="ag-download__meta">(PDF, 234 KB)</span></a></p>
      </div>''', current="Fees", breadcrumb=crumbs(("fees.html", "Fees")))

# ---------------------------------------------------------------- offices


def tel(number):
    digits = number.replace(" ", "")
    shown = f"{digits[:4]} {digits[4:7]} {digits[7:]}" if len(digits) == 10 else number
    return f'<a href="tel:+233{digits[1:]}">{shown}</a>'


REGIONAL = [
    ("Ahafo", "0204203481"), ("Ashanti", "0204399936"), ("Bono", "0201723197"), ("Bono East", "0204185428"),
    ("Central", "0299002324"), ("Eastern", "0299002379"), ("Greater Accra", "0204196481"),
]

DISTRICT = [
    ("Tano North", "Ahafo", "0204185610"), ("Tano South", "Ahafo", "0207876511"),
    ("Amansie West", "Ashanti", "0204210568"), ("Asante Akim North", "Ashanti", "0201721639"), ("Suame", "Ashanti", "0575681775"),
    ("Sunyani East", "Bono", "0201723123"), ("Wenchi", "Bono", "0201721597"),
    ("Techiman North", "Bono East", "0204175526"), ("Techiman South", "Bono East", "0204185732"),
    ("Upper Denkyira East", "Central", "0204447667"), ("Twifo Atti Morkwa", "Central", "0204185280"),
    ("Kwahu South", "Eastern", "0204153613"), ("Suhum", "Eastern", "0201623971"), ("Yilo Krobo", "Eastern", "0204196126"),
    ("La Nkwantanang", "Greater Accra", "0204467233"), ("Tema Central", "Greater Accra", "0204203558"), ("Shai-Osudoku", "Greater Accra", "0204209440"),
    ("Chereponi", "North East", "0204435289"), ("Yunyoo-Nasuan", "North East", "0204435245"),
    ("Tamale Central", "Northern", "0204184819"), ("Yendi", "Northern", "0204196616"),
    ("East Gonja", "Savannah", "0204175455"), ("West Gonja", "Savannah", "0204165376"),
    ("Talensi", "Upper East", "0204203416"), ("Tempane", "Upper East", "0204503097"),
    ("Lambussie", "Upper West", "0204476496"), ("Sissala West", "Upper West", "0204488119"),
]

P["offices.html"] = shell("Offices", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Offices</h1>
        <p class="ag-lead">The authority has a head office in Accra, an office in every region, and district offices across the country. All are open Monday to Friday, 8am to 5pm.</p>

        <h2 id="head-office">Head office</h2>
      </div>
      <dl class="ag-summary">
        <div class="ag-summary__row"><dt class="ag-summary__key">Address</dt><dd class="ag-summary__value">No. 8 Nelson Mandela Avenue, off Gulf House Street, South Legon, Accra</dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Digital address</dt><dd class="ag-summary__value">GA-237-1033</dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Post</dt><dd class="ag-summary__value">P. O. Box M680, Ministries Post Office, Accra</dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Phone</dt><dd class="ag-summary__value">{tel("0302999306")}, {tel("0302999307")}, {tel("0302999309")}, {tel("0549889525")}</dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Email</dt><dd class="ag-summary__value"><a href="mailto:info@nia.gov.gh">info@nia.gov.gh</a></dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Open</dt><dd class="ag-summary__value">Monday to Friday, 8am to 5pm</dd></div>
      </dl>

      <h2 id="regional">Regional offices</h2>{table("Regional offices", ["Region", "Phone"], [(name, tel(phone)) for name, phone in REGIONAL], hide_caption=True)}

      <h2 id="district">District offices</h2>{table("District offices", ["Office", "Region", "Phone"], [(name, region, tel(phone)) for name, region, phone in DISTRICT], hide_caption=True)}
      <div class="ag-prose">
        <div class="ag-inset">
          <p>The authority lists 307 offices. This rebuild shows the head office, seven regional offices and {len(DISTRICT)} district offices, taken from its list on 2 October 2026. <a href="{REAL}nia-regional-and-operational-district-offices/">See every office on nia.gov.gh</a>.</p>
        </div>
        <p>Children aged 6 to 14 are registered at chosen centres. <a href="centres-6-14.html">Registration centres for ages 6 to 14</a>.</p>
      </div>''', current="Offices", breadcrumb=crumbs(("offices.html", "Offices")))

P["centres-6-14.html"] = shell("Registration centres for ages 6 to 14", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Registration centres for ages 6 to 14</h1>
        <p class="ag-lead">Ghanaian children aged 6 to 14 are registered at Premium Centres and at chosen schools in each district.</p>
        <div class="ag-inset"><p>A parent must come with the child, and bring the child's National Health Insurance card so the two records can be linked.</p></div>
        <div class="ag-empty">
          <h2 class="ag-empty__title">No school centres are listed yet</h2>
          <p>The authority's list of schools, by district and region, had no entries when this page was built on 2 October 2026. Children can be registered at any <a href="offices.html">Premium Centre</a> in the meantime.</p>
        </div>
        <p>Children under six are not fingerprinted. Their number is linked to a parent's Ghana Card, and their own biometrics are taken when they turn six.</p>
      </div>''', current="Offices", breadcrumb=crumbs(("offices.html", "Offices"), ("centres-6-14.html", "Centres for ages 6 to 14")))

# ---------------------------------------------------------------- questions

QUESTIONS = [
    ("system", "The Ghana Card", [
        ("What is the Ghana Card?", "The national identity card. The authority issues it to Ghanaian citizens in Ghana and abroad, and to foreign nationals who live in Ghana legally and permanently."),
        ("Why should I register?", "The card is required wherever you must prove who you are: opening a bank account, registering land, applying for a driver's licence or a passport. Without one you can be shut out of those."),
        ("Is it the same as a passport?", "No, but it has the features of an e-passport. It can be used for travel where no immigration stamp is needed, and Ghanaians living abroad can enter Ghana with it without a visa."),
        ("Does the card expire?", "Yes, ten years after it is issued. The card itself is made to last that long, and your photograph should be renewed by then."),
        ("I registered between 2008 and 2018. Do I register again?", "Yes. Registering again brings your details in the register up to date, and you receive a new card."),
        ("I registered in the mass exercise and never received a card. Do I register again?", "No. Give your details at a registration office or a Ghana Mission and they will find your record and print the card. Registering twice is an offence."),
    ]),
    ("eligibility", "Who can register and what to bring", [
        ("Who can register?", "Ghanaian citizens of any age living in Ghana, Ghanaian citizens of any age living abroad, and foreign nationals who live in Ghana legally and permanently."),
        ("What documents do I need?", "One of: a birth certificate from the Births and Deaths Registry, a valid Ghana passport, a certificate of acquired citizenship, or an Oath of Identity form from the vouching process. Bring any other government cards you hold, so your records can be linked."),
        ("What if I have none of those documents?", "A relative aged 18 or over who holds a Ghana Card can vouch for you. Without a relative, two cardholders aged 18 or over can vouch for you before a Commissioner for Oaths."),
        ("Can I register with a passport that has just expired?", "No. The passport must be valid."),
        ("Can I register for someone else?", "No. Every applicant must come in person."),
        ("Do I need a digital address?", "Yes, if you live in Ghana. Ghanaians abroad give the address of their home and its post code or zip code."),
        ("How long does it take to get the card?", "If you are 15 or over it is printed and given to you on the day, where there is power and a network connection. Where there is not, the officer tells you when and where to collect it."),
        ("I was born in Ghana to parents who are not Ghanaian. Am I Ghanaian?", "Not by birth in Ghana alone. A registration officer will interview you and apply the citizenship laws to decide."),
    ]),
    ("fees", "Fees", [
        ("How much is a Ghana Card?", "A first card is free at a district office if you are under 25, and GH₵30 if you are 25 or over. A Premium Centre charges GH₵410. Ghanaians abroad pay the cedi equivalent of US$55, US$75 or US$115, depending on where they live."),
        ("How much is an update or a replacement?", "A replacement is GH₵200 at a district office. Updating your record is free there unless a new card is needed, which is GH₵200. The full list is on the fees page."),
        ("Why do I pay to correct a mistake that was not mine?", "You are shown your details before the card is printed and you sign to confirm them. It is the applicant's responsibility to check them at that point, so a correction afterwards is charged for."),
    ]),
    ("access", "Access", [
        ("Are Ghanaians abroad registered?", "Yes. The law covers every Ghanaian wherever they live. Registration takes place at Ghana Missions, and Ghanaians visiting Ghana can register here."),
        ("How are people with disabilities registered?", "Registration officers assist, and applicants may bring a relative or friend to help. Disability status is recorded during registration."),
        ("How are babies registered when their fingerprints are not formed?", "Children under six have their number linked to a parent's Ghana Card. When they turn six, their fingerprints and other biometrics are taken at an NIA office."),
    ]),
    ("security", "Security and your data", [
        ("How safe is my information?", "The register is kept in a secure environment, and the law protects the privacy of the people in it."),
        ("Who can see my data?", "Only organisations the law allows, and only after they meet the authority's rules for handling it. A breach is an offence."),
        ("How is registering twice prevented?", "Your fingerprints are compared with every set in the register whenever you register, update or replace a card. A second registration is found at once."),
        ("Is it an offence not to register?", "No. But without a card you may be shut out of services that require one."),
        ("How do I tell a non-citizen card from a citizen's?", "A non-citizen card has NON-CITIZEN IDENTITY CARD printed in red on the front."),
        ("What happens to someone who gives false information?", "It is an offence. Offenders are investigated, arrested and prosecuted."),
    ]),
    ("updates", "Updates and replacements", [
        ("What do I do when my details change?", "Tell the authority within 30 days, at a registration office or a Ghana Mission. Not doing so is an offence."),
        ("Do I need proof for an update?", "Yes, wherever proof exists. Some details, such as a phone number, email address or next of kin, need none."),
        ("Can I change my date of birth?", "No. It can be corrected only if the officer entered a date different from the one on your document or application form."),
        ("Why is a marriage certificate not accepted for a change of name?", "Marriage does not change a name by itself. To take a spouse's name, the change must be gazetted."),
        ("Is an affidavit accepted for a change of name or date of birth?", "No. An affidavit is your own statement. The change must be gazetted."),
        ("What do I do if my card is lost, stolen or damaged?", "Report it to the police and get a police extract. Then visit a registration office or a Ghana Mission, and pay the replacement fee."),
        ("Is a photocopy of the police extract accepted?", "No. Bring the original. It is scanned and given back to you."),
        ("Can every update be done on the same day?", "No. You are told when a decision has been made."),
    ]),
    ("integration", "Using the card", [
        ("Will the Ghana Card replace other ID cards?", "It has room on its chip for the data other cards hold. Whether another card is replaced is for the organisation that issues it to decide."),
        ("Can I travel in ECOWAS with it?", "Yes, once countries in the region operate e-gates at their borders."),
        ("An organisation refuses to accept my Ghana Card. What do I do?", "Report it to the authority. Refusing the card as identification is against the law."),
    ]),
]

q_sections = "".join(
    f'''
      <h2 id="{anchor}">{title}</h2>
{accordion(pairs)}'''
    for anchor, title, pairs in QUESTIONS
)
q_count = sum(len(p) for _, _, p in QUESTIONS)

P["questions.html"] = shell("Questions and answers", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Questions and answers</h1>
        <p class="ag-lead">The questions people ask most about the Ghana Card: who can register, what to bring, what it costs, and what to do when details change.</p>
        <ul>
          {"".join(f'<li><a href="#{a}">{t}</a></li>' for a, t, _ in QUESTIONS)}
        </ul>
      </div>{q_sections}
      <div class="ag-prose">
        <p>These {q_count} answers are shortened from the 70 on the authority's site. <a href="{REAL}faqs/">Read them all on nia.gov.gh</a>, or <a href="contact.html">ask the authority</a>.</p>
      </div>''', current="Questions", breadcrumb=crumbs(("questions.html", "Questions")))

P["scam-alert.html"] = shell("Scam alert", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Scam alert</h1>
        <p class="ag-lead">Fraudsters pose as NIA officials to take money from people applying for a Ghana Card. Here is how to tell, and what to do.</p>
        <div class="ag-alert ag-alert--warning" role="status">
          <h2 class="ag-alert__title">Fees are paid to the bank, never to a person</h2>
          <p>Anyone who asks you for cash, or for payment to a personal mobile money number, is not acting for the authority.</p>
        </div>
        <h2>What is true</h2>
        <ul>
          <li>At a district office a first Ghana Card is free if you are under 25, and GH₵30 if you are 25 or over.</li>
          <li>Premium Centres charge more. Every fee is set by law and <a href="fees.html">published</a>.</li>
          <li>Fees are paid at a CalBank branch, with the CalBank app, by dialling *771#, or on another approved payment platform.</li>
          <li>No official takes payment in cash or to a personal mobile money number.</li>
        </ul>
        <h2>Report a scam</h2>
        <p>Email <a href="mailto:info@nia.gov.gh">info@nia.gov.gh</a> with what happened, where and when. Or <a href="contact.html">send a message</a> and choose "Report fraud or a scam".</p>
        <div class="ag-inset"><p>This page is itself part of an unofficial rebuild. For anything that involves money or your identity, use <a href="{REAL}scam-alert/">nia.gov.gh</a>.</p></div>
      </div>''', breadcrumb=crumbs(("scam-alert.html", "Scam alert")))

# ---------------------------------------------------------------- about

P["about.html"] = shell("About the authority", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">About the authority</h1>
        <p class="ag-lead">The National Identification Authority was set up by the National Identification Authority Act, 2006 (Act 707) to create, maintain and promote the use of national identity cards, known as Ghana Cards.</p>

        <h2 id="mandate">Our mandate</h2>
        <p>The authority collects the personal data of Ghanaians in Ghana and abroad, and of foreign nationals who live in Ghana permanently, and issues each of them a Ghana Card. It keeps that data accurate, confidential and secure, and makes it available to the people and organisations the law allows.</p>

        <h2 id="vision">Vision and mission</h2>
      </div>
      <dl class="ag-summary">
        <div class="ag-summary__row"><dt class="ag-summary__key">Vision</dt><dd class="ag-summary__value">A robust national identification system that fosters a trusted society through digitalisation, for the economic, political and social development of Ghana.</dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Mission</dt><dd class="ag-summary__value">To deliver exceptional identity services through a digitalised ecosystem, for safety, security, good governance and development in a trusted Ghanaian society.</dd></div>
      </dl>
      <div class="ag-prose">
        <h2 id="system">The National Identification System</h2>
        <p>The system does five things:</p>
        <ul>
          <li>creates a unique identity for each person from fingerprints, irises and the face</li>
          <li>gives each person a personal identification number that stays with them for life</li>
          <li>issues Ghana Cards to everyone eligible, from birth</li>
          <li>keeps accurate personal information on Ghanaians at home and abroad, and on foreign nationals resident in Ghana</li>
          <li>confirms the identity of a person who holds a Ghana Card</li>
        </ul>
      </div>

      <section class="ag-statement ag-statement--full" aria-labelledby="executive-secretary">
        <figure class="ag-figure ag-statement__media">
          <img class="ag-figure__image" src="{PORTRAIT}" alt="" width="480" height="480" loading="lazy" />
          <figcaption class="ag-figure__caption">The Executive Secretary's portrait goes here.</figcaption>
        </figure>
        <div class="ag-statement__body">
          <h2 class="ag-statement__title" id="executive-secretary">The Executive Secretary</h2>
          <p>Mr Wisdom Kwaku Deku has worked in cybersecurity, systems analysis and IT strategy for more than 15 years. As Head of Systems Administration at the authority he helped put the National Identification System in place.</p>
          <p>He holds an MSc in Cyber Security from the University of Liverpool, and certificates in ethical hacking, IT management, database administration and network administration.</p>
          <p class="ag-statement__by"><strong>Mr Wisdom Kwaku Deku</strong>Executive Secretary, National Identification Authority</p>
          <p>Summarised from his profile on <a href="{REAL}our-governing-board-managment-members/wisdom-kwaku-deku/">nia.gov.gh</a>. <a href="board.html">Board and management</a>.</p>
        </div>
      </section>

      <div class="ag-prose">
        <h2 id="partner">Technical partner</h2>
        <p>Identity Management Systems II Limited (IMS II) is a special purpose vehicle set up to design, build, finance and deliver the digital National Identification System with the authority, in a public-private partnership.</p>
        <p>IMS II, 5th Floor, The Octagon, Accra. <a href="mailto:info@imsgh.org">info@imsgh.org</a></p>

        <h2 id="more">More about the authority</h2>
        <ul>
          <li><a href="board.html">Board and management</a></li>
          <li><a href="statistics.html">Registration statistics</a></li>
          <li><a href="documents.html">Reports, laws and regulations</a></li>
          <li><a href="careers.html">Careers</a></li>
        </ul>
      </div>''', current="About", breadcrumb=crumbs(("about.html", "About")))

BOARD = [
    ("Mr Moses Afetsi Positive", "Chairman"), ("Mr Wisdom Kwaku Deku", "Executive Secretary and member"), ("Dr Gifty Seiwaa Nyorho", "Member"),
    ("Ms Rosemary Addo-Parker", "Member"), ("Mr Samuel Adom Botchway", "Member"), ("Mr Kwesi Afreh Biney", "Member"),
    ("Dr Okofo Twum Barimah V", "Member"), ("Mr Philip Peter Andoh", "Member"), ("Dr Victor Asare Bampoe", "Member"), ("Dr Alhassan Iddrisu", "Member"),
]
MANAGEMENT = [
    ("Mr Wisdom Kwaku Deku", "Executive Secretary"),
    ("Alhaji Mohammed Naziru Seidu", "Deputy Executive Secretary, General Services"),
    ("Dr Fred Bedzrah", "Deputy Executive Secretary, Technical Services"),
    ("Lt Col George Appiah", "Acting Director, Technology and Biometrics"),
    ("Lt Col Joseph Nii Okaija Quaye", "Acting Director, Operations"),
    ("Lt Col Kwabena Owusu Nimako", "Acting Director, Human Resources and Administration"),
    ("Mr Williams Ampomah Emmanuel Darlas", "Head, Corporate Affairs"),
    ("Mr Frederick Doe", "Director, Finance"),
    ("Ms Theresa Eson-Benjamin", "Head, Legal"),
    ("Dr Bernard Gumah", "Acting Head, Policy Planning, Monitoring, Research and Evaluation"),
    ("Mr Mahama Suleiman Sualihu", "Head, Internal Audit"),
    ("Mrs Martha Fasoranti", "Deputy Head, Finance"),
    ("Mr Isaac Tetteh", "Head, Procurement"),
]

def people(rows, variant=""):
    items = "".join(
        f'''
        <li class="ag-person">
          <img class="ag-person__photo" src="{PORTRAIT}" alt="" width="{128 if variant == "ag-people--rows" else 320}" height="{128 if variant == "ag-people--rows" else 320}" loading="lazy" />
          <div>
            <h3 class="ag-person__name">{name}</h3>
            <p class="ag-person__role">{role}</p>
          </div>
        </li>'''
        for name, role in rows
    )
    return f'      <ul class="ag-people{(" " + variant) if variant else ""}">{items}\n      </ul>'


P["board.html"] = shell("Board and management", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Board and management</h1>
        <p class="ag-lead">The governing board sets the authority's direction. The management team runs it day to day. The portraits on the authority's site are not reproduced; grey frames stand where they go.</p>
        <h2 id="board">Governing board</h2>
      </div>
{people(BOARD[:2], "ag-people--2")}
      <div class="ag-prose">
        <h3>Members</h3>
      </div>
{people(BOARD[2:], "ag-people--4")}
      <div class="ag-prose">
        <h2 id="management">Management</h2>
      </div>
{people(MANAGEMENT, "ag-people--rows")}''', current="About", breadcrumb=crumbs(("about.html", "About"), ("board.html", "Board and management")))

AGENCIES = [
    "Universal Merchant Bank", "OmniBSIC Bank Ghana", "Bank of Africa Ghana", "Access Bank Ghana", "NIB Ghana", "Société Générale Ghana",
    "First National Bank Ghana", "Zenith Bank Ghana", "CalBank", "First Atlantic Bank Ghana", "Prudential Bank", "Guaranty Trust Bank Ghana",
    "Fidelity Bank Ghana", "Advans Ghana Savings and Loans", "Jins Savings and Loans", "Pan African Savings and Loans",
    "Bayport Savings and Loans", "Multicredit Savings and Loans", "Adehyeman Savings and Loans", "Affinity Savings and Loans",
    "Izwe Savings and Loans", "ABii National Savings and Loans", "ARB Apex Bank, for 125 rural banks", "Surfline Communications", "Glo Mobile Ghana",
]

P["user-agencies.html"] = shell("User agencies", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">User agencies</h1>
        <p class="ag-lead">Organisations that the law allows to check identities against the National Identity Register, for their own work and to bring their records into line with it.</p>
        <p>Public institutions that use the register include the Driver and Vehicle Licensing Authority and the Ghana Immigration Service. Private institutions are listed below.</p>
        <h2 id="private">Private institutions</h2>
      </div>{table("Private institutions with access to the register", ["Number", "Institution"], [(str(i), name) for i, name in enumerate(AGENCIES, start=1)], hide_caption=True)}
      <nav aria-label="Pagination">
        <ul class="ag-pagination ag-pagination--simple">
          <li><a class="ag-pagination__link" href="{REAL}user-agencies/" rel="next">The rest of the list, on nia.gov.gh</a></li>
        </ul>
      </nav>
      <div class="ag-prose">
        <h2 id="join">Does your organisation need to verify identities?</h2>
        <p>Joining the verification platform helps prevent fraud and builds trust in your services. <a href="services/verification.html">How an organisation joins</a>.</p>
      </div>''', current="About", breadcrumb=crumbs(("about.html", "About"), ("user-agencies.html", "User agencies")))

STATS = [
    ("20,146,876", "Ghanaians enrolled"), ("20,045,761", "Cards printed"), ("19,161,930", "Cards issued"),
    ("238,263", "Non-citizens enrolled"), ("733,954", "Cards replaced"), ("308,216", "Records updated"),
]

P["statistics.html"] = shell("Registration statistics", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Registration statistics</h1>
        <p class="ag-lead">How many people have been registered and how many cards have been printed, issued and replaced. Figures as at 17 August 2026.</p>
      </div>{table("Registration statistics as at 17 August 2026", ["Measure", "Number"], [(label, n) for n, label in STATS], numeric=(1,), hide_caption=True)}
      <div class="ag-prose">
        <p>For other figures, <a href="contact.html">contact the authority</a>.</p>
      </div>''', current="About", breadcrumb=crumbs(("about.html", "About"), ("statistics.html", "Registration statistics")))

# ---------------------------------------------------------------- news

P["news.html"] = shell("News", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">News</h1>
        <p class="ag-lead">Announcements and press releases from the authority.</p>
      </div>
      <ul class="ag-list">{news_items(NEWS)}
      </ul>
      <nav aria-label="Pagination">
        <ul class="ag-pagination ag-pagination--simple">
          <li><a class="ag-pagination__link" href="{REAL}news/" rel="next">Older news, on nia.gov.gh</a></li>
        </ul>
      </nav>''', current="News", breadcrumb=crumbs(("news.html", "News")))

P["news/biometric-verification.html"] = shell("Biometric verification becomes mandatory for checking a Ghana Card", f'''      <div class="ag-prose">
        <p class="ag-caption">Press release · 16 July 2026</p>
        <h1 class="ag-heading-xl">Biometric verification becomes mandatory for checking a Ghana Card</h1>
        <p class="ag-lead">New regulations require organisations to verify identity against the authority's database in real time. Looking at a Ghana Card, or photocopying it, no longer counts.</p>

        <p>The National Identity Register (Amendment) Regulations, 2026 (L.I. 2523) are now in force. The Minister responsible for the National Identification System, Hon. Muntaka Mohammed Mubarak, signed them on 27 March 2026. They were gazetted the same day and took effect on 9 June 2026.</p>

        <h2>What changes</h2>
        <ul>
          <li>Identity must be verified by real-time biometric check against the authority's database.</li>
          <li>A Ghana Card must not be photocopied, scanned or kept to verify identity, unless the law allows it.</li>
          <li>Looking at the card is not proof of identity.</li>
          <li>Where a biometric check is available, a person does not have to show the card at all.</li>
        </ul>

        <h2>Why</h2>
        <p>The regulations are meant to make identity more secure, protect cardholders' personal data, and close off fraud and misuse.</p>

        <h2>What organisations must do</h2>
        <p>Businesses, ministries, departments, agencies and every institution that verifies identity must begin joining the Identity Verification System Platform now. The authority will provide onboarding, technical support and public education.</p>
        <div class="ag-button-group"><a class="ag-button" href="../services/verification.html">How an organisation joins</a></div>

        <p>The Minister will set out the timetable for the national rollout in the coming days.</p>
        <div class="ag-inset"><p>Enquiries: <a href="mailto:idverification@nia.gov.gh">idverification@nia.gov.gh</a>. Issued by the Head of Corporate Affairs, Williams Ampomah Emmanuel Darlas.</p></div>
        <p class="ag-caption">Rewritten from the press release on <a href="{REAL}government-makes-biometric-verification-mandatory-for-ghana-card-verification-under-new-l-i-2523/">nia.gov.gh</a>.</p>
      </div>''', current="News", root="../", breadcrumb=crumbs(("news.html", "News"), ("news/biometric-verification.html", "Biometric verification")))

# ---------------------------------------------------------------- documents

UP = REAL + "wp-content/uploads/"
FORMS = [
    ("Ghana Card application form (Form One)", "487 KB", UP + "Ghana-Card-Application-Form-Form-1-A.pdf"),
    ("Mobile registration request form", "85 KB", UP + "Mobile-Registration-Request-Form_fillable.pdf"),
    ("Identity verification system user request form", "487 KB", UP + "IVSP-User-Request-Form_v2.225F.pdf"),
    ("Approved fees and charges", "234 KB", UP + "January-2026-New-Fees-and-Charges-For-Website.pdf"),
    ("Right to information request form", "75 KB", UP + "Request-Right-To-Information-RTI-Request-Form.pdf"),
    ("Biometric device dealer licence application form", "75 KB", UP + "Biometric-Device-Dealer-Licence-APPLICATION-FORM_V1.pdf"),
]
REPORTS = [(f"Annual report and financial statement, {y}", size, UP + f"DECEMBER-{y}.pdf") for y, size in (("2023", "5.7 MB"), ("2022", "4.7 MB"), ("2021", "4.5 MB"), ("2020", "4 MB"))]
LAWS = [
    "National Identity Register (Amendment) Regulations, 2026 (L.I. 2523)",
    "Specification of types of portable identity card readers, Gazette No. 30 of 15 February 2024",
    "Notification of registration centre premises, Gazette No. 132 of 24 July 2024",
    "Notification of institutions given access to the register, Gazette No. 196 of 2 November 2023",
    "National Identity Register (Amendments) Regulations, 2018 (L.I. 2356)",
    "Mandatory use of the national identity card, Gazette No. 52 of 2 May 2018",
    "National Identity Register (Amendment) Act, 2017 (Act 950)",
    "National Identity Register Regulations, 2012 (L.I. 2111)",
    "National Identity Register Act, 2008 (Act 750)",
    "National Identification Authority Act, 2006 (Act 707)",
]


def downloads(caption, rows):
    return table(caption, ["Document", "Size"], [(f'<a class="ag-download" href="{url}">{name} <span class="ag-download__meta">(PDF)</span></a>', size) for name, size, url in rows], numeric=(1,), hide_caption=True, striped=False)


P["documents.html"] = shell("Forms, reports and laws", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Forms, reports and laws</h1>
        <p class="ag-lead">Application forms, the authority's annual reports, and the laws and regulations it works under. Every file is a PDF on nia.gov.gh.</p>
        <h2 id="forms">Forms</h2>
      </div>{downloads("Forms", FORMS)}
      <div class="ag-prose">
        <h2 id="reports">Reports</h2>
      </div>{downloads("Reports", REPORTS)}
      <div class="ag-prose">
        <h2 id="laws">Laws and regulations</h2>
        <ul>
          <li><a class="ag-download" href="{UP}LI-2523-national-identity-register-amendment-regulations-2026.pdf">{LAWS[0]} <span class="ag-download__meta">(PDF)</span></a></li>
          {"".join(f"<li>{law}</li>" for law in LAWS[1:])}
        </ul>
        <p>The other documents are on the authority's <a href="{REAL}legal-and-regulations/">laws and regulations page</a>.</p>
      </div>''', breadcrumb=crumbs(("documents.html", "Forms, reports and laws")))

P["careers.html"] = shell("Careers", '''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Careers</h1>
        <p class="ag-lead">Openings at the National Identification Authority are announced here, on the authority's social media, and in the news.</p>
        <div class="ag-empty">
          <h2 class="ag-empty__title">The authority is not recruiting at the moment</h2>
          <p>Any offer of a job in exchange for payment is a scam. <a href="scam-alert.html">Scam alert</a>.</p>
        </div>
      </div>''', current="About", breadcrumb=crumbs(("about.html", "About"), ("careers.html", "Careers")))

# ---------------------------------------------------------------- contact

P["contact.html"] = shell("Contact the authority", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Contact the authority</h1>
        <p class="ag-lead">Send a message, or call between 8am and 5pm, Monday to Friday.</p>
        <div class="ag-inset"><p>This form is part of an unofficial rebuild. Nothing you type is sent to the authority. To reach it, use <a href="{REAL}contact/">nia.gov.gh</a>.</p></div>
      </div>
      <form action="contact-sent.html" method="get" novalidate>
        <div class="ag-field">
          <label class="ag-label" for="name">Full name</label>
          <input class="ag-input" id="name" type="text" autocomplete="name" />
        </div>
        <div class="ag-field">
          <label class="ag-label" for="email">Email address</label>
          <span class="ag-hint" id="email-hint">We will reply to this address</span>
          <input class="ag-input" id="email" type="email" autocomplete="email" aria-describedby="email-hint" />
        </div>
        <fieldset class="ag-field">
          <legend class="ag-legend">Where are you asking about?</legend>
          <div class="ag-choices">
            <label class="ag-radio"><input type="radio" name="where" value="ghana" /><span class="ag-radio__label">Services in Ghana</span></label>
            <label class="ag-radio"><input type="radio" name="where" value="abroad" /><span class="ag-radio__label">Services outside Ghana</span></label>
          </div>
        </fieldset>
        <div class="ag-field">
          <label class="ag-label" for="subject">What is it about?</label>
          <select class="ag-select" id="subject">
            <option value="">Choose a subject</option>
            <option>General enquiry</option>
            <option>Update of personal information</option>
            <option>Card replacement</option>
            <option>The online registration portal</option>
            <option>A payment</option>
            <option>Report fraud or a scam</option>
            <option>Something else</option>
          </select>
        </div>
        <div class="ag-field" data-ag-char-count>
          <label class="ag-label" for="message">Your message</label>
          <span class="ag-hint" id="message-hint">Up to 500 characters. Do not include your Ghana Card number or bank details.</span>
          <textarea class="ag-textarea" id="message" rows="6" data-ag-max="500" aria-describedby="message-hint message-count"></textarea>
          <span class="ag-char-count__message" id="message-count"></span>
        </div>
        <button class="ag-button" type="submit">Send message</button>
      </form>
      <div class="ag-prose">
        <h2>Other ways to reach the authority</h2>
      </div>
      <dl class="ag-summary">
        <div class="ag-summary__row"><dt class="ag-summary__key">Phone</dt><dd class="ag-summary__value">{tel("0302999306")}, {tel("0302999307")}, {tel("0302999309")}, {tel("0549889525")}</dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Email</dt><dd class="ag-summary__value"><a href="mailto:info@nia.gov.gh">info@nia.gov.gh</a></dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Visit</dt><dd class="ag-summary__value">No. 8 Nelson Mandela Avenue, off Gulf House Street, South Legon, Accra. <a href="offices.html">All offices</a></dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Post</dt><dd class="ag-summary__value">P. O. Box M680, Ministries Post Office, Accra</dd></div>
      </dl>''', breadcrumb=crumbs(("contact.html", "Contact")))

P["contact-sent.html"] = shell("Message not sent", f'''      <div class="ag-panel ag-panel--neutral"><h1 class="ag-panel__title">This is where a message would be sent</h1><p class="ag-panel__body">Nothing was sent, because this is an unofficial rebuild.</p></div>
      <div class="ag-prose"><p>On a real service this page confirms the message and gives a reference. To reach the authority, use <a href="{REAL}contact/">nia.gov.gh</a>.</p><p><a href="index.html">Return to the home page</a></p></div>''')

# ---------------------------------------------------------------- the replacement journey
# The real service is in person. These pages show how an online request could work.
# Personal fields carry no name attribute, so the browser sends nothing when a step is submitted.

DEMO = '<div class="ag-inset"><p>A demonstration. The real service is in person, and nothing you type here is sent or stored.</p></div>'


def question(title, body, back, action):
    return shell(title, f'''      <a class="ag-back-link" href="{back}">Back</a>
      <form action="{action}" method="get" novalidate>
{body}
        <button class="ag-button" type="submit">Continue</button>
      </form>''', current="Services", root="../")


def legend(text, hint=None, hid="q-hint"):
    h = f'\n          <span class="ag-hint" id="{hid}">{hint}</span>' if hint else ""
    return f'<legend class="ag-legend ag-legend--xl"><h1 class="ag-heading-legend">{text}</h1></legend>{h}'


P["replace/start.html"] = shell("Ask for a replacement Ghana Card", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Ask for a replacement Ghana Card</h1>
        <p class="ag-lead">Tell the authority what happened to your card and where you will collect the new one, so the office is ready when you arrive.</p>
        <div class="ag-alert" role="status">
          <h2 class="ag-alert__title">This is a demonstration</h2>
          <p>Today a card is replaced in person from start to finish. These pages show how the first part could be done online. Nothing you type is sent or stored. <a href="../services/replace-card.html">How to replace a card today</a>.</p>
        </div>
        <h2>Before you start</h2>
        <p>You will need:</p>
        <ul>
          <li>a police extract, which you get by reporting the loss, theft or damage at a police station</li>
          <li>your Ghana Card number, if you know it</li>
          <li>a phone number for text messages</li>
        </ul>
        <p>It takes about five minutes. You still visit an office once, to have your fingerprints and photograph taken and to collect the card.</p>
        <div class="ag-button-group"><a class="ag-button ag-button--start" href="what-happened.html">Start now</a></div>
        <h2>What it costs</h2>
        <p>GH₵200 at a district office, or GH₵520 at a Premium Centre. You pay after the request is approved. <a href="../fees.html#card-replacement">Replacement fees</a>.</p>
      </div>''', current="Services", root="../", breadcrumb=crumbs(("services.html", "Services"), ("services/replace-card.html", "Replace a card"), ("replace/start.html", "Online request")))

P["replace/what-happened.html"] = question("What happened to your card?", f'''        <fieldset class="ag-field">
          {legend("What happened to your card?")}
          <div class="ag-choices">
            <label class="ag-radio"><input type="radio" name="what" value="lost" /><span class="ag-radio__label">It is lost</span></label>
            <label class="ag-radio"><input type="radio" name="what" value="stolen" /><span class="ag-radio__label">It was stolen</span></label>
            <label class="ag-radio"><input type="radio" name="what" value="damaged" /><span class="ag-radio__label">It is damaged or defaced <span class="ag-radio__hint">You will hand the card in at the office</span></span></label>
          </div>
        </fieldset>''', "start.html", "police-extract.html")

P["replace/police-extract.html"] = question("Do you have a police extract?", f'''        <fieldset class="ag-field" aria-describedby="extract-hint">
          {legend("Do you have a police extract?", "The paper the police give you when you report the loss, theft or damage. The office needs the original.", "extract-hint")}
          <div class="ag-choices">
            <label class="ag-radio"><input type="radio" name="extract" value="yes" /><span class="ag-radio__label">Yes</span></label>
            <label class="ag-radio"><input type="radio" name="extract" value="no" /><span class="ag-radio__label">Not yet <span class="ag-radio__hint">You can carry on, and bring it on the day</span></span></label>
          </div>
        </fieldset>''', "what-happened.html", "card-number.html")

P["replace/card-number.html"] = question("What is your Ghana Card number?", '''        <div class="ag-prose"><h1 class="ag-heading-xl">What is your Ghana Card number?</h1></div>
        <div class="ag-field">
          <label class="ag-label" for="card">Ghana Card number</label>
          <span class="ag-hint" id="card-hint">It was on the front of your card, like GHA-123456789-0</span>
          <input class="ag-input ag-id-input" id="card" type="text" autocomplete="off" spellcheck="false" maxlength="15" pattern="GHA-[0-9]{9}-[0-9]" aria-describedby="card-hint" />
        </div>
        <details class="ag-details">
          <summary class="ag-details__summary">If you do not know your number</summary>
          <div class="ag-details__body">
            <p>Leave it empty and continue. The office can find your record from your fingerprints.</p>
          </div>
        </details>''', "police-extract.html", "phone.html")

P["replace/phone.html"] = question("What is your phone number?", f'''        <fieldset class="ag-field" aria-describedby="phone-hint">
          {legend("What is your phone number?", "We will text you when the request is approved. For example, 024 123 4567", "phone-hint")}
          <div class="ag-phone">
            <div class="ag-phone__item ag-phone__item--code"><label class="ag-phone__label" for="code">Country code</label><select class="ag-select" id="code" autocomplete="tel-country-code"><option value="+233" selected>+233 Ghana</option></select></div>
            <div class="ag-phone__item ag-phone__item--number"><label class="ag-phone__label" for="phone">Number</label><input class="ag-input" id="phone" type="tel" inputmode="tel" autocomplete="tel-national" /></div>
          </div>
        </fieldset>''', "card-number.html", "office.html")

OFFICE_GROUPS = {}
for name, region, _ in DISTRICT:
    OFFICE_GROUPS.setdefault(region, []).append(name)
region_options = "".join(f"<option>{region}</option>" for region in OFFICE_GROUPS)
office_options = "".join(
    f'<optgroup label="{region}">' + "".join(f"<option>{name}</option>" for name in names) + "</optgroup>"
    for region, names in OFFICE_GROUPS.items()
)

P["replace/office.html"] = question("Where will you collect the new card?", f'''        <div class="ag-prose"><h1 class="ag-heading-xl">Where will you collect the new card?</h1>
          <p>Choose the region, then the office. You will go there once, to have your fingerprints and photograph taken and to collect the card.</p></div>
        <div class="ag-field">
          <label class="ag-label" for="region">Region</label>
          <select class="ag-select" id="region" data-ag-region-for="office">
            <option value="">Choose a region</option>
            {region_options}
          </select>
        </div>
        <div class="ag-field">
          <label class="ag-label" for="office">District office</label>
          <select class="ag-select" id="office">
            <option value="">Choose an office</option>
            {office_options}
          </select>
        </div>''', "phone.html", "check-answers.html")

P["replace/check-answers.html"] = shell("Check your answers", '''      <a class="ag-back-link" href="office.html">Back</a>
      <div class="ag-prose">
        <h1 class="ag-heading-xl">Check your answers</h1>
        <p>These are example answers. On a real service they are the ones you gave.</p>
      </div>
      <dl class="ag-summary">
        <div class="ag-summary__row"><dt class="ag-summary__key">What happened</dt><dd class="ag-summary__value">The card is lost</dd><dd class="ag-summary__action"><a href="what-happened.html">Change<span class="ag-visually-hidden"> what happened</span></a></dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Police extract</dt><dd class="ag-summary__value">Yes</dd><dd class="ag-summary__action"><a href="police-extract.html">Change<span class="ag-visually-hidden"> police extract</span></a></dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Ghana Card number</dt><dd class="ag-summary__value">GHA-123456789-0</dd><dd class="ag-summary__action"><a href="card-number.html">Change<span class="ag-visually-hidden"> Ghana Card number</span></a></dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Phone number</dt><dd class="ag-summary__value">024 123 4567</dd><dd class="ag-summary__action"><a href="phone.html">Change<span class="ag-visually-hidden"> phone number</span></a></dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Collect from</dt><dd class="ag-summary__value">Tema Central district office, Greater Accra</dd><dd class="ag-summary__action"><a href="office.html">Change<span class="ag-visually-hidden"> office</span></a></dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Fee</dt><dd class="ag-summary__value">GH₵200, paid after approval</dd></div>
      </dl>
      <div class="ag-prose">
        <h2>Send your request</h2>
        <p>By sending this request you confirm that the details are correct, to the best of your knowledge.</p>
        <div class="ag-button-group"><a class="ag-button" href="confirmation.html">Send request</a></div>
      </div>''', current="Services", root="../")

P["replace/confirmation.html"] = shell("Request received", f'''      <div class="ag-panel">
        <h1 class="ag-panel__title">Request received</h1>
        <p class="ag-panel__body">Your reference <span class="ag-panel__ref">GH-RPL-2026-00417</span></p>
      </div>
      <div class="ag-prose">
        {DEMO}
        <h2>What happens next</h2>
{steps([
    "An approval officer reviews your request. We text you the result, usually within two working days.",
    "You pay the fee at a CalBank branch, with the CalBank app, or by dialling *771#.",
    "You visit the office you chose, with the original police extract. Your fingerprints, irises and photograph are taken.",
    "Your new Ghana Card is printed and handed to you.",
])}
        <p><a href="../services/replace-card.html">How to replace a card today</a>, or <a href="../index.html">return to the home page</a>.</p>
      </div>''', current="Services", root="../")

for path, content in P.items():
    write(path, content)
print(f"{len(P)} pages written")
