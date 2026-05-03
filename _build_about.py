#!/usr/bin/env python3
"""Generate /about/index.html"""
import sys, json
sys.path.insert(0, '/home/claude/triangle')
from _gen import *

PATH = "/about/"
TITLE = "About Triangle Flooring | Bradenton FL Flooring Contractor"
DESC = "Meet Triangle Flooring — a local flooring contractor serving Bradenton, Sarasota, Lakewood Ranch & Tampa Bay. 300+ projects, 5★ rated, 1-year warranty."

bc_items = [("Home", "/"), ("About", None)]
bc_schema = render_breadcrumb_schema([(n,u) for n,u in bc_items])

faqs = [
  ("Where is Triangle Flooring based?",
   "<p>We're based in Palmetto, FL (Manatee County), and we serve all of Tampa Bay and Southwest Florida — including Bradenton, Sarasota, Lakewood Ranch, Parrish, Venice, St. Petersburg, and Tampa. We typically arrive within 24 hours of your call for a free in-home estimate.</p>"),
  ("How long has Triangle Flooring been installing flooring?",
   "<p>Our crew has 5+ years of professional flooring experience across hardwood, vinyl plank, tile, laminate, and stair treads. We've completed 300+ residential and small-commercial projects in Tampa Bay, including post-hurricane reflooring after Ian and Helene.</p>"),
  ("Are you licensed and insured?",
   "<p>Triangle Flooring is fully insured for both general liability and worker's compensation. Insurance certificates are available on request before any project begins. Florida does not require a state-level license for flooring installers (unlike general contractors), but we comply with all county-level requirements.</p>"),
  ("Do you do the work yourselves or subcontract?",
   "<p>We do all work in-house. The same crew that measures your home is the same crew that finishes the last baseboard. No subcontractor handoffs, no quality drop-off mid-project — the person you meet during your estimate is the person standing behind the work.</p>"),
]
faq_html, faq_schema = render_faq(faqs)

org_schema = {
  "@context":"https://schema.org",
  "@type":"AboutPage",
  "@id":f"https://{DOMAIN}/about/#aboutpage",
  "url":f"https://{DOMAIN}/about/",
  "name":"About Triangle Flooring",
  "description":DESC,
  "mainEntity":{"@id":f"https://{DOMAIN}/#organization"}
}

