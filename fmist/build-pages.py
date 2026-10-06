# Generates the rebuilt pages from one shell. Run: python3 build-pages.py
import os, html, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
CDN = os.environ.get("AFRIGOV_CDN", "https://cdn.jsdelivr.net/npm/afrigov@0.15.0/dist/")
REAL = "https://scienceandtech.gov.ng/"
UP = REAL + "wp-content/uploads/"
ORG = "Federal Ministry of Innovation, Science and Technology"
ICONS = json.load(open(os.path.join(HERE, "assets", "social-icons.json")))
TODAY = "2026-10-03"

PORTRAIT = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1 1'%3E%3Crect width='1' height='1' fill='%23dfe6ec'/%3E%3C/svg%3E"
# A wordless drawing where a video's first frame would go: a screen with a play shape.
POSTER = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 9'%3E%3Crect width='16' height='9' fill='%23cfe0d6'/%3E%3Crect x='2' y='1.5' width='12' height='6' rx='0.4' fill='%23a9c7b5'/%3E%3Ccircle cx='8' cy='4.5' r='1.6' fill='%23007d4b'/%3E%3C/svg%3E"
# A wordless drawing for the youth programme: a laptop and a phone.
YSI_DRAWING = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 8 5'%3E%3Crect width='8' height='5' fill='%23e3eee8'/%3E%3Crect x='1.4' y='1' width='3.6' height='2.3' rx='0.15' fill='%23007d4b'/%3E%3Crect x='1.6' y='1.2' width='3.2' height='1.9' fill='%23cfe0d6'/%3E%3Crect x='1' y='3.3' width='4.4' height='0.3' rx='0.1' fill='%23007d4b'/%3E%3Crect x='5.6' y='1.6' width='1.2' height='2.1' rx='0.15' fill='%23007d4b'/%3E%3Crect x='5.75' y='1.8' width='0.9' height='1.6' fill='%23cfe0d6'/%3E%3C/svg%3E"

SOCIAL = [
    ("Facebook", "https://www.facebook.com/fmstng"),
    ("Instagram", "https://www.instagram.com/officialfmstng/"),
    ("X", "https://x.com/FmstNg"),
]

# The navigation: a flat link, or a section with a menu. The first link in a menu is the section's own page.
NAV = [
    ("About", "about.html", [("Mandate and vision", "about.html"), ("Management", "management.html"), ("Departments and units", "departments.html"), ("Agencies", "agencies.html"), ("Policies and resources", "resources.html")]),
    ("Programs", "programs.html", [("All programs", "programs.html"), ("Youth and Students in Innovation", "ysi.html"), ("Events", "events.html")]),
    ("Services", "services.html", None),
    ("Media", "news.html", [("News", "news.html"), ("Videos", "videos.html"), ("Gallery", "gallery.html")]),
    ("Contact", "contact.html", None),
]

MINISTER = ("Dr Kingsley Tochukwu Udeh, SAN", "Honourable Minister of Innovation, Science and Technology", "minister.html")
PERMSEC = ("Dr Mukhtar Yawale Muhammad, MFR, mni", "Permanent Secretary", "permanent-secretary.html")

# (slug or None, name, short name, head). A slug of None means the real site has no page for it.
# The order is the real site's.
DEPARTMENT_LIST = [
    ("human-resource-management", "Human Resource Management", "HRM", "Mr Mark Ochala"),
    ("planning-research-policy", "Planning, Research and Policy Analysis", "PRPA", "Mr Temitope Moses Fatogun"),
    ("finance-accounts", "Finance and Accounts", "F&amp;A", "Mr Umar Mikailu"),
    ("chemical-technology", "Chemical Technology", "CT", "Mrs Stella Igwilo"),
    ("technology-acquisition", "Technology Acquisition and Adaptation", "TAA", "Mr Anpe F. Michael"),
    ("procurement", "Procurement", "", "Mrs Ramota Bamidele Baba-Ahmed"),
    ("energy-technology", "Renewable and Conventional Energy Technology", "RCET", "Mr Adamu A. Suleiman, overseeing director"),
    (None, "Science and Technology Promotion", "STP", "Mr Agoro Olayiwola"),
    ("bioresources-technology", "Bioresources Technology", "BRT", "Mrs Eunice Orekha"),
    (None, "Environmental Science and Technology", "EST", "Mrs Bernadette Ogwuche"),
    ("ict", "Information and Communication Technology", "ICT", "Mr Alex Joseph Gwaske"),
    ("health-biomedical-sciences", "Health and Biomedical Sciences", "HBS", "Mr Adeyemi Adebayo"),
    ("general-services", "General Services", "GS", "Mr Francis Uzoma Oguike"),
    ("special-duties", "Special Duties", "SD", "Mr Kanu Paul Obilo"),
    ("reform-coordination", "Reform Coordination and Service Improvement", "RCSI", "Mr Solomon S.J. Waziri"),
]
UNIT_LIST = [
    (None, "Press and Public Relations", "", "Mrs Pauline Sule"),
    (None, "Legal", "", None),
    (None, "Internal Audit", "", "Mr Aminu Aliyu"),
]

