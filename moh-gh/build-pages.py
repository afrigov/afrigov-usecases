# Generates the rebuilt pages from one shell. Run: python3 build-pages.py
import os, html, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
CDN = os.environ.get("AFRIGOV_CDN", "https://cdn.jsdelivr.net/npm/afrigov@0.14.0/dist/")
REAL = "https://moh.gov.gh/"
UP = REAL + "wp-content/uploads/"
ORG = "Ministry of Health"
ICONS = json.load(open(os.path.join(HERE, "assets", "social-icons.json")))
LOGOS = json.load(open(os.path.join(HERE, "assets", "agencies", "logos.json"))) if os.path.exists(os.path.join(HERE, "assets", "agencies", "logos.json")) else {}

PORTRAIT = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1 1'%3E%3Crect width='1' height='1' fill='%23dfe6ec'/%3E%3C/svg%3E"
THUMB = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 3 2'%3E%3Crect width='3' height='2' fill='%23dfe6ec'/%3E%3C/svg%3E"

SOCIAL = [
    ("Facebook", "https://www.facebook.com/MOHGhana"),
    ("X", "https://twitter.com/Health_ghana"),
    ("Instagram", "https://www.instagram.com/ministryofhealthghana"),
    ("YouTube", "https://youtube.com/user/MOHGhana"),
]

# The navigation: a flat link, or a section with a menu. The first link in a menu is the section's own page.
NAV = [
    ("Home", "index.html", None),
    ("About", "about.html", [("The ministry", "about.html"), ("Office of the Chief Director", "chief-director.html"), ("Organogram", "organogram.html"), ("Health partners", "partners.html")]),
    ("Agencies", "agencies.html", None),
    ("Directorates", "directorates.html", None),  # filled below
    ("Publications", "publications.html", None),  # filled below
    ("Programmes", "programmes.html", None),  # filled below
    ("Media", "news.html", [("News", "news.html"), ("Press releases", "press-releases.html"), ("Events", "events.html"), ("Gallery", "gallery.html"), ("Videos", "videos.html")]),
    ("Tenders", "tenders.html", None),
    ("Contact", "contact.html", [("Contact us", "contact.html"), ("Useful links", "useful-links.html")]),
]

DIRECTORATES = [
    ("ppme", "Policy, Planning, Budgeting, Monitoring and Evaluation", "Leads the development of the ministry's policies, plans, programmes and budgets, and the systems that check whether they work.", [
        ("Policy coordination", "Starts and coordinates the development and review of the sector's policies, strategies and regulations, and leads the design of sector plans."),
        ("Planning", "Coordinates the preparation and harmonisation of the sector plan, and guides its implementation."),
        ("Budgeting", "Coordinates the preparation and harmonisation of the sector budget, and guides its implementation."),
        ("Collaboration", "Develops the private sector and inter-sectoral strategies, and finds opportunities to develop the health sector with them."),
        ("Resource mobilisation", "Develops the financing options for the ministry's policies, programmes and projects, and leads the sourcing and coordination of external funding, including for health commodities, services and works."),
        ("Quality management", "Develops the sector's quality policies and standards, to make treatment more effective and patients more satisfied."),
        ("Monitoring and evaluation", "Designs and runs the systems that assess whether the ministry's strategies and interventions are working."),
    ]),
    ("human-resources", "Human Resource Management and Development", "Sets the sector's policy on workforce planning, training, performance and labour relations, and keeps a stable management framework for the sector's staff.", [
        ("Human resource planning", "Sets policy on the sector's staffing needs, plans careers, and estimates the demand for and supply of health workers. Handles deployment, secondments and postings."),
        ("Training and development", "Reviews and develops career training policies, collects the training needs found in appraisals, and oversees promotions."),
        ("Performance management", "Develops the framework for institutional and staff performance, including appraisals and performance agreements."),
        ("Health training institutions", "Facilitates admission to public and private health training institutions, sets staffing norms for them, monitors their performance, and arranges their accreditation and international exchanges."),
        ("Labour relations", "Develops the means to deal with labour unrest and related challenges."),
    ]),
    ("research-statistics", "Research, Statistics and Information Management", "Creates the conditions for evidence to be generated and used in policy, in public health programmes and in decisions across the sector, and leads the digital transformation of Ghana's health sector.", [
        ("Digital health", "Leads the digital transformation of healthcare delivery, patient outcomes and innovation in health services."),
        ("Data science and health statistics", "Strengthens the sector's statistical systems and the use of data in decisions."),
        ("Health research systems", "Strengthens the systems through which health research is done and used."),
        ("Information and knowledge management", "Manages the sector's information and knowledge."),
    ]),
    ("traditional-medicine", "Traditional and Alternative Medicine", "Provides the expertise behind the policies, regulations, standards, programmes and projects for traditional and alternative medicine.", [
        ("Policy and regulations", "Develops the policies for the sub-sector, and designs the licensing and regulatory schemes, standards and systems that govern it."),
        ("Research, monitoring and evaluation", "Creates and reviews the research behind policy, and monitors and evaluates the industry's activities."),
        ("Information and communication", "Develops the strategies and platforms for discussion, education and public awareness of alternative medicine."),
    ]),
    ("procurement", "Procurement and Supply Chain", "Provides the expertise behind procurement and supply chain policies, coordinates central procurement, and supervises the Central Medical Stores, so that goods, works and services reach the sector efficiently.", [
        ("Procurement regulations and standards", "Maintains the procurement procedures and standard bidding documents, carries out the ministry's procurement of goods, services and works, manages procurement through agencies, coordinates emergency procurement and donations, and trains procurement staff."),
        ("Central Medical Stores", "Receives and distributes goods for the ministry's agencies, and monitors the supply chain for timeliness and quality."),
    ]),
    ("administration", "General Administration", "Turns the ministry's personnel policies on employment, records, training, wages and salaries into day-to-day practice, and keeps the services and facilities the ministry needs running.", [
        ("Personnel welfare", "Keeps staff files and records: recruitment, leave, promotion, salary, transfer and appraisal."),
        ("Records management", "Stores documents and information so they are confidential and easy to find."),
        ("Transport", "Runs the ministry's transport."),
        ("Estates", "Advises on estates and sees that repairs and works on facilities and equipment are done properly."),
        ("Security", "Keeps staff and property safe."),
        ("General stores", "Manages the stores, supports procurement, and keeps stock replaced on time."),
        ("Protocol", "Manages the ministry's protocol at state and ministry ceremonies and national days, and hosts foreign dignitaries and guests."),
    ]),
    ("finance", "Finance", "Responsible for financial management policy, resource mobilisation, disbursement, accounting and reporting, and for the finances of the ministry's headquarters.", [
        ("Accounts", "Processes headquarters transactions for government subventions, the health fund and earmarked funds, prepares financial and management reports, and supports the ministry's regulatory and statutory agencies with their financial management."),
        ("Financial information", "Prepares financial statements for external use, keeps financial information for management control, and leads the development of accounting systems."),
        ("Business analysis", "Helps plan and monitor the ministry's performance, and advises on the control of expenditure and budgets."),
        ("Statutory audit", "Prepares for and controls the statutory audit, and plans the follow-up of audit findings."),
        ("Asset management", "Grows the ministry's financial and physical assets, monitors cash flow, and helps control and investigate the risk of fraud."),
    ]),
    ("internal-audit", "Internal Audit", "Sets internal audit policy, coordinates and monitors internal audit across the ministry, and helps streamline financial management in line with the financial regulations.", [
        ("Audit procedures", "Drafts and updates the procedures audit staff use to conduct audits, assess controls, verify assets, inspect records, check compliance, evaluate performance and follow up recommendations."),
        ("Audit coverage", "Decides how much audit coverage is adequate and how best to use people, equipment and money to give reasonable assurance."),
        ("Quality assurance", "Keeps a system of quality assurance in the unit, so that work is planned, supervised, coordinated and reviewed to the standard."),
        ("Reporting", "Reports regularly on internal audit to the Minister and the Health Sector Audit Reports Implementation Committee, and coordinates with the external auditors."),
    ]),
    ("infrastructure", "Infrastructure", "Provides the expertise behind the ministry's capital investment policies and standards, and the implementation of its national strategic programmes and projects.", [
        ("Capital investment and project management", "Coordinates, supervises, monitors and evaluates every strategic national project of the health sector, reviews the capital investment plan and budget, assures quality and specifications, and advises on investment opportunities and funding."),
        ("Biomedical engineering", "Manages the deployment of healthcare technology and the acquisition and upkeep of medical equipment, including installation, calibration, user support and training across the country."),
    ]),
    ("technical-coordination", "Technical Coordination", "Provides the expertise behind the policies, plans, regulations, standards and programmes in the sector's specialised fields: medical and dental, pharmacy, nursing and midwifery, public health and health promotion, and allied health.", [
        ("Medical and dental", "Develops the policies, standards and regulations that promote clinical care across the country."),
        ("Pharmacy", "Develops the policies, standards and regulations for the pharmaceutical industry: the production of medicines, their supply and distribution, their pricing, and access to quality medicines and medical devices for priorities such as antimicrobial resistance and non-communicable diseases."),
        ("Nursing and midwifery", "Develops the policies and standards for nursing and midwifery."),
        ("Public health and health promotion", "Develops the policies and standards for public health, health promotion, regenerative health and nutrition."),
        ("Allied health", "Develops the policies and standards for the allied health professions."),
    ]),
]
NAV[3] = ("Directorates", "directorates.html", [("All directorates", "directorates.html")] + [(short, f"directorates/{slug}.html") for slug, short, _, _ in [(d[0], d[1], d[2], d[3]) for d in DIRECTORATES]])

