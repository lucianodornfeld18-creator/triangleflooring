#!/usr/bin/env python3
"""Build high-value content assets (reusing _gen.py site chrome):
  A) /flooring-cost-report-2026/  — first-party data study (PR + AI-citation magnet)
  C) /guides/how-to-fix-a-squeaky-floor/        — HowTo schema
     /guides/what-to-do-after-floor-water-damage/ — HowTo schema
Idempotent (overwrites its own output). New pages -> add to sitemap separately.
"""
import os, json
import _gen as G

ROOT = os.path.dirname(os.path.abspath(__file__))
DOM = "https://triangle-floor.com"

def schema_block(*objs):
    return "".join(f'<script type="application/ld+json">{json.dumps(o,ensure_ascii=False,separators=(",",":"))}</script>' for o in objs)

def write(rel, html):
    full = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8", newline="").write(html)

def shell(title, desc, path, body, schemas, crumbs):
    return (G.page_head(title, desc, path) + G.header() +
            G.breadcrumbs(crumbs) + body + G.final_cta() + G.footer() +
            G.whatsapp_float() + schema_block(*schemas) + G.menu_script() + "\n</body></html>")

QA = ('<div class="quick-answer" data-tf-quickanswer style="background:#E8F2FB;border-left:4px solid #2E8DD9;'
      'padding:16px 20px;border-radius:0 10px 10px 0;margin:1.4rem auto;max-width:820px;font-size:1.02rem;'
      'line-height:1.6;color:#0F3A6E"><strong>Quick answer:</strong> {}</div>')

