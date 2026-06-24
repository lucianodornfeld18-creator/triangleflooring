#!/usr/bin/env python3
"""Generate /financing/index.html — flooring financing & payment options page."""
import json
from _gen import *

PATH = "/financing/"
TITLE = "Flooring Financing in Bradenton & Tampa Bay | Triangle"
DESC = "Flexible flooring financing across Bradenton, Sarasota & Tampa Bay — low monthly payments, 0% intro options, and insurance-claim billing. Free 24-hr estimate."

bc_items = [("Home", "/"), ("Financing", None)]
bc_schema = render_breadcrumb_schema([(n, u) for n, u in bc_items])

faqs = [
  ("Do you offer financing for flooring installation?",
   "<p>Yes. Triangle Flooring works with third-party financing partners so you can spread the cost of your new floors over fixed monthly payments instead of paying everything up front. Plans range from short 6–12 month promotional terms to longer 24–60 month plans, depending on the lender and your approval. Ask us for current options when we send your written estimate.</p>"),
  ("Is there a 0% interest option?",
   "<p>Promotional 0% APR plans are frequently available through our lending partners on qualifying projects (typically with a same-as-cash window of 6–18 months). Terms change, so we'll tell you exactly what's available the week you book. If you pay the balance within the promotional window, you pay zero interest.</p>"),
  ("How much will my monthly payment be?",
   "<p>It depends on the project total, the term length, and your approved rate. As a rough guide, a $6,000 flooring project financed over 36 months lands near $185–$210/month on a standard plan, or $0 interest if paid within a promotional same-as-cash window. We'll show you real numbers — not a sales gimmick — before you commit.</p>"),
  ("Can you bill my homeowners insurance for storm or water damage?",
   "<p>Yes. After Hurricane Ian and Helene we completed 80+ insurance and post-storm reflooring jobs across Manatee and Sarasota counties. We can quote directly from your adjuster's scope or provide our own itemized estimate for your claim, photograph the damage progression, and stage the work so the most-needed rooms are livable first. This lets many homeowners reflooring after water damage pay little or nothing out of pocket beyond the deductible.</p>"),
  ("What do I need to apply for financing?",
   "<p>Applications take a few minutes and are handled through our lending partner — typically you'll need to be 18+, a U.S. resident, and provide basic ID and income information for a soft or hard credit check (varies by lender). Approval decisions are usually instant. We never see your full financial details; the lender handles that privately.</p>"),
  ("Is there a penalty for paying off early?",
   "<p>No. Our financing partners do not charge prepayment penalties — if you pay your balance off early (or within a 0% promotional window), you simply save on interest. You're never locked in.</p>"),
]
faq_html, faq_schema = render_faq(faqs)

page_schema = {
  "@context": "https://schema.org",
  "@type": "WebPage",
  "@id": f"https://{DOMAIN}/financing/#webpage",
  "url": f"https://{DOMAIN}/financing/",
  "name": "Flooring Financing & Payment Options",
  "description": DESC,
  "isPartOf": {"@id": f"https://{DOMAIN}/#website"},
  "about": {"@id": f"https://{DOMAIN}/#organization"},
  "breadcrumb": {"@id": f"https://{DOMAIN}/financing/#breadcrumb"},
}