PUBLICATIONS = {
    "policy-documents": ("Policy documents", "Policies, strategies and plans for the health sector.", [
        ("Health Sector Medium-Term Development Plan 2026 to 2029", "2026", UP + "2026/08/HSMTDP_Final-Draft_compiled_latest_signed.pdf"),
        ("Health National Adaptation Plan", "2026", UP + "2026/08/HEALTH-NATIONAL-ADAPTATION-PLAN-HNAP.pdf"),
        ("National Health Accounts 2023", "2026", UP + "2026/08/Signed-Ghana-2023-NHA-Report_15.07.2026.pdf"),
        ("National Health Sector Gender Action Plan", "2025", UP + "2025/07/HEALTH_SECTOR-ACTION-PLAN.16.10.pdf"),
        ("National Health Sector Gender Policy", "2025", UP + "2025/07/NATIONAL-HEALTH-SECTOR-GENDER-POLICY_16_11_2024.pdf"),
        ("Reproductive Health Financing in Ghana, 2018 to 2022", "2025", UP + "2025/05/Final_2018-2022_Ghana_Reproductive_Health_Financing_Policy_Brief.pdf"),
        ("Healthcare Financing in Ghana, 2018 to 2022", "2025", UP + "2025/05/Final_2018-2022_Ghana_Health_FInancing_Policy_Brief.pdf"),
        ("National Health Quality Strategy 2024 to 2030", "2025", UP + "2025/05/National-Health-Quality-Strategy-2024-2030.pdf"),
        ("Ghana Health Supply Chain Master Plan 2025 to 2029", "2025", UP + "2025/02/Ghana_HSCMP_2025-2029_Final-Print-Version_17January2025.pdf"),
        ("National Surgical, Obstetric and Anaesthesia Plan", "2024", UP + "2024/10/FINAL-NSOAP-for-press-2.pdf"),
        ("Nursing and Midwifery Strategic Plan and Services Framework 2024 to 2028", "2024", UP + "2024/08/Nursing-and-Midwifery-Strategic-Plan.pdf"),
        ("Ghana Health Financing Strategy 2023 to 2030", "2024", UP + "2024/06/GHANA-HFS-REVISION.pdf"),
    ], 45),
    "programme-of-work": ("Annual programme of work", "The ministry's programme of work for each year.", [
        ("2026 Programme of Work", "2026", UP + "2026/08/2026-Annual-Program-of-work.pdf"),
        ("2024 Programme of Work", "2024", UP + "2024/04/Final-2024-Annual-Programme-of-Work.pdf"),
        ("2023 Programme of Work", "2023", UP + "2023/07/2023-POW.pdf"),
        ("2022 Programme of Work", "2022", UP + "2022/04/FINAL-2022-ANNUAL-PROGRAMME-OF-WORK-l.pdf"),
        ("2021 Programme of Work", "2021", UP + "2021/08/Ministry-of-Health-2021-APOW-6-July-2021-very-final-v2-1.pdf"),
        ("Annual Programme of Work 2015", "2015", UP + "2016/02/Programme-of-Work-2015.pdf"),
        ("Annual Programme of Work 2014", "2014", UP + "2016/02/Annual-Programme-of-Work-2014.pdf"),
        ("Annual Programme of Work 2013", "2013", UP + "2016/02/Annual-Programme-of-Work-2013.pdf"),
        ("Annual Programme of Work 2012", "2012", UP + "2016/02/Annual-Programme-of-Work-2012.pdf"),
        ("Annual Programme of Work 2011", "2011", UP + "2016/03/Programme%20of%20Work%202011.pdf"),
        ("Annual Programme of Work 2010", "2010", UP + "2016/03/Programme%20of%20Work%202010.pdf"),
        ("Annual Programme of Work 2009", "2009", UP + "2016/02/Annual-Programme-of-Work-2009.pdf"),
    ], 21),
    "annual-reviews": ("Annual reviews", "Holistic assessments and reviews of each year's programme of work.", [
        ("Annual Health Sector Holistic Assessment Tool, 4th edition", "2025", UP + "2025/01/Holistic-Assessment-Tool_4thEdition_FINAL.pdf"),
        ("Mid-term review of the Health Sector Medium-Term Development Plan", "2025", UP + "2025/01/GHANA-HSMTDP-MTR-REPORT.pdf"),
        ("2023 Holistic Assessment Report", "2025", UP + "2025/01/2023-HOLISTIC-ASSESSMENT-REPORT.pdf"),
        ("2022 Holistic Assessment Report", "2024", UP + "2024/03/2022-Holistic-Assessment-Report.pdf"),
        ("2021 Holistic Assessment Report", "2022", UP + "2022/09/2021-Holistic-Assessment-Report.pdf"),
        ("2020 Holistic Assessment Report", "2022", UP + "2022/09/2020-Holistic-Assessment-Report.pdf"),
        ("CHPS Review Report", "2016", UP + "2016/02/CHPS-Review-Report-FINAL-180509.pdf"),
        ("2017 Holistic Assessment Report", "2018", UP + "2018/09/2017-Holistic-Assessment-Report.pdf"),
    ], 20),
    "policy-briefs": ("Policy briefs", "Short briefs on financing, programmes and health goals.", [
        ("Healthcare financing in Ghana, excerpts from the 2023 National Health Accounts", "2026", UP + "2026/08/Policy-Brief-on-Healthcare-Financing-in-Ghana.pdf"),
        ("Financing reproductive health in Ghana", "2026", UP + "2026/08/Policy-Brief-on-Financing-RH-in-Ghana.pdf"),
        ("Financing primary health care in Ghana", "2026", UP + "2026/08/Policy-Brief-on-Financing-PHC-in-Ghana.pdf"),
        ("Financing non-communicable diseases in Ghana", "2026", UP + "2026/08/Policy-Brief-on-Financing-NCDs-in-Ghana.pdf"),
        ("Ambulance services", "2016", UP + "2016/02/Ambulance.pdf"),
        ("Guinea worm", "2016", UP + "2016/02/Guinea-worm-Brochure.pdf"),
        ("Health-related Millennium Development Goals", "2016", UP + "2016/02/MOH-HEALTH-RELATED-MILLENIUM-DEVELOPMENT-GOALS.pdf"),
    ], 20),
    "manuals-guidelines": ("Manuals and guidelines", "Standards, treatment guidelines and operating procedures.", [
        ("Harmonised Climate Change and Health Vulnerability and Adaptation Assessment Report", "2026", UP + "2026/08/HARMONIZED-CLIMATE-CHANGE-AND-HEALTH-VULNERABILITY-ADAPTATION-ASSESSMENT-REPORT.pdf"),
        ("Right to Information Manual 2026", "2026", UP + "2026/03/2026-RIGHT-TO-INFORMATION-MANUAL.pdf"),
        ("NITAG Ghana Internal Procedures Manual", "2024", UP + "2024/10/NITAG-Ghana_IP-Manual_Final_09Oct24_Shared-with-Minister.pdf"),
        ("Standard operating procedure for procurement complaints", "2024", UP + "2024/04/COMPLAINTS-MECHANISMS.pdf"),
        ("National guidelines for laboratory testing and reporting on respiratory infectious diseases", "2020", UP + "2020/07/National-Guidelines-for-Laboratory-Testing.pdf"),
        ("Ghana Essential Medicines List 2017", "2017", UP + "2020/07/GHANA-EML-2017.pdf"),
        ("Ghana Standard Treatment Guidelines 2017", "2017", UP + "2020/07/GHANA-STG-2017-1.pdf"),
        ("Essential Medicines List 2010", "2010", UP + "2016/02/Essential-Medicine-List-2010.pdf"),
    ], 31),
    "facts-figures": ("Facts and figures", "The sector's statistics, one booklet a year from 2007 to 2015.", [
        (f"Facts and Figures {y}", y, UP + p) for y, p in [
            ("2015", "2017/07/Facts-and-figures-2015.pdf"), ("2014", "2017/07/Facts-and-figures-2014.pdf"), ("2013", "2017/07/Facts-and-Figure-2013.pdf"),
            ("2012", "2017/07/Facts-and-Figures-2012.pdf"), ("2011", "2017/07/Facts-and-Figure-2011.pdf"), ("2010", "2016/02/Facts-and-Figures-2010.pdf"),
            ("2009", "2016/02/Facts-and-Figures-2009.pdf"), ("2008", "2016/02/Facts-and-Figures-2008.pdf"), ("2007", "2016/02/Facts-and-Figures-2007.pdf"),
        ]
    ], 9),
    "covid-19": ("COVID-19 response documents", "Plans, frameworks and guidelines from the COVID-19 response and the primary health care investment programme.", [
        ("Ghana Primary Health Care Investment Program, environmental and social commitment plan", "2022", UP + "2022/05/Environment-and-Social-Commitment-Plan.pdf"),
        ("Third additional financing, stakeholder engagement plan", "2022", UP + "2022/03/Additional-Financing-SEP.pdf"),
        ("COVID-19 Emergency Response on Vaccines, second additional financing", "2021", UP + "2021/06/COVID-19-Project-Second-Additional-Financing_ESMF.pdf"),
        ("COVID-19 Standard Treatment Guidelines 2020", "2020", UP + "2016/02/COVID-19-STG-JUNE-2020-1.pdf"),
        ("Additional financing, stakeholder engagement plan", "2020", UP + "2020/10/Additional-Financing-Stakeholder-Engagement-Plan.pdf"),
    ], 14),
    "capital-projects": ("Capital projects", "Hospitals, polyclinics and CHPS compounds being built or upgraded.", [], 10),
    "financial-reports": ("Financial reports", "The ministry's consolidated financial reports and accounting instructions.", [
        ("Finance and Accounting Instructions for the Ministry of Health", "2026", UP + "2026/02/MOH-Financial-Instructions.pdf"),
        ("Consolidated financial report, year ended December 2024", "2025", UP + "2025/03/2024-Consolidated-Financial-Report.pdf"),
        ("Consolidated financial report, year ended December 2023", "2024", UP + "2024/04/MoH-2023FS.pdf"),
        ("Consolidated financial report, year ended December 2022", "2025", UP + "2025/05/MOH-Fin.-St-2022.pdf"),
        ("Consolidated financial report, year ended December 2021", "2025", UP + "2025/05/2021-MOH-Fin.-St.pdf"),
    ], 5),
}
NAV[4] = ("Publications", "publications.html", [("All publications", "publications.html")] + [(title, f"publications/{slug}.html") for slug, (title, _, _, _) in PUBLICATIONS.items()])

