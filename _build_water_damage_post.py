#!/usr/bin/env python3
"""
Generate /blog/water-damaged-hardwood-floor-repair-florida/index.html

Approach: slice the EXACT shared boilerplate (head styles + GA/Ads tag,
blog CSS, header, footer, whatsapp float, final-cta, closing scripts) from
a recently-deployed blog post so the new page is byte-identical chrome to
the live site (the repo's _gen.py header/footer are stale vs deployed HTML).
Only the unique content + meta + JSON-LD are authored here.

Run:  py -3 _build_water_damage_post.py
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).parent
EXEMPLAR = ROOT / "blog" / "best-flooring-florida-humidity" / "index.html"
SLUG = "water-damaged-hardwood-floor-repair-florida"
OUT_DIR = ROOT / "blog" / SLUG
OUT = OUT_DIR / "index.html"

DOMAIN = "triangle-floor.com"
URL = f"https://{DOMAIN}/blog/{SLUG}/"

TITLE = "How to Fix Water-Damaged Hardwood Floors in Florida"          # 51 chars
DESC = ("Can water-damaged hardwood be saved? A Tampa Bay flooring contractor explains the warning "
        "signs, what to do first, and repair-vs-replace costs.")        # < 155
H1 = "How to Fix Water-Damaged Hardwood Floors in Florida (Repair or Replace?)"
CATEGORY = "Repair Guides"
OG_IMAGE = "card-repair.webp"
DATE = "2026-06-07"
READ_MIN = 10
BC_SHORT = "How to Fix Water-Damaged Hardwood..."  # breadcrumb last (truncated like siblings)

src = EXEMPLAR.read_text(encoding="utf-8")


def slc(start, end, inclusive_end=True):
    i = src.index(start)
    j = src.index(end, i)
    return src[i:(j + len(end)) if inclusive_end else j]


HEAD_STYLES_AND_GA = slc("<style>\n:root", "</head>")
BODY_CSS = slc("<style>\n.blog-list", "</style>")
HEADER = slc('<header class="site-header">', "</header>")
FOOTER = slc("<footer>", "</footer>")
FINAL_CTA = slc('<section class="final-cta">', "</section>")
WA_FLOAT = slc('<a href="https://wa.me/19414026861?text=Hi%20Triangle%20Flooring', "</a>")
CLOSING_SCRIPTS = src[src.index("<script>\n(function(){var t=document.getElementById('menuToggle')"):
                      src.rindex("</html>") + len("</html>")]

# ---------------------------------------------------------------------------
# HEAD (authored — deterministic, matches _gen.page_head pattern)
# ---------------------------------------------------------------------------
HEAD_HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<link rel="canonical" href="{URL}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="geo.region" content="US-FL">
<meta name="geo.placename" content="Palmetto, Florida">
<meta property="og:type" content="article">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://{DOMAIN}/images/{OG_IMAGE}">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="Triangle Flooring">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{TITLE}">
<meta name="twitter:description" content="{DESC}">
<meta name="twitter:image" content="https://{DOMAIN}/images/{OG_IMAGE}">
<link rel="icon" type="image/png" sizes="32x32" href="/images/favicon.png">
<link rel="apple-touch-icon" sizes="180x180" href="/images/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Lato:wght@400;700&display=swap" rel="stylesheet">
"""

BREADCRUMB = (f'<nav class="breadcrumbs" aria-label="Breadcrumb"><div class="container"><ol>'
              f'<li><a href="/">Home</a></li><li><a href="/blog/">Blog</a></li><li>{BC_SHORT}</li>'
              f'</ol></div></nav>')

ARTICLE_HERO = f"""<section class="article-hero">
  <div class="container">
    <span class="eyebrow">{CATEGORY}</span>
    <h1>{H1}</h1>
    <div class="article-meta"><span>📅 Updated {DATE}</span><span>✍️ Jose Mauricio, Owner</span><span>📖 {READ_MIN} min read</span></div>
  </div>
</section>"""

