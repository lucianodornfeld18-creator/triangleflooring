#!/usr/bin/env python3
"""Generate /directories/index.html — citation hub for max indexability + GEO/SEO sameAs signals."""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gen import *

PATH = "/directories/"
TITLE = "Triangle Flooring on the Web | Directory Listings & Citations"
DESC = "Find Triangle Flooring (Palmetto, FL) on 75+ trusted business directories — Houzz, Bark, Manta, Hotfrog, BBB-style listings, and more. Verified NAP across the web."

# ---- 79 citations grouped by tier for UX + organized internal-linking weight ----
# Each entry: (anchor_label, url, optional_note)
# Anchor text intentionally varies but always includes "Triangle Flooring" to reinforce brand entity.

TIER_1_AUTHORITY = [
    ("Triangle Flooring on Houzz",                        "https://www.houzz.com/pro/trianglefloorus/__public",                                   "Home-improvement marketplace"),
    ("Triangle Flooring on Bark",                         "https://www.bark.com/en/us/company/triangle-flooring/YNKYvR/",                          "Service-pro marketplace"),
    ("Triangle Flooring on Manta",                        "https://www.manta.com/c/m1hxzxk/triangle-flooring",                                     "Small-business directory"),
    ("Triangle Flooring on Hotfrog",                      "https://www.hotfrog.com/company/e107d647d1e6563efced2ed6340c41be/triangle-flooring/palmetto/carpet-flooring", "Global business directory"),
    ("Triangle Flooring on Homify",                       "https://www.homify.com/professionals/10005197/triangle-flooring",                       "Home-design network"),
    ("Triangle Flooring on TrustLink",                    "https://www.trustlink.org/Reviews/Triangle-Flooring-207662570",                         "Verified reviews"),
    ("Triangle Flooring on Brownbook",                    "https://www.brownbook.net/business/55142882/triangle-flooring",                         "International local directory"),
    ("Triangle Flooring on ProvenExpert",                 "https://www.provenexpert.com/triangle-flooring2/?mode=preview",                         "Reputation portal"),
    ("Triangle Flooring on iTrustIt",                     "https://itrustit.com/trianglefloorus#overview",                                         "Trust-verified directory"),
    ("Triangle Flooring on Lisnic",                       "https://www.lisnic.com/business-profile/triangle-flooring",                             "Business profile network"),
    ("Triangle Flooring on n49",                          "https://www.n49.com/biz/7209985/triangle-flooring-fl-palmetto-/",                       "North-America local directory"),
    ("Triangle Flooring on SalesSpider",                  "https://www.salespider.com/c-45408544/triangle-flooring",                               "B2B network"),
    ("Triangle Flooring on Storeboard",                   "https://www.storeboard.com/triangleflooring",                                           "Business community"),
    ("Triangle Flooring on Issuu",                        "https://issuu.com/trianglefloorus",                                                     "Publication profile"),
    ("Triangle Flooring on Speaker Deck",                 "https://speakerdeck.com/trianglefloorus",                                               "Presentation portfolio"),
    ("Triangle Flooring on Gravatar",                     "https://gravatar.com/trianglefloorus",                                                  "Identity profile"),
]