# The pages for departments that have one: (lead, divisions, [(heading, [items])]).
# Condensed from the real pages; the lists keep their substance.
DEPARTMENTS = {
    "human-resource-management": (
        "Sets and runs the policies on how the ministry recruits, pays, trains and looks after its staff, and applies the Federal Government's civil service rules to the ministry and its agencies.",
        ["Appointment, Promotion and Discipline", "Training and Staff Welfare"],
        [("What the department handles", [
            "Appointments, promotions and discipline", "Records of service and salary variations", "Enrolment on IPPIS, the government payroll",
            "Absence requests and redeployment between departments", "The nominal roll", "Conversion, advancement and upgrading of staff",
            "Training needs and requests for further study", "Pensions, retirement and death benefits", "Resettlement allowances",
            "Staff identity cards and NHIS registration"])]),
    "planning-research-policy": (
        "Plans, coordinates, monitors and evaluates the ministry's programmes, across the work of every department. It supervises the National Centre for Technology Management (NACETEM).",
        ["Planning", "Research and Statistics", "Policy Analysis"],
        [("Planning", [
            "Development plans, the capital budget and the medium-term sector strategy", "Links with other federal and state ministries, departments and agencies",
            "Meetings of the Minister and Permanent Secretary with the heads of agencies", "Matters of the National Council on Science and Technology",
            "Liaison with the National Assembly", "The sustainable blue economy"]),
         ("Research and Statistics", [
            "Monitoring and evaluating projects", "Quarterly and annual reports of the ministry's agencies", "Links with research institutes, industry and the private sector",
            "Manpower surveys and statistical data", "Research grants", "The annual ministerial press briefing and the ministerial retreat",
            "The library, and the ministry's key performance indicators"]),
         ("Policy Analysis", [
            "Bilateral and multilateral cooperation, including UNESCO, the African Union and partners in Asia, Europe and the Americas",
            "Science, technology and innovation policy and its review", "Links with the National Planning Commission, the academies, professional bodies and the NUC",
            "Meetings of the Honorary Presidential Advisory Council on Science and Technology", "Memos to the Federal Executive Council",
            "Sustainable Development Goals matters"])]),
    "finance-accounts": (
        "Manages the ministry's budget, payments, payroll and accounts, and answers audit queries. A common service department, it serves every other department.",
        ["Accounts", "Budget"],
        [("What the department handles", [
            "Coordinating the ministry's budget and monitoring how it is spent", "Payments and payroll", "Receipt of funds",
            "Final accounts and financial reports", "Responding to audit queries"]),
         ("Its responsibilities", [
            "Seeing that staff follow the financial regulations and the accounting code", "Supervising the disbursement of funds and accounting for revenue",
            "Advising the accounting officer on financial matters", "Keeping the books of account and ledgers",
            "Sending returns on time, such as monthly accounts and bank reconciliations", "Preparing and defending the budget, and comparing it with actual spending",
            "Keeping an audit query unit that answers the Internal Audit Unit, the Accountant-General, the Auditor-General and the Public Accounts Committee",
            "Training the department's staff"])]),
    "chemical-technology": (
        "Develops policy on chemicals and materials technology, and coordinates research and development in them across Nigeria. Created in 2015 from the former Chemical Technology and Energy Research department.",
        ["Chemical Technology Research and Development", "Materials Technology Research and Development"],
        [("Vision and mission", [
            "Vision: to make Nigeria a globally recognised leader in science, technology and innovation through chemical technology.",
            "Mission: to make chemical technology contribute to Nigeria's sustainable development."]),
         ("What the department does", [
            "Develops and reviews policies on chemical, materials, leather, solid minerals and nanotechnology",
            "Works with ministries, universities, regulators and laboratories on using chemical and materials technologies",
            "Builds national capacity in producing, storing, supplying and standardising chemicals",
            "Works with research institutes on indigenous chemical and process technologies",
            "Coordinates the reduction of persistent organic pollutants, and mercury-free devices",
            "Develops policies for a National Chemical Bank, a National Toxicology Centre and chemical risk assessment",
            "Works with the Organisation for the Prohibition of Chemical Weapons and the Rotterdam, Stockholm, Basel, Minamata and Bamako conventions",
            "Supports research for the building, construction, agricultural and petrochemical sectors"]),
         ("Achievements the department lists", [
            "A National Policy on Nanotechnology, prepared for the Federal Executive Council",
            "A draft National Policy on Chemical Technology, validated by stakeholders in Kano and Akwa Ibom",
            "Work with the Federal Ministry of Education on teaching chemical safety and security, with a pilot in schools in the North Central zone",
            "Forums in the South West on the misuse of chemical, biological, radiological, nuclear and explosive materials",
            "A consultative forum in Ibadan towards a national policy on dyes and dye products"])]),
    "technology-acquisition": (
        "Bridges the gap between research and industry: it helps turn research results into businesses, through technology incubation, pilot ventures with private investors, and the acquisition and adaptation of technologies. It supervises PRODA, NOTAP and SHESTCO.",
        ["Technology Acquisition", "Technology Adaptation"],
        [("Vision and mission", [
            "Vision: to coordinate the acquisition of foreign and indigenous technologies and their use in Nigeria.",
            "Mission: to develop Nigeria technologically through indigenous invention, innovation and adopted technology."]),
         ("What the department does", [
            "Sets policy on acquiring technology from Nigeria's research institutes and universities, and from other countries",
            "Assesses and promotes technologies developed by Nigerian inventors and entrepreneurs",
            "Designs programmes that set up incubator industries from those technologies, with technical and financial partners",
            "Works with lawmakers on laws that protect Nigerian enterprises built on local or acquired technology",
            "Works with ministries, agencies and the private sector on turning research into industry"]),
         ("Its four sections", [
            "Innovation, Research and Development: data on invention in universities, institutes and among individuals, and support for inventors under the Presidential Standing Committee on Inventions and Innovations",
            "Technology Acquisition and Reverse Engineering: improving local technology to international standards, and adapting foreign technology to Nigerian conditions",
            "Technology Needs Assessment: identifying the country's technology needs",
            "Technology Impact Assessment: surveying how introduced technologies are working, and proposing fixes"])]),
    "procurement": (
        "Plans and carries out the procurement for all the ministry's projects and programmes, under the Public Procurement Act 2007. It has fifteen staff.",
        ["Capital Procurement", "Recurrent Procurement"],
        [("What the department does", [
            "Procurement planning and implementation for the ministry", "Serves as secretariat to the Ministerial Tenders Board and the Procurement Planning Committee",
            "Checks with stock verifiers and user departments that goods, works and services meet the contract",
            "Sends procurement records and plans to the Bureau of Public Procurement each year, and requests its certificates of no objection",
            "Handles petitions about procurement processes"])]),
    "energy-technology": (
        "Promotes and coordinates research and development for better generation, transmission, distribution and use of energy, in ways that protect the environment. It works with other ministries, the private sector and international bodies on nuclear, renewable and conventional energy.",
        ["Renewable Energy", "Conventional Energy", "Nuclear Energy"],
        [("What the department does", [
            "Develops energy policies with other ministries and the private sector, consistent with the National Energy Policy",
            "Sets priorities for energy research, including nuclear, oil and gas, and tar sands",
            "Supervises the ministry's energy research institutions",
            "Plans how renewable energy joins the energy mix, and its use to transform rural communities",
            "Develops capability in solar, wind, biofuel and hydro energy, and in locally made power equipment",
            "Works with the International Atomic Energy Agency on nuclear power and the use of radioactive agents",
            "Promotes clean coal technology",
            "Keeps a record of energy statistics and economics",
            "Runs public awareness programmes on energy sources"])]),
    "bioresources-technology": (
        "Responsible for developing and sustainably managing Nigeria's biological resources. The National Biotechnology Research and Development Agency (NBRDA), with 24 bioresource centres across the six geopolitical zones, is under its supervision.",
        ["Biotechnology Research and Development", "Biodiversity Conservation and Utilisation Research and Development"],
        [("What the department does", [
            "Formulates, monitors and reviews science, technology and innovation policy for bioresources",
            "Applies science and technology to conserve, map, bio-prospect, commercialise and manage Nigeria's biodiversity",
            "Gives technical support to entrepreneurs and the private sector in bioresource conservation and commercialisation",
            "Monitors and coordinates research and development in bioresources",
            "Writes guidelines on conserving and using bioresources, on commercialising them, and on releasing agricultural varieties",
            "Works with local and international bodies on biodiversity management"])]),
    "ict": (
        "Sets, carries out and monitors policy for information and communication technology in science and technology, and runs the ministry's own computers, networks and websites. Created in 2007, it reports directly to the Permanent Secretary.",
        [],
        [("What the department does", [
            "Oversees ICT infrastructure and software development", "Runs the ministry's computer networks and internet connection",
            "Builds and maintains the ministry's websites, including scienceandtech.gov.ng and nigeriatechnoexpo.gov.ng",
            "Trains the ministry's staff in ICT", "Represents the ministry on ICT committees and at conferences such as ITU and WSIS",
            "Contributes to reviews of the National ICT Policy"]),
         ("Day-to-day services", [
            "Hardware, software and network management", "Email administration", "Databases", "Business process automation",
            "The IT help desk and technical support", "Buying hardware and software", "IT security"])]),
    "health-biomedical-sciences": (
        "Develops policy on health and biomedical technologies, and promotes inventions that meet local needs. It supervises science programmes at NITR in Kaduna, NNMDA in Lagos, and NiCFoST.",
        [],
        [("What the department does", [
            "Develops and reviews policies on health and biomedical technologies",
            "Works with local and international bodies on nutrition, food safety and food security",
            "Builds capacity in health and biomedical technologies",
            "Works with the private sector and research institutions to develop and use indigenous health technologies",
            "Coordinates and evaluates research in health and biomedical technologies in institutions the ministry supervises"]),
         ("Programmes", [
            "Better planting materials grown with temporary immersion bioreactors, for food security",
            "Testing and preserving beans and grains, and training on the safe use of pesticides",
            "Developing and testing herbal remedies for epilepsy, malaria, sickle cell anaemia and trypanosomiasis",
            "Reducing post-harvest losses in fruits and vegetables",
            "Labour-saving technologies that reduce women's workload, in the six geopolitical zones",
            "Research on under-used, highly nutritious foods",
            "Research on herbal medicine use among urban residents",
            "A social innovation in health initiative for vulnerable communities",
            "Small grants to standardise local recipes and portion sizes",
            "Herbal antidotes for snake bites"])]),
    "general-services": (
        "Maintains and services all the ministry's movable and immovable assets, so the offices work and staff are looked after.",
        ["Maintenance", "Stores", "Office Management", "Transport"],
        [("What the department does", [
            "Manages and pays the cleaning contractors, and disinfects the offices each quarter", "Environmental management and office space",
            "Buys supplies and runs the stores", "Registers, allocates, fuels and maintains the ministry's vehicles",
            "Buys new vehicles and disposes of unserviceable ones", "Repairs equipment and installs new equipment"])]),
    "special-duties": (
        "Supports the Permanent Secretary in managing the ministry and its agencies, and runs three units that used to report to the Permanent Secretary directly. Created in March 2014.",
        ["Travel and Protocol", "Anti-Corruption and Transparency", "Stock Verification"],
        [("What the department does", [
            "Helps the Permanent Secretary supervise the staff of the ministry and its agencies",
            "Represents the Permanent Secretary at some functions, and manages access and schedules",
            "Coordinates responses to emergencies, and supports leadership transitions",
            "Monitors capital and constituency projects", "Liaises with the National Assembly"]),
         ("Travel and Protocol", [
            "Travel, passports, visas and hotels for the Minister, the Permanent Secretary and staff", "Courtesy calls, reception and airport arrivals",
            "Liaison with the Ministry of Foreign Affairs, embassies and the State House"]),
         ("Anti-Corruption and Transparency", [
            "Inaugurated by the ICPC on 13 April 2017",
            "Educates staff and the public on corruption", "Monitors budget implementation", "Enforces the codes of ethics",
            "Carries out preliminary investigations", "Observes the staff, procurement and tender committees"]),
         ("Stock Verification", [
            "Checks supplies, works and services when they are delivered and before payment", "Checks the stores at least twice a year",
            "Analyses prices", "Keeps a yearly inventory of furniture, equipment and vehicles"])]),
    "reform-coordination": (
        "Leads reform and service improvement in the ministry, and runs SERVICOM, the federal service charter programme, in the ministry and its agencies.",
        [],
        [("What the department does", [
            "Drives reform, innovation and improvement in line with the framework of the Head of the Civil Service of the Federation",
            "Manages SERVICOM in the ministry and its agencies, quarterly",
            "Works with the ministry's leaders to find gaps in processes, systems and services, and develops fixes for them",
            "Investigates service failures, and adopts good practice from elsewhere",
            "Builds a culture of continuous service improvement"])]),
}