# ---------------------------------------------------------------------------
# FAQ — single source of truth (drives both visible accordion AND FAQPage schema)
# ---------------------------------------------------------------------------
FAQS = [
    ("Can water-damaged hardwood floors be repaired, or do they need replacing?",
     "It depends on how long the wood was wet and how far it moved. Surface stains and light cupping caught within 24–48 hours can often be dried and refinished. Once boards crown, crack, separate at the seams, or the subfloor stays wet, board replacement or full replacement is usually the more cost-effective fix."),
    ("How long does it take for water to ruin hardwood floors?",
     "Damage starts within hours. Solid hardwood begins absorbing water and cupping within 24 hours of standing water; permanent damage is common after 48–72 hours. Engineered hardwood can delaminate even faster because water attacks the glue layers. The faster you extract water and start drying, the more boards you save."),
    ("Will my hardwood floor go back to normal after it dries?",
     "Sometimes. Mild cupping frequently flattens on its own once the wood's moisture content returns to equilibrium with the room — a process that can take weeks to months in Florida. If it's still cupped or crowned after the floor reads dry on a moisture meter, sanding and refinishing is the next step. Boards that cracked or buckled won't recover and need replacing."),
    ("Does homeowners insurance cover water-damaged hardwood floors in Florida?",
     "Usually yes for sudden, accidental events — a burst supply line, an overflowing dishwasher, or an AC condensate failure. Gradual leaks and long-term humidity damage are typically excluded, and flood from storm surge needs a separate FEMA flood policy. Document everything with photos and moisture readings before any work begins."),
    ("How much does it cost to repair water-damaged hardwood floors?",
     "Spot board replacement and refinishing a single room typically runs $1,200–$4,000. Refinishing a whole floor that cupped but survived runs $3–$8 per sq ft. Full tear-out and replacement runs $9–$18 per sq ft installed. We give every water-damage assessment in writing within 24 hours of inspection."),
    ("Can cupped hardwood floors be sanded flat?",
     "Yes — but only after the wood is fully dry. Sanding a floor that still holds moisture is the most common mistake we're called to fix: the boards finish flat, then shrink and over-dry into a 'crowned' shape weeks later, forcing a second sanding. Always confirm the floor reads dry on a moisture meter first."),
]


def faq_accordion(faqs):
    items = "".join(
        f'<details class="faq-item"><summary>{q}</summary>'
        f'<div class="faq-content"><p>{a}</p></div></details>'
        for q, a in faqs)
    return f'<div class="faq-list">{items}</div>'


def faqpage_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