def cost_report():
    path = "/flooring-cost-report-2026/"
    title = "2026 Flooring Cost Report — Bradenton, Sarasota & Tampa Bay"
    desc = "Real 2026 flooring installation costs in Bradenton, Sarasota, Lakewood Ranch & Tampa Bay, from 300+ itemized Triangle Flooring quotes."
    rows = [
        ("Luxury Vinyl Plank (LVP/SPC)", "$3.91", "$11.11", "$782", "$2,222", "Waterproof — best for FL humidity & rentals"),
        ("Laminate", "$3.50", "$8.50", "$700", "$1,700", "Budget wood look; not for wet areas"),
        ("Hardwood (engineered & solid)", "$7.35", "$20.70", "$1,470", "$4,140", "Engineered preferred over FL slabs"),
        ("Porcelain / Ceramic Tile", "$7.50", "$22.00", "$1,500", "$4,400", "Best long-term in humidity"),
        ("Hardwood Refinishing", "$3.50", "$7.00", "$700", "$1,400", "Far cheaper than replacement"),
    ]
    tbl_rows = "".join(
        f'<tr><td style="font-weight:600">{n}</td><td class="price">{lo}–{hi}</td>'
        f'<td class="price">{rlo}–{rhi}</td><td style="font-size:.88rem;color:var(--gray)">{note}</td></tr>'
        for n, lo, hi, rlo, rhi, note in rows)
    other = ('<tr><td style="font-weight:600">Stair Tread Replacement</td><td class="price">$80–$220 / tread</td>'
             '<td class="price">$1,200–$3,300 (15 stairs)</td><td style="font-size:.88rem;color:var(--gray)">Solid oak/maple/hickory</td></tr>'
             '<tr><td style="font-weight:600">Floor Repair</td><td class="price">$250–$1,500+ / repair</td>'
             '<td class="price">varies</td><td style="font-size:.88rem;color:var(--gray)">Planks, water damage, squeaks</td></tr>')
    faqs = [
        ("How much does flooring cost in Bradenton or Sarasota in 2026?",
         "Installed costs range from $3.50/sq ft for laminate to $22/sq ft for premium tile. LVP averages $3.91–$11.11/sq ft and hardwood $7.35–$20.70/sq ft. A typical 500 sq ft room runs roughly $1,750–$11,000 depending on material and prep."),
        ("What drives flooring price up in Florida specifically?",
         "Three things: subfloor/slab moisture prep, humidity-rated materials and acclimation, and removal/disposal of old flooring. Skipping prep is the #1 cause of failed installs in the Gulf climate."),
        ("Is the cheapest quote a good idea?",
         "Usually not. The lowest bids typically skip acclimation, subfloor moisture testing, and real warranties. A correct install costs 25–40% more and lasts far longer."),
        ("How is this report calculated?",
         "From 300+ real, itemized Triangle Flooring quotes across Bradenton, Sarasota, Lakewood Ranch, Palmetto, Parrish, Venice, Tampa and St. Petersburg in 2025–2026."),
    ]
    faq_html, faq_schema = G.render_faq(faqs)
    body = f"""<section class="page-hero"><div class="container">
      <span class="eyebrow">First-Party Data · Updated 2026</span>
      <h1>2026 Flooring Cost Report</h1>
      <p>Real installation costs across Bradenton, Sarasota, Lakewood Ranch & Tampa Bay — from 300+ itemized Triangle Flooring quotes.</p>
    </div></section>
    <section><div class="container">
      {QA.format("In 2026, installed flooring in the Bradenton–Sarasota–Tampa Bay area ranges from $3.50/sq ft (laminate) to $22/sq ft (premium tile). LVP averages $3.91–$11.11/sq ft and hardwood $7.35–$20.70/sq ft. This report is built from 300+ real itemized quotes.")}
      <div class="intro-content">
        <p>Most flooring "cost calculators" use national averages that don't reflect Florida's slab construction, humidity, or local labor. This report uses <strong>300+ real itemized quotes</strong> Triangle Flooring produced across Manatee, Sarasota, Hillsborough and Pinellas counties in 2025–2026.</p>
      </div>
      <h2 style="text-align:center;margin:2rem 0 1rem">2026 Installed Cost by Flooring Type</h2>
      <div class="pricing-table"><table>
        <thead><tr><th>Flooring Type</th><th>Per sq ft (installed)</th><th>Typical 200 sq ft room</th><th>Florida note</th></tr></thead>
        <tbody>{tbl_rows}{other}</tbody>
      </table></div>
      <p class="pricing-note">Ranges are installed (material + labor). Final price depends on material grade, subfloor prep, removal, and layout. <a href="/contact/#quote">Get a free itemized quote →</a></p>
      <h2 style="text-align:center;margin:2.5rem 0 1rem">What Drives Florida Flooring Cost</h2>
      <div class="intro-content">
        <p><strong>1. Subfloor &amp; slab prep.</strong> Concrete slabs frequently need moisture testing and self-leveling — $0.50–$2.00/sq ft added when required.</p>
        <p><strong>2. Humidity-rated material + acclimation.</strong> Engineered hardwood and waterproof LVP cost more upfront but survive Gulf humidity; solid hardwood over slab without prep fails.</p>
        <p><strong>3. Removal &amp; disposal.</strong> Tearing out old tile or glued flooring adds labor most "from $X" ads hide.</p>
      </div>
      <div class="stat-badge"><span class="stat-badge-icon">📊</span><div><p>Across 300+ 2026 projects, LVP was chosen in ~55% of installs — driven by waterproofing, pet/scratch resistance, and price.</p><p>Source: Triangle Flooring quote data, 2025–2026</p></div></div>
    </div></section>
    <section class="faq-section"><div class="container"><div class="section-head"><span class="eyebrow">Cost FAQ</span><h2>2026 Flooring Cost — FAQ</h2></div>{faq_html}</div></section>"""
    art = G.render_article_schema(title, desc, "flooring-cost-report-2026", "hero-bg.jpg", "2026-06-10", "2026-06-10", 1100, "Flooring Cost")
    art["@id"] = f"{DOM}{path}#article"
    art["mainEntityOfPage"] = {"@type": "WebPage", "@id": f"{DOM}{path}"}
    schemas = [art, G.render_breadcrumb_schema([("Home", "/"), ("2026 Flooring Cost Report", None)]),
               G.render_local_business_schema("Cost Report", desc, path), faq_schema]
    html = shell(title[:65], desc[:158], path, body, schemas, [("Home", "/"), ("2026 Cost Report", None)])
    write("flooring-cost-report-2026/index.html", html)
    return path