PROGRAMS = [
    # (slug or None, name, summary)
    ("technology-innovation-expo", "Technology and Innovation Expo", "Nigeria's yearly science and technology exhibition, held in the third week of October, where researchers and inventors meet investors."),
    ("yonspa", "774 Young Nigerian Scientists Presidential Award", "A yearly science competition for secondary school students in all 774 local government areas."),
    (None, "Presidential Standing Committee on Inventions and Innovations", "Promotes and funds Nigerian inventions, with a focus on bringing them to market."),
    ("ncist", "National Council on Innovation, Science and Technology", "The yearly policy meeting of governments, scientists, industry and partners on Nigeria's science agenda."),
    (None, "Waste to Wealth", "Turning waste into useful resources, for jobs and a cleaner environment."),
    (None, "Nanotechnology", "Research on materials at the molecular level, for medicine, electronics, agriculture and manufacturing."),
    (None, "Methanol", "Methanol as a cleaner fuel and a way to store renewable energy for transport and power."),
    ("grand-challenges-nigeria", "Grand Challenges Nigeria", "A network of local researchers working on public health, agriculture, nutrition and climate, launched in November 2024."),
]

SERVICES = [
    ("Patent registration", "Protect an invention, so you hold the rights to it.", "National Office for Technology Acquisition and Promotion (NOTAP)", "https://notap.gov.ng/"),
    ("Technology transfer registration", "Register an agreement to bring in or license a technology, between inventors, researchers and companies.", "National Office for Technology Acquisition and Promotion (NOTAP)", "https://notap.gov.ng/services/ttr.html"),
    ("Technology incubation", "Space, mentoring and support for an early-stage technology business.", "National Board for Technology Incubation (NBTI)", "https://nbti.gov.ng/"),
    ("Master's or postgraduate diploma in technology management", "Study the management of technology and innovation.", "National Centre for Technology Management (NACETEM)", "https://nacetem.gov.ng/postgraduate-diploma-in-technology-management/"),
    ("Science laboratory technology membership", "Join the professional body for science laboratory technologists.", "Nigerian Institute of Science Laboratory Technology (NISLT)", "https://www.nislt.gov.ng/aboutmembership.php"),
]

AGENCIES = [
    ("Energy Commission of Nigeria", "ECN", "https://energy.gov.ng/"),
    ("Nigerian Institute for Trypanosomiasis Research", "NITR", "https://www.nitr.gov.ng/"),
    ("Nigeria Natural Medicine Development Agency", "NNMDA", "https://nnmda.gov.ng/"),
    ("Projects Development Institute", "PRODA", "https://proda.gov.ng/"),
    ("Nigerian Building and Road Research Institute", "NBRRI", "https://nbrri.gov.ng/"),
    ("National Space Research and Development Agency", "NASRDA", "https://central.nasrda.gov.ng/"),
    ("National Board for Technology Incubation", "NBTI", "https://nbti.gov.ng/"),
    ("Raw Materials Research and Development Council", "RMRDC", "https://rmrdc.gov.ng/"),
    ("Sheda Science and Technology Complex", "SHESTCO", "https://shestco.gov.ng/"),
    ("Nigerian Institute of Science Laboratory Technology", "NISLT", "https://www.nislt.gov.ng/"),
    ("Federal Institute of Industrial Research, Oshodi", "FIIRO", "https://www.fiiro.gov.ng/"),
    ("National Centre for Technology Management", "NACETEM", "https://www.nacetem.gov.ng/"),
    ("National Office for Technology Acquisition and Promotion", "NOTAP", "https://www.notap.gov.ng/"),
    ("National Biotechnology Research and Development Agency", "NBRDA", "https://nbrda.gov.ng/"),
    ("Nigerian Council of Food Science and Technology", "NiCFoST", "https://nicfost.gov.ng/"),
    ("Nigerian Institute of Leather and Science Technology, Zaria", "NILEST", "https://nilest.edu.ng/"),
    ("National Research Institute for Chemical Technology", "NARICT", "https://narict.gov.ng/"),
]

# (link, headline, date). The first four are rebuilt; the rest open on the real site.
NEWS = [
    ("news/nbti-ebsu-dispute.html", "Minister resolves the land dispute between NBTI and Ebonyi State University", "9 June 2026"),
    ("news/forensic-science.html", "Ministry seeks a partnership to advance forensic science in the justice system", "4 June 2026"),
    ("news/wipo-partnership.html", "Ministry and WIPO move towards a partnership on innovation and intellectual property", "3 June 2026"),
    ("news/plasstifest-2026.html", "Minister sets out what states can do for innovation, at PLASSTIFEST 2026", "3 June 2026"),
    (REAL + "fmist-reaffirms-commitment-to-institutional-reforms-innovation-driven-governance-and-efficient-public-service-delivery/", "Ministry reaffirms its commitment to institutional reform and public service delivery", "14 May 2026"),
    (REAL + "fg-launches-aggressive-solarization-drive-breaks-ground-on-solar-minigrids-in-kano/", "Work starts on solar minigrids for tertiary institutions in Kano", "4 May 2026"),
    (REAL + "first-lady-sen-oluremi-tinubu-flags-off-econ-hails-fmist-minister-as-nigeria-ignites-innovation-to-wealth-drive/", "First Lady launches the Energise Commercialisation Now initiative", "24 April 2026"),
    (REAL + "fmist-swap-unitaid-forge-alliance-on-climate-smart-healthcare-in-nigeria/", "Ministry, SWAP and Unitaid partner on climate-smart healthcare", "20 April 2026"),
    (REAL + "fmist-gains-momentum-for-national-econ-flag-off-as-plateau-commissioner-visits-minister/", "Plateau commissioner visits the Minister ahead of the ECoN launch", "17 April 2026"),
    (REAL + "ebiogeh-bows-out-as-mukhtar-takes-over-as-permanent-secretary-fmist/", "Dr Mukhtar Yawale Muhammad takes over as Permanent Secretary", "16 April 2026"),
]

# (title, link, ISO date or None, day, month, meta line, one line about it)
EVENTS = [
    ("Technology and Innovation Expo 2026", "events/technology-innovation-expo.html", None, "", "", "Third week of October 2026. The ministry has not announced the dates or the venue.", "Inventions, research and new companies on show, with investors and agencies."),
    ("Youth and Students in Innovation, in-person session", "ysi.html", None, "", "", "Enugu. The ministry has not announced the date.", "Three days in person for the people who complete the online phase."),
    ("Launch of Energise Commercialisation Now (ECoN)", REAL + "first-lady-sen-oluremi-tinubu-flags-off-econ-hails-fmist-minister-as-nigeria-ignites-innovation-to-wealth-drive/", "2026-04-24", "24", "Apr", "24 April 2026", "Launched by the First Lady, to move research from laboratories to the market."),
]

VIDEOS = [
    # (slug, title, source, date, length m:ss, length words, file, what it covers)
    ("econ-good-morning-nigeria", "The ECoN initiative on Good Morning Nigeria", "NTA", "16 April 2026", "4:04", "4 min 4 s",
     UP + "2026/04/WhatsApp-Video-2026-04-16-at-10.31.04-AM.mp4",
     "A television interview on NTA's Good Morning Nigeria about Energise Commercialisation Now, the initiative to move research from laboratories to the market, ahead of its launch."),
    ("minister-arise-news", "The Minister on Arise News", "Arise News", "17 April 2026", "2:02", "2 min 2 s",
     UP + "2026/04/WhatsApp-Video-2026-04-17-at-2.52.37-PM.mp4",
     "The Minister, Dr Kingsley Tochukwu Udeh, interviewed on Arise News."),
]