# ---------------------------------------------------------------------------
# ARTICLE BODY (unique content)
# ---------------------------------------------------------------------------
ARTICLE = """<article class="article-body">
<div class="article-toc">
  <strong>What's in this guide</strong>
  <ol>
    <li><a href="#can-it-be-saved">Can water-damaged hardwood be saved?</a></li>
    <li><a href="#first-48">The first 48 hours: what to do right now</a></li>
    <li><a href="#repair-vs-replace-signs">Signs it's reparable vs a total loss</a></li>
    <li><a href="#cost">Repair or replace? 2026 cost comparison</a></li>
    <li><a href="#florida">Why Florida floors fail differently</a></li>
    <li><a href="#process">How the professional repair process works</a></li>
    <li><a href="#insurance">Will insurance cover it?</a></li>
    <li><a href="#faq">Frequently Asked Questions</a></li>
  </ol>
</div>

<p data-speakable="true"><strong>Lightly water-damaged hardwood can usually be saved if you act within 24&ndash;48 hours:</strong> stop the water source, pull up standing water, and force-dry the room. But once boards cup hard, crown, crack, or the subfloor stays wet, replacing the affected boards is normally cheaper than repeated repairs. A moisture-meter reading tells you which situation you're actually in.</p>

<p>We've inspected hundreds of water-damaged floors across Tampa Bay &mdash; from single burst icemaker lines in Lakewood Ranch to 100+ storm-flooded homes after Hurricanes Ian and Helene. This guide is the same triage we walk every homeowner through on site: what's salvageable, what isn't, and how to avoid the expensive mistakes that turn a $2,000 repair into a $14,000 replacement.</p>

<h2 id="can-it-be-saved">Can water-damaged hardwood be saved?</h2>

<p>Three variables decide it: <strong>how long the wood stayed wet, how much it moved, and whether the subfloor dried out.</strong> Clean water (a supply line) caught quickly is the best case. Gray or black water (sewage, storm surge) is the worst &mdash; contamination usually forces removal regardless of how the boards look.</p>

<div class="key-callout">
  <strong>The single rule that saves floors:</strong> never sand, refinish, or re-cover a water-damaged floor until a moisture meter confirms both the boards <em>and</em> the subfloor have returned to normal moisture content. In Florida humidity that can take 3&ndash;8 weeks. Rushing this step is the #1 reason a "repaired" floor fails again.
</div>

<h2 id="first-48">The first 48 hours: what to do right now</h2>

<p>What you do in the first two days determines how much floor you keep. In order:</p>

<ol>
  <li><strong>Stop the water source.</strong> Shut the supply valve, kill the appliance, or tarp the roof. Nothing else matters until the water stops.</li>
  <li><strong>Remove standing water fast.</strong> Wet-vac or pump it out. Every hour of standing water pushes more boards past the point of saving.</li>
  <li><strong>Lift area rugs, mats, and wet furniture.</strong> Trapped moisture under rugs creates the worst cupping and the fastest mold.</li>
  <li><strong>Force-dry the room.</strong> Run the AC at 72&ndash;75&deg;F, add a dehumidifier, and aim fans across (not down onto) the floor. The goal is to pull moisture out of the air so the wood can release it evenly.</li>
  <li><strong>Photograph everything before you clean up.</strong> Wide shots and close-ups, plus the source. This is what your insurer pays on.</li>
  <li><strong>Check the subfloor, not just the surface.</strong> Water wicks under the finish. A floor that looks dry on top is often still soaked underneath &mdash; that's what a moisture meter is for.</li>
  <li><strong>Call a flooring contractor before a "restoration" upsell.</strong> Get an independent read on what's actually reparable before anyone tears out boards or quotes a full replacement.</li>
</ol>

<div class="cta-inline">
  <strong>Floor underwater right now in Bradenton, Sarasota, or Tampa Bay?</strong>
  <p>We give same-day water-damage assessments 7 days a week and a written repair-or-replace plan within 24 hours &mdash; with moisture readings, not guesses.</p>
  <a href="/floor-repair/water-damage/">See our water-damage repair service &rarr;</a>
</div>

<h2 id="repair-vs-replace-signs">Signs it's reparable vs a total loss</h2>

<p>Walk the floor and look for these. The more "replace" signals you see, the less sense a repair makes.</p>

<table>
  <thead><tr><th>What you see</th><th>Likely reparable</th><th>Likely replace</th></tr></thead>
  <tbody>
    <tr><td><strong>Cupping</strong> (edges higher than center)</td><td>Mild, caught early, dries flat</td><td>Severe or still cupped after drying</td></tr>
    <tr><td><strong>Crowning</strong> (center higher than edges)</td><td>Rare to recover &mdash; usually sanded after full dry</td><td>Crowned + cracked boards</td></tr>
    <tr><td><strong>Buckling</strong> (boards lifted off subfloor)</td><td>&mdash;</td><td>Almost always replace affected area</td></tr>
    <tr><td><strong>Gaps / separation at seams</strong></td><td>Minor, closes on drying</td><td>Permanent gaps after drying</td></tr>
    <tr><td><strong>Staining / discoloration</strong></td><td>Surface stains sand out</td><td>Black stains (deep mold) into the wood</td></tr>
    <tr><td><strong>Engineered delamination</strong> (top veneer peeling)</td><td>&mdash;</td><td>Replace &mdash; glue layers are compromised</td></tr>
    <tr><td><strong>Water type</strong></td><td>Clean water, dried fast</td><td>Gray/black water or storm surge</td></tr>
    <tr><td><strong>Subfloor</strong></td><td>Reads dry within 1&ndash;2 weeks</td><td>Stays wet, soft, or smells musty</td></tr>
  </tbody>
</table>

<p>One nuance Florida homeowners miss: <strong>engineered hardwood and solid hardwood fail differently.</strong> Solid wood cups and can often be sanded flat once dry. Engineered wood has a thin veneer over glued plies &mdash; once water gets into those glue layers and the veneer lifts, there's nothing to sand and the board has to go.</p>

<h2 id="cost">Repair or replace? 2026 cost comparison</h2>

<p>Here's how the math typically lands in the Tampa Bay market. Use it to sanity-check any quote you're handed.</p>

<table>
  <thead><tr><th>Scenario</th><th>Approach</th><th>Typical 2026 cost</th></tr></thead>
  <tbody>
    <tr><td>A few cupped/stained boards, rest of floor sound</td><td>Spot board replacement + refinish the room</td><td class="price">$1,200 &ndash; $4,000</td></tr>
    <tr><td>Whole room cupped but dried flat, no rot</td><td>Sand &amp; refinish entire floor</td><td class="price">$3 &ndash; $8 / sq ft</td></tr>
    <tr><td>Subfloor wet, mold, or widespread buckling</td><td>Tear out + new engineered hardwood</td><td class="price">$9 &ndash; $18 / sq ft</td></tr>
    <tr><td>Flood / storm-surge (gray-black water)</td><td>Full removal, subfloor dry-out, replace</td><td class="price">$12 &ndash; $22 / sq ft</td></tr>
  </tbody>
</table>

<p>The rule of thumb we give clients: <strong>if the repair will cost more than about 60% of a replacement &mdash; or the subfloor is compromised &mdash; replace.</strong> Repeated patch jobs on a floor that keeps moving end up costing more than doing it once, correctly. Compare against our full <a href="/blog/floor-repair-cost-bradenton/">floor repair cost breakdowns by city</a> if you want city-specific numbers.</p>

<h2 id="florida">Why Florida floors fail differently</h2>

<p>The same leak that's a minor repair up north is often a bigger problem here, for three reasons:</p>

<ul>
  <li><strong>Slab construction.</strong> Most Florida homes are on concrete slab. Moisture vapor migrates up through the slab year-round, so a wood floor that gets wet from above <em>and</em> sits on damp concrete dries slowly and unevenly &mdash; the recipe for cupping.</li>
  <li><strong>Humidity swings.</strong> Outdoor humidity runs 70&ndash;85% while air-conditioned interiors sit at 45&ndash;55%. Wood that absorbed water releases it slowly in this environment, which is why "wait and see if it flattens" can take two months here, not two weeks.</li>
  <li><strong>Storm and flood exposure.</strong> After Hurricanes Ian and Helene we saw hardwood as a near-total loss in 95%+ of flooded homes, while properly installed <a href="/guides/waterproof-flooring-florida/">waterproof flooring</a> was often salvageable. If you're in a FEMA flood zone, that comparison matters when you rebuild.</li>
</ul>

<p>This is also why product choice matters on the replacement. Plenty of homeowners use a water-damage event to switch the wettest rooms to a waterproof material &mdash; see our honest <a href="/blog/best-flooring-florida-humidity/">best flooring for Florida humidity</a> comparison before you decide.</p>

<h2 id="process">How the professional repair process works</h2>

<p>When we handle a water-damaged hardwood floor, it runs in five stages:</p>

<ol>
  <li><strong>Inspection &amp; moisture mapping.</strong> We meter the boards and subfloor across the room and document readings &mdash; the baseline that decides repair vs replace and supports your insurance claim.</li>
  <li><strong>Source confirmation &amp; dry-out.</strong> We confirm the leak is fixed and the subfloor is drying. No flooring work starts on a wet substrate.</li>
  <li><strong>Repair or removal.</strong> Salvageable floors get spot board swaps and a full sand. Total losses get clean tear-out with the subfloor inspected and dried before anything new goes down.</li>
  <li><strong>Reinstall &amp; refinish.</strong> Matching boards (we keep leftover material boxed from our own installs) or new engineered hardwood, acclimated 48&ndash;72 hours to your home first.</li>
  <li><strong>Final walk-through &amp; warranty.</strong> Every repair is backed by our 1-year written labor warranty, same as a new install.</li>
</ol>

<p>Need a fresh floor instead of a patch? See our <a href="/hardwood-flooring/">hardwood flooring installation</a> and <a href="/hardwood-refinishing/">hardwood refinishing</a> services, or the full <a href="/floor-repair/">floor repair &amp; replacement</a> hub.</p>

<h2 id="insurance">Will insurance cover it?</h2>

<p>Sudden, accidental water damage (burst pipe, appliance failure, AC condensate line) is usually covered by standard Florida homeowners policies. <strong>Gradual leaks and long-term humidity damage are typically excluded</strong>, and storm-surge flooding requires a separate FEMA flood policy. Three things protect your claim:</p>

<ul>
  <li>Photos and video <em>before</em> cleanup, including the source.</li>
  <li>Documented moisture readings (boards and subfloor).</li>
  <li>A written, itemized assessment from a licensed contractor &mdash; which we provide within 24 hours of inspection.</li>
</ul>

<h2 id="faq">Frequently Asked Questions</h2>
""" + "".join(
    f"<h3>{q}</h3>\n<p>{a}</p>\n\n" for q, a in FAQS
) + """<p>Dealing with a wet hardwood floor? <a href="/floor-repair/water-damage/">See our water-damage floor repair service</a>, browse <a href="/floor-repair/">repair &amp; replacement</a>, or <a href="/contact/">request a free in-home assessment</a>. We'll meter your floor, tell you honestly whether it's reparable, and put the plan in writing within 24 hours.</p>

  <div class="author-card">
    <div style="width:64px;height:64px;border-radius:50%;flex-shrink:0;background:linear-gradient(135deg,var(--navy),var(--cerulean));color:#fff;display:grid;place-items:center;font-family:var(--font-head);font-weight:800;font-size:1.4rem">JM</div>
    <div>
      <strong>Jose Mauricio &mdash; Triangle Flooring</strong>
      <p>Owner and lead installer at Triangle Flooring, a licensed and insured Florida flooring contractor serving Bradenton, Sarasota, Lakewood Ranch, and Tampa Bay since 2023. 300+ projects completed, including 100+ storm-damage floor inspections after Hurricanes Ian and Helene. Every install backed by a 1-year written labor warranty.</p>
    </div>
  </div>
</article>"""