PROGRAMMES = [
    ("nutrition-malaria", "Nutrition and Malaria Control for Child Survival", "Improving the use of community-based health and nutrition services for children under two and pregnant women in selected districts.",
     ["The project's development objective is to improve the use of selected community-based health and nutrition services for children under the age of two and for pregnant women in the chosen districts.",
      "The project was restructured after three problems: more than a year and a half's delay in scaling up the interventions, weak ownership by the implementing agencies, and slow progress on its indicators."]),
    ("maf", "Millennium Accelerated Framework", "Reducing maternal and newborn deaths through proven, affordable interventions in communities and health facilities.",
     ["The MDG Acceleration Framework focuses on maternal health, in communities and in health facilities, using evidence-based, feasible and cost-effective interventions to cut maternal and newborn deaths faster.",
      "Its three priorities are family planning, skilled delivery, and emergency obstetric and newborn care."]),
    ("climate-change", "Climate Change Health Project", "A national strategy for bringing climate change risks into health sector policies, piloted in three districts.",
     ["Climate Health Ghana is the national strategy for mainstreaming climate change risks into the health sector's policies and measures, led by the ministry.",
      "Pilot interventions run in Keta District, Gomoa West and Apam District, and Bongo District."]),
    ("regenerative-health", "Regenerative Health and Nutrition", "A preventive programme for healthy lifestyles that strengthen the body and mind and prevent disease.",
     ["Regenerative health is the attainment of optimal physical and mental well-being through holistic healthy lifestyles that strengthen and renew the body and mind and prevent disease.",
      "The Regenerative Health and Nutrition Programme is a preventive and promotive programme begun by the ministry as the logical step after health insurance. Over the long term it is meant to cut the cost of lifestyle diseases such as hypertension, diabetes, cancer and gout, all of which are rising.",
      "The programme draws on the experience of an African Hebrew community living in Dimona, Israel, adapted to Ghana. Its aim is to lower the risk of disease for individuals, households and communities, towards a healthier and more productive population."]),
]
NAV[5] = ("Programmes", "programmes.html", [("All programmes", "programmes.html")] + [(name, f"programmes/{slug}.html") for slug, name, _, _ in PROGRAMMES])

AGENCIES = [
    ("Ghana Health Service", "ghs", "ghana-health-service"), ("Korle-Bu Teaching Hospital", "korle-bu", "korle-bu-teaching-hospital"),
    ("Komfo Anokye Teaching Hospital", "kath", "komfo-anokye-teaching-hospital"), ("Tamale Teaching Hospital", "tamale", "tamale-teaching-hospital"),
    ("Cape Coast Teaching Hospital", "cape-coast", "cape-coast-teaching-hospital"), ("Ho Teaching Hospital", "ho", "ho-teaching-hospital"),
    ("Food and Drugs Authority", "fda", "foods-and-drug-authority"), ("Pharmacy Council", "pharmacy-council", "pharmacy-council-ghana"),
    ("Nursing and Midwifery Council", "nmc", "nursing-and-midwifery-council"), ("Medical and Dental Council", "mdc", "ghana-medical-and-dental-council"),
    ("Psychology Council", "psychology-council", "psychology-council"), ("Centre for Plant Medicine Research", "cpmr", "centre-for-plant-medicine-research"),
]

PARTNERS = ["Department for International Development", "European Union Delegation to Ghana", "Gavi, the Vaccine Alliance", "The Global Fund",
            "Japan International Cooperation Agency", "Korea International Cooperation Agency", "Korea Foundation for International Healthcare",
            "United Nations Population Fund", "UNICEF", "UNAIDS", "World Health Organization"]