RESOURCES = [
    ("National Science, Technology and Innovation Policy", "The policy for using science, technology and innovation to build a large, diverse and competitive economy.", UP + "2025/12/National-Science-Technology-and-Innovation-Policy-NSTIP-POLICY.pdf", "PDF, 759 KB"),
    ("National Science, Technology and Innovation Roadmap 2030", "The roadmap in three periods: 2017 to 2020, 2021 to 2025, and 2026 to 2030.", UP + "2025/12/National-Science-Technology-and-Innovation-Roadmap-NSTIR-2030-An-Integrated-Roadmap-2017-2030_1661865171.pdf", "PDF, 21.1 MB"),
    ("Presidential Executive Order No. 5, Official Gazette", "Local content in science, technology and innovation, for self-reliance.", UP + "2025/12/OfficialGazette_ExecOrderNo5-.pdf", "PDF, 1.6 MB"),
    ("National Policy on Methanol Fuel Production Technology", "Using natural gas and biomass to expand the chemicals industry.", UP + "2025/12/METHANOL-POLICY-JUNE-6-2022.pdf", "PDF, 484 KB"),
    ("Communique of the 2023 National Council on Science, Technology and Innovation", "STI for all: advancing Nigeria's Agenda 2050.", UP + "2025/12/COMMUNIQUE-SUMMARY-of-the-2023-ncsti.docx", "Word document, 27 KB"),
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


def shell(title, main, current=None, root="", breadcrumb=None, wide=False, index=True):
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
          <p>This is a demonstration built on afrigov. It is not run by the Federal Ministry of Innovation, Science and Technology. The real website is <a href="{REAL}">scienceandtech.gov.ng</a>.</p>
          <p>Official websites use .gov.ng. This one does not, and it carries no government seal. Nothing you type here is sent to the ministry.</p>
        </details>
      </div>
    </section>

    <header class="ag-header">
      <div class="ag-container ag-header__inner">
        <a class="ag-header__brand" href="{r}index.html">
          <img class="ag-header__logo" src="{r}assets/mark.svg" alt="" width="40" height="40" />
          <span>
            <span class="ag-header__org">Innovation, Science and Technology</span>
            <span class="ag-header__sub">Federal Ministry, Nigeria</span>
          </span>
        </a>
        <details class="ag-header__search" data-ag-menu>
          <summary class="ag-header__search-toggle"><span class="ag-search__icon" aria-hidden="true"></span><span class="ag-visually-hidden">Search</span></summary>
          <div class="ag-header__search-panel">
            <div class="ag-container">
              <form class="ag-search" role="search" action="{r}search.html" method="get">
                <label class="ag-search__label" for="header-q">Search this site</label>
                <div class="ag-search__row">
                  <input class="ag-search__input" type="search" id="header-q" name="q" />
                  <button class="ag-search__button" type="submit"><span class="ag-search__icon" aria-hidden="true"></span>Search</button>
                </div>
              </form>
            </div>
          </div>
        </details>
        <button class="ag-header__toggle" type="button" aria-expanded="false" aria-controls="nav" data-ag-toggle>Menu</button>
        <nav class="ag-header__nav" id="nav" aria-label="Main">
          <ul class="ag-nav">
{nav_html(current, r)}
          </ul>
        </nav>
      </div>
    </header>

    <main class="{main_class}" id="main" tabindex="-1"{" data-pagefind-body" if index else ""}>
{crumb}{main}
    </main>

    <footer class="ag-footer">
      <div class="ag-container">
        <div class="ag-footer__columns">
          <div>
            <h2 class="ag-footer__heading">The ministry</h2>
            <ul class="ag-footer__list">
              <li><a href="{r}about.html">Mandate and vision</a></li>
              <li><a href="{r}management.html">Management</a></li>
              <li><a href="{r}departments.html">Departments and units</a></li>
              <li><a href="{r}agencies.html">Agencies</a></li>
            </ul>
          </div>
          <div>
            <h2 class="ag-footer__heading">What we do</h2>
            <ul class="ag-footer__list">
              <li><a href="{r}services.html">Services</a></li>
              <li><a href="{r}programs.html">Programs</a></li>
              <li><a href="{r}events.html">Events</a></li>
              <li><a href="{r}resources.html">Policies and resources</a></li>
              <li><a href="{r}news.html">News</a></li>
              <li><a href="{r}videos.html">Videos</a></li>
            </ul>
          </div>
          <div>
            <h2 class="ag-footer__heading">Contact</h2>
            <address class="ag-footer__address">
              Federal Secretariat Complex Phase II,<br />
              Block D, 4th to 8th Floor,<br />
              Shehu Shagari Way, Abuja, FCT
            </address>
            <ul class="ag-footer__list">
              <li><a href="tel:+2348140000278">+234 814 000 0278</a></li>
              <li><a href="mailto:info@scienceandtech.gov.ng">info@scienceandtech.gov.ng</a></li>
              <li><a href="{r}contact.html">Send a message</a></li>
            </ul>
            <ul class="ag-social">
{social}
            </ul>
          </div>
        </div>
        <div class="ag-footer__bar">
          <span class="ag-flag" aria-hidden="true"><span></span><span></span><span></span></span>
          <p>Unofficial rebuild of <a href="{REAL}">scienceandtech.gov.ng</a> on <a href="https://github.com/omoyolab/afrigov">afrigov</a>, for demonstration. The ministry and its agencies own their content.</p>
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


def cards(items, level="h2", variant="", root=""):
    out = ""
    for title, text, href, meta in items:
        if href:
            href = href if href.startswith("http") else root + href
        heading = f'<a class="ag-card__link" href="{href}">{title}</a>' if href else title
        m = f'\n          <p class="ag-card__meta">{meta}</p>' if meta else ""
        out += f'''
        <li class="ag-card{(" " + variant) if variant else ""}">
          <{level} class="ag-card__title">{heading}</{level}>
          <p class="ag-card__text">{text}</p>{m}
        </li>'''
    return f'      <ul class="ag-cards">{out}\n      </ul>'


def people(rows, variant="", level="h3", root=""):
    items = ""
    for row in rows:
        name, role = row[0], row[1]
        link = row[2] if len(row) > 2 else None
        title = f'<a href="{root}{link}">{name}</a>' if link else name
        items += f'''
        <li class="ag-person">
          <img class="ag-person__photo" src="{PORTRAIT}" alt="" width="320" height="320" loading="lazy" />
          <div>
            <{level} class="ag-person__name">{title}</{level}>
            <p class="ag-person__role">{role}</p>
          </div>
        </li>'''
    return f'      <ul class="ag-people{(" " + variant) if variant else ""}">{items}\n      </ul>'


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
            <p class="ag-event__meta">{meta}{". Past event." if past else ""}</p>{line}
          </div>
        </li>'''
    return f'      <ul class="ag-events">{out}\n      </ul>'


def dated(rows, root=""):
    return "".join(
        f'''
        <li class="ag-list__item">
          <a class="ag-list__link" href="{h if h.startswith("http") else root + h}">{t}</a><span class="ag-list__meta">{m}</span>
        </li>'''
        for h, t, m in rows
    )


def video_cards(rows, level="h2", root=""):
    out = ""
    for slug, title, source, date, length, _, _, _ in rows:
        out += f'''
        <li class="ag-card ag-card--video">
          <div class="ag-card__image">
            <img src="{POSTER}" alt="" width="640" height="360" loading="lazy" />
            <span class="ag-card__duration"><span class="ag-visually-hidden">Length </span>{length}</span>
          </div>
          <{level} class="ag-card__title"><a class="ag-card__link" href="{root}videos/{slug}.html">{title}</a></{level}>
          <p class="ag-card__text">{source} · {date}</p>
        </li>'''
    return f'      <ul class="ag-cards">{out}\n      </ul>'


def bullets(items):
    return "<ul>" + "".join(f"\n          <li>{i}</li>" for i in items) + "\n        </ul>"


P = {}

# ---------------------------------------------------------------- home

P["index.html"] = shell(ORG, f'''      <div class="ag-hero ag-hero--primary ag-hero--tall">
        <div class="ag-container ag-hero__inner">
          <div>
            <h1 class="ag-heading-xl ag-hero__title">Science, technology and innovation for Nigeria</h1>
            <p class="ag-lead ag-hero__lead">Our mission is a sustainable, knowledge-based economy for Nigeria, built on research and new technology.</p>
            <div class="ag-button-group ag-hero__actions">
              <a class="ag-button ag-button--start" href="services.html">Find a service</a>
              <a class="ag-button ag-button--secondary" href="programs.html">Our programs</a>
            </div>
            <div class="ag-mt-6">
              <p>Coming up: <a href="events/technology-innovation-expo.html">Technology and Innovation Expo 2026</a>, third week of October.</p>
              <p class="ag-mb-0">Read the <a href="{RESOURCES[0][2]}">National Science, Technology and Innovation Policy</a> (PDF, 759 KB).</p>
            </div>
          </div>
        </div>
      </div>

      <div class="ag-container">
        <h2 class="ag-visually-hidden">The ministry in numbers</h2>
        <dl class="ag-stats">
          <div class="ag-stats__item"><dt class="ag-stats__label">Founded</dt><dd class="ag-stats__value">1980</dd></div>
          <div class="ag-stats__item"><dt class="ag-stats__label"><a href="departments.html">Departments</a></dt><dd class="ag-stats__value">15</dd></div>
          <div class="ag-stats__item"><dt class="ag-stats__label"><a href="departments.html#units">Units</a></dt><dd class="ag-stats__value">3</dd></div>
          <div class="ag-stats__item"><dt class="ag-stats__label"><a href="agencies.html">Agencies</a></dt><dd class="ag-stats__value">17</dd></div>
        </dl>

        <h2>Services</h2>
        <p class="ag-prose">The ministry's agencies deliver these services. Each link goes to the agency that handles it.</p>
{cards([(t, d, u, "Handled by " + re.sub(r" \\(.*\\)", "", a)) for t, d, a, u in SERVICES[:3]], level="h3", variant="ag-card--accent")}
        <p><a href="services.html">All five services</a></p>
      </div>

      <div class="ag-band ag-band--tint">
        <div class="ag-container">
          <div class="ag-feature ag-mb-0">
            <figure class="ag-figure ag-feature__media">
              <img class="ag-figure__image" src="{YSI_DRAWING}" alt="" width="800" height="500" loading="lazy" />
            </figure>
            <div class="ag-feature__body">
              <h2 class="ag-feature__title">Youth and Students in Innovation 2026</h2>
              <p>Practical training in digital skills, AI and innovation for Nigerians aged 18 to 30: three weeks online, then three days in person in Enugu.</p>
              <ul class="ag-feature__list">
                <li>Eight tracks, from software and AI to agritech and fintech</li>
                <li>Mentoring after the programme</li>
                <li>Applications closed on 14 September 2026</li>
              </ul>
              <p><a href="ysi.html">About the programme</a></p>
            </div>
          </div>
        </div>
      </div>

      <div class="ag-container">
        <h2>Events</h2>
{events_html(EVENTS[:2])}
        <p><a href="events.html">All events</a></p>

        <h2>Leadership</h2>
{people([MINISTER, PERMSEC], "ag-people--2")}
        <p><a href="management.html">Management and directors</a></p>

        <h2 id="news">News</h2>
        <ul class="ag-list">{dated(NEWS[:4])}
        </ul>
        <p><a href="news.html">All news</a></p>

        <h2>Latest videos</h2>
{video_cards(VIDEOS, level="h3")}
        <p><a href="videos.html">All videos</a></p>
      </div>''', current="Home", wide=True)

# ---------------------------------------------------------------- about

P["about.html"] = shell("Mandate and vision", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Mandate and vision</h1>
        <p class="ag-lead">The ministry was established in 1980 to use science, technology and innovation for Nigeria's economic and social development. It works with research institutes, its agencies and other parts of government.</p>
      </div>
      <dl class="ag-summary">
        <div class="ag-summary__row"><dt class="ag-summary__key">Mission</dt><dd class="ag-summary__value">To use science, technology and innovation to build a sustainable, knowledge-based economy for Nigeria.</dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Vision</dt><dd class="ag-summary__value">To be the leading national science, technology and innovation institution in Africa, comparable with the best in the world.</dd></div>
      </dl>
      <div class="ag-prose">
        <h2 id="why">Why the ministry exists</h2>
        <p>The National Science, Technology and Innovation Policy of 2022 makes the ministry the platform where federal agencies and state ministries work together on science, technology and innovation. It promotes research and new technology in every sector of the economy, for inclusive growth, national security, agriculture, infrastructure and industry.</p>

        <h2 id="mandate">Mandate</h2>
        <ol>
          <li>To promote science and technology in Nigeria, under chapter 2, section 18(2) of the 1999 Constitution.</li>
          <li>To establish research institutes, with the President's approval, under the National Science and Technology Act of 1980.</li>
          <li>To be the platform for collaboration between federal agencies and state ministries on science, technology and innovation, under the 2022 policy.</li>
          <li>To work as a service ministry with every relevant agency, so the results of research are applied across the economy: industry, agriculture, health, energy, the environment, security, youth and women's empowerment, and more.</li>
        </ol>

        <h2 id="objectives">Objectives</h2>
      </div>
      <dl class="ag-summary">
        <div class="ag-summary__row"><dt class="ag-summary__key">Promote science and innovation</dt><dd class="ag-summary__value">Advance their use to raise productivity in every sector.</dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Work with federal and state bodies</dt><dd class="ag-summary__value">Be the platform where they carry out science initiatives together.</dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Implement the national policy</dt><dd class="ag-summary__value">Carry out the National Science, Technology and Innovation Policy.</dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Support research</dt><dd class="ag-summary__value">Encourage research and development that solves problems.</dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Transfer technology</dt><dd class="ag-summary__value">Move technology between researchers, inventors and industry.</dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Build the legal framework</dt><dd class="ag-summary__value">Create the policies, laws and institutions that support the sector.</dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Fund the sector</dt><dd class="ag-summary__value">Secure and allocate money for science and innovation projects.</dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Build skills</dt><dd class="ag-summary__value">Train people in science and technology.</dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Industrialise and digitise</dt><dd class="ag-summary__value">Lead the industrialisation and digitisation of the economy.</dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Solve national problems</dt><dd class="ag-summary__value">Apply science to agriculture, health, education and security.</dd></div>
      </dl>
      <div class="ag-prose">
        <h2 id="leaders">Leadership</h2>
        <p>The ministry is led by the Honourable Minister, <a href="minister.html">{MINISTER[0]}</a>, and the Permanent Secretary, <a href="permanent-secretary.html">{PERMSEC[0]}</a>. See the <a href="management.html">management and directors</a>.</p>
      </div>''', current="About", breadcrumb=crumbs(("about.html", "Mandate and vision")))