FAQ_SECTION = f"""<section class="faq-section">
  <div class="container">
    <div class="section-head"><span class="eyebrow">More Questions</span><h2>Frequently Asked</h2></div>
    {faq_accordion(FAQS)}
  </div>
</section>"""

# Related blog cards (reuse blog-card markup) ---------------------------------
def card(href, img, cat, date, title, blurb):
    return (f'<a href="{href}" class="blog-card">\n'
            f'          <div class="blog-card-photo"><img src="/images/{img}" alt="{title}" loading="lazy"></div>\n'
            f'          <div class="blog-card-body">\n'
            f'            <div class="blog-card-meta"><span>{cat}</span><span>{date}</span></div>\n'
            f'            <h3>{title}</h3>\n'
            f'            <p>{blurb}</p>\n'
            f'            <span class="blog-card-link">Read article →</span>\n'
            f'          </div>\n        </a>')

RELATED = f"""<section class="related" style="background:var(--gray-light)">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Continue Reading</span><h2>Related Guides</h2></div>
    <div class="blog-list">{card("/blog/best-flooring-florida-humidity/", "card-tile.webp", "Buyer Guides", "2026-05-03", "Best Flooring for Florida Humidity (2026 Comparison)", "Which flooring actually survives Florida humidity, floods, and hurricanes? An installer's room-by-room comparison.")}{card("/blog/hardwood-floor-refinishing-tampa-bay/", "card-hardwood.webp", "How-To Guides", "2026-04-29", "Hardwood Floor Refinishing in Tampa Bay (When & How)", "When a sand-and-refinish brings hardwood back to life — and when it's time to replace instead.")}{card("/blog/floor-repair-cost-bradenton/", "card-repair.webp", "Pricing Guides", "2026-05-03", "Floor Repair Cost in Bradenton, FL (2026)", "What floor repair and board replacement actually cost in Bradenton — by damage type and material.")}</div>
  </div>
</section>"""

