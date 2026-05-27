#!/usr/bin/env python3
"""Generate /faq/, /financing/, /warranty/ — support pages."""
import sys, json, os
sys.path.insert(0, '/home/claude/triangle')
from _gen import *

# ============================================================================
# /faq/ — Master FAQ page (gathers all common questions)
# ============================================================================

def build_faq():
    PATH = "/faq/"
    TITLE = "Flooring FAQ | Common Questions Answered | Triangle Flooring"
    DESC = "Common flooring questions answered by a Tampa Bay installer. Pricing, materials, installation timelines, warranties, hurricane damage, and more."
    if len(TITLE) > 65: TITLE = "Flooring FAQ | Triangle Flooring Tampa Bay"

    bc_items = [("Home","/"),("FAQ", None)]
    bc_schema = render_breadcrumb_schema(bc_items)

    # Comprehensive FAQ — organized in categories
    faq_categories = [
        ("Getting Started", [
            ("How do I get a quote from Triangle Flooring?",
             "<p>The fastest way is to call us at <a href='tel:+19414026861'>(941) 402-6861</a> or send a quick message on <a href='https://wa.me/19414026861' target='_blank'>WhatsApp</a>. You can also fill out the <a href='/contact/'>contact form</a>. We respond same-day, 7 days a week.</p><p>From there, we schedule a free in-home measurement (typically within 24-48 hours). At the measurement, we discuss your goals, test your subfloor, recommend materials based on your specific home and budget, and email you a fully itemized written quote within 24 hours.</p>"),
            ("How long does the quote process take?",
             "<p>From initial contact to receiving a written quote, expect 2-3 days total. The in-home measurement itself takes 30-60 minutes. We email the itemized quote within 24 hours of the measurement. There's no obligation — many clients get multiple quotes before deciding.</p>"),
            ("What information do I need to provide for a quote?",
             "<p>For an accurate quote, we need to see the space in person — photos and rough square footage are not enough for a real bid. During the in-home visit, we measure every room precisely, identify subfloor conditions, evaluate door clearance for new floor heights, and discuss material preferences. The whole process is consultative, not high-pressure.</p>"),
            ("Do you charge for the in-home estimate?",
             "<p>No. All measurements and estimates are free, with no obligation. We don't try to close you on the first visit, and we don't follow up with high-pressure sales tactics. If you decide to go with another contractor, no hard feelings.</p>"),
        ]),
        ("Pricing & Payment", [
            ("How much does flooring cost installed in Tampa Bay?",
             "<p>It varies significantly by material and project complexity. As a rough range for 2026 Tampa Bay rates: <strong>laminate</strong> $3-$8/sqft installed, <strong>vinyl plank</strong> $4-$11/sqft installed, <strong>engineered hardwood</strong> $9-$18/sqft installed, <strong>tile</strong> $8-$25/sqft installed. We provide free itemized quotes that break down material, labor, and prep separately.</p>"),
            ("What payment terms do you offer?",
             "<p>For most residential projects, we collect a 40-50% deposit at contract signing (covers material costs), then the balance upon completion and customer walk-through. For larger projects ($15,000+), we can structure milestone payments (e.g., deposit / mid-project / final). We accept check, ACH transfer, credit card, and cash.</p>"),
            ("Do you offer financing?",
             "<p>Yes, through partner lenders we can offer 6, 12, 18, and 24-month financing options (some 0% APR). See our <a href='/financing/'>financing page</a> for details and to start a soft-pull pre-qualification (no credit score impact).</p>"),
            ("Are there any hidden fees?",
             "<p>No. Every quote is fully itemized: material cost, labor cost, removal/disposal, subfloor prep, transition strips, baseboards, waste percentage. The number on your contract is the number on your final invoice. The only exception is if we discover hidden subfloor damage during demolition (e.g., rotted plywood under existing tile) — in that case, we stop work, document the issue, and provide a written change order before proceeding.</p>"),
        ]),
        ("Materials & Recommendations", [
            ("What's the best flooring for Florida humidity?",
             "<p>Porcelain tile and SPC vinyl plank are the most humidity-tolerant options. Engineered hardwood (not solid) handles humidity well when properly acclimated. Laminate and solid hardwood are more sensitive to Florida's humidity swings. See our <a href='/blog/best-flooring-florida-humidity/'>complete guide</a> for room-by-room recommendations.</p>"),
            ("Can I install hardwood on a Florida concrete slab?",
             "<p>Solid hardwood is generally not recommended directly on slab in Florida. We recommend engineered hardwood instead — it's multi-ply construction makes it far more dimensionally stable in humid coastal climates. If you really want solid hardwood, we'd install plywood underlayment first (raises floor height ~3/4 inch).</p>"),
            ("What's the difference between LVP and SPC?",
             "<p>Both are luxury vinyl, but the core construction differs. LVP has a flexible PVC core. SPC (Stone Plastic Composite) has a rigid mineral-filled core that's more dimensionally stable in Florida humidity, more resistant to subfloor imperfections, and slightly more impact-resistant. For most Florida homes, we recommend SPC over standard LVP.</p>"),
            ("Should I match flooring throughout the whole house?",
             "<p>Many newer Florida homes have continuous flooring throughout main living areas (one material from kitchen to bedrooms), with separate tile in bathrooms only. This creates a more open, larger-feeling space. However, it's also fine to use different materials in different rooms — we can recommend a configuration during your consultation that balances aesthetics with practicality.</p>"),
            ("How do I choose between hardwood and vinyl plank?",
             "<p>Hardwood looks and feels more premium, lasts longer (50+ years vs 20-30), and has stronger resale ROI. Vinyl plank is 100% waterproof, more scratch-resistant, costs less, and installs faster. See our <a href='/blog/hardwood-vs-vinyl-plank-lakewood-ranch/'>side-by-side comparison</a> for the full breakdown.</p>"),
        ]),
        ("Installation Process", [
            ("How long does flooring installation take?",
             "<p>Depends on size and complexity. <strong>Single rooms</strong> take 1-2 days. <strong>1,200-1,500 sqft projects</strong> typically take 2-4 working days for vinyl plank or laminate, 3-5 days for hardwood. <strong>Whole-home installs</strong> (2,500+ sqft) can take 5-10 days. <strong>Tile work</strong> takes longer than wood-based products (typically 1.5-2x the time) because of mortar cure time.</p>"),
            ("Do I need to move all my furniture before installation?",
             "<p>You can do it yourself to save money ($200-600 per room), or we can move it for you. We charge a furniture-moving fee per room. For larger items (pianos, antiques, large bookcases), we recommend professional movers — we can refer you to local options if needed.</p>"),
            ("Will I need to leave my home during installation?",
             "<p>Most homeowners stay in their homes during installation. We work room-by-room when possible, so you typically have access to bedrooms, bathrooms, and kitchen during the project. The main exception is during the final coating phase of nail-down hardwood (light fumes for a few hours) or during full-home tile installs. We'll discuss any considerations during your consultation.</p>"),
            ("How do you protect my home during the install?",
             "<p>We bring our own dust containment plastic, drop cloths for non-floor surfaces, vacuum systems with HEPA filtration, and we tape off rooms not being worked on. Your home will be clean every day when we leave. Our 42-Point Standard requires at least two daily clean-up passes — including dust-vacuuming the work area and damp-mopping with the manufacturer's recommended cleaner.</p>"),
            ("Will the installation damage my walls or trim?",
             "<p>Some baseboard or quarter-round damage is common during demolition. We discuss this upfront — typically the most cost-effective approach is to remove existing baseboards (which usually come off without damage), install the new floor, then reinstall the baseboards or install new quarter-round. We touch up paint where needed at no extra charge as part of every install.</p>"),
        ]),
        ("Warranties & Issues", [
            ("What warranties come with my flooring?",
             "<p>Two warranties: the <strong>manufacturer's product warranty</strong> (typically 15 years to lifetime depending on the specific product) and our <strong>Triangle Flooring 1-year labor warranty</strong>. The manufacturer warranty covers material defects. Our labor warranty covers any installation-related issues — plank lifting, tile cracking at grout, stair tread squeaking, transition strip failures. See our <a href='/warranty/'>warranty page</a> for full details.</p>"),
            ("What if something goes wrong with my floor after installation?",
             "<p>Call us. The fastest path is the same number you used to get your quote: <a href='tel:+19414026861'>(941) 402-6861</a>. Within the 1-year labor warranty period, we come out and fix anything related to installation at no charge. Outside that period, we offer paid repair work at fair rates.</p>"),
            ("Can you fix flooring installed by another contractor?",
             "<p>Yes. We do repairs and partial reflooring on floors installed by other contractors regularly. We can usually source matching materials (or close matches) and do partial repairs, plank replacements, tile crack fixes, subfloor repairs, and more. We provide a separate <a href='/floor-repair/'>repair service quote</a> for these projects.</p>"),
            ("What if I find subfloor damage mid-project?",
             "<p>We document it (photos, written description), stop work, and provide a written change order with the additional cost before proceeding. This is the only scenario where pricing might change after contract signing. We never proceed with extra charges without your written approval.</p>"),
        ]),
        ("Hurricane & Insurance", [
            ("Can you handle hurricane damage flooring repairs?",
             "<p>Yes — we've completed 80+ post-hurricane reflooring projects in Manatee and Sarasota counties since Hurricane Ian (2022) and Helene (2024). We work with insurance adjusters, can quote based on your adjuster's scope, and provide photo documentation that supports your claim.</p>"),
            ("Will my insurance cover post-hurricane flooring damage?",
             "<p>It depends on your policy and the cause of damage. Generally: flood damage is covered only by separate flood insurance (NFIP), wind-driven rain damage through a damaged roof is usually covered by standard homeowners, and storm surge is flood insurance only. We're not insurance adjusters, but we can document damage in claim-friendly format and have worked with most major Florida insurers.</p>"),
            ("How fast can you respond to water emergencies?",
             "<p>For active emergencies (burst pipes, fresh storm damage), we can typically have a crew on-site within 24 hours for damage assessment. Full repairs depend on materials availability and damage extent — usually we begin repair within 3-7 days of initial assessment.</p>"),
            ("What flooring survives flooding best?",
             "<p>Porcelain tile and SPC vinyl plank are by far the most flood-resistant. Tile typically survives flooding with no damage to the floor itself. SPC is salvageable in 70-80% of flooded homes (only subfloor and adhesive need replacement, not the planks). Hardwood and laminate are typically total losses after flooding.</p>"),
        ]),
    ]

    # Build sectioned FAQ HTML
    sections_html = ""
    all_faqs = []
    for cat_name, faqs in faq_categories:
        items = "".join(f'<details class="faq-item"><summary>{q}</summary><div class="faq-content">{a}</div></details>' for q,a in faqs)
        sections_html += f"""<div style="max-width:820px;margin:0 auto 3rem">
          <h2 style="font-size:1.5rem;color:var(--navy);margin-bottom:1.2rem;padding-bottom:.6rem;border-bottom:2px solid var(--navy-light)">{cat_name}</h2>
          <div class="faq-list">{items}</div>
        </div>"""
        for q, a in faqs:
            import re as r
            plain_a = r.sub(r'<[^>]+>', '', a).strip()
            all_faqs.append({"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":plain_a}})

    faq_schema = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":all_faqs}

    content = f"""{page_head(TITLE, DESC, PATH)}
{header()}
{breadcrumbs(bc_items)}

<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Resources</span>
    <h1>Flooring <span>FAQ</span></h1>
    <p>Real questions, real answers — from a contractor who actually does the work. Click any question to expand.</p>
    <div class="page-hero-trust">
      <span>{len(all_faqs)} questions answered</span>
      <span>6 categories</span>
      <span>Updated 2026</span>
    </div>
  </div>
</section>

<section class="faq-section">
  <div class="container">
    {sections_html}
  </div>
</section>

<section class="related">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Still Have Questions?</span><h2>We're Easy to Reach</h2></div>
    <div class="related-grid">
      <a href="tel:+19414026861" class="related-card"><strong>📞 Call Us →</strong><span>(941) 402-6861 · 7 days a week</span></a>
      <a href="https://wa.me/19414026861" target="_blank" rel="noopener" class="related-card"><strong>💬 WhatsApp →</strong><span>Reply within 1 hour, business hours</span></a>
      <a href="/contact/" class="related-card"><strong>📝 Contact Form →</strong><span>Free quote within 24 hours</span></a>
    </div>
  </div>
</section>

{final_cta()}
{footer()}
{whatsapp_float()}

<script type="application/ld+json">{json.dumps(bc_schema)}</script>
<script type="application/ld+json">{json.dumps(faq_schema)}</script>

{menu_script()}
</body>
</html>"""

    out = f"{OUT_DIR}/faq/index.html"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f: f.write(content)
    print(f"  ✓ /faq/ ({len(content)//1024}KB · {len(all_faqs)} questions)")