DIRECTORS = [(head.replace(", overseeing director", ""), ("Overseeing Director, " if "overseeing" in head else "Director, ") + name + (f" ({short})" if short else ""))
             for _, name, short, head in DEPARTMENT_LIST] + [
    ("Dr Victor Fadipe", "Head, Public-Private Partnership"),
    ("Mrs Pauline Sule", "Head, Press and Public Relations"),
    ("Mr Aminu Aliyu", "Director, Internal Audit"),
]

P["management.html"] = shell("Management", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Management</h1>
        <p class="ag-lead">The ministry has 15 departments, 3 units and 17 agencies, under the supervision of the Honourable Minister.</p>
        <h2>Leadership</h2>
      </div>
{people([MINISTER, PERMSEC], "ag-people--2")}
      <div class="ag-prose">
        <h2>Directors and heads of units</h2>
      </div>
{people(DIRECTORS, "ag-people--4")}
      <div class="ag-prose">
        <p>See what each <a href="departments.html">department and unit</a> does.</p>
      </div>''', current="About", breadcrumb=crumbs(("about.html", "About"), ("management.html", "Management")))

P["minister.html"] = shell(MINISTER[0], f'''      <div class="ag-prose">
        <p class="ag-caption">{MINISTER[1]}</p>
        <h1 class="ag-heading-xl">{MINISTER[0]}</h1>
        <p class="ag-lead">A lawyer, academic and public administrator, appointed by President Bola Ahmed Tinubu and confirmed by the Senate in November 2025.</p>
      </div>
{people([("Dr Kingsley Tochukwu Udeh", "Honourable Minister")], "ag-people--rows", level="h2")}
      <div class="ag-prose">
        <p>Dr Udeh is a Senior Advocate of Nigeria, with experience in public, constitutional and administrative law and in policy development. Before his appointment he was Attorney-General and Commissioner for Justice of Enugu State, where he worked on legal reform and the administration of justice.</p>
        <p>He holds a Bachelor of Laws from the University of Nigeria, a Master of Laws in Public International Law from the University of Nottingham, and a Doctor of Laws in Public Law from Stellenbosch University. His research is on public procurement law and governance.</p>
        <p><a href="management.html">Management</a></p>
      </div>''', current="About", breadcrumb=crumbs(("management.html", "Management"), ("minister.html", "The Minister")))

P["permanent-secretary.html"] = shell(PERMSEC[0], f'''      <div class="ag-prose">
        <p class="ag-caption">{PERMSEC[1]}</p>
        <h1 class="ag-heading-xl">{PERMSEC[0]}</h1>
        <p class="ag-lead">A public health physician and medical epidemiologist, Permanent Secretary of the ministry since April 2026.</p>
      </div>
{people([("Dr Mukhtar Yawale Muhammad", "Permanent Secretary")], "ag-people--rows", level="h2")}
      <div class="ag-prose">
        <p>Dr Muhammad joined the Federal Civil Service as a medical officer in the Federal Ministry of Health and became a Director in 2021. He has also worked with Family Health International, the US Centers for Disease Control, the Global Fund, the World Health Organization and UNAIDS, on HIV epidemiology, surveillance and quality management.</p>
        <p>During the COVID-19 pandemic he was National Incident Manager, then National Coordinator of the Presidential Task Force on COVID-19, leading the technical team behind testing, surveillance and isolation centres.</p>
        <p>Before this appointment he was Director of the Basic Healthcare Provision Fund, and Permanent Secretary of the Federal Ministry of Arts, Culture, Tourism and Creative Economy. He represents the North-West zone among the Federal Permanent Secretaries.</p>
        <p>He holds an MBBS from the University of Maiduguri, a postgraduate diploma in epidemiology from the University of Liverpool, a Master's in Public Health from Ahmadu Bello University, a Master's in Legislative Studies from the University of Benin and an MBA from the University of Cumbria. He is an alumnus of the National Institute for Policy and Strategic Studies, and a Member of the Order of the Federal Republic.</p>
        <p><a href="management.html">Management</a></p>
      </div>''', current="About", breadcrumb=crumbs(("management.html", "Management"), ("permanent-secretary.html", "The Permanent Secretary")))

# ---------------------------------------------------------------- departments


def dept_cards(rows):
    items = []
    for slug, name, short, head in rows:
        title = name + (f" ({short})" if short else "")
        if slug:
            items.append((title, DEPARTMENTS[slug][0].split(". ")[0].rstrip(".") + ".", f"departments/{slug}.html", f"Director: {head}" if head else None))
        else:
            role = "Head" if name == "Press and Public Relations" else "Director"
            head_line = f"{role}: {head}. " if head else ""
            items.append((title, f"{head_line}The ministry's site has no page for this yet.", None, None))
    return cards(items, level="h3")


P["departments.html"] = shell("Departments and units", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Departments and units</h1>
        <p class="ag-lead">The ministry does its work through 15 departments and 3 units, each led by a director or head who reports to the Permanent Secretary.</p>
        <h2>Departments</h2>
      </div>
{dept_cards(DEPARTMENT_LIST)}
      <div class="ag-prose">
        <h2 id="units">Units</h2>
      </div>
{dept_cards(UNIT_LIST)}''', current="About", breadcrumb=crumbs(("about.html", "About"), ("departments.html", "Departments and units")))