NEWS = [
    ("news/free-primary-healthcare.html", "Free primary healthcare to begin in 150 districts", ""),
    (REAL + "health-ministry-engages-ga-mantse-on-fphc-launch/", "Ministry calls on the Ga Mantse ahead of the free primary healthcare launch", ""),
    (REAL + "government-moves-to-equip-health-facilities-for-free-primary-health-care-delivery-24534-pieces-of-equipment-procured/", "24,534 pieces of equipment procured for health facilities", ""),
    (REAL + "ministry-of-health-advances-cardiovascular-care-with-new-guidelines/", "New guidelines and donated equipment for cardiovascular care", ""),
    (REAL + "president-mahama-opens-66th-wacs-conference-calls-for-stronger-surgical-capacity-in-west-africa/", "President opens the 66th West African College of Surgeons conference", ""),
    (REAL + "health-ministry-to-sponsor-nurses-and-midwives-for-phd-training/", "Ministry to sponsor nurses and midwives for PhD training", ""),
    (REAL + "category/news/", "Africa's pharmaceutical manufacturing plan moves beyond paper", ""),
    (REAL + "category/news/", "Africa's health debate turns urgent in Accra", ""),
]
PRESS = [
    (REAL + "government-moves-to-equip-health-facilities-for-free-primary-health-care-delivery-24534-pieces-of-equipment-procured/", "24,534 pieces of equipment procured for free primary health care"),
    (REAL + "nurses-leadership-apologised-to-health-minister/", "Nurses' leadership apologises to the Minister", "3 September 2025"),
    (REAL + "5790-2/", "Completed hospitals under Agenda 111"),
    (REAL + "press-release-report-on-investigation-into-alleged-abandonment-of-patient-at-ojobi/", "Report on the investigation into the alleged abandonment of a patient at Ojobi"),
    (REAL + "procurement-of-janssen-vaccines/", "Procurement of Janssen vaccines"),
    (REAL + "ministerial-directive-on-wearing-face-mask/", "Ministerial directive on wearing face masks in public places"),
    (REAL + "transport-services-for-health-workers/", "Transport services for health workers"),
    (REAL + "press-release-update-on-covid-19/", "Update on coronavirus disease, COVID-19"),
]
# (title, link, ISO date or None, day, month, meta line, one line about it). Dates come from the
# flyers the real site posts as pictures; where a flyer gives none, the block says so.
EVENTS = [
    ("African Union Extraordinary Summit on Health", "events/au-summit.html", "2026-07-21", "21", "Jul", "21 and 22 July 2026, Accra", "Ending AIDS and TB, improving maternal health, and tackling endemic non-communicable and neglected tropical diseases in Africa."),
    ("Launch of free primary healthcare", REAL + "launch-of-free-primary-healthcare/", None, "", "", "Date not given on the ministry's site", "Removing the financial barrier to care, towards universal health coverage."),
    ("Media engagement on free primary healthcare", REAL + "media-engagement-on-free-primary-healthcare/", "2026-04-13T11:00", "13", "Apr", "Monday 13 April 2026, 11am", ""),
    ("Government accountability series with the Minister for Health", REAL + "government-accountability-series-with-minister-for-health/", None, "", "", "A Friday at 11am; the date is not given on the ministry's site", ""),
    ("Launch of the Ghana Medical Trust Fund", REAL + "launch-of-ghana-medical-trust-fund/", None, "", "", "Date not given on the ministry's site", "A new era in chronic disease care, launched by the President and the Minister."),
    ("National policy dialogue on the health workforce", REAL + "5863-2/", "2025-04-09", "9", "Apr", "9 and 10 April 2025", "Transforming Ghana's health workforce for universal health coverage: align, invest and sustain."),
    ("Inauguration of the MahamaCares taskforce", REAL + "launch-of-mahamacares-taskforce/", "2025-03-12", "12", "Mar", "Wednesday 12 March 2025, Ministry of Health auditorium", "The taskforce that put the Ghana Medical Care Trust Fund into operation."),
    ("National Prostate Cancer Dialogue 2024", REAL + "national-prostate-cancer-dialogue-2024/", "2024-10-02T09:00", "2", "Oct", "2 October 2024, 9am, Alisa Hotel, North Ridge, Accra", "Bridging the gap in prostate cancer care in Ghana, with the Ghana Association of Urological Surgeons and GIZ."),
]
TODAY = "2026-10-03"


def events_html(rows, root=""):
    out = ""
    for title, link, iso, day, month, meta, text in rows:
        href = link if link.startswith("http") else root + link
        past = bool(iso) and iso[:10] < TODAY
        if iso:
            block = f'<time class="ag-event__date" datetime="{iso}"><span class="ag-event__day">{day}</span><span class="ag-event__month">{month}</span></time>'
        else:
            block = '<span class="ag-event__date ag-event__date--tbc">TBC<span class="ag-visually-hidden">, date to be confirmed</span></span>'
        line = f'\n            <p class="ag-event__text">{text}</p>' if text else ""
        out += f'''
        <li class="ag-event{" ag-event--past" if past else ""}">
          {block}
          <div class="ag-event__body">
            <h3 class="ag-event__title"><a href="{href}">{title}</a></h3>
            <p class="ag-event__meta">{meta}{", past event" if past else ""}</p>{line}
          </div>
        </li>'''
    return f'      <ul class="ag-events">{out}\n      </ul>'
PROJECTS = [
    ("Upgraded cardiac centre commissioned under the trust fund", "A newly built cardiac catheterisation laboratory, commissioned by the President."),
    ("Seven district hospitals, including Dodowa, Sekondi, Fomena and Garu-Tempane", "Design, construction and equipping of seven district hospitals with integrated IT systems."),
    ("1,600 new CHPS compounds across the country", "The CHPS concept was reviewed and the designs revised, with a good share of the compounds for maternal and newborn care."),
    ("Five polyclinics in Greater Accra", "Cabinet approval received; parliamentary approval awaited from the Ministry of Finance."),
    ("Ten polyclinics in Central Region", "Cabinet and parliamentary approval received; the Ministry of Finance has yet to conclude the financing."),
    ("Ghana eight-hospital project", "Eight hospitals, including the Wa Regional Hospital, under a US$339 million project."),
    ("Upgrade and rehabilitation of Ridge Regional Hospital, Accra, 420 beds", "Funded by HSBC and the Export-Import Bank of the United States."),
]

LEADERS = [
    ("Hon. Kwabena Mintah Akandoh, MP", "Minister for Health"),
    ("Hon. Prof. Dr Grace Ayensu-Danquah", "Deputy Minister"),
    ("Mr Desmond Boateng", "Chief Director"),
]


def describe(title, main):
    m = re.search(r'<p class="ag-lead[^"]*">(.*?)</p>', main, flags=re.S) or re.search(r"<p>(.*?)</p>", main, flags=re.S)
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else title
    if len(text) > 158:
        text = text[:158].rsplit(" ", 1)[0].rstrip(",;:") + "…"
    return text


def nav_html(current, root):
    out = []
    for label, href, menu in NAV:
        cur = ' aria-current="page"' if label == current and not menu else ""
        if not menu:
            out.append(f'            <li><a class="ag-nav__link" href="{root}{href}"{cur}>{label}</a></li>')
            continue
        section_cur = ' aria-current="true"' if label == current else ""
        items = "".join(f'\n                <li><a class="ag-nav__menu-link" href="{root}{h}">{t}</a></li>' for t, h in menu)
        out.append(f'''            <li class="ag-nav__section">
              <details class="ag-nav__details" data-ag-menu>
                <summary class="ag-nav__link ag-nav__summary"{section_cur}>{label}</summary>
                <ul class="ag-nav__menu">{items}
                </ul>
              </details>
            </li>''')
    return "\n".join(out)


