#!/usr/bin/env python3
"""Generate /[city]/index.html — city hub pages for all 8 cities.
Each city hub showcases all 6 services available in that city."""
import sys, json, os
sys.path.insert(0, '/home/claude/triangle')
from _gen import *
from _build_services import CITIES, SERVICES, render_neighborhoods_section, render_stat_badge

def build_city_hub(city_slug, city):
    PATH = f"/{city_slug}/"
    TITLE = f"Flooring Contractor in {city['name']}, FL | Triangle Flooring"
    if len(TITLE) > 65:
        TITLE = f"Flooring in {city['name']}, FL | Triangle Flooring"
    DESC = f"Flooring contractor in {city['name']}, FL. Hardwood, vinyl plank, tile, laminate, stair treads & repair. Serving {len(city['neighborhoods'])}+ neighborhoods. Free 24h estimate."
    if len(DESC) > 158: DESC = DESC[:155] + "..."

    bc_items = [("Home","/"),(city['name'], None)]
    bc_schema = render_breadcrumb_schema(bc_items)

    business_schema = render_local_business_schema(
        f"Flooring Contractor in {city['name']}",
        f"Professional flooring installation and repair in {city['name']}, FL — serving {city['county']}.",
        PATH, city=city['name']
    )

    # Build service cards (6 services with photos)
    service_cards_html = ""
    for s_slug, s in SERVICES.items():
        service_cards_html += f"""<a href="/{s_slug}/{city_slug}/" class="service-card">
        <div class="service-photo"><img src="/images/{s['card_image']}" alt="{s['name'].replace('&amp;','and')} in {city['name']} FL by Triangle Flooring" width="800" height="500" loading="lazy"></div>
        <div class="service-body">
          <h3>{s['name']} in {city['name']}</h3>
          <p>{s['intro_lead']}</p>
          <span class="service-link">Explore {s['short'].lower()}
            <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 12h14M13 5l7 7-7 7"/></svg>
          </span>
        </div>
      </a>"""

    # City-specific FAQs
    city_faqs = [
        (f"Do you really cover all of {city['name']}?",
         f"<p>Yes — we serve all of {city['name']} and surrounding {city['county']}, including {', '.join(city['neighborhoods'][:5])} and {len(city['neighborhoods'])-5}+ other neighborhoods. We provide free in-home estimates anywhere in our service area, typically within 24 hours of your call.</p>"),
        (f"What is the most popular flooring choice in {city['name']}?",
         f"<p>It varies by neighborhood and home type. In waterfront and beach areas, <strong>luxury vinyl plank (LVP/SPC)</strong> dominates because of moisture resistance. In newer inland communities, <strong>engineered hardwood</strong> (especially wide-plank European white oak) is the preferred premium choice. <strong>Large-format porcelain tile</strong> is increasingly popular in kitchens, baths, and entryways across {city['name']}. We can recommend the right material for your specific home during a free consultation.</p>"),
        (f"How quickly can you start a flooring project in {city['name']}?",
         f"<p>For most {city['name']} projects, we can begin work within 1-2 weeks of contract signing. Smaller projects (single rooms, repairs, stair treads) can often start within days. Larger custom projects (herringbone hardwood, full-home installations) may require 2-4 weeks of lead time for material acclimation and crew scheduling.</p>"),
        (f"Are you licensed and insured to work in {city['name']}?",
         f"<p>Yes. Triangle Flooring carries full general liability and worker's compensation insurance — certificates available on request before any project begins. Florida does not require state licensing for flooring installers (as it does for general contractors), but we comply with all county and city-level requirements in {city['county']}.</p>"),
        (f"Do you offer warranties on flooring work in {city['name']}?",
         f"<p>Every installation in {city['name']} comes with our written <strong>1-year labor warranty</strong>, in addition to the product manufacturer's warranty (typically 15 years to lifetime). If anything fails because of installation within 12 months — plank lifting, tile cracking at grout, stair tread squeaking — we come back and fix it. No fine print.</p>"),
        (f"Can I see examples of your {city['name']} work?",
         f"<p>Absolutely. We have a portfolio of completed {city['name']} projects available — from small bathroom tile installations to full-home herringbone hardwood. During your in-home consultation, we can show you photos of recent work in your specific neighborhood and even schedule a visit to a recently completed install if a client agrees. Just <a href='/contact/'>request your free quote</a> and ask to see local examples.</p>"),
    ]
    faq_html, faq_schema = render_faq(city_faqs)

    content = f"""{page_head(TITLE, DESC, PATH)}
{header()}
{breadcrumbs(bc_items)}

<section class="page-hero">
  <div class="container">
    <span class="eyebrow">📍 {city['county']}</span>
    <h1>Flooring Contractor in <span>{city['name']}, FL</span></h1>
    <p>Hardwood, vinyl plank, tile, laminate, stair treads, and repair — installed by a local crew you can call directly. Free estimate within 24 hours.</p>
    <div class="page-hero-trust">
      <span>{len(city['neighborhoods'])}+ neighborhoods served</span>
      <span>300+ projects</span>
      <span>5★ Google rated</span>
      <span>1-year warranty</span>
    </div>
  </div>
</section>

<section class="intro">
  <div class="container">
    <div class="intro-content">
      <p>{city['context']}</p>

      <p>Triangle Flooring has installed flooring in {len(city['neighborhoods'])}+ neighborhoods across {city['name']}, including <strong>{', '.join(city['neighborhoods'][:6])}</strong>, and many others. From small repair jobs to full-home reflooring projects, we bring the same crew, the same standards, and the same 42-Point Standard to every install — whether you're in a 1950s historic home or a brand-new luxury build.</p>

      <p>Local landmarks we work near regularly include <strong>{city['landmarks']}</strong>. Our team is based in Palmetto, FL, and we typically respond to {city['name']} estimate requests within 24 hours.</p>

      {render_stat_badge()}
    </div>
  </div>
</section>

<section class="services" id="services">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">All Flooring Services</span>
      <h2>What We Install in {city['name']}</h2>
      <p>Six core services, all delivered by the same in-house crew. Click any service for {city['name']}-specific details.</p>
    </div>
    <div class="services-grid">
      {service_cards_html}
    </div>
  </div>
</section>

{render_neighborhoods_section(city, "Flooring Services")}

<section class="intro" style="background:#fff">
  <div class="container">
    <div class="intro-content">
      <h2 style="margin-bottom:1.4rem">Flooring Recommendations by {city['name']} Property Type</h2>
      <p>Different {city['name']} homes have different flooring needs. Here's how we typically advise local clients based on the type of property they own:</p>

      <h3 style="margin:1.8rem 0 .8rem;font-size:1.2rem;color:var(--text)">For waterfront and beachfront homes</h3>
      <p>If you own a property near the water in {city['name']}, salt-air exposure and elevated humidity make moisture management critical. We typically recommend <strong>large-format porcelain tile</strong> in entryways, bathrooms, and kitchens; <strong>premium SPC vinyl plank</strong> in living areas; and we generally avoid solid hardwood unless the home has excellent climate control. Storm surge potential is also a factor — waterproof flooring can survive flooding events that would total any wood-based floor.</p>

      <h3 style="margin:1.8rem 0 .8rem;font-size:1.2rem;color:var(--text)">For new construction homes</h3>
      <p>{city['name']} new builds give you the best opportunity to install premium flooring properly. The slab is fresh, doors haven't been installed yet (so you can pick any height), and we can spec the subfloor for optimal performance. For new construction, our most common recommendation is <strong>wide-plank engineered hardwood</strong> in main living areas, <strong>premium SPC</strong> in kitchens and bedrooms, and <strong>large-format porcelain tile</strong> in bathrooms and laundry rooms. This configuration optimizes both daily livability and long-term resale.</p>

      <h3 style="margin:1.8rem 0 .8rem;font-size:1.2rem;color:var(--text)">For renovation projects (existing homes)</h3>
      <p>Older {city['name']} homes (pre-2000) often have subfloor conditions that need attention before new flooring goes down — moisture migration through the slab, uneven concrete, soft spots in plywood subfloors. We always test and document subfloor conditions before installation. For renovations, we typically lean toward <strong>premium SPC vinyl plank</strong> because it's more forgiving of minor subfloor imperfections and dramatically less expensive than hardwood while still looking high-end.</p>

      <h3 style="margin:1.8rem 0 .8rem;font-size:1.2rem;color:var(--text)">For investment properties and rentals</h3>
      <p>If you own rental property in {city['name']} (long-term or vacation rental), prioritize durability and ease of repair over premium aesthetics. <strong>Premium SPC with 22-mil+ wear layer</strong> handles tenant turnover, pet damage, and turnover cleaning crews better than any other flooring choice. Single-plank repairs are simple, the floor photographs well in listings, and the per-year cost over 15-20 years is excellent. Hardwood's resale advantage doesn't apply to rental property — go for durability.</p>

      <h3 style="margin:1.8rem 0 .8rem;font-size:1.2rem;color:var(--text)">For older homes with character</h3>
      <p>If you own a 1950s-1980s {city['name']} home with original features worth preserving, we lean toward materials that complement the era. Refinishing existing solid hardwood (where viable) often makes more sense than replacement — preserving the original wood character that you can't replicate with new floors. For rooms where original flooring isn't salvageable, we match new engineered hardwood to the existing tone and grain pattern as closely as possible.</p>
    </div>
  </div>
</section>

<section class="intro" style="background:var(--gray-light)">
  <div class="container">
    <div class="intro-content">
      <h2 style="margin-bottom:1.4rem">{city['name']} Climate Considerations for Flooring</h2>
      <p>{city['county']} is part of Florida's subtropical climate zone, which creates unique conditions every flooring contractor working here needs to plan for:</p>

      <p><strong>Outdoor humidity averages 70-85% annually</strong>, peaking above 90% on summer afternoons and dipping to 55-65% during dry winter weeks. <strong>Indoor humidity in air-conditioned homes</strong> typically runs 45-55%. That 20-30 point swing between outdoor and indoor humidity creates dimensional movement in any wood-based flooring, which is why proper acclimation (48-72 hours minimum on-site before installation) is non-negotiable. Generic national install protocols don't account for this; our 42-Point Standard does.</p>

      <p><strong>Hurricane season (June through November)</strong> brings additional considerations. Even homes far from the coast face wind-driven rain through compromised roofs, plumbing failures during power outages, and storm-related water events. We've completed 80+ post-hurricane reflooring projects across Manatee and Sarasota counties since Ian (2022) and Helene (2024), and the patterns are clear: porcelain tile and SPC vinyl plank survive flooding events that totally destroy hardwood and laminate. For {city['name']} homeowners weighing flooring options, this real-world data should factor into the decision.</p>

      <p><strong>Salt-air exposure</strong> in coastal {city['name']} neighborhoods accelerates wear on flooring finishes — especially gloss finishes on hardwood. Matte and satin finishes are more forgiving in salt-exposed environments. For homes within 1-2 miles of open Gulf water, we typically specify either porcelain tile or premium SPC for high-exposure areas.</p>

      <p><strong>Slab construction</strong> is standard for most {city['name']} homes built after 1980. Concrete slabs in Florida have moisture migration risk that wood subfloors don't — moisture vapor moves up through the slab from the soil, especially in homes built without modern vapor barriers. We always perform subfloor moisture testing (calcium chloride or pin-style hygrometer) before any flooring install on slab construction. If readings exceed manufacturer limits for the chosen flooring, we install vapor barriers or recommend different products.</p>

      <p>These climate factors don't make flooring impossible in {city['name']} — they just require Florida-experienced contractors who plan for them. Triangle Flooring has been doing this for 5+ years across {city['county']}, and we'd be happy to walk you through the specifics for your particular home.</p>
    </div>
  </div>
</section>

<section class="intro" style="background:#fff">
  <div class="container">
    <div class="intro-content">
      <h2 style="margin-bottom:1.4rem">Why {city['name']} Homeowners Choose Triangle Flooring</h2>
      <p>The {city['name']} flooring market is crowded — big-box stores, national chains, handymen, and dozens of installation companies all compete for your business. Here's why locals consistently choose us:</p>

      <h3 style="margin:1.8rem 0 .8rem;font-size:1.2rem">1. Same crew from quote to walk-through</h3>
      <p>The installer who measures your {city['name']} home is the same installer who finishes the last baseboard. No subcontractor handoffs. No quality drop-off mid-project. Most contractors in this market sub out their work to the cheapest available crew — we don't, and the difference shows in every install.</p>

      <h3 style="margin:1.8rem 0 .8rem;font-size:1.2rem">2. Florida-specific installation standards</h3>
      <p>Generic national install protocols don't account for {city['county']}'s 70-85% summer humidity, salt-air exposure (in coastal neighborhoods), or the dimensional movement of materials between AC-cooled interiors and Florida summers. Our 42-Point Standard was built specifically for the conditions we work in here.</p>

      <h3 style="margin:1.8rem 0 .8rem;font-size:1.2rem">3. Transparent itemized pricing</h3>
      <p>Every {city['name']} quote we provide includes itemized line items: material cost, labor cost, removal/disposal, subfloor prep, transition strips, baseboards, waste percentage. No surprise upcharges mid-project. The number on your contract is the number on your final invoice.</p>

      <h3 style="margin:1.8rem 0 .8rem;font-size:1.2rem">4. Real local accountability</h3>
      <p>If anything goes wrong with your {city['name']} install — at the time of installation or in the year that follows — you call our owner directly, not a corporate hotline. That's the difference between a local owner-operated business and a faceless flooring chain. Most of our work in {city['name']} comes from referrals because of how we handle problems when (rarely) they come up.</p>

      <h3 style="margin:1.8rem 0 .8rem;font-size:1.2rem">5. Verified 5-star reputation</h3>
      <p>Six verified Google reviews, all 5 stars. Three hundred plus projects completed across Tampa Bay. Insured. Same-day response, 7 days a week. We're not the biggest flooring company in {city['name']} — but we're the most responsive, the most transparent, and (we believe) the most carefully run.</p>
    </div>
  </div>
</section>

<section class="faq-section">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Common Questions</span><h2>Flooring in {city['name']} — FAQ</h2></div>
    {faq_html}
  </div>
</section>

<section class="related">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Other Service Areas</span><h2>We Also Serve</h2></div>
    <div class="related-grid">
      {"".join(f'<a href="/{cs}/" class="related-card"><strong>📍 {cd["name"]} →</strong><span>{cd["county"]} · {len(cd["neighborhoods"])}+ neighborhoods</span></a>' for cs, cd in CITIES.items() if cs != city_slug)}
    </div>
  </div>
</section>

{final_cta()}
{footer()}
{whatsapp_float()}

<script type="application/ld+json">{json.dumps(bc_schema)}</script>
<script type="application/ld+json">{json.dumps(business_schema)}</script>
<script type="application/ld+json">{json.dumps(faq_schema)}</script>

{menu_script()}
</body>
</html>"""

    out = f"{OUT_DIR}/{city_slug}/index.html"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f: f.write(content)
    print(f"  ✓ /{city_slug}/index.html ({len(content)//1024}KB)")

print("\n→ Building city hub pages (8 cities):")
for cs, cd in CITIES.items():
    build_city_hub(cs, cd)

print("\n✓ City hubs complete")