for slug, name, short, head in DEPARTMENT_LIST:
    if not slug:
        continue
    lead, divisions, sections = DEPARTMENTS[slug]
    full = f"{name} Department"
    rows = [f'<div class="ag-summary__row"><dt class="ag-summary__key">Director</dt><dd class="ag-summary__value">{head}</dd></div>']
    if divisions:
        label = "Divisions" if len(divisions) > 1 else "Division"
        rows.append(f'<div class="ag-summary__row"><dt class="ag-summary__key">{label}</dt><dd class="ag-summary__value">{", ".join(divisions)}</dd></div>')
    body = "".join(f"\n        <h2>{h}</h2>\n        {bullets(items)}" for h, items in sections)
    P[f"departments/{slug}.html"] = shell(full, f'''      <div class="ag-prose">
        <p class="ag-caption">Department{f" · {short}" if short else ""}</p>
        <h1 class="ag-heading-xl">{full}</h1>
        <p class="ag-lead">{lead}</p>
      </div>
      <dl class="ag-summary">{"".join(rows)}</dl>
      <div class="ag-prose">{body}
        <p><a href="../departments.html">All departments and units</a></p>
      </div>''', current="About", root="../", breadcrumb=crumbs(("departments.html", "Departments and units"), (f"departments/{slug}.html", name)))

# ---------------------------------------------------------------- programs

P["programs.html"] = shell("Programs", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Programs</h1>
        <p class="ag-lead">The ministry's programs for inventors, researchers, students and young people. See also <a href="ysi.html">Youth and Students in Innovation</a> and the <a href="events.html">events</a>.</p>
      </div>
{cards([(name, text, f"programs/{slug}.html" if slug else None, None if slug else "The ministry's site has no page for this yet.") for slug, name, text in PROGRAMS], level="h2")}''', current="Programs", breadcrumb=crumbs(("programs.html", "Programs")))

PROGRAM_PAGES = {
    "technology-innovation-expo": f'''        <p>The Expo began as National Science and Technology Week, first held in October 1988. The Federal Executive Council set the third week of October each year for it. It took its current name in 2017, when the first Expo was held at Eagle Square, Abuja.</p>
        <p>The ministry reports that patents for research findings rose from 6 in 2015 and 16 in 2016 to 50 by the end of 2017. Future editions are planned for each of the six geopolitical zones.</p>
        <h2>What the Expo is for</h2>
        {bullets(["Promoting research and development", "Bringing inventions and research results to market", "Encouraging Nigerians to take up science careers", "Showing the public what research institutions can do", "Building partnerships between researchers and investors", "Encouraging businesses built on Nigerian knowledge and technology"])}
        <p><a href="../events/technology-innovation-expo.html">The 2026 Expo</a></p>''',
    "yonspa": f'''        <p>The competition covers all 774 local government areas in Nigeria's 36 states and the Federal Capital Territory. Students compete in biology, chemistry, mathematics and physics.</p>
        <p>Its goal is to encourage students to study science and to choose careers in science, technology, engineering and mathematics. The ministry also promotes teaching science subjects in local languages.</p>''',
    "ncist": f'''        <h2>What the meeting does</h2>
        {bullets(["Reviews reports on science, technology and innovation across the country", "Shows new research and technology", "Promotes work across disciplines on national problems", "Brings policymakers, researchers and industry together on the future of innovation", "Improves cooperation between stakeholders"])}
        <h2>Who takes part</h2>
        <p>Policymakers, scientists, planners, entrepreneurs, universities, industry and development partners such as UNIDO, UNICEF, UNESCO, ECOWAS, UNDP, JICA, KOICA and the World Bank. Professional bodies such as the Nigerian Society of Engineers and COREN, and the five Nigerian academies, also take part.</p>
        <h2>What it produces</h2>
        {bullets(["The main problems and opportunities in the sector", "Recommendations for policy", "Partnerships across sectors"])}
        <p>The communique of the 2023 Council is on the <a href="../resources.html">policies and resources</a> page.</p>''',
    "grand-challenges-nigeria": f'''        <p>The project builds a network of Nigerian researchers and development practitioners who can innovate for impact, scale, sustainability and gender equity. Its priorities are public health, science and technology, agriculture, food systems, nutrition and climate change.</p>
        <p>The Vice President, Senator Kashim Shettima, launched it on 18 November 2024, with a call for proposals on maternal, newborn and child health. The call is run by the <a href="https://scienceforafrica.foundation/media-center/grand-challenges-nigeria-launch-funding-call-maternal-child-health">Science for Africa Foundation</a>.</p>''',
}
for slug, name, text in PROGRAMS:
    if not slug:
        continue
    P[f"programs/{slug}.html"] = shell(name, f'''      <div class="ag-prose">
        <p class="ag-caption">Program</p>
        <h1 class="ag-heading-xl">{name}</h1>
        <p class="ag-lead">{text}</p>
{PROGRAM_PAGES[slug]}
        <p><a href="../programs.html">All programs</a></p>
      </div>''', current="Programs", root="../", breadcrumb=crumbs(("programs.html", "Programs"), (f"programs/{slug}.html", name)))

TRACKS = ["Innovation branding, digital content and science communication", "Software, web and AI development", "Data analytics and innovation project management",
          "Agritech and agribusiness", "Green and renewable energy, and climate", "Health technology and biotechnology", "Manufacturing, hardware and making", "Fintech and digital finance"]
P["ysi.html"] = shell("Youth and Students in Innovation", f'''      <div class="ag-prose">
        <p class="ag-caption">Program</p>
        <h1 class="ag-heading-xl">Youth and Students in Innovation 2026</h1>
        <p class="ag-lead">Practical training in digital skills, AI and innovation for young Nigerians: three weeks online, three days in person, then mentoring.</p>
        <div class="ag-inset"><p><strong>Applications are closed.</strong> They ran from 31 August to 14 September 2026.</p></div>
        <h2>Who could apply</h2>
        {bullets(["Nigerians aged 18 to 30", "With a smartphone or laptop of their own, or access to one", "With an interest in digital skills, AI, technology or innovation"])}
        <h2>How it works</h2>
      </div>
      <ol class="ag-steps">
        <li class="ag-steps__item"><h3 class="ag-steps__title">Choose a track</h3><p>One of the eight tracks below.</p></li>
        <li class="ag-steps__item"><h3 class="ag-steps__title">Learn online for three weeks</h3><p>The virtual learning phase.</p></li>
        <li class="ag-steps__item"><h3 class="ag-steps__title">Three days in person</h3><p>The first in-person edition is in Enugu, in the South East zone. The date has not been announced.</p></li>
        <li class="ag-steps__item"><h3 class="ag-steps__title">Join the community</h3><p>Ongoing mentoring after the programme.</p></li>
      </ol>
      <div class="ag-prose">
        <h2>The eight tracks</h2>
        {bullets(TRACKS)}
        <p>The programme has its own site at <a href="https://ysi.scienceandtech.gov.ng/">ysi.scienceandtech.gov.ng</a>.</p>
      </div>''', current="Programs", breadcrumb=crumbs(("programs.html", "Programs"), ("ysi.html", "Youth and Students in Innovation")))

P["services.html"] = shell("Services", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Services</h1>
        <p class="ag-lead">The services the ministry offers through its agencies. Each one is handled by the agency named, on its own website.</p>
      </div>
{cards([(t, d, u, "Handled by " + a) for t, d, a, u in SERVICES], level="h2", variant="ag-card--accent")}
      <div class="ag-prose">
        <p>For anything else, <a href="contact.html">contact the ministry</a> or find the right <a href="agencies.html">agency</a>.</p>
      </div>''', current="Services", breadcrumb=crumbs(("services.html", "Services")))