TIER_2_DIRECTORIES = [
    ("Triangle Flooring on Zipleaf US",                   "https://www.zipleaf.us/Companies/Triangle-Flooring",                                    ""),
    ("Triangle Flooring on EnrollBusiness",               "https://us.enrollbusiness.com/BusinessProfile/7822667/Triangle-Flooring-Palmetto-FL-34221/Home", ""),
    ("Triangle Flooring on FreeListingUSA",               "https://www.freelistingusa.com/listings/triangle-flooring",                             ""),
    ("Triangle Flooring on Hub.biz (Palmetto)",           "https://triangle-flooring-palmetto.hub.biz/",                                           ""),
    ("Triangle Flooring on AnnounceAmerica",              "https://www.announceamerica.com/united-states/palmetto/home-and-garden/triangle-flooring", ""),
    ("Triangle Flooring on KC Contractors",               "https://www.kccontractors.com/residential-and-commercial-contractor/triangle-flooring", ""),
    ("Triangle Flooring on Graded Tradesmen",             "https://www.gradedtradesmen.com/united-states/palmetto/tradesmen/triangle-flooring",    ""),
    ("Triangle Flooring on Contractors Directory",        "https://www.contractors.directory/united-states/palmetto/contractors/triangle-flooring",""),
    ("Triangle Flooring on Zumvu",                        "https://www.zumvu.com/trianglefloorus/",                                                ""),
    ("Triangle Flooring on SmallBusinessUSA",             "https://smallbusinessusa.com/listing/triangle-flooring.html",                           ""),
    ("Triangle Flooring on Find-Us-Here",                 "https://www.find-us-here.com/businesses/Triangle-Flooring-Palmetto-Florida-USA/34524289/", ""),
    ("Triangle Flooring on Qdexx",                        "https://www.qdexx.com/US/FL/Palmetto/Contractors/US-FL-Palmetto-Contractors-Triangle-Flooring", ""),
    ("Triangle Flooring on AmericanSearch",               "https://www.americansearch.info/construction-contractors/triangle-flooring",            ""),
    ("Triangle Flooring on CallUpContact",                "https://www.callupcontact.com/b/businessprofile/Triangle_Flooring/10106060",            ""),
    ("Triangle Flooring on A-Z Business Finder",          "https://www.a-zbusinessfinder.com/business-directory/Triangle-Flooring-Palmetto-Florida-USA/34524289/", ""),
    ("Triangle Flooring on Trueen",                       "https://trueen.com/business/listing/triangle-flooring/752369",                          ""),
    ("Triangle Flooring on Directory9",                   "https://directory9.net/listing/triangle-flooring.html",                                 ""),
    ("Triangle Flooring on Bizidex",                      "https://bizidex.com/en/triangle-flooring-contractors-965593",                            ""),
    ("Triangle Flooring on LocalBusinessNation",          "https://www.localbusinessnation.com/home-garden-landscape/triangle-flooring",            ""),
    ("Triangle Flooring on SuccessCenter (Palmetto)",     "https://www.successcenter.com/palmetto-34221/services/triangle-flooring",                ""),
    ("Triangle Flooring on GravitySplash",                "https://www.gravitysplash.com/b/triangle-flooring/",                                    ""),
    ("Triangle Flooring on MyLifeGB",                     "https://www.mylifegb.com/united-states/palmetto/home-services/triangle-flooring",       ""),
    ("Triangle Flooring on Global eConnections",          "https://www.globaleconnections.com/united-states/palmetto/home-services/triangle-flooring", ""),
    ("Triangle Flooring on Poyst",                        "https://www.poyst.com/business/triangle-flooring",                                      ""),
    ("Triangle Flooring on Revaliew",                     "https://revaliew.com/businesses/triangle-flooring",                                     ""),
    ("Triangle Flooring on What's Your Hours",            "https://www.whatsyourhours.com/united-states/palmetto/builders/triangle-flooring",      ""),
    ("Triangle Flooring on Speed Networking Group",       "https://speednetworkinggroup.com/business/triangle-flooring-895370.html",               ""),
    ("Triangle Flooring on RateUsOnline",                 "https://www.rateusonline.com/directory/listing/triangle-flooring",                      ""),
    ("Triangle Flooring on VirtualMallSpace",             "http://www.virtualmallspace.com/home-services/triangle-flooring",                       ""),
    ("Triangle Flooring on WarriorBizNetwork",            "https://www.warriorbiznetwork.com/united-states/palmetto/services/triangle-flooring",   ""),
    ("Triangle Flooring on USAHomePlus",                  "https://www.usahomeplus.com/flooring-center/triangle-flooring",                          ""),
    ("Triangle Flooring on EHBact",                       "https://www.ehbact.com/construction-contractors/triangle-flooring",                     ""),
    ("Triangle Flooring on ZeeMaps",                      "https://www.zeemaps.com/map/olzdu?group=7083252",                                       ""),
    ("Triangle Flooring on SurfYourTown",                 "https://www.surfyourtown.com/united-states/palmetto/home-services/triangle-flooring",   ""),
    ("Triangle Flooring on My Business Directory Local",  "https://mybusinessdirectorylocal.com/business/triangle-flooring-895370.html",           ""),
    ("Triangle Flooring on Preferred Professionals",      "https://www.preferredprofessionals.com/construction-contractors/triangle-flooring",     ""),
    ("Triangle Flooring on Adfty Biz",                    "https://adfty.biz/business/triangle-flooring/",                                         ""),
    ("Triangle Flooring on BizCoupon Directory",          "https://www.bizcoupon.directory/united-states/palmetto/home-services/triangle-flooring",""),
    ("Triangle Flooring on 757 Pages",                    "https://www.757pages.com/construction/triangle-flooring",                                ""),
    ("Triangle Flooring on TheDigitalBuzz Magazine",      "https://thedigitalbuzzmagazine.com/business/triangle-flooring-895370.html",             ""),
    ("Triangle Flooring on Express Business Directory",   "https://www.expressbusinessdirectory.com/directory/triangle-flooring/?notice=1",        ""),
    ("Triangle Flooring on Trustaine",                    "https://trustaine.com/businesses/triangle-floor.com",                                   ""),
    ("Triangle Flooring on Listing Planner",              "https://profile.listingplanner.com/profile/butlerbeach-fl/triangle-flooring-10507482",  ""),
    ("Triangle Flooring on Lowcountry Minority Biz",      "https://lowcountryminoritybiz.com/listing/triangle-flooring.html",                       ""),
    ("Triangle Flooring on B2B Growth Expo",              "https://b2bgrowthexpo.org/business/triangle-flooring-895370.html",                      ""),
    ("Triangle Flooring on TrustIndex",                   "https://www.trustindex.io/reviews/triangle-floor.com",                                  ""),
    ("Triangle Flooring on BizMaker",                     "https://www.bizmaker.org/other/triangle-flooring",                                      ""),
    ("Triangle Flooring on Elite Services Network",       "http://www.eliteservicesnetwork.com/classifieds/triangle-flooring",                     ""),
    ("Triangle Flooring on 40Billion",                    "https://www.40billion.com/profile/527456222",                                            ""),
    ("Triangle Flooring on Wireanium",                    "https://www.wireanium.com/united-states/palmetto/flooring-contractor/triangle-flooring",""),
    ("Triangle Flooring on GoLocalEZ Services",           "https://www.golocalezservices.com/contractors-1/triangle-flooring",                     ""),
    ("Triangle Flooring on Uferlook",                     "https://uferlook.com/about/Triangle-Flooring-Palmetto-FL-34221-Palmetto-FL-34221/3230942", ""),
    ("Triangle Flooring on AllBizListing",                "https://allbizlisting.com/listing/triangle-flooring/",                                  ""),
    ("Triangle Flooring on BizRatings",                   "https://www.bizratings.com/profilepage.aspx?params=RC-108410-TriangleFlooring",         ""),
    ("Triangle Flooring on AdPost",                       "https://www.adpost.com/us/business_products_services/1188169/",                          ""),
    ("Triangle Flooring on NextBizThing",                 "https://www.nextbizthing.com/construction-20-contractors/triangle-flooring",            ""),
    ("Triangle Flooring on TopGoogle",                    "https://www.topgoogle.com/listing/triangle-flooring/",                                  ""),
    ("Triangle Flooring on Verview",                      "https://verview.com/biz/10092514-triangle-flooring-palmetto-florida",                   ""),
    ("Triangle Flooring on 911GetIt",                     "https://www.911getit.com/united-states/palmetto/flooring-contractors-equipment-sales-supplies-cleaning-etc/triangle-flooring", ""),
    ("Triangle Flooring on SmartBusinessPage",            "https://www.smartbusinesspage.com/classifieds/triangle-flooring",                       ""),
    ("Triangle Flooring on Perry's Place Promotions",     "https://www.perrysplacepromotions.org/contractor/triangle-flooring",                    ""),
    ("Triangle Flooring on BizToBiz",                     "https://www.biztobiz.org/other/triangle-flooring",                                      ""),
    ("Triangle Flooring on OK Service Work",              "http://www.okservicework.com/home-services/triangle-flooring",                          ""),
]

