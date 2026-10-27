# Scope cards for the META daily run

Read only the card you were assigned. The watchlists below are the defaults. The orchestrator (`meta-intel-daily`) keeps the master watchlists; if the two disagree, follow the orchestrator.

## A — Tier-1 KSA newsroom sweep, standing questions, Lenovo-specific
- **Newsrooms to check directly:**
  - alat.com/en/newsroom
  - humain.com, and HUMAIN on PRNewswire
  - aramco.com/en/news-media
  - pif.gov.sa media centre
  - stc.com.sa IR and Tadawul announcements: 7010 stc, 7202 solutions by stc, 7200 MIS, 7203 Elm
  - solutions.com.sa press
  - sdaia.gov.sa and mcit.gov.sa
  - spa.gov.sa (EN and AR)
  - neom.com newsroom
  - news.lenovo.com
- **KSA watchlist:** CST, NIC, Mobily, Zain KSA, center3, Tonomus, ROSHN, Red Sea Global, Diriyah, Qiddiya, Riyadh Air, MISA, MoIT, Mawani.
- **Standing questions:** give a status line for each every cycle, even if it is "no change". The current list is in `.claude/agents/meta-market-intel.md`.
- **Lenovo names:** Salman Faqeeh, Tareq Alangari, Lawrence Yu.

## B — Arabic and regional press, Pillar 3 deals and funding
- **Press:** Asharq Al-Awsat (AR and EN), Al-Eqtisadiah, Argaam (AR and EN), Mubasher, Saudi Gazette, Arab News, Aljazirah, Al-Riyadh, SPA.
- **Arab News, mandatory direct sweep every cycle** (do not rely on search hits). Load the section listings and read every item time-stamped inside the window:
  - arabnews.com/saudi-arabia, /business-economy, /middleeast and /tech (also the Corporate News listing)
  - Arab News Pakistan (arabnews.pk) for Pakistan items
  - Page times show no timezone; read them as KSA and say so. If WebFetch is blocked, use `curl -sL -A "Mozilla/5.0"` in Bash or the Google News sitemap. In the report, give Arab News its own status line (items found, or "checked, nothing in window").
- **Funding sources:** MAGNiTT, Wamda (AR and EN), Jawlah, SaudiVC.
- **Wires:** Reuters, Bloomberg, CNBC Arabia.
- **Arabic search terms:** «مذكرة تفاهم تقنية», «مركز بيانات», «الذكاء الاصطناعي اتفاقية», «جولة تمويل».
- **For each deal:** both parties, the value, and whether a hardware OEM is named. Report funding rounds of $20M or more.

## C — Pillar 1 data centres
- **What counts:** any DC news in KSA, GCC, MEA, Türkiye, Pakistan or Africa. That includes builds, groundbreakings, MW figures (mandatory where available), land, PPAs, cooling and grid deals, colocation entries, sovereign AI factories and hyperscaler regions.
- **Feeds:** DCD RSS, Data Center Frontier, W.Media, Zawya Projects, MEED, SaudiGulf Projects.
- **Global DC news:** only when it involves a watchlist entity (CoreWeave, Nebius, Crusoe, Nscale, Lambda, OpenAI Stargate, Meta, Microsoft, xAI) or signals a capacity or supply shift.
- **For each item:** the hardware supplier, or "undisclosed → open ISG".

## D — Pillar 2 memory and components
- **What to report:**
  - DRAM, NAND and HBM contract and spot prices.
  - TrendForce, DRAMeXchange and TechInsights prints.
  - Capacity, fab and allocation news from Samsung, SK hynix, Micron, Kioxia, SanDisk, WD, CXMT and YMTC.
  - Analyst notes, naming both the analyst and the firm.
  - OEM impact.
  - GPU and CPU supply and pricing.
- **Sources:** DigiTimes, TrendForce, Tom's Hardware, Korea Herald, Korea Times, KED Global, Nikkei Asia.
- **Always include** the latest DRAMeXchange spot values with their print time. If nothing new printed in the window, give the last-known reference value and its date.

## E — Tier 2 GCC/MEA and Pillar 4 (global tech in META)
- **Tier 2 by country:**
  - UAE: G42, Core42, Khazna, Presight, Bayanat, Space42, MGX, MBZUAI, IHC, ADQ, Mubadala, ADNOC, e&, du, Stargate UAE.
  - Qatar: Ooredoo, QIA, MEEZA.
  - Kuwait, Bahrain and Oman: sovereign funds and telcos.
  - Egypt: Telecom Egypt, Vodafone Egypt, MNT-Halan.
  - Türkiye: Turkcell, Türk Telekom.
  - Pakistan: Jazz, Telenor, MoITT.
  - Africa: MTN, Vodacom, Safaricom, Airtel Africa, IHS, Flutterwave, Raxio, Africa Data Centres, Teraco.
- **Pillar 4, global tech companies in META:**
  - US: Microsoft, Google, AWS, Oracle, Meta, Apple, Nvidia, AMD, Intel, Dell, HPE, HP, Cisco, IBM, Salesforce, ServiceNow.
  - Chinese: Huawei, Alibaba Cloud, Tencent, ByteDance, Xiaomi, vivo, OPPO, Honor, Hikvision, Hisense, Haier, ZTE, Lenovo.
  - Others: Samsung, SAP, Ericsson, Nokia, NEC, Fujitsu.
- **Chinese rule:** search each Chinese company individually and give a one-line status for every one. Any of them with META presence and news in the window must be reported, even if the event happened outside the region.

## F — Tier 3 global
- **Watchlist:**
  - AI labs: OpenAI, Anthropic, Google DeepMind, Meta AI, Mistral, DeepSeek, xAI, Cohere.
  - Chips and hardware: Nvidia, AMD, Intel, Dell, HPE, HP, Supermicro, TSMC, SMIC.
  - Cloud: Microsoft, Google, AWS, Oracle.
  - DC operators and neoclouds: Equinix, Digital Realty, CoreWeave, Nebius, Lambda, Crusoe, Nscale.
  - DC power and cooling: Vertiv, Schneider (DC).
- **Also:** US export controls (especially Gulf licences and China), tariffs, and PC, server and smartphone market data from IDC, Gartner, Canalys/Omdia and Counterpoint.
- **Priority:** items with a META hook, or items that shift Lenovo's competitive position.

## H — Events and conferences
Covered by the `meta-events-intel` agent. Its coverage and calendar rules are in `.claude/agents/meta-events-intel.md`. It follows this skill's window and verification rules.