# Pillar guide cards (reuse the styled pillar block) --------------------------
RELATED_POSTS = """<section class="related-posts" style="padding:3rem 0;background:var(--gray-light)">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Keep Reading</span><h2>Related Florida flooring guides</h2></div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1.4rem;max-width:980px;margin:0 auto">
      <a href="/floor-repair/water-damage/" style="background:#fff;border-radius:14px;padding:1.4rem;box-shadow:var(--shadow-sm);border:1px solid var(--gray-border);transition:transform .2s">
        <div style="font-size:.78rem;font-weight:700;letter-spacing:.1em;color:var(--cerulean);text-transform:uppercase;margin-bottom:.4rem">Repair Service</div>
        <h3 style="font-size:1.05rem;margin-bottom:.5rem;color:var(--text)">Water Damage Floor Repair</h3>
        <p style="font-size:.9rem;color:var(--gray);margin:0">Same-day assessments and written repair-or-replace plans across Tampa Bay.</p>
      </a>
      <a href="/guides/waterproof-flooring-florida/" style="background:#fff;border-radius:14px;padding:1.4rem;box-shadow:var(--shadow-sm);border:1px solid var(--gray-border);transition:transform .2s">
        <div style="font-size:.78rem;font-weight:700;letter-spacing:.1em;color:var(--cerulean);text-transform:uppercase;margin-bottom:.4rem">Pillar Guide</div>
        <h3 style="font-size:1.05rem;margin-bottom:.5rem;color:var(--text)">Waterproof Flooring for Florida</h3>
        <p style="font-size:.9rem;color:var(--gray);margin:0">What survives leaks, 90% humidity, and hurricane water — when it's time to switch materials.</p>
      </a>
      <a href="/hardwood-flooring/" style="background:#fff;border-radius:14px;padding:1.4rem;box-shadow:var(--shadow-sm);border:1px solid var(--gray-border);transition:transform .2s">
        <div style="font-size:.78rem;font-weight:700;letter-spacing:.1em;color:var(--cerulean);text-transform:uppercase;margin-bottom:.4rem">Service</div>
        <h3 style="font-size:1.05rem;margin-bottom:.5rem;color:var(--text)">Hardwood Flooring Installation</h3>
        <p style="font-size:.9rem;color:var(--gray);margin:0">Engineered &amp; solid hardwood installed and acclimated for Florida slab homes.</p>
      </a>
    </div>
  </div>
</section>"""