def howto(slug, title, desc, intro, steps, faqs, quick):
    path = f"/guides/{slug}/"
    body_steps = "".join(
        f'<div style="background:var(--gray-light);padding:1.4rem;border-radius:14px;border-left:5px solid var(--orange);margin-bottom:1rem">'
        f'<h3 style="margin:0 0 .4rem;color:var(--navy)">{i}. {s[0]}</h3>'
        f'<p style="margin:0;color:var(--gray)">{s[1]}</p></div>'
        for i, s in enumerate(steps, 1))
    faq_html, faq_schema = G.render_faq(faqs)
    body = f"""<section class="page-hero"><div class="container">
      <span class="eyebrow">Florida Flooring Guide</span><h1>{title}</h1><p>{desc}</p></div></section>
    <section><div class="container">
      {QA.format(quick)}
      <div class="intro-content"><p>{intro}</p></div>
      <div style="max-width:820px;margin:1.5rem auto 0">{body_steps}</div>
      <div class="whatsapp-banner"><div class="whatsapp-banner-text"><strong>Need a pro instead?</strong><span>Free estimate within 24 hours · we speak EN/PT/ES.</span></div>
        <a href="https://wa.me/19414026861" target="_blank" rel="noopener" class="whatsapp-banner-btn">💬 WhatsApp Us</a></div>
    </div></section>
    <section class="faq-section"><div class="container"><div class="section-head"><span class="eyebrow">FAQ</span><h2>Common Questions</h2></div>{faq_html}</div></section>"""
    howto_schema = {
        "@context": "https://schema.org", "@type": "HowTo", "name": title, "description": desc,
        "step": [{"@type": "HowToStep", "position": i, "name": s[0], "text": s[1]} for i, s in enumerate(steps, 1)],
    }
    schemas = [howto_schema, G.render_breadcrumb_schema([("Home", "/"), ("Guides", "/guides/"), (title, None)]),
               G.render_local_business_schema("", desc, path), faq_schema]
    html = shell(title[:65], desc[:158], path, body, schemas, [("Home", "/"), ("Guides", "/guides/"), (title, None)])
    write(f"guides/{slug}/index.html", html)
    return path

built = [cost_report()]