def shell(title, main, current=None, root="", breadcrumb=None, wide=False):
    page_title = ORG if title == ORG else f"{title} – {ORG}"
    description = html.escape(describe(title, main), quote=True)
    r = root
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
          <p>This is a demonstration built on afrigov. It is not run by the Ministry of Health. The real website is <a href="{REAL}">moh.gov.gh</a>.</p>
          <p>Official websites use .gov.gh. This one does not, and it carries no government seal. Nothing you type here is sent to the ministry.</p>
        </details>
      </div>
    </section>

    <header class="ag-header ag-header--stacked ag-header--striped">
      <div class="ag-container ag-header__inner">
        <a class="ag-header__brand" href="{r}index.html">
          <img class="ag-header__logo" src="{r}assets/mark.svg" alt="" width="40" height="40" />
          <span>
            <span class="ag-header__org">Ministry of Health</span>
            <span class="ag-header__sub">Republic of Ghana</span>
          </span>
        </a>
        <button class="ag-header__toggle" type="button" aria-expanded="false" aria-controls="nav" data-ag-toggle>Menu</button>
        <nav class="ag-header__nav" id="nav" aria-label="Main">
          <ul class="ag-nav">
{nav_html(current, r)}
          </ul>
        </nav>
      </div>
    </header>

    <main class="{main_class}" id="main" tabindex="-1">
{crumb}{main}
    </main>

    <footer class="ag-footer ag-footer--striped">
      <div class="ag-container">
        <div class="ag-footer__columns">
          <div>
            <h2 class="ag-footer__heading">The ministry</h2>
            <ul class="ag-footer__list">
              <li><a href="{r}about.html">About</a></li>
              <li><a href="{r}agencies.html">Agencies</a></li>
              <li><a href="{r}directorates.html">Directorates</a></li>
              <li><a href="{r}partners.html">Health partners</a></li>
              <li><a href="{r}tenders.html">Tenders</a></li>
            </ul>
          </div>
          <div>
            <h2 class="ag-footer__heading">Information</h2>
            <ul class="ag-footer__list">
              <li><a href="{r}publications.html">Publications</a></li>
              <li><a href="{r}programmes.html">Programmes</a></li>
              <li><a href="{r}news.html">News</a></li>
              <li><a href="{r}press-releases.html">Press releases</a></li>
              <li><a href="{r}events.html">Events</a></li>
              <li><a href="{r}useful-links.html">Useful links</a></li>
            </ul>
          </div>
          <div>
            <h2 class="ag-footer__heading">Contact</h2>
            <address class="ag-footer__address">
              Sekou Toure Street, North Ridge,<br />
              next to the National Health Insurance head office,<br />
              Accra. P.O. Box M44
            </address>
            <ul class="ag-footer__list">
              <li><a href="tel:+233302665651">+233 302 665 651</a></li>
              <li><a href="mailto:info@moh.gov.gh">info@moh.gov.gh</a></li>
              <li><a href="{r}contact.html">Send a message</a></li>
            </ul>
            <ul class="ag-social">
{social}
            </ul>
          </div>
        </div>
        <div class="ag-footer__bar">
          <span class="ag-flag" aria-hidden="true"><span></span><span></span><span></span></span>
          <p>Unofficial rebuild of <a href="{REAL}">moh.gov.gh</a> on <a href="https://github.com/omoyolab/afrigov">afrigov</a>, for demonstration. The ministry and its agencies own their content and marks.</p>
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


def cards(items, level="h2", variant="", wide=False):
    out = ""
    for title, text, href, meta in items:
        heading = f'<a class="ag-card__link" href="{href}">{title}</a>' if href else title
        m = f'\n          <p class="ag-card__meta">{meta}</p>' if meta else ""
        out += f'''
        <li class="ag-card{(" " + variant) if variant else ""}">
          <{level} class="ag-card__title">{heading}</{level}>
          <p class="ag-card__text">{text}</p>{m}
        </li>'''
    return f'      <ul class="ag-cards{" ag-cards--wide" if wide else ""}">{out}\n      </ul>'


def logo_cards(level="h3", root=""):
    out = ""
    for name, slug, page in AGENCIES:
        logo = LOGOS.get(slug)
        img = f'\n          <div class="ag-card__logo"><img src="{root}assets/agencies/{slug}.webp" alt="" width="{logo[0]}" height="{logo[1]}" loading="lazy" /></div>' if logo else ""
        out += f'''
        <li class="ag-card">{img}
          <{level} class="ag-card__title"><a class="ag-card__link" href="{REAL}{page}/">{name}</a></{level}>
        </li>'''
    return f'      <ul class="ag-cards">{out}\n      </ul>'


def dated(rows, root=""):
    """A dated list. An item with no date has no meta line; the real site gives none for news."""
    return "".join(
        f'''
        <li class="ag-list__item">
          <a class="ag-list__link" href="{h if h.startswith("http") else root + h}">{t}</a>{f'<span class="ag-list__meta">{m}</span>' if m else ""}
        </li>'''
        for h, t, m in rows
    )


def download_table(caption, rows):
    body = "".join(
        f'<tr><th scope="row"><a class="ag-download" href="{url}">{name} <span class="ag-download__meta">(PDF)</span></a></th><td>{year}</td></tr>'
        for name, year, url in rows
    )
    return f'''
      <div class="ag-table-wrap" role="region" aria-label="{html.escape(caption, quote=True)}" tabindex="0">
        <table class="ag-table"><caption class="ag-visually-hidden">{caption}</caption><thead><tr><th scope="col">Document</th><th scope="col">Year</th></tr></thead><tbody>{body}</tbody></table>
      </div>'''


def people(rows, variant=""):
    items = "".join(
        f'''
        <li class="ag-person">
          <img class="ag-person__photo" src="{PORTRAIT}" alt="" width="320" height="320" loading="lazy" />
          <div>
            <h3 class="ag-person__name">{name}</h3>
            <p class="ag-person__role">{role}</p>
          </div>
        </li>'''
        for name, role in rows
    )
    return f'      <ul class="ag-people{(" " + variant) if variant else ""}">{items}\n      </ul>'


P = {}

# ---------------------------------------------------------------- home

P["index.html"] = shell(ORG, f'''      <div class="ag-hero ag-hero--cover">
        <img class="ag-hero__cover" src="assets/hero.svg" alt="" width="1600" height="700" />
        <div class="ag-container ag-hero__inner">
          <div class="ag-hero__panel">
            <h1 class="ag-heading-xl ag-hero__title">Free primary healthcare begins in 150 districts</h1>
            <p class="ag-lead ag-hero__lead">Care at CHPS compounds, health centres and polyclinics at no charge, starting with the districts that need it most.</p>
            <div class="ag-button-group ag-hero__actions">
              <a class="ag-button ag-button--start" href="news/free-primary-healthcare.html">What it means for you</a>
              <a class="ag-button ag-button--secondary" href="programmes.html">Our programmes</a>
            </div>
          </div>
        </div>
      </div>

      <div class="ag-container">
        <h2>What the ministry does</h2>
{cards([
    ("Sets health policy", "Direction, standards and regulation for everyone who delivers health care in Ghana. The agencies deliver it.", "about.html", None),
    ("Oversees twelve agencies", "The Ghana Health Service, five teaching hospitals, the regulators of medicines and professions, and a research centre.", "agencies.html", None),
    ("Publishes the sector's plans and reports", "Policies, programmes of work, annual reviews, guidelines and financial reports.", "publications.html", None),
], level="h3", variant="ag-card--accent")}

        <h2 id="news">News</h2>
        <ul class="ag-list">{dated([(h, t, m) for h, t, m in NEWS[:5]])}
        </ul>
        <p><a href="news.html">All news</a>, or the <a href="press-releases.html">press releases</a>.</p>
      </div>

      <div class="ag-band ag-band--tint">
        <div class="ag-container">
          <h2 class="ag-mt-0">Leadership</h2>
{people(LEADERS, "ag-people--3")}
          <p class="ag-mb-0"><a href="chief-director.html">The Office of the Chief Director</a> and <a href="organogram.html">how the ministry is organised</a>.</p>
        </div>
      </div>

      <div class="ag-container">
        <h2>Agencies</h2>
        <p class="ag-prose">The ministry supervises twelve agencies. Each has its own website.</p>
{logo_cards()}

        <h2>Programmes</h2>
{cards([(name, short, f"programmes/{slug}.html", None) for slug, name, short, _ in PROGRAMMES], level="h3", variant="ag-card--flag")}
      </div>

      <div class="ag-band ag-band--primary">
        <div class="ag-container">
          <h2 class="ag-mt-0">Events</h2>
{events_html(EVENTS[:3])}
          <p class="ag-mb-0"><a href="events.html">All events</a></p>
        </div>
      </div>

      <div class="ag-container">
        <h2>Latest publications</h2>
        <ul class="ag-list">
          <li class="ag-list__item"><a class="ag-download ag-list__link" href="{PUBLICATIONS["policy-documents"][2][0][2]}">Health Sector Medium-Term Development Plan 2026 to 2029 <span class="ag-download__meta">(PDF)</span></a><span class="ag-list__meta">Policy document, 2026</span></li>
          <li class="ag-list__item"><a class="ag-download ag-list__link" href="{PUBLICATIONS["programme-of-work"][2][0][2]}">2026 Programme of Work <span class="ag-download__meta">(PDF)</span></a><span class="ag-list__meta">Annual programme of work, 2026</span></li>
          <li class="ag-list__item"><a class="ag-download ag-list__link" href="{PUBLICATIONS["policy-documents"][2][2][2]}">National Health Accounts 2023 <span class="ag-download__meta">(PDF)</span></a><span class="ag-list__meta">Policy document, 2026</span></li>
          <li class="ag-list__item"><a class="ag-download ag-list__link" href="{PUBLICATIONS["financial-reports"][2][1][2]}">Consolidated financial report, year ended December 2024 <span class="ag-download__meta">(PDF)</span></a><span class="ag-list__meta">Financial report, 2025</span></li>
        </ul>
        <p><a href="publications.html">All publications</a></p>
      </div>''', current="Home", wide=True)