# ---------------------------------------------------------------------------
# JSON-LD
# ---------------------------------------------------------------------------
plain_words = len(re.sub(r"<[^>]+>", " ", ARTICLE).split())

breadcrumb_schema = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"https://{DOMAIN}/"},
    {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"https://{DOMAIN}/blog/"},
    {"@type": "ListItem", "position": 3, "name": BC_SHORT}]}

author = {"@type": "Person", "name": "Jose Mauricio", "jobTitle": "Owner & Lead Installer",
          "worksFor": {"@type": "Organization", "name": "Triangle Flooring", "url": f"https://{DOMAIN}/about/"},
          "knowsAbout": ["Water-damaged hardwood floor repair", "Hardwood flooring installation",
                         "Subfloor moisture management", "Floor refinishing", "Storm and flood floor restoration",
                         "Engineered hardwood"]}

article_schema = {"@context": "https://schema.org", "@type": "Article",
                  "@id": f"{URL}#article", "headline": H1, "description": DESC,
                  "image": [f"https://{DOMAIN}/images/{OG_IMAGE}"],
                  "datePublished": f"{DATE}T08:00:00-04:00", "dateModified": f"{DATE}T08:00:00-04:00",
                  "author": author,
                  "publisher": {"@type": "Organization", "name": "Triangle Flooring",
                                "logo": {"@type": "ImageObject", "url": f"https://{DOMAIN}/images/logo.png",
                                         "width": 200, "height": 200}},
                  "mainEntityOfPage": {"@type": "WebPage", "@id": URL},
                  "articleSection": CATEGORY, "wordCount": plain_words, "inLanguage": "en-US"}