# ============================================================================
# /financing/ — Financing options page
# ============================================================================

def build_financing():
    PATH = "/financing/"
    TITLE = "Flooring Financing | Triangle Flooring Tampa Bay"
    DESC = "Flooring financing options for Bradenton, Sarasota & Tampa Bay homeowners. 6, 12, 18 & 24-month plans. Soft credit pull, no impact on your score."

    bc_items = [("Home","/"),("Financing", None)]
    bc_schema = render_breadcrumb_schema(bc_items)

    faqs = [
        ("Will applying for financing affect my credit score?",
         "<p>No. The pre-qualification is a soft credit pull — it does NOT affect your credit score. Only if you proceed with a full application after pre-qualification will a hard inquiry occur. You can pre-qualify just to see your options without any commitment.</p>"),
        ("What credit score do I need to qualify?",
         "<p>Our partner lenders offer financing options at multiple credit tiers. Borrowers with scores above 680 typically qualify for the most favorable rates (including some 0% promotional terms). Borrowers with scores in the 620-680 range can usually qualify for standard rates. Below 620, we recommend reviewing other payment options or building credit first.</p>"),
        ("How long does financing approval take?",
         "<p>Pre-qualification is instant (under 2 minutes). Full approval after you choose a financing plan typically takes 24-48 hours. We can begin your project as soon as approval is finalized.</p>"),
        ("Are there any fees or hidden charges?",
         "<p>Promotional 0% APR terms have no interest and no fees if paid in full within the promotional period. Standard installment loans charge interest at the rate disclosed at approval — no application fees, no prepayment penalties. We'll always show you the exact total cost before you sign anything.</p>"),
        ("Can I pay off my loan early?",
         "<p>Yes — all our financing partners allow early payoff with no penalties. You can pay extra toward principal anytime to reduce the total interest paid.</p>"),
        ("Do you finance smaller projects?",
         "<p>Most lenders have a minimum financed amount of $1,000-$2,500. Smaller repair projects under that threshold are typically paid by check, card, or cash. For projects above the minimum, financing is available.</p>"),
    ]
    faq_html, faq_schema = render_faq(faqs)

    content = f"""{page_head(TITLE, DESC, PATH)}
{header()}
{breadcrumbs(bc_items)}

<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Easy Payment Options</span>
    <h1>Flooring <span>Financing</span></h1>
    <p>Get the floor you want now. Pay over 6, 12, 18, or 24 months. Soft credit check, no impact on your score.</p>
  </div>
</section>

<section class="intro">
  <div class="container">
    <div class="intro-content">
      <h2 style="margin-bottom:1.4rem">How Triangle Flooring Financing Works</h2>
      <p>Your floor is one of the largest interior surfaces in your home — it deserves to be done right, not rushed because of cash flow. We've partnered with top-tier consumer financing lenders so you can install the flooring you actually want, then pay it off on a comfortable schedule.</p>

      <p>The process is simple:</p>
      <ol style="margin:1.5rem 0;padding-left:1.5rem">
        <li style="margin-bottom:.7rem"><strong>Get a free quote.</strong> We measure your home and provide an itemized written estimate within 24 hours.</li>
        <li style="margin-bottom:.7rem"><strong>Pre-qualify in 2 minutes.</strong> Soft credit pull — no impact on your score. See your available terms instantly.</li>
        <li style="margin-bottom:.7rem"><strong>Choose your plan.</strong> 6, 12, 18, or 24-month options. Some plans include 0% APR promotional periods.</li>
        <li style="margin-bottom:.7rem"><strong>We start your project.</strong> Once financing is approved, we begin scheduling your install on your timeline.</li>
        <li><strong>Pay on schedule.</strong> Monthly auto-debit from your bank account or credit card. No early payoff penalties.</li>
      </ol>

      <h2 style="margin:2.5rem 0 1.4rem">Sample Financing Scenarios</h2>
      <p>Here are some real example monthly payments based on common Tampa Bay flooring project sizes:</p>

      <div style="overflow-x:auto;margin:1.5rem 0">
        <table style="width:100%;border-collapse:collapse;background:#fff;border-radius:14px;overflow:hidden;box-shadow:var(--shadow);min-width:560px">
          <thead style="background:linear-gradient(135deg,var(--navy-dark),var(--navy));color:#fff">
            <tr>
              <th style="padding:14px 18px;text-align:left;font-family:var(--font-head);font-weight:600">Project Total</th>
              <th style="padding:14px 18px;text-align:left;font-family:var(--font-head);font-weight:600">12-Month Plan</th>
              <th style="padding:14px 18px;text-align:left;font-family:var(--font-head);font-weight:600">24-Month Plan</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom:1px solid var(--gray-border)"><td style="padding:13px 18px;font-weight:600">$5,000</td><td style="padding:13px 18px">~$417/mo (0% APR)</td><td style="padding:13px 18px">~$229/mo (9.99% APR)</td></tr>
            <tr style="border-bottom:1px solid var(--gray-border);background:var(--gray-light)"><td style="padding:13px 18px;font-weight:600">$10,000</td><td style="padding:13px 18px">~$833/mo (0% APR)</td><td style="padding:13px 18px">~$458/mo (9.99% APR)</td></tr>
            <tr style="border-bottom:1px solid var(--gray-border)"><td style="padding:13px 18px;font-weight:600">$15,000</td><td style="padding:13px 18px">~$1,250/mo (0% APR)</td><td style="padding:13px 18px">~$687/mo (9.99% APR)</td></tr>
            <tr><td style="padding:13px 18px;font-weight:600">$20,000</td><td style="padding:13px 18px">~$1,667/mo (0% APR)</td><td style="padding:13px 18px">~$916/mo (9.99% APR)</td></tr>
          </tbody>
        </table>
      </div>
      <p style="font-size:.85rem;color:var(--gray);margin-top:.5rem"><em>Rates are approximate and subject to credit approval. Actual rates vary based on credit score and term length. 0% APR promotional terms typically require full payoff within 12 months to avoid retroactive interest.</em></p>

      <h2 style="margin:2.5rem 0 1.4rem">Who Qualifies?</h2>
      <p>To pre-qualify for financing, you'll need:</p>
      <ul style="margin:0 0 1.5rem 1.5rem">
        <li style="margin-bottom:.5rem">US residency and a valid Social Security Number or ITIN</li>
        <li style="margin-bottom:.5rem">Verified income (typically $25,000+ annual)</li>
        <li style="margin-bottom:.5rem">Credit score of 620 or higher (best terms at 680+)</li>
        <li>Project minimum of $1,000-$2,500 depending on the lender</li>
      </ul>

      <p>Most homeowners qualify for at least one option, even with less-than-perfect credit. The pre-qualification process takes about 2 minutes and shows you exactly what you'll qualify for before you commit to anything.</p>

      <div class="stat-badge">
        <span class="stat-badge-icon">💳</span>
        <div>
          <p>Ready to See Your Options?</p>
          <p>Soft credit pull · No impact on score · 2-minute pre-qualification · No obligation</p>
        </div>
      </div>

      <h2 style="margin:2.5rem 0 1.4rem">How to Apply</h2>
      <p>Financing is offered as part of our quote process — we'll discuss it during your in-home estimate visit if you're interested. <a href="/contact/" style="color:var(--cerulean);font-weight:600">Request a free quote</a> and mention financing in the message field, or just bring it up at the consultation.</p>

      <p>You can also call us directly at <a href="tel:+19414026861" style="color:var(--cerulean);font-weight:600">(941) 402-6861</a> if you have specific financing questions before scheduling your estimate. We're happy to walk you through your options on the phone.</p>
    </div>
  </div>
</section>

<section class="faq-section">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Common Questions</span><h2>Financing FAQ</h2></div>
    {faq_html}
  </div>
</section>

{final_cta()}
{footer()}
{whatsapp_float()}

<script type="application/ld+json">{json.dumps(bc_schema)}</script>
<script type="application/ld+json">{json.dumps(faq_schema)}</script>

{menu_script()}
</body>
</html>"""

    out = f"{OUT_DIR}/financing/index.html"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f: f.write(content)
    print(f"  ✓ /financing/ ({len(content)//1024}KB)")