# ---------------------------------------------------------------- about

P["about.html"] = shell("About the ministry", '''      <div class="ag-prose">
        <h1 class="ag-heading-xl">About the ministry</h1>
        <p class="ag-lead">The Ministry of Health works to improve the health of everyone living in Ghana, towards the government's goal of universal health coverage and a healthy population.</p>
        <p>Working with its agencies and partners, the ministry aims to build the country's human capital, creating wealth through health, by developing and carrying out policies that improve health and vitality.</p>

        <h2 id="vision">Vision and mission</h2>
      </div>
      <dl class="ag-summary">
        <div class="ag-summary__row"><dt class="ag-summary__key">Vision</dt><dd class="ag-summary__value">A healthy population for national development.</dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Mission</dt><dd class="ag-summary__value">To contribute to the country's development, and to a local health industry, by promoting health and vitality through access to quality health care for everyone living in Ghana, delivered by motivated staff.</dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Policy thrust</dt><dd class="ag-summary__value">To reduce inequities in access to care and to raise the coverage, quality and use of health services, towards a healthier population.</dd></div>
      </dl>
      <div class="ag-prose">
        <h2 id="goal">Goal</h2>
        <p>To improve the health of everyone living in Ghana through policy, the mobilisation of resources, and the monitoring and regulation of the care that the health agencies deliver.</p>

        <h2 id="objectives">Policy objectives</h2>
        <ul>
          <li>Universal access to better and more efficiently managed health services.</li>
          <li>Fewer avoidable deaths and disabilities among mothers, adolescents and children.</li>
          <li>Better access to responsive clinical and public health emergency services.</li>
        </ul>

        <h2 id="role">What the headquarters does</h2>
        <ul>
          <li>Sets the overall policy direction for everyone involved in delivering health care.</li>
          <li>Advocates for action on health across other sectors.</li>
          <li>Mobilises resources and allocates them to all providers of health services.</li>
          <li>Provides the information needed to coordinate and manage health services.</li>
          <li>Sets the regulatory framework for all providers of health services.</li>
          <li>Monitors and evaluates health services in Ghana.</li>
        </ul>

        <h2 id="more">More about the ministry</h2>
        <ul>
          <li><a href="chief-director.html">The Office of the Chief Director</a></li>
          <li><a href="organogram.html">How the ministry is organised</a></li>
          <li><a href="directorates.html">The ten directorates</a></li>
          <li><a href="agencies.html">The twelve agencies</a></li>
          <li><a href="partners.html">Health partners</a></li>
        </ul>
      </div>''', current="About", breadcrumb=crumbs(("about.html", "About")))

P["chief-director.html"] = shell("Office of the Chief Director", '''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Office of the Chief Director</h1>
        <p class="ag-lead">The Chief Director holds the highest office in the ministry, reports to the Minister, and guides, coordinates and supervises the work of the directors.</p>

        <h2 id="reports">Who reports to the Chief Director</h2>
        <p>The directors of the ten directorates: policy, planning, monitoring and evaluation; research, statistics and information management; human resource development and management; administration; finance; procurement and supplies; technical coordination; infrastructure; and traditional and alternative medicine. <a href="directorates.html">The directorates</a>.</p>

        <h2 id="responsibilities">Responsibilities</h2>
        <ul>
          <li>Leads the setting of policies and objectives for the sector, and their implementation.</li>
          <li>Coordinates work programmes, and sets the rules, guidelines and procedures for reaching the ministry's targets.</li>
          <li>Sees that training programmes are organised in line with sector policy.</li>
          <li>Sets up the systems for cooperation between ministries and across the sector, so programmes do not duplicate one another.</li>
          <li>Develops the systems for work flow and feedback within the sector.</li>
          <li>Plans and accelerates the decentralisation of the sector where it is needed.</li>
        </ul>
        <p>In relation to the ministry, the Chief Director also:</p>
        <ul>
          <li>recommends how budgets are disbursed, within the financial regulations</li>
          <li>recommends leave for directors and heads of organisations, and coordinates leave across the sector</li>
          <li>requests action programmes and budgets from every implementing agency</li>
          <li>sees that every implementing agency has proper codes of conduct for its administrative, financial and operational work</li>
          <li>recommends major changes to the structure of implementing agencies, and any disposal of capital assets</li>
          <li>sees that discipline is enforced across the sector</li>
        </ul>

        <h2 id="authority">Authority</h2>
        <p>The Chief Director's authority comes from these responsibilities, and from what the Minister delegates.</p>
      </div>''', current="About", breadcrumb=crumbs(("about.html", "About"), ("chief-director.html", "Office of the Chief Director")))

P["organogram.html"] = shell("How the ministry is organised", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">How the ministry is organised</h1>
        <p class="ag-lead">The Minister and Deputy Minister lead the ministry. The Chief Director runs it, through ten directorates. Twelve agencies deliver and regulate health care.</p>
        <div class="ag-inset"><p>The ministry publishes its organogram as one picture, which cannot be read aloud or searched. This page says the same thing as text.</p></div>
        <h2>Political leadership</h2>
        <ul>
          <li>Minister for Health: {LEADERS[0][0]}</li>
          <li>Deputy Minister: {LEADERS[1][0]}</li>
        </ul>
        <h2>Administrative leadership</h2>
        <ul>
          <li>Chief Director: {LEADERS[2][0]}. <a href="chief-director.html">The Office of the Chief Director</a>.</li>
        </ul>
        <h2>Directorates, reporting to the Chief Director</h2>
        <ol>
          {"".join(f'<li><a href="directorates/{slug}.html">{short}</a></li>' for slug, short, _, _ in DIRECTORATES)}
        </ol>
        <h2>Agencies, supervised by the ministry</h2>
        <ol>
          {"".join(f"<li>{name}</li>" for name, _, _ in AGENCIES)}
        </ol>
        <p><a href="agencies.html">The agencies, with links to their websites</a>.</p>
      </div>''', current="About", breadcrumb=crumbs(("about.html", "About"), ("organogram.html", "Organogram")))

P["partners.html"] = shell("Health partners", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Health partners</h1>
        <p class="ag-lead">The development partners that fund and support the health sector's work with the ministry.</p>
        <ul>
          {"".join(f"<li>{p}</li>" for p in PARTNERS)}
        </ul>
        <p>The ministry's site shows each partner's logo. The logos belong to the partners and are not reproduced here.</p>
      </div>''', current="About", breadcrumb=crumbs(("about.html", "About"), ("partners.html", "Health partners")))