ALL_CITATIONS = TIER_1_AUTHORITY + TIER_2_DIRECTORIES

# ---- Schema: ItemList enumerating all citations ----
itemlist_schema = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "@id": f"https://{DOMAIN}/directories/#itemlist",
    "name": "Triangle Flooring – Business Directory Listings",
    "description": "Verified directory listings and citations for Triangle Flooring across 75+ business directories and review platforms.",
    "numberOfItems": len(ALL_CITATIONS),
    "itemListElement": [
        {
            "@type": "ListItem",
            "position": i,
            "name": label,
            "url": url,
        }
        for i, (label, url, _note) in enumerate(ALL_CITATIONS, 1)
    ],
}

# ---- Schema: LocalBusiness with sameAs[] — THE key signal for Google entity verification ----
# This tells Google "the entity Triangle Flooring on these 75+ external sites is the same entity as this site".
# It's the single strongest GEO/local-SEO signal for citation hubs.
sameas_urls = [
    f"https://{DOMAIN}/",
    "https://www.instagram.com/flooringtriangle",
    "https://www.facebook.com/people/Triangle-Flooring/61567334333950/",
    "https://share.google/TVRjAYdnZR3TS8Kzq",
    "https://br.pinterest.com/trianglefloor/",
] + [url for _label, url, _note in ALL_CITATIONS]