# ---------------------------------------------------------------- events

P["events.html"] = shell("Events", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Events</h1>
        <p class="ag-lead">Exhibitions, launches and programme sessions run by the ministry. Upcoming first.</p>
        <div class="ag-inset"><p>The ministry's site has no events page. These events come from its programme pages and its news.</p></div>
      </div>
{events_html(EVENTS)}''', current="Programs", breadcrumb=crumbs(("events.html", "Events")))

P["events/technology-innovation-expo.html"] = shell("Technology and Innovation Expo 2026", f'''      <div class="ag-event">
        <span class="ag-event__date ag-event__date--tbc ag-event__date--lg">TBC<span class="ag-visually-hidden">, date to be confirmed</span></span>
        <div class="ag-event__body">
          <p class="ag-caption">Event, upcoming</p>
          <h1 class="ag-heading-xl">Technology and Innovation Expo 2026</h1>
          <p class="ag-lead">Nigeria's yearly exhibition of inventions, research and new technology companies, with investors, agencies and the public.</p>
        </div>
      </div>
      <dl class="ag-summary">
        <div class="ag-summary__row"><dt class="ag-summary__key">When</dt><dd class="ag-summary__value">The third week of October 2026. The exact dates have not been announced.</dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Where</dt><dd class="ag-summary__value">Not announced. Earlier editions were in Abuja.</dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Host</dt><dd class="ag-summary__value">Federal Ministry of Innovation, Science and Technology</dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Who it is for</dt><dd class="ag-summary__value">Inventors, researchers, students, investors, companies and the public</dd></div>
      </dl>
      <div class="ag-prose">
        <h2>What happens there</h2>
        {bullets(["Research institutions and inventors show their work", "Researchers meet investors", "Students see what a science career can lead to", "Agencies show the services they offer"])}
        <div class="ag-inset"><p>The Expo is set in law for the third week of October, but the ministry's site gives no date, venue or flyer for 2026. When it does, they go here, with the flyer beside these details.</p></div>
        <p>About the <a href="../programs/technology-innovation-expo.html">Technology and Innovation Expo</a>.</p>
        <h2>Questions</h2>
        <p>Email <a href="mailto:info@scienceandtech.gov.ng">info@scienceandtech.gov.ng</a> or call <a href="tel:+2348140000278">+234 814 000 0278</a>.</p>
        <p><a href="../events.html">All events</a></p>
      </div>''', current="Programs", root="../", breadcrumb=crumbs(("events.html", "Events"), ("events/technology-innovation-expo.html", "Technology and Innovation Expo 2026")))

# ---------------------------------------------------------------- media

P["news.html"] = shell("News", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">News</h1>
        <p class="ag-lead">Press releases from the ministry's Press and Public Relations Unit, newest first.</p>
      </div>
      <ul class="ag-list">{dated(NEWS)}
      </ul>
      <nav aria-label="Pagination">
        <ul class="ag-pagination ag-pagination--simple">
          <li><a class="ag-pagination__link" href="{REAL}news/" rel="next">Older news, on scienceandtech.gov.ng</a></li>
        </ul>
      </nav>''', current="Media", breadcrumb=crumbs(("news.html", "News")))

FRAME = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 9'%3E%3Crect width='16' height='9' fill='%23dfe6ec'/%3E%3C/svg%3E"
ARTICLES = {
    "nbti-ebsu-dispute": ("9 June 2026", "Minister resolves the land dispute between NBTI and Ebonyi State University",
        "The Minister, Dr Kingsley Tochukwu Udeh, has brought an end to a long land dispute between the National Board for Technology Incubation and Ebonyi State University, so the two can work together again.",
        ["The Minister announced the settlement when the Director-General of NBTI, Dr Kazeem Kolawole Raji, visited him in Abuja. He thanked the Governor of Ebonyi State, Francis Ogbonna Nwifuru, whose intervention helped the parties agree.",
         "Dr Udeh said the government's innovation agenda depends on government, universities and the private sector working together.",
         "Dr Raji said the renewed relationship would let NBTI do more for start-ups, innovators and young Nigerians in Ebonyi State, through incubation, technical support and business development services."],
        "fmist-minister-resolves-longstanding-nbti-ebsu-land-dispute-restores-strategic-collaboration/"),
    "forensic-science": ("4 June 2026", "Ministry seeks a partnership to advance forensic science in the justice system",
        "The Minister has said forensic science is essential to Nigeria's criminal justice system, public safety and evidence-based decisions.",
        ["The Permanent Secretary, Dr Mukhtar Yawale Muhammad, received a delegation from the Forensic Ambassadors Academy Africa on the Minister's behalf, at the ministry in Abuja.",
         "The Minister said using science in investigations and trials makes justice more transparent and accountable, and called for Nigerian expertise in forensic science.",
         "The Academy's Executive Secretary, Abraham Kwaghfan, said the non-profit wants to work with the ministry on forensic science education, research and training across Africa."],
        "fmist-seeks-strategic-partnership-to-advance-forensic-science-for-a-stronger-justice-system-in-nigeria/"),
    "wipo-partnership": ("3 June 2026", "Ministry and WIPO move towards a partnership on innovation and intellectual property",
        "The Minister received a delegation from the World Intellectual Property Organization, led by its Director General, Daren Tang, in Abuja.",
        ["They discussed bringing research results to market, protecting intellectual property, and supporting innovators, researchers, start-ups and creative businesses.",
         "The Minister said the ministry would work with WIPO to raise public awareness of intellectual property and to strengthen how it is administered and protected in Nigeria.",
         "Mr Tang said WIPO would support Nigeria with technical assistance and training. Both sides agreed to work towards a memorandum of understanding."],
        "fmist-wipo-move-to-forge-strategic-partnership-to-accelerate-nigerias-innovation-and-intellectual-property-agenda/"),
    "plasstifest-2026": ("3 June 2026", "Minister sets out what states can do for innovation, at PLASSTIFEST 2026",
        "At the Plateau State Science, Technology and Innovation Festival in Jos, the Minister urged states to set up their own institutions for innovation.",
        ["Dr Udeh said the National Science, Technology and Innovation Policy 2022 aims to move Nigeria from a resource-based economy to a knowledge-based one, and that research must leave the laboratory and reach the market.",
         "He described Energise Commercialisation Now, or ECoN, which finds research that can be sold, connects innovators with investors and supports incubation. He also described the National Research and Innovation Development Fund, which the ministry is setting up to finance research and prototypes.",
         "He asked states to create innovation councils, research commercialisation offices, innovation funds and technology transfer platforms, and named Plateau's opportunities in agriculture, mining, renewable energy and digital services. He thanked the Governor, Caleb Manasseh Mutfwang, for hosting the festival."],
        "fmist-strengthens-federal-state-collaboration-on-innovation-as-minister-highlights-opportunities-for-subnational-governments-at-plasstifest-2026/"),
}
for slug, (date, title, lead, paras, path) in ARTICLES.items():
    body = "".join(f"\n        <p>{p}</p>" for p in paras)
    P[f"news/{slug}.html"] = shell(title, f'''      <div class="ag-prose">
        <p class="ag-caption">Press release · {date}</p>
        <h1 class="ag-heading-xl">{title}</h1>
        <p class="ag-lead">{lead}</p>
      </div>
      <figure class="ag-figure ag-figure--16-9" style="max-width: 48rem">
        <img class="ag-figure__image" src="{FRAME}" alt="" width="1200" height="675" />
        <figcaption class="ag-figure__caption">The photograph goes here. The ministry's photographs are not reproduced in this rebuild.</figcaption>
      </figure>
      <div class="ag-prose">{body}
        <p>Issued by Mrs Pauline Sule, Head, Press and Public Relations.</p>
        <div class="ag-inset"><p>This is a shorter account. The ministry's full release is on <a href="{REAL}{path}">scienceandtech.gov.ng</a>.</p></div>
        <p><a href="../news.html">All news</a></p>
      </div>''', current="Media", root="../", breadcrumb=crumbs(("news.html", "News"), (f"news/{slug}.html", title)))