P["agencies.html"] = shell("Agencies", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Agencies</h1>
        <p class="ag-lead">The ministry supervises twelve agencies: the service that runs public health care, five teaching hospitals, five regulators, and a research centre. Each link goes to the agency's page on the ministry's site.</p>
      </div>
{logo_cards(level="h2")}''', current="Agencies", breadcrumb=crumbs(("agencies.html", "Agencies")))

# ---------------------------------------------------------------- directorates

P["directorates.html"] = shell("Directorates", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Directorates</h1>
        <p class="ag-lead">The ten directorates through which the ministry does its work, each reporting to the Chief Director.</p>
      </div>
{cards([(short, lead, f"directorates/{slug}.html", None) for slug, short, lead, _ in DIRECTORATES], level="h2")}''', current="Directorates", breadcrumb=crumbs(("directorates.html", "Directorates")))

for slug, short, lead, units in DIRECTORATES:
    rows = "".join(f'<div class="ag-summary__row"><dt class="ag-summary__key">{u}</dt><dd class="ag-summary__value">{d}</dd></div>' for u, d in units)
    P[f"directorates/{slug}.html"] = shell(f"{short} Directorate", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">{short} Directorate</h1>
        <p class="ag-lead">{lead}</p>
        <h2 id="units">Units</h2>
      </div>
      <dl class="ag-summary">{rows}</dl>
      <div class="ag-prose">
        <p>The directorate reports to the <a href="../chief-director.html">Chief Director</a>. <a href="../directorates.html">All directorates</a>.</p>
      </div>''', current="Directorates", root="../", breadcrumb=crumbs(("directorates.html", "Directorates"), (f"directorates/{slug}.html", short)))

# ---------------------------------------------------------------- publications

P["publications.html"] = shell("Publications", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Publications</h1>
        <p class="ag-lead">The sector's policies, plans, reviews, guidelines, statistics and financial reports, as PDF files on the ministry's site.</p>
      </div>
{cards([(title, f"{lead} {count} documents.", f"publications/{slug}.html", None) for slug, (title, lead, _, count) in PUBLICATIONS.items()], level="h2")}''', current="Publications", breadcrumb=crumbs(("publications.html", "Publications")))

for slug, (title, lead, rows, count) in PUBLICATIONS.items():
    if slug == "capital-projects":
        body = cards([(name, text, f"{REAL}category/capital-projects/", None) for name, text in PROJECTS], level="h2", variant="ag-card--plain")
        note = f'<p>The ministry lists {count} projects. The seven above are the current ones; <a href="{REAL}category/capital-projects/">the rest are on moh.gov.gh</a>.</p>'
    else:
        body = download_table(title, rows)
        shown = len(rows)
        note = (f'<p>Showing the {shown} most recent of {count} documents. <a href="{REAL}">The rest are on moh.gov.gh</a>. The ministry does not state file sizes, so they are missing here too; a live service must add them.</p>'
                if count > shown else "<p>The ministry does not state file sizes, so they are missing here too; a live service must add them.</p>")
    P[f"publications/{slug}.html"] = shell(title, f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">{title}</h1>
        <p class="ag-lead">{lead}</p>
      </div>
{body}
      <div class="ag-prose">
        {note}
        <p><a href="../publications.html">All publications</a></p>
      </div>''', current="Publications", root="../", breadcrumb=crumbs(("publications.html", "Publications"), (f"publications/{slug}.html", title)))

# ---------------------------------------------------------------- programmes

P["programmes.html"] = shell("Programmes", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Programmes</h1>
        <p class="ag-lead">The ministry's programmes and projects for child survival, maternal health, climate and health, and healthy living.</p>
      </div>
{cards([(name, short, f"programmes/{slug}.html", None) for slug, name, short, _ in PROGRAMMES], level="h2", variant="ag-card--flag")}
      <div class="ag-prose">
        <p>The ministry's site also carries updates on the <a href="{REAL}qualityrights-in-mental-health-ghana-project/">QualityRights in Mental Health project</a>, a three-year effort to roll out mental health services that respect people's rights.</p>
      </div>''', current="Programmes", breadcrumb=crumbs(("programmes.html", "Programmes")))

for slug, name, short, paras in PROGRAMMES:
    P[f"programmes/{slug}.html"] = shell(name, f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">{name}</h1>
        <p class="ag-lead">{short}</p>
        {"".join(f"<p>{p}</p>" for p in paras)}
        <p><a href="../programmes.html">All programmes</a></p>
      </div>''', current="Programmes", root="../", breadcrumb=crumbs(("programmes.html", "Programmes"), (f"programmes/{slug}.html", name)))

# ---------------------------------------------------------------- media

P["news.html"] = shell("News", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">News</h1>
        <p class="ag-lead">What the ministry and its agencies are doing. The ministry's site does not date its news, so the list is in the order it appears there.</p>
      </div>
      <ul class="ag-list">{dated(NEWS)}
      </ul>
      <nav aria-label="Pagination">
        <ul class="ag-pagination ag-pagination--simple">
          <li><a class="ag-pagination__link" href="{REAL}category/news/" rel="next">Older news, on moh.gov.gh</a></li>
        </ul>
      </nav>''', current="Media", breadcrumb=crumbs(("news.html", "News")))

P["news/free-primary-healthcare.html"] = shell("Free primary healthcare to begin in 150 districts", f'''      <div class="ag-prose">
        <p class="ag-caption">News</p>
        <h1 class="ag-heading-xl">Free primary healthcare to begin in 150 districts</h1>
        <p class="ag-lead">The Minister for Health, Hon. Kwabena Mintah Akandoh, has announced that the free primary healthcare initiative will begin in 150 districts, starting with those that need it most.</p>
      </div>
      <figure class="ag-figure ag-figure--16-9" style="max-width: 48rem">
        <img class="ag-figure__image" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 9'%3E%3Crect width='16' height='9' fill='%23dfe6ec'/%3E%3C/svg%3E" alt="" width="1200" height="675" />
        <figcaption class="ag-figure__caption">The Minister at the announcement. The photograph goes here; the ministry's photographs are not reproduced in this rebuild.</figcaption>
      </figure>
      <div class="ag-prose">
        <p>Under the initiative, care at CHPS compounds, health centres and polyclinics in the chosen districts will be provided at no charge to patients. The ministry has procured 24,534 pieces of medical equipment for the facilities that will deliver it, and a delegation has called on the Ga Mantse ahead of the launch in Accra.</p>
        <p>The rollout is the first phase of a national programme. The ministry has said that more districts will follow as facilities are equipped and staffed.</p>
        <div class="ag-inset"><p>This is a short account. The ministry's own article, which this rebuild does not reproduce in full, is on <a href="{REAL}free-primary-healthcare/">moh.gov.gh</a>.</p></div>
        <p><a href="../news.html">All news</a></p>
      </div>''', current="Media", root="../", breadcrumb=crumbs(("news.html", "News"), ("news/free-primary-healthcare.html", "Free primary healthcare")))

P["press-releases.html"] = shell("Press releases", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Press releases</h1>
        <p class="ag-lead">Statements issued by the ministry. Each link opens the statement on the ministry's site.</p>
      </div>
      <ul class="ag-list">{dated([(r[0], r[1], r[2] if len(r) > 2 else "") for r in PRESS])}
      </ul>
      <nav aria-label="Pagination">
        <ul class="ag-pagination ag-pagination--simple">
          <li><a class="ag-pagination__link" href="{REAL}category/press-releases/" rel="next">Older press releases, on moh.gov.gh</a></li>
        </ul>
      </nav>''', current="Media", breadcrumb=crumbs(("press-releases.html", "Press releases")))

P["events.html"] = shell("Events", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Events</h1>
        <p class="ag-lead">Summits, launches and briefings run or hosted by the ministry, most recent first.</p>
        <div class="ag-inset"><p>The ministry's site posts each event as a picture of its flyer, with no date in the text. The dates here were read from the flyers. Where a flyer gives no date, the block says so.</p></div>
      </div>
{events_html(EVENTS)}''', current="Media", breadcrumb=crumbs(("events.html", "Events")))