local_business = {"@context": "https://schema.org",
                  "@type": ["LocalBusiness", "HomeAndConstructionBusiness"],
                  "@id": f"https://{DOMAIN}/#business", "name": "Triangle Flooring",
                  "description": "Licensed and insured flooring contractor and water-damaged floor repair specialist serving Bradenton, Sarasota, Lakewood Ranch and Tampa Bay, Florida.",
                  "url": f"https://{DOMAIN}/", "telephone": "+19414026861",
                  "image": f"https://{DOMAIN}/images/{OG_IMAGE}",
                  "address": {"@type": "PostalAddress", "streetAddress": "8737 Royal Acacia Ave",
                              "addressLocality": "Palmetto", "addressRegion": "FL",
                              "postalCode": "34221", "addressCountry": "US"},
                  "geo": {"@type": "GeoCoordinates", "latitude": 27.5214, "longitude": -82.5723},
                  "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0",
                                      "reviewCount": "13", "bestRating": "5"},
                  "priceRange": "$$",
                  "areaServed": [{"@type": "City", "name": c} for c in
                                 ["Bradenton", "Sarasota", "Lakewood Ranch", "Palmetto",
                                  "Parrish", "Venice", "St. Petersburg", "Tampa"]],
                  "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                      "opens": "07:00", "closes": "19:00"}]}

def ld(obj):
    return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>'

JSONLD = "\n".join([ld(breadcrumb_schema), ld(article_schema),
                    ld(faqpage_schema(FAQS)), ld(local_business)])

# ---------------------------------------------------------------------------
# ASSEMBLE
# ---------------------------------------------------------------------------
page = (HEAD_HTML + HEAD_STYLES_AND_GA + "\n<body>\n" + BODY_CSS + "\n" + HEADER + "\n"
        + BREADCRUMB + "\n\n" + ARTICLE_HERO + "\n\n" + ARTICLE + "\n\n" + FAQ_SECTION + "\n\n"
        + RELATED + "\n\n" + FINAL_CTA + "\n\n" + RELATED_POSTS + "\n\n" + FOOTER + "\n"
        + WA_FLOAT + "\n\n" + JSONLD + "\n\n" + CLOSING_SCRIPTS + "\n")

OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT.write_text(page, encoding="utf-8")
print(f"Wrote {OUT}")
print(f"  words (approx): {plain_words}")
print(f"  FAQ items: {len(FAQS)} (visible accordion == FAQPage schema)")
print(f"  JSON-LD blocks: BreadcrumbList, Article, FAQPage, LocalBusiness")