P["videos.html"] = shell("Videos", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Videos</h1>
        <p class="ag-lead">Television interviews and recordings about the ministry's work, newest first.</p>
      </div>
{video_cards(sorted(VIDEOS, key=lambda v: v[3], reverse=True))}''', current="Media", breadcrumb=crumbs(("videos.html", "Videos")))

for i, (slug, title, source, date, length, words, file, about) in enumerate(VIDEOS):
    others = [v for v in VIDEOS if v[0] != slug]
    P[f"videos/{slug}.html"] = shell(title, f'''      <div class="ag-prose">
        <p class="ag-caption">{source} · {date}</p>
        <h1 class="ag-heading-xl">{title}</h1>
        <p class="ag-lead">{about}</p>
        <figure class="ag-video">
          <a class="ag-video__poster" href="{file}" data-ag-video="{file}" data-ag-video-title="{title}">
            <img src="{POSTER}" alt="" width="1280" height="720" />
            <span class="ag-video__play" aria-hidden="true"></span>
            <span class="ag-video__label">Play video: {title}<span class="ag-video__length">{words}</span></span>
          </a>
          <figcaption class="ag-video__caption">No captions. MP4 file from the ministry's site.</figcaption>
        </figure>
        <div class="ag-inset"><p>The ministry posted this clip with no title, captions or transcript. A live service must add a transcript here, so people who cannot hear it, or cannot afford to stream it, get the same information.</p></div>
        <p><a href="../videos.html">All videos</a></p>
      </div>
      <h2>More videos</h2>
{video_cards(others, level="h3", root="../")}''', current="Media", root="../", breadcrumb=crumbs(("videos.html", "Videos"), (f"videos/{slug}.html", title)))

P["gallery.html"] = shell("Gallery", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Gallery</h1>
        <p class="ag-lead">Photographs of the Minister, the ministry's programs and its events.</p>
        <div class="ag-empty">
          <h2 class="ag-empty__title">No photos yet</h2>
          <p>The ministry's gallery had filters for the Minister, programs and events, but no photographs, when this page was built on 3 October 2026. See the <a href="videos.html">videos</a> and <a href="news.html">news</a>.</p>
        </div>
      </div>''', current="Media", breadcrumb=crumbs(("gallery.html", "Gallery")))

# ---------------------------------------------------------------- agencies, resources, contact

P["agencies.html"] = shell("Agencies", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Agencies</h1>
        <p class="ag-lead">The ministry supervises 17 research institutes, councils and agencies. Each link goes to the agency's own website.</p>
      </div>
{cards([(name, url.split("//")[1].rstrip("/").replace("www.", ""), url, short) for name, short, url in AGENCIES], level="h2")}''', current="About", breadcrumb=crumbs(("about.html", "About"), ("agencies.html", "Agencies")))

rows = "".join(f'''
        <li class="ag-list__item">
          <a class="ag-download ag-list__link" href="{url}">{name} <span class="ag-download__meta">({meta})</span></a><span class="ag-list__meta">{text}</span>
        </li>''' for name, text, url, meta in RESOURCES)
P["resources.html"] = shell("Policies and resources", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Policies and resources</h1>
        <p class="ag-lead">The national policies, roadmap and reports for science, technology and innovation.</p>
      </div>
      <ul class="ag-list">{rows}
      </ul>
      <div class="ag-prose">
        <p>The roadmap is a large file. On a mobile connection it can take several minutes to download.</p>
        <p>The ministry's site also lists a performance report for a former Minister, with no file attached. It is left out here.</p>
      </div>''', current="About", breadcrumb=crumbs(("about.html", "About"), ("resources.html", "Policies and resources")))

P["contact.html"] = shell("Contact the ministry", f'''      <div class="ag-prose">
        <h1 class="ag-heading-xl">Contact the ministry</h1>
        <p class="ag-lead">Send a message, or call, email or visit the ministry in Abuja.</p>
        <div class="ag-inset"><p>This form is part of an unofficial rebuild. Nothing you type is sent to the ministry. To reach it, use <a href="{REAL}contact/">scienceandtech.gov.ng</a>.</p></div>
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
            <option>A program or event</option>
            <option>An invention or research project</option>
            <option>A department or agency</option>
            <option>A media enquiry</option>
            <option>Something else</option>
          </select>
        </div>
        <div class="ag-field" data-ag-char-count>
          <label class="ag-label" for="message">Your message</label>
          <span class="ag-hint" id="message-hint">Up to 500 characters. Do not include your NIN or bank details.</span>
          <textarea class="ag-textarea" id="message" rows="6" data-ag-max="500" aria-describedby="message-hint message-count"></textarea>
          <span class="ag-char-count__message" id="message-count"></span>
        </div>
        <button class="ag-button" type="submit">Send message</button>
      </form>
      <div class="ag-prose">
        <h2>Other ways to reach the ministry</h2>
      </div>
      <dl class="ag-summary">
        <div class="ag-summary__row"><dt class="ag-summary__key">Phone</dt><dd class="ag-summary__value"><a href="tel:+2348140000278">+234 814 000 0278</a></dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Email</dt><dd class="ag-summary__value"><a href="mailto:info@scienceandtech.gov.ng">info@scienceandtech.gov.ng</a></dd></div>
        <div class="ag-summary__row"><dt class="ag-summary__key">Visit</dt><dd class="ag-summary__value">Federal Secretariat Complex Phase II, Block D, 4th to 8th Floor, Shehu Shagari Way, Abuja, FCT</dd></div>
      </dl>''', current="Contact", breadcrumb=crumbs(("contact.html", "Contact")))

# ---------------------------------------------------------------- search

# The results come from Pagefind: `npx pagefind --site .` after this script writes the pages builds a
# small index in pagefind/, and this page asks it in the browser. There is no server to run.
WHERE = {"departments": "Departments", "programs": "Programs", "news": "News", "events": "Events", "videos": "Videos"}
P["search.html"] = shell("Search", f'''      <h1 class="ag-heading-xl">Search</h1>
      <form class="ag-search ag-search--lg" role="search" action="search.html" method="get">
        <label class="ag-search__label ag-visually-hidden" for="q">Search this site</label>
        <div class="ag-search__row">
          <input class="ag-search__input" type="search" id="q" name="q" />
          <button class="ag-search__button" type="submit"><span class="ag-search__icon" aria-hidden="true"></span>Search</button>
        </div>
      </form>
      <p class="ag-results__count" id="count" role="status"></p>
      <ol class="ag-results" id="results" hidden></ol>
      <div class="ag-empty" id="none" hidden>
        <h2 class="ag-empty__title">Try another way</h2>
        <ul>
          <li>Check the spelling, or use fewer words.</li>
          <li>Start from the <a href="services.html">services</a>, the <a href="departments.html">departments</a> or the <a href="programs.html">programs</a>.</li>
          <li><a href="contact.html">Contact the ministry</a>.</li>
        </ul>
      </div>
      <noscript><p>Search needs JavaScript in this browser. Start from the <a href="services.html">services</a>, the <a href="departments.html">departments</a> or the <a href="programs.html">programs</a>.</p></noscript>
      <script type="module">
        const where = {json.dumps(WHERE)};
        const text = (s) => s.replace(/[&<>"]/g, (c) => ({{ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }})[c]);
        const q = (new URLSearchParams(location.search).get("q") || "").trim();
        const count = document.getElementById("count");
        const list = document.getElementById("results");
        document.getElementById("q").value = q;
        if (q) {{
          count.textContent = "Searching…";
          const pagefind = await import("./pagefind/pagefind.js");
          const found = await pagefind.search(q);
          const shown = await Promise.all(found.results.slice(0, 10).map((r) => r.data()));
          const n = found.results.length;
          count.innerHTML = n
            ? `${{n}} ${{n === 1 ? "result" : "results"}} for <strong>${{text(q)}}</strong>${{n > 10 ? ", the first 10 shown" : ""}}`
            : `No results for <strong>${{text(q)}}</strong>`;
          document.getElementById("none").hidden = n > 0;
          list.hidden = n === 0;
          list.innerHTML = shown
            .map((r) => {{
              const path = new URL(r.url, location.href).pathname.split("/").filter(Boolean);
              const section = where[path[path.length - 2]] || "The ministry";
              return `<li class="ag-result"><h2 class="ag-result__title"><a href="${{r.url}}">${{text(r.meta.title.replace(/ – .*$/, ""))}}</a></h2><p class="ag-result__where">${{section}}</p><p class="ag-result__text">${{r.excerpt}}</p></li>`;
            }})
            .join("");
        }}
      </script>''', current=None, breadcrumb=crumbs(("search.html", "Search")), index=False)

P["contact-sent.html"] = shell("Message not sent", f'''      <div class="ag-panel ag-panel--neutral"><h1 class="ag-panel__title">This is where a message would be sent</h1><p class="ag-panel__body">Nothing was sent, because this is an unofficial rebuild.</p></div>
      <div class="ag-prose"><p>On a real service this page confirms the message and gives a reference. To reach the ministry, use <a href="{REAL}contact/">scienceandtech.gov.ng</a>.</p><p><a href="index.html">Return to the home page</a></p></div>''', index=False)

for path, content in P.items():
    write(path, content)
print(f"{len(P)} pages written")