content = f"""{page_head(TITLE, DESC, PATH)}
{header()}
{breadcrumbs(bc_items)}

<section class="page-hero">
  <div class="container">
    <span class="eyebrow">About Us</span>
    <h1>The Story Behind <span>Triangle Flooring</span></h1>
    <p>A locally-owned flooring crew built on precision, transparency, and Florida-tough installations. 300+ projects across Tampa Bay and counting.</p>
    <div class="page-hero-trust">
      <span>5+ years experience</span>
      <span>300+ projects</span>
      <span>5★ Google rated</span>
      <span>Insured</span>
    </div>
  </div>
</section>

<section class="intro">
  <div class="container">
    <div class="intro-content">
      <h2 style="margin-bottom:1.2rem">Built for Florida. Built to Last.</h2>
      <p>Triangle Flooring was founded with one frustration in mind: <strong>too many flooring "contractors" in Tampa Bay treat installation like a side hustle.</strong> Subcontracted crews, no-show estimators, products that buckle the first humid summer — homeowners deserve better.</p>
      <p>We do things differently. The crew that measures your home on Monday is the same crew finishing your stair treads on Friday. Every plank, tile, and board acclimates 48–72 hours on-site at your home's actual humidity before a single nail goes in. And every install passes our proprietary <strong>42-Point Standard</strong> before we hand over the keys.</p>
      <p>That obsession with detail is why we've installed 300+ floors across Bradenton, Sarasota, Lakewood Ranch, Tampa, and beyond — and why our Google rating sits at a perfect 5.0.</p>

      <h2 style="margin:2.5rem 0 1.2rem">What Makes Us Different</h2>
      <p><strong>1. Same-crew installations.</strong> No subcontractor handoffs. The installer who quotes your job is the same one finishing it. This is rare in Florida flooring — most companies sell you the job and pass it to the cheapest available crew the next day.</p>
      <p><strong>2. Florida-acclimated materials.</strong> Coastal humidity is the #1 cause of buckled hardwood and gapped vinyl in Tampa Bay. We acclimate every product on-site for 48–72 hours so it expands and contracts with your home, not against it.</p>
      <p><strong>3. The 42-Point Standard.</strong> Our proprietary checklist covers subfloor moisture testing, expansion gap verification, transition strip alignment, and 38 other steps every install must pass before we call it done. You get a printed copy at handover.</p>
      <p><strong>4. Transparent pricing.</strong> Itemized written quotes — materials, labor, removal, prep — all line-by-line. No "surprise" upcharges mid-project. What you sign is what you pay.</p>
      <p><strong>5. 1-year written warranty.</strong> If a plank lifts, a tile cracks at the grout line, or a stair tread squeaks within 12 months of install — we come back and fix it. No fine print. No "act of God" loopholes.</p>

      <div class="stat-badge">
        <span class="stat-badge-icon">⭐</span>
        <div>
          <p>300+ Projects Completed Across Tampa Bay</p>
          <p>5.0 Google Rating · Insured · Same-crew installations · 1-year warranty</p>
        </div>
      </div>

      <h2 style="margin:2.5rem 0 1.2rem">Hurricane Damage? We've Done That.</h2>
      <p>After Hurricane Ian and Helene, we completed 80+ insurance and post-storm reflooring projects across Sarasota and Manatee counties. We know how to work with insurance documentation, photograph water damage progressions, and prioritize the rooms that need to be livable first. If you're filing a claim, we can quote based on your adjuster's scope or provide our own detailed estimate.</p>

      <h2 style="margin:2.5rem 0 1.2rem">Where We Serve</h2>
      <p>Headquartered in Palmetto, we serve all of <strong>Manatee County</strong> (Bradenton, Lakewood Ranch, Parrish, Palmetto, Ellenton), <strong>Sarasota County</strong> (Sarasota, Venice, North Port, Osprey, Nokomis, Siesta Key), and parts of <strong>Hillsborough</strong> (Tampa, Brandon, Riverview) and <strong>Pinellas</strong> (St. Petersburg, Clearwater). Not sure if we cover your area? <a href="/contact/" style="color:var(--cerulean);font-weight:600">Just ask</a> — we travel for the right project.</p>

      <h2 style="margin:2.5rem 0 1.2rem">The Triangle 42-Point Standard — Our Quality System</h2>
      <p>Most flooring contractors install your floor and call it a day. We install your floor and then run it through a 42-step quality check before we hand over the keys. The 42 points are organized into five phases: <strong>Pre-Install Inspection</strong> (8 checks — moisture testing, flatness, acclimation logging), <strong>Demolition &amp; Prep</strong> (8 checks — clean removal, screw-down loose subfloor, vapor barrier when needed), <strong>Installation</strong> (10 checks — expansion gaps verified, end joints staggered properly, transition strips fitted), <strong>Finish Detail Work</strong> (8 checks — quarter-round flush, paint touch-ups, dust-vacuumed twice), and <strong>Final Walk-Through</strong> (8 checks — every room reviewed with installer, manufacturer warranty registered, leftover material boxed for future repairs).</p>
      <p>You get a printed copy of the checklist at handover, with each item initialed by the installer who completed it. We're the only flooring contractor in Tampa Bay we know of who works this way. Most clients tell us the checklist is the moment they trust us — it shows we've thought through every detail before the job started.</p>

      <h2 style="margin:2.5rem 0 1.2rem">Materials We Work With</h2>
      <p>We're brand-agnostic — meaning we install whatever product is right for your project, not whatever we get the highest commission on. Brands we install regularly include:</p>
      <p><strong>Hardwood:</strong> Anderson, Mirage, Hallmark, Mohawk RevWood, Bruce, Shaw, DuChâteau, European White Oak from various mills. <strong>Luxury Vinyl Plank / SPC:</strong> COREtec, Karndean, Mohawk SolidTech, Shaw Floorté, Mannington Adura, LifeProof, Pergo Extreme. <strong>Tile:</strong> Daltile, MSI, Florida Tile, Marazzi, Anatolia, plus boutique large-format porcelain from Italian and Spanish mills. <strong>Laminate:</strong> Pergo, Mohawk RevWood, Shaw, Mannington Restoration. <strong>Stair Treads:</strong> Stair Treads Direct, custom-milled from your hardwood manufacturer's matching collections.</p>
      <p>If you've already picked out a product from Floor &amp; Decor, Lumber Liquidators, or another retailer, we'll happily install it. We'll also tell you honestly if we think it's the wrong product for your space — better to have that conversation before installation than after a return visit.</p>

      <h2 style="margin:2.5rem 0 1.2rem">Pricing Philosophy</h2>
      <p>We're not the cheapest. We're also not the most expensive. <strong>We're fairly priced for the quality we deliver</strong>, and we'll always tell you what your money is buying. Every quote is itemized: material cost, labor cost, removal/disposal, subfloor prep, transition strips, baseboards, waste percentage. No "package" pricing that hides what each line item costs. No surprise upcharges mid-project.</p>
      <p>If you receive a quote from us and another from a competitor that's significantly lower, ask the competitor: Are they testing subfloor moisture? Acclimating materials for 48-72 hours? Including subfloor prep? Providing a written labor warranty? In our experience, the gap usually disappears when you compare scopes line by line.</p>

      <h2 style="margin:2.5rem 0 1.2rem">Communication You Can Count On</h2>
      <p>Here's what to expect when you hire us: <strong>Day 1</strong> — initial call returned within 4 hours during business hours. <strong>Day 1-2</strong> — in-home measurement and consultation scheduled. <strong>Day 3-4</strong> — written itemized quote emailed within 24 hours of measurement. <strong>Pre-install</strong> — clear schedule with daily milestones. <strong>During install</strong> — daily text updates with photos. <strong>End of each day</strong> — clean job site, materials secured. <strong>Post-install</strong> — walk-through with installer, printed 42-point checklist, manufacturer warranty registration, 1-year labor warranty document. <strong>Year 1</strong> — we follow up at the 6-month and 12-month marks to make sure everything is still performing.</p>

      <h2 style="margin:2.5rem 0 1.2rem">Our Founder's Promise</h2>
      <p>I started Triangle Flooring because I was tired of seeing what was happening in Tampa Bay flooring. Subcontracted crews. No-show estimators. Materials that buckle the first humid summer. The local market deserves better, and so do the homeowners hiring us.</p>
      <p>Every project I take on, I personally meet the customer. I personally walk the job before we start. And if anything goes wrong — at the install or in the year that follows — you call me directly, not a corporate hotline. That's the difference between a local owner-operated business and a faceless flooring chain.</p>
      <p>Whether you're investing in a forever home in Lakewood Ranch, prepping a beachfront rental on Anna Maria Island, or just trying to fix a water-damaged floor before it spreads — I'd be honored to earn your trust. Call us, text us, WhatsApp us, or fill out the form. We'll reply same-day, every day.</p>

      <p style="text-align:center;font-style:italic;color:var(--navy);margin-top:2.5rem;font-family:var(--font-head);font-size:1.1rem">— The Triangle Flooring crew</p>

      {whatsapp_banner()}
    </div>
  </div>
</section>

<section class="faq-section">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Common Questions</span>
      <h2>About Triangle Flooring</h2>
    </div>
    {faq_html}
  </div>
</section>

<section class="related">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Explore More</span><h2>Browse Our Services</h2></div>
    <div class="related-grid">
      <a href="/hardwood-flooring/" class="related-card"><strong>Hardwood Flooring →</strong><span>Solid &amp; engineered hardwood for Florida homes</span></a>
      <a href="/vinyl-plank-flooring/" class="related-card"><strong>Luxury Vinyl Plank →</strong><span>100% waterproof LVP &amp; SPC installation</span></a>
      <a href="/tile-installation/" class="related-card"><strong>Tile Installation →</strong><span>Porcelain, ceramic &amp; large-format tile</span></a>
      <a href="/contact/" class="related-card"><strong>Get a Free Quote →</strong><span>In-home estimate within 24 hours</span></a>
    </div>
  </div>
</section>

{final_cta()}
{footer()}
{whatsapp_float()}

<script type="application/ld+json">{json.dumps(bc_schema)}</script>
<script type="application/ld+json">{json.dumps(faq_schema)}</script>
<script type="application/ld+json">{json.dumps(org_schema)}</script>

{menu_script()}
</body>
</html>"""

with open(f"{OUT_DIR}/about/index.html", "w") as f:
    f.write(content)
print(f"✓ /about/index.html ({len(content)//1024} KB)")