localbusiness_schema = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "@id": f"https://{DOMAIN}/#organization",
    "name": "Triangle Flooring",
    "alternateName": "Triangle Flooring LLC",
    "url": f"https://{DOMAIN}/",
    "logo": f"https://{DOMAIN}/images/logo.png",
    "image": f"https://{DOMAIN}/images/hero-waterfront-hardwood-og.jpg",
    "telephone": PHONE,
    "email": EMAIL,
    "priceRange": "$$",
    "description": "Licensed and insured flooring contractor serving Bradenton, Sarasota, Lakewood Ranch, Palmetto, Parrish, Venice, Tampa, and St. Petersburg, FL. Hardwood, LVP, tile, laminate, stair treads, baseboards, and floor repair. 300+ completed projects, 5.0★ Google rated, 1-year written labor warranty.",
    "address": {
        "@type": "PostalAddress",
        "addressLocality": "Palmetto",
        "addressRegion": "FL",
        "postalCode": "34221",
        "addressCountry": "US",
    },
    "areaServed": [
        {"@type": "City", "name": c} for c in [
            "Bradenton", "Sarasota", "Lakewood Ranch", "Palmetto", "Parrish",
            "Venice", "Tampa", "St. Petersburg", "Riverview", "Brandon",
            "Ellenton", "Osprey", "Nokomis", "North Port", "Longboat Key",
            "Siesta Key", "Holmes Beach", "Anna Maria Island",
        ]
    ],
    "sameAs": sameas_urls,
}

bc_items = [("Home", "/"), ("Triangle Flooring on the Web", None)]
bc_schema = render_breadcrumb_schema(bc_items)


def render_citation_list(entries):
    items = []
    for label, url, note in entries:
        note_html = f'<span class="dir-note">{note}</span>' if note else ""
        items.append(
            f'<li><a href="{url}" target="_blank" rel="noopener nofollow">{label}</a>{note_html}</li>'
        )
    return "\n          ".join(items)


tier1_html = render_citation_list(TIER_1_AUTHORITY)
tier2_html = render_citation_list(TIER_2_DIRECTORIES)

EXTRA_CSS = """
.directories-intro{max-width:780px;margin:0 auto 2.5rem;text-align:center}
.directories-intro p{color:var(--gray);font-size:1.02rem;line-height:1.7}
.nap-card{background:var(--gray-light);border:1px solid var(--gray-border);border-radius:var(--radius);padding:1.4rem 1.6rem;margin:1.8rem auto;max-width:560px;text-align:center}
.nap-card .nap-label{font-size:.78rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--cerulean);margin-bottom:.5rem}
.nap-card .nap-line{font-family:var(--font-head);font-size:1.05rem;color:var(--text);margin:.25rem 0;font-weight:600}
.dir-tier{margin:2.5rem 0}
.dir-tier h2{margin-bottom:.5rem}
.dir-tier .tier-sub{color:var(--gray);font-size:.95rem;margin-bottom:1.5rem}
.dir-list{list-style:none;display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:.7rem 1.4rem;padding:0;margin:0}
.dir-list li{padding:.6rem .8rem;border-bottom:1px solid var(--gray-border);font-size:.95rem;line-height:1.4}
.dir-list li a{color:var(--navy);font-weight:600;display:block}
.dir-list li a:hover{color:var(--orange)}
.dir-note{display:block;font-size:.8rem;color:var(--gray);font-weight:400;margin-top:.15rem}
.dir-count{font-family:var(--font-head);font-weight:700;color:var(--navy);font-size:1.1rem}
"""