# ============================================================================
# /warranty/ — Warranty details page
# ============================================================================

def build_warranty():
    PATH = "/warranty/"
    TITLE = "Flooring Warranty Details | Triangle Flooring Tampa Bay"
    DESC = "Triangle Flooring's 1-year labor warranty + manufacturer product warranties (15 years to lifetime). What's covered, how to file a claim, exclusions explained."

    bc_items = [("Home","/"),("Warranty", None)]
    bc_schema = render_breadcrumb_schema(bc_items)

    faqs = [
        ("How do I file a warranty claim?",
         "<p>Just call us at <a href='tel:+19414026861'>(941) 402-6861</a> or send a message via <a href='/contact/'>our contact form</a> describing the issue. Photos help. We'll schedule a site visit (typically within 5-7 business days) to assess the issue and determine if it's a labor warranty matter (we fix it free) or a product warranty matter (we coordinate with the manufacturer on your behalf).</p>"),
        ("What's the difference between labor warranty and product warranty?",
         "<p>The <strong>labor warranty</strong> covers issues caused by installation — planks lifting from improper expansion gaps, tile cracking from inadequate substrate prep, transition strips coming loose, etc. We provide this directly. The <strong>product warranty</strong> covers manufacturing defects in the flooring itself — delamination, finish failure, dimensional defects. The manufacturer provides this; we help you process the claim.</p>"),
        ("What's NOT covered by the warranty?",
         "<p>The 1-year labor warranty does NOT cover: damage from water events (flooding, leaks, hurricane), damage from misuse (dragging heavy furniture without protection, wearing high heels on hardwood), damage from improper cleaning (vinegar, ammonia, bleach voiding the manufacturer warranty), damage from extreme indoor humidity (uncontrolled HVAC), or normal wear-and-tear from daily use.</p>"),
        ("Is the warranty transferable if I sell my home?",
         "<p>The Triangle Flooring 1-year labor warranty is non-transferable — it applies to the original homeowner only. Most manufacturer product warranties ARE transferable to new homeowners but typically require registration within a specific time window after purchase. We help original homeowners register manufacturer warranties at the time of installation.</p>"),
        ("What if I need a repair after the 1-year period?",
         "<p>We offer paid repair services at fair rates after the warranty period expires. Most simple repairs (single plank replacement, small tile repair, transition strip refit) cost $200-$500. Larger issues are quoted case-by-case. Repeat customers often qualify for discounted repair rates.</p>"),
    ]
    faq_html, faq_schema = render_faq(faqs)

    content = f"""{page_head(TITLE, DESC, PATH)}
{header()}
{breadcrumbs(bc_items)}

<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Our Promise</span>
    <h1>Flooring <span>Warranty Coverage</span></h1>
    <p>Two layers of protection on every install — our written 1-year labor warranty plus manufacturer product warranties up to lifetime.</p>
  </div>
</section>

<section class="intro">
  <div class="container">
    <div class="intro-content">
      <h2 style="margin-bottom:1.4rem">The Triangle Flooring 1-Year Labor Warranty</h2>
      <p>Every installation we do — hardwood, vinyl plank, tile, laminate, stair treads, repairs — comes with our written 1-year labor warranty. <strong>If anything fails because of installation within 12 months of your project completion date, we come back and fix it at no charge.</strong> No fine print, no "act of God" loopholes, no negotiation required.</p>

      <p>This warranty covers any issue traceable to how we installed the flooring, including:</p>
      <ul style="margin:0 0 1.5rem 1.5rem">
        <li style="margin-bottom:.5rem"><strong>Plank lifting or buckling</strong> from inadequate expansion gaps or acclimation</li>
        <li style="margin-bottom:.5rem"><strong>Tile cracking at grout lines</strong> from substrate flex or improper mortar coverage</li>
        <li style="margin-bottom:.5rem"><strong>Squeaking subfloor or stair treads</strong> from inadequate fastening</li>
        <li style="margin-bottom:.5rem"><strong>Transition strip failures</strong> from poor fit or fastening</li>
        <li style="margin-bottom:.5rem"><strong>Adhesive failures</strong> on glue-down installations</li>
        <li style="margin-bottom:.5rem"><strong>Visible installation defects</strong> like uneven seams, lippage, or misaligned planks</li>
        <li><strong>Quarter-round or baseboard failures</strong> from improper installation</li>
      </ul>

      <h2 style="margin:2.5rem 0 1.4rem">Manufacturer Product Warranties</h2>
      <p>In addition to our labor warranty, every flooring product we install carries the manufacturer's own warranty covering material defects. These typically range from 15 years to lifetime depending on the specific product and brand. Common warranty periods we see:</p>

      <div style="overflow-x:auto;margin:1.5rem 0">
        <table style="width:100%;border-collapse:collapse;background:#fff;border-radius:14px;overflow:hidden;box-shadow:var(--shadow);min-width:560px">
          <thead style="background:linear-gradient(135deg,var(--navy-dark),var(--navy));color:#fff">
            <tr><th style="padding:14px 18px;text-align:left;font-family:var(--font-head);font-weight:600">Material Type</th><th style="padding:14px 18px;text-align:left;font-family:var(--font-head);font-weight:600">Typical Warranty Period</th></tr>
          </thead>
          <tbody>
            <tr style="border-bottom:1px solid var(--gray-border)"><td style="padding:13px 18px;font-weight:600">Engineered Hardwood</td><td style="padding:13px 18px">25 years to lifetime (residential)</td></tr>
            <tr style="border-bottom:1px solid var(--gray-border);background:var(--gray-light)"><td style="padding:13px 18px;font-weight:600">Solid Hardwood</td><td style="padding:13px 18px">25 years to lifetime (residential)</td></tr>
            <tr style="border-bottom:1px solid var(--gray-border)"><td style="padding:13px 18px;font-weight:600">Premium SPC / LVP</td><td style="padding:13px 18px">Lifetime residential (some commercial-grade)</td></tr>
            <tr style="border-bottom:1px solid var(--gray-border);background:var(--gray-light)"><td style="padding:13px 18px;font-weight:600">Mid-Range Vinyl Plank</td><td style="padding:13px 18px">20-25 years residential</td></tr>
            <tr style="border-bottom:1px solid var(--gray-border)"><td style="padding:13px 18px;font-weight:600">Porcelain Tile</td><td style="padding:13px 18px">Lifetime (typically)</td></tr>
            <tr style="border-bottom:1px solid var(--gray-border);background:var(--gray-light)"><td style="padding:13px 18px;font-weight:600">Laminate (AC4-AC5)</td><td style="padding:13px 18px">15-25 years residential</td></tr>
          </tbody>
        </table>
      </div>

      <p>We register every product warranty at the time of installation and email you the registration confirmation. Keep this paperwork — you'll need it if you ever file a manufacturer claim.</p>

      <h2 style="margin:2.5rem 0 1.4rem">What Voids Manufacturer Warranties</h2>
      <p>Most manufacturer warranties are voided by:</p>
      <ul style="margin:0 0 1.5rem 1.5rem">
        <li style="margin-bottom:.5rem">Cleaning with non-approved products (vinegar, ammonia, bleach, steam mops)</li>
        <li style="margin-bottom:.5rem">Indoor humidity outside the recommended 35-55% range</li>
        <li style="margin-bottom:.5rem">Standing water or flooding events</li>
        <li style="margin-bottom:.5rem">Damage from pets, furniture, or sharp objects</li>
        <li style="margin-bottom:.5rem">Subfloor moisture exceeding manufacturer limits</li>
        <li>Failure to follow manufacturer maintenance schedules</li>
      </ul>

      <p>We provide written care instructions at handover for every install, including approved cleaning products and maintenance schedules. Keeping the manufacturer warranty valid is mostly about following these straightforward guidelines.</p>

      <div class="stat-badge">
        <span class="stat-badge-icon">🛡️</span>
        <div>
          <p>Triangle Flooring Stands Behind Every Install</p>
          <p>1-year labor warranty in writing · Manufacturer registration handled · Same-day claim response</p>
        </div>
      </div>

      <h2 style="margin:2.5rem 0 1.4rem">How to Make a Warranty Claim</h2>
      <p><strong>Step 1:</strong> Call us at <a href='tel:+19414026861' style="color:var(--cerulean);font-weight:600">(941) 402-6861</a> or fill out our <a href='/contact/' style="color:var(--cerulean);font-weight:600">contact form</a> describing the issue. Photos and a brief description help us prepare for the visit.</p>
      <p><strong>Step 2:</strong> We schedule a site visit, typically within 5-7 business days. The visit is free.</p>
      <p><strong>Step 3:</strong> We assess whether the issue is a labor matter (we fix it free) or a product manufacturing defect (we coordinate with the manufacturer). Most labor issues we can repair on the same visit.</p>
      <p><strong>Step 4:</strong> If a manufacturer claim is required, we handle the documentation and coordinate with their warranty department. You don't have to navigate manufacturer customer service yourself.</p>

      <p>Most legitimate warranty issues are resolved within 2-3 weeks total from initial call to completed repair.</p>
    </div>
  </div>
</section>

<section class="faq-section">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Common Questions</span><h2>Warranty FAQ</h2></div>
    {faq_html}
  </div>
</section>

{final_cta()}
{footer()}
{whatsapp_float()}

<script type="application/ld+json">{json.dumps(bc_schema)}</script>
<script type="application/ld+json">{json.dumps(faq_schema)}</script>

{menu_script()}
</body>
</html>"""

    out = f"{OUT_DIR}/warranty/index.html"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f: f.write(content)
    print(f"  ✓ /warranty/ ({len(content)//1024}KB)")


# Run all
print("\n→ Building support pages:")
build_faq()
build_financing()
build_warranty()
print("\n✓ Support pages complete")