P["events/au-summit.html"] = shell("African Union Extraordinary Summit on Health", f'''      <div class="ag-event">
        <time class="ag-event__date ag-event__date--lg" datetime="2026-07-21"><span class="ag-event__day">21</span><span class="ag-event__month">Jul</span></time>
        <div class="ag-event__body">
          <p class="ag-caption">Event, past</p>
          <h1 class="ag-heading-xl">African Union Extraordinary Summit on Health</h1>
          <p class="ag-lead">Heads of state and ministers met in Accra on ending AIDS and TB, improving maternal health, and tackling endemic non-communicable and neglected tropical diseases in Africa.</p>
        </div>
      </div>
      <dl class="ag-summary">
        <div class="ag-summary__row"><dt class="ag-summary__key">When</dt><dd class="ag-summary__value">21 and 22 July 2026</dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Where</dt><dd class="ag-summary__value">Accra, Ghana</dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Host</dt><dd class="ag-summary__value">The Government of Ghana, with the African Union</dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Who it was for</dt><dd class="ag-summary__value">Heads of state, health ministers and partners from African Union member states</dd></div>
      </dl>
      <div class="ag-prose">
        <h2>What it covered</h2>
        <ul>
          <li>Ending AIDS and tuberculosis</li>
          <li>Improving maternal health</li>
          <li>Endemic non-communicable diseases</li>
          <li>Neglected tropical diseases and conditions</li>
        </ul>
        <p>The ministry's news from the summit: <a href="../news.html">Africa's health debate turns urgent in Accra</a>, and the President's call to move Africa's pharmaceutical manufacturing plan beyond paper.</p>
        <div class="ag-inset"><p>This page is built from the summit's flyer on the ministry's site, which gives the dates, the place and the theme. The real page is <a href="{REAL}african-union-extraordinary-summit-on-health/">on moh.gov.gh</a>.</p></div>
        <h2>Questions</h2>
        <p>Email <a href="mailto:info@moh.gov.gh">info@moh.gov.gh</a> or call <a href="tel:+233302665651">+233 302 665 651</a>, Monday to Friday.</p>
        <p><a href="../events.html">All events</a></p>
      </div>''', current="Media", root="../", breadcrumb=crumbs(("events.html", "Events"), ("events/au-summit.html", "African Union summit")))

P["gallery.html"] = shell("Gallery of projects", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Gallery of projects</h1>
        <p class="ag-lead">Photographs of the ministry's capital projects.</p>
        <div class="ag-empty">
          <h2 class="ag-empty__title">No albums are published yet</h2>
          <p>The ministry's gallery page had no photographs when this page was built on 3 October 2026. The projects themselves are described under <a href="publications/capital-projects.html">capital projects</a>.</p>
        </div>
      </div>''', current="Media", breadcrumb=crumbs(("gallery.html", "Gallery")))

P["videos.html"] = shell("Videos", '''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Videos</h1>
        <p class="ag-lead">Recordings from the ministry's events and campaigns.</p>
        <div class="ag-empty">
          <h2 class="ag-empty__title">No videos are published yet</h2>
          <p>The ministry's video page had nothing on it when this page was built on 3 October 2026. Its <a href="https://youtube.com/user/MOHGhana">YouTube channel</a> has recordings.</p>
        </div>
      </div>''', current="Media", breadcrumb=crumbs(("videos.html", "Videos")))

# ---------------------------------------------------------------- tenders, contact, links

P["tenders.html"] = shell("Tenders", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Tenders</h1>
        <p class="ag-lead">Invitations to bid for the ministry's contracts for goods, works and services.</p>
        <div class="ag-empty">
          <h2 class="ag-empty__title">No tenders are open</h2>
          <p>The most recent notices on the ministry's site are from 2017: the printing of medical forms, and of healthcare service registers and reporting forms, both under the Maternal, Child Health and Nutrition Improvement Project. <a href="{REAL}tenders/">See them on moh.gov.gh</a>.</p>
        </div>
        <p>Procurement is run by the <a href="directorates/procurement.html">Procurement and Supply Chain Directorate</a>. Complaints follow the <a href="{UP}2024/04/COMPLAINTS-MECHANISMS.pdf">procurement complaints procedure</a> (PDF).</p>
      </div>''', current="Tenders", breadcrumb=crumbs(("tenders.html", "Tenders")))

P["useful-links.html"] = shell("Useful links", '''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Useful links</h1>
        <p class="ag-lead">Other organisations in Ghana's health sector and in government.</p>
        <h2>Health sector</h2>
        <ul>
          <li><a href="https://ghs.gov.gh/">Ghana Health Service</a></li>
          <li><a href="https://www.nhis.gov.gh/">National Health Insurance Scheme</a></li>
          <li><a href="https://chag.org.gh/">Christian Health Association of Ghana</a></li>
          <li>Community-Based Health Planning and Services</li>
          <li>Regenerative Health</li>
        </ul>
        <h2>Government</h2>
        <ul>
          <li><a href="https://presidency.gov.gh/">The Presidency</a></li>
          <li><a href="https://www.ghana.gov.gh/">The Government of Ghana</a></li>
          <li><a href="https://mofa.gov.gh/">Ministry of Food and Agriculture</a></li>
          <li><a href="https://mrh.gov.gh/">Ministry of Roads and Highways</a></li>
        </ul>
        <h2>International</h2>
        <ul>
          <li><a href="https://www.who.int/">World Health Organization</a></li>
          <li><a href="https://www.unicef.org/ghana/">UNICEF Ghana</a></li>
        </ul>
      </div>''', current="Contact", breadcrumb=crumbs(("useful-links.html", "Useful links")))

P["contact.html"] = shell("Contact the ministry", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Contact the ministry</h1>
        <p class="ag-lead">Send a message, or call or write to the ministry's headquarters in Accra.</p>
        <div class="ag-inset"><p>This form is part of an unofficial rebuild. Nothing you type is sent to the ministry. To reach it, use <a href="{REAL}contact-us/">moh.gov.gh</a>.</p></div>
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
        <div class="ag-field">
          <label class="ag-label" for="subject">What is it about?</label>
          <select class="ag-select" id="subject">
            <option value="">Choose a subject</option>
            <option>A health facility or service</option>
            <option>A publication or document</option>
            <option>A tender</option>
            <option>A media enquiry</option>
            <option>Something else</option>
          </select>
        </div>
        <div class="ag-field" data-ag-char-count>
          <label class="ag-label" for="message">Your message</label>
          <span class="ag-hint" id="message-hint">Up to 500 characters. Do not include medical records or your Ghana Card number.</span>
          <textarea class="ag-textarea" id="message" rows="6" data-ag-max="500" aria-describedby="message-hint message-count"></textarea>
          <span class="ag-char-count__message" id="message-count"></span>
        </div>
        <button class="ag-button" type="submit">Send message</button>
      </form>
      <div class="ag-prose">
        <h2>Other ways to reach the ministry</h2>
      </div>
      <dl class="ag-summary">
        <div class="ag-summary__row"><dt class="ag-summary__key">Phone and fax</dt><dd class="ag-summary__value"><a href="tel:+233302665651">+233 302 665 651</a></dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Email</dt><dd class="ag-summary__value"><a href="mailto:info@moh.gov.gh">info@moh.gov.gh</a></dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Visit</dt><dd class="ag-summary__value">Sekou Toure Street, North Ridge, Accra, next to the National Health Insurance head office</dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Post</dt><dd class="ag-summary__value">P.O. Box M44, Accra</dd></div>
      </dl>''', current="Contact", breadcrumb=crumbs(("contact.html", "Contact")))

P["contact-sent.html"] = shell("Message not sent", f'''      <div class="ag-panel ag-panel--neutral"><h1 class="ag-panel__title">This is where a message would be sent</h1><p class="ag-panel__body">Nothing was sent, because this is an unofficial rebuild.</p></div>
      <div class="ag-prose"><p>On a real service this page confirms the message and gives a reference. To reach the ministry, use <a href="{REAL}contact-us/">moh.gov.gh</a>.</p><p><a href="index.html">Return to the home page</a></p></div>''')

for path, content in P.items():
    write(path, content)
print(f"{len(P)} pages written")