content = f"""{page_head(TITLE, DESC, PATH)}
{header()}
{breadcrumbs(bc_items)}

<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Financing & Payment Options</span>
    <h1>Flooring Financing in <span>Bradenton &amp; Tampa Bay</span></h1>
    <p>New floors now, paid your way. Flexible monthly plans, promotional 0% options, and insurance-claim billing across Manatee, Sarasota, Hillsborough &amp; Pinellas counties.</p>
    <div class="page-hero-trust">
      <span>Low monthly payments</span>
      <span>0% intro options</span>
      <span>Insurance claims welcome</span>
      <span>No prepayment penalty</span>
    </div>
  </div>
</section>

<section class="intro">
  <div class="container">
    <div class="intro-content">
      <h2 style="margin-bottom:1.2rem">You Shouldn't Have to Wait on the Floor You Need</h2>
      <p>A quality floor is an investment in your home — and like any investment, you shouldn't have to drain your savings to make it. Triangle Flooring works with trusted third-party financing partners so you can install <strong>hardwood, luxury vinyl plank, tile, laminate, or stair treads</strong> today and pay over comfortable fixed monthly payments. Whether you're upgrading a forever home in Lakewood Ranch, reflooring a rental in Bradenton, or repairing water-damaged floors after a storm, there's a plan that fits.</p>

      <h2 style="margin:2.5rem 0 1.2rem">Three Ways to Pay for Your Floors</h2>
      <p><strong>1. Monthly payment plans.</strong> Spread your project across 12, 24, 36, or up to 60 months through our lending partners. Predictable payments, no surprises, and you keep your cash reserves intact for everything else life throws at a Florida homeowner.</p>
      <p><strong>2. Promotional 0% / same-as-cash.</strong> On qualifying projects, our partners frequently offer 6–18 month promotional windows where you pay <strong>zero interest</strong> if the balance is cleared in time. It's the cheapest money you'll ever borrow — we'll tell you exactly what's available the week you book.</p>
      <p><strong>3. Insurance-claim billing.</strong> If your floors were damaged by a hurricane, burst pipe, or appliance leak, we bill from your adjuster's scope (or provide our own itemized estimate). Many homeowners pay nothing beyond their deductible. We document the damage, register the claim scope, and stage the work room by room.</p>

      <div class="stat-badge">
        <span class="stat-badge-icon">💳</span>
        <div>
          <p>Estimated Monthly Payments (illustrative)</p>
          <p>$3,000 project ≈ $95–$110/mo · $6,000 ≈ $185–$210/mo · $10,000 ≈ $300–$345/mo (36-mo standard term) — or $0 interest within a promotional same-as-cash window. Final terms depend on lender approval.</p>
        </div>
      </div>

      <h2 style="margin:2.5rem 0 1.2rem">How the Process Works</h2>
      <p><strong>Step 1 — Free estimate.</strong> We measure your home and send an itemized written quote within 24 hours. <strong>Step 2 — Pick a plan.</strong> We share the current financing options and you choose what fits your budget. <strong>Step 3 — Quick application.</strong> Apply through our lending partner in minutes; most decisions are instant. <strong>Step 4 — Install.</strong> Once approved, we schedule your install — usually within days. <strong>Step 5 — Pay over time.</strong> You enjoy your new floors immediately and pay on your chosen monthly schedule, with no penalty for paying off early.</p>

      <h2 style="margin:2.5rem 0 1.2rem">Storm &amp; Water Damage? Let's Talk Insurance.</h2>
      <p>Florida's humidity, hurricanes, and flooding put more floors underwater than almost anywhere in the country. If you're filing a homeowners claim after Ian, Helene, a roof leak, or a plumbing failure, Triangle Flooring can work directly with your insurance documentation. We've completed <strong>80+ insurance and post-storm reflooring projects</strong> across Tampa Bay and know how to photograph damage progressions, match adjuster scopes, and prioritize the rooms you need livable first. <a href="/floor-repair/" style="color:var(--cerulean);font-weight:600">See our floor repair &amp; water-damage service →</a></p>

      <p style="margin-top:1.6rem"><em>Financing is provided by third-party lenders and is subject to credit approval. Rates, promotional windows, and monthly payment examples shown above are illustrative and not a guarantee of terms. Triangle Flooring does not make credit decisions and does not access your full financial information.</em></p>

      {whatsapp_banner()}
    </div>
  </div>
</section>

<section class="faq-section">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Common Questions</span>
      <h2>Flooring Financing FAQ</h2>
    </div>
    {faq_html}
  </div>
</section>

<section class="related">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Explore More</span><h2>Ready to Get Started?</h2></div>
    <div class="related-grid">
      <a href="/contact/" class="related-card"><strong>Get a Free Quote →</strong><span>In-home estimate within 24 hours</span></a>
      <a href="/floor-repair/" class="related-card"><strong>Storm &amp; Water Damage →</strong><span>Insurance-claim reflooring across Tampa Bay</span></a>
      <a href="/hardwood-flooring/" class="related-card"><strong>Browse Hardwood →</strong><span>Solid &amp; engineered hardwood for Florida homes</span></a>
      <a href="/vinyl-plank-flooring/" class="related-card"><strong>Browse Vinyl Plank →</strong><span>100% waterproof LVP &amp; SPC installation</span></a>
    </div>
  </div>
</section>

{final_cta()}
{footer()}
{whatsapp_float()}

<script type="application/ld+json">{json.dumps(bc_schema)}</script>
<script type="application/ld+json">{json.dumps(faq_schema)}</script>
<script type="application/ld+json">{json.dumps(page_schema)}</script>

{menu_script()}
</body>
</html>"""

import os
os.makedirs(f"{OUT_DIR}/financing", exist_ok=True)
with open(f"{OUT_DIR}/financing/index.html", "w", encoding="utf-8") as f:
    f.write(content)
print(f"✓ /financing/index.html ({len(content)//1024} KB)")