built.append(howto(
    "how-to-fix-a-squeaky-floor",
    "How to Fix a Squeaky Floor",
    "Step-by-step guide to silencing squeaky hardwood, laminate and subfloors — what works, what doesn't, and when to call a pro in Florida.",
    "Floor squeaks come from boards or subfloor rubbing against each other or the fasteners. In Florida, humidity swings make seasonal gapping and squeaks common. Most squeaks are fixable from above or below without replacing the floor.",
    [("Find the exact squeak", "Walk slowly and mark each squeak with painter's tape. Squeaks usually cluster near joists, seams, or transitions."),
     ("Access from below if you can", "If there's a crawlspace or unfinished ceiling underneath, you can fix it invisibly from below — the best option."),
     ("From below: shim the gap", "Where a joist meets the subfloor with a gap, tap a thin wood shim with construction adhesive into the gap. Don't force it — you only fill the space, not lift the floor."),
     ("From below: glue/screw the seam", "For longer gaps, run a bead of construction adhesive along the joist-subfloor seam, or drive short screws up through the subfloor (not through the finish floor)."),
     ("From above (carpet/laminate)", "Locate the joist and drive a specialized squeak-eliminator screw through the subfloor into the joist, then snap off the head below the surface."),
     ("From above (hardwood)", "Drill an angled pilot hole near the squeak into a joist, drive a trim screw, and fill with matching wood filler. Test load before filling."),
     ("Address humidity if squeaks are seasonal", "Widespread seasonal squeaks point to a humidity/acclimation issue — keep indoor RH stable (45–55%) and have a pro assess if gapping is severe.")],
    [("Can I fix a squeaky floor permanently?", "Yes — fixing the board-to-joist connection (shims, adhesive, or proper screws) is permanent. Squeaks that return seasonally usually indicate a humidity or subfloor issue that needs a pro."),
     ("Does talcum powder or WD-40 fix floor squeaks?", "Powder (talc/graphite) between hardwood boards can silence minor friction squeaks temporarily, but it doesn't fix the underlying movement. Lubricants like WD-40 are not a real fix."),
     ("When should I call a professional?", "If squeaks are widespread, the floor feels bouncy/soft, or there's water damage, the subfloor or joists may need attention. Triangle Flooring offers free assessments across Bradenton–Sarasota–Tampa Bay.")],
    "Most squeaky floors are fixed by re-securing the board or subfloor to the joist — shims and adhesive from below, or specialized squeak screws from above. Seasonal squeaks across a whole floor usually mean a humidity/acclimation problem, common in Florida."))

built.append(howto(
    "what-to-do-after-floor-water-damage",
    "What to Do After Floor Water Damage in Florida",
    "A step-by-step plan for hardwood, laminate, vinyl and tile after a leak, flood or hurricane — what to save, what to replace, and how to avoid mold.",
    "Florida floors face leaks, storm surge and hurricane flooding. Acting in the first 24–48 hours decides whether you can save the floor or face mold and subfloor rot. Different materials respond very differently to water.",
    [("Stop the water and stay safe", "Shut off the source, and if flooding contacted outlets or the panel, kill power to the area before walking on it."),
     ("Remove standing water fast", "Extract water within hours. Standing water past 24–48 hours risks subfloor saturation and mold regardless of floor type."),
     ("Dry aggressively", "Run fans, a dehumidifier, and AC. Pull baseboards and, for floating floors, lift a few planks at the edge to let the subfloor breathe."),
     ("Assess by material", "Tile: usually fine if the substrate dried. LVP/SPC: waterproof but water trapped underneath must be dried. Laminate: swells and usually must be replaced. Hardwood: may be refinishable if dried within ~48 hours, otherwise plank replacement."),
     ("Check the subfloor", "The floor on top can look fine while the subfloor stays wet. Have moisture metered — wet subfloor must dry to spec before any reinstall, or the new floor fails."),
     ("Document for insurance", "Photograph everything, keep damaged samples, and get a written assessment before disposal — it supports your claim."),
     ("Decide refinish vs replace", "A pro can tell you whether hardwood can be sanded/refinished or needs replacement, and which waterproof material best prevents a repeat.")],
    [("Can hardwood floors be saved after water damage?", "Sometimes. If the water is removed and the wood dried within roughly 48 hours, hardwood can often be refinished. Prolonged saturation causes cupping, crowning and subfloor rot that require replacement."),
     ("Does vinyl plank need to be replaced after a flood?", "LVP/SPC is waterproof, so the plank itself usually survives — but water trapped beneath it must be dried to prevent mold, which often means lifting the floor to dry the subfloor."),
     ("How fast do I need to act to prevent mold?", "Mold can start within 24–48 hours. Extract water and start drying immediately, and keep indoor humidity down. For hurricane/flood damage, call a pro for a moisture assessment.")],
    "After floor water damage, extract the water and start drying within 24–48 hours to prevent mold. Tile and waterproof LVP often survive (dry the subfloor underneath); laminate usually needs replacing; hardwood may be refinishable if dried fast. Always check the subfloor before reinstalling."))

print(json.dumps({"built": built}, indent=2))