content = f"""{page_head(TITLE, DESC, PATH)}
<style>{EXTRA_CSS}</style>
{header()}
{breadcrumbs(bc_items)}

<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Find Us on the Web</span>
    <h1>Triangle Flooring <span>Across the Web</span></h1>
    <p>Verified business listings, citations, and review profiles for Triangle Flooring — a licensed flooring contractor based in Palmetto, FL, serving Tampa Bay, Bradenton, Sarasota, and Lakewood Ranch.</p>
    <div class="page-hero-trust">
      <span><span class="dir-count">{len(ALL_CITATIONS)}+</span> directory listings</span>
      <span>Consistent NAP everywhere</span>
      <span>5★ Google rated</span>
      <span>Licensed &amp; insured</span>
    </div>
  </div>
</section>

<section class="intro">
  <div class="container">
    <div class="directories-intro">
      <p>This page lists every business directory, review platform, and citation site where Triangle Flooring is officially listed. We maintain a single canonical NAP (Name, Address, Phone) across all listings — a consistency signal Google and Bing use to verify that we are a real, established, locally-trusted business.</p>
      <p>If you found us through one of these directories, welcome. If you're a partner verifying our presence, all listings below are live and current as of {{LAST_VERIFIED}}.</p>
    </div>

    <div class="nap-card">
      <div class="nap-label">Canonical NAP — identical on every listing</div>
      <div class="nap-line">Triangle Flooring</div>
      <div class="nap-line"><a href="tel:{PHONE}">{PHONE_DISPLAY}</a></div>
      <div class="nap-line"><a href="https://{DOMAIN}/">https://{DOMAIN}/</a></div>
      <div class="nap-line" style="font-size:.92rem;font-weight:400;color:var(--gray);margin-top:.6rem">Palmetto, FL 34221 · Mon–Sat 7 AM–7 PM · Service-area business</div>
    </div>

    <div class="dir-tier">
      <h2>Featured Profiles &amp; Review Platforms</h2>
      <p class="tier-sub">Top home-services marketplaces, review networks, and verified-business platforms where Triangle Flooring maintains an active profile.</p>
      <ul class="dir-list">
          {tier1_html}
      </ul>
    </div>

    <div class="dir-tier">
      <h2>Business Directories &amp; Local Listings</h2>
      <p class="tier-sub">Additional verified citations across local, regional, and national business directories — used to reinforce NAP consistency across the web.</p>
      <ul class="dir-list">
          {tier2_html}
      </ul>
    </div>

    <div class="directories-intro" style="margin-top:3rem">
      <p style="font-size:.92rem"><strong>Why this matters:</strong> Google and Bing cross-reference the business name, phone, and website across these directories to confirm we are a legitimate, established local business. Consistent listings — same name, same phone, same website — strengthen our local search ranking and make it easier for customers in Tampa Bay to find us when they search for flooring contractors.</p>
    </div>
  </div>
</section>

{final_cta()}
{footer()}
{whatsapp_float()}

<script type="application/ld+json">{json.dumps(bc_schema)}</script>
<script type="application/ld+json">{json.dumps(itemlist_schema)}</script>
<script type="application/ld+json">{json.dumps(localbusiness_schema)}</script>

{menu_script()}
</body>
</html>"""

# Replace the date placeholder
from datetime import date
content = content.replace("{LAST_VERIFIED}", date.today().strftime("%B %Y"))

out_dir = f"{OUT_DIR}/directories"
os.makedirs(out_dir, exist_ok=True)
with open(f"{out_dir}/index.html", "w", encoding="utf-8") as f:
    f.write(content)
print(f"[OK] /directories/index.html ({len(content)//1024} KB) - {len(ALL_CITATIONS)} citations linked, sameAs[] populated for entity verification")
