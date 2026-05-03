#!/usr/bin/env python3
"""Generate all service pages (hubs + city pages) with rich, unique content."""
import sys, json, os
sys.path.insert(0, '/home/claude/triangle')
from _gen import *

# ============================================================================
# SHARED: 42-POINT CHECKLIST (used across all service pages)
# ============================================================================
CHECKLIST_42 = [
  ("Pre-Install Inspection", "🔍", [
    "Subfloor moisture reading recorded (target ≤4% wood, ≤3% concrete)",
    "Floor flatness verified (max 3/16″ deviation per 10ft)",
    "Existing baseboards photographed for reference",
    "Door clearance measured for new floor height",
    "HVAC humidity check (target 35–55% RH)",
    "Material acclimation logged (48–72 hr minimum)",
    "Underlayment compatibility verified",
    "Customer walk-through &amp; final scope signed",
  ]),
  ("Demolition &amp; Prep", "🔨", [
    "Old flooring removed without damaging subfloor",
    "Staples and adhesive residue ground/scraped flush",
    "Debris hauled away same-day",
    "Subfloor screwed where needed (squeak elimination)",
    "Loose nails counter-sunk or removed",
    "Self-leveling compound applied where needed",
    "Vapor barrier installed on concrete (when required)",
    "Rooms protected with plastic sheeting / dust containment",
  ]),
  ("Installation Standards", "📐", [
    "Expansion gaps verified at all walls (3/8″ minimum)",
    "First row laser-aligned to longest sight line",
    "End joints staggered minimum 6–12 inches",
    "Glue/adhesive coverage 100% (no voids)",
    "Nail/staple spacing per manufacturer spec",
    "Plank end-cuts sealed against moisture",
    "Transition strips fitted at all doorways",
    "T-molding installed at >40ft continuous runs",
    "Reducer strips at flooring height changes",
    "Threshold transitions level to ±1mm",
  ]),
  ("Finish Detail Work", "✨", [
    "Quarter-round / shoe molding nailed flush",
    "Caulk lines applied at baseboard top",
    "Touch-up paint on existing baseboards",
    "Plug holes filled (nail-down hardwood only)",
    "Floor surface dust-vacuumed twice",
    "Damp mop with manufacturer-approved cleaner",
    "Furniture protectors installed (when retained)",
    "HVAC vents cleaned and reinstalled",
  ]),
  ("Final Walk-Through", "✅", [
    "Customer walk-through with installer (every room)",
    "Plank/tile alignment reviewed at all transitions",
    "All cuts and fills inspected at close range",
    "Maintenance instructions handed over (printed)",
    "Manufacturer warranty card filled out and emailed",
    "1-year Triangle Flooring labor warranty signed",
    "Leftover material left for future repairs (boxed)",
    "Final invoice and receipt emailed within 24 hrs",
  ]),
]

def render_checklist():
    """Render the 42-point checklist as cards."""
    cards = []
    total_pts = 0
    for cat, icon, items in CHECKLIST_42:
        total_pts += len(items)
        items_html = "".join(f"<li>{i}</li>" for i in items)
        cards.append(f"""<div class="checklist-card">
          <div class="checklist-card-head"><strong>{icon} {cat}</strong><span>{len(items)} points</span></div>
          <ol>{items_html}</ol>
        </div>""")
    return f'<div class="checklist-grid">{"".join(cards)}</div>', total_pts

# ============================================================================
# CITY DATA — real neighborhoods, ZIPs, market context
# ============================================================================
CITIES = {
  "bradenton": {
    "name": "Bradenton",
    "county": "Manatee County",
    "zips": ["34201","34202","34203","34204","34205","34206","34207","34208","34209","34210","34211","34212"],
    "neighborhoods": ["West Bradenton","River Strand","Lakewood Ranch (Bradenton side)","Heritage Harbour","Greyhawk Landing","Tara","Country Club East","Riverdale","Mill Creek","Stoneybrook","Esplanade","Rosedale","Braden Woods","Cortez","Palma Sola","Anna Maria Island","Holmes Beach","Bradenton Beach"],
    "context": "<strong>Bradenton</strong> is the seat of Manatee County, with a population of roughly 60,000 in the city and 420,000+ in the metro area. The area has seen significant growth from northern transplants relocating to Florida, driving high demand for full-home reflooring projects — particularly luxury vinyl plank in beachfront condos and engineered hardwood in inland new builds. Coastal humidity averages 70-80% year-round, making moisture-resistant flooring (LVP, porcelain tile, properly acclimated engineered hardwood) the smartest choice for most homes here.",
    "landmarks": "LECOM Park, IMG Academy, Riverwalk, Anna Maria Island bridges, Robinson Preserve",
  },
  "sarasota": {
    "name": "Sarasota",
    "county": "Sarasota County",
    "zips": ["34230","34231","34232","34233","34234","34235","34236","34237","34238","34239","34240","34241","34242","34243"],
    "neighborhoods": ["Downtown Sarasota","St. Armands Key","Lido Key","Siesta Key","Longboat Key","Bird Key","Golden Gate Point","The Meadows","Palmer Ranch","Gulf Gate","Oakford","Laurel Park","Southside Village","Cherokee Park","Indian Beach","Sapphire Shores","University Park","Lakewood Ranch (Sarasota side)","Hidden Lake"],
    "context": "<strong>Sarasota</strong> is one of Florida's most affluent coastal cities, home to roughly 58,000 residents within city limits and over 450,000 in the metro. The market is dominated by waterfront condos on Siesta Key and Lido Key, mid-century homes in West of Trail neighborhoods, and luxury new construction east of I-75. Sarasota homeowners favor wide-plank European White Oak hardwood, large-format porcelain tile (24×48 and up), and high-end LVP for rental properties. Properties on the keys require especially careful subfloor moisture management due to salt air and elevated humidity.",
    "landmarks": "Siesta Key Beach (#1 ranked beach in US), Ringling Museum, St. Armands Circle, Sarasota Opera House, Marie Selby Botanical Gardens",
  },
  "lakewood-ranch": {
    "name": "Lakewood Ranch",
    "county": "Manatee/Sarasota Counties",
    "zips": ["34202","34211","34240","34238"],
    "neighborhoods": ["Country Club East","Lakewood Ranch Country Club","Esplanade","The Lake Club","Greenbrook","Summerfield","Edgewater","Mallory Park","Indigo","Lorraine Lakes","Polo Run","Del Webb","Cresswind","Star Farms","Sweetwater","Waterside","Azario","Avanti","Solera","Savanna"],
    "context": "<strong>Lakewood Ranch</strong> has been ranked the #1 best-selling multigenerational master-planned community in the US for eight consecutive years, with a population of 60,000+ across more than 31 villages. The community spans both Manatee and Sarasota counties and continues to grow rapidly with new developments like Star Farms, Sweetwater, and Waterside Place. Lakewood Ranch homeowners typically select premium materials: 7-9 inch wide-plank engineered hardwood, custom herringbone patterns, and large-format porcelain tile. Many homes feature covered lanais and second-floor bonus rooms, requiring precise stair tread work and continuous flooring transitions.",
    "landmarks": "Main Street at Lakewood Ranch, Waterside Place, Lakewood Ranch Medical Center, The Premier Sports Campus, UTC (University Town Center)",
  },
}

# ============================================================================
# SERVICE DATA
# ============================================================================
SERVICES = {
  "hardwood-flooring": {
    "name": "Hardwood Flooring",
    "short": "Hardwood",
    "h1_phrase": "Hardwood Flooring",
    "intro_lead": "Solid and engineered hardwood — installed by hand, acclimated for Florida humidity, and built to outlast the next decade of Gulf Coast living.",
    "card_image": "card-hardwood.webp",
    "hero_image": "hero-bg.jpg",
    "intro_long": """Hardwood flooring is the most timeless, value-adding floor you can install in a Florida home — but only when it's installed correctly. <strong>The single biggest mistake we see in Tampa Bay hardwood jobs is rushed acclimation.</strong> Florida's humidity sits between 70–85% most months, while air-conditioned home interiors run closer to 45–55%. If a hardwood plank moves from a humid warehouse straight to your living room without acclimating to your home's actual climate, it will expand, contract, and gap within months.

Triangle Flooring acclimates every hardwood shipment for 48–72 hours on-site, monitored with a digital hygrometer. We also moisture-test the subfloor (≤12% for wood subfloors, ≤3% calcium chloride reading for concrete slabs) before a single nail goes in. This isn't extra work — it's the only way to give you a hardwood floor that still looks tight in year ten.

We install both <strong>solid hardwood</strong> (3/4″ thick, sandable up to 8 times, ideal for second-floor and above-grade installs) and <strong>engineered hardwood</strong> (multi-ply construction, more dimensionally stable, our preferred choice for Florida slab homes and ground-floor installs). Species we work with regularly include White Oak, Red Oak, Brazilian Cherry, Maple, Hickory, Walnut, and Acacia.""",
    "scope_items": ["Solid hardwood installation (3/4″ tongue-and-groove)","Engineered hardwood installation (5–9 inch widths)","Wide-plank European White Oak (7-9″)","Custom herringbone &amp; chevron patterns","Nail-down installation (plywood subfloor)","Glue-down installation (concrete slab)","Floating engineered installation","Threshold &amp; transition strip work","Quarter-round &amp; shoe molding","Flush-mount baseboard refits","Staircase nosing &amp; tread integration","Subfloor moisture testing &amp; logging","Subfloor leveling (self-level pour or shim)","Vapor barrier on concrete subfloors"],
    "pricing_rows": [
      ("Engineered Hardwood (5″ wide)", "$8.50–$11/sq ft", "Glue-down or nail-down install"),
      ("Engineered Hardwood (7–9″ wide)", "$10–$14/sq ft", "Most popular for Lakewood Ranch homes"),
      ("Solid Hardwood (3/4″, 3-5″ width)", "$9–$13/sq ft", "Nail-down on plywood subfloor"),
      ("Premium Wide-Plank European Oak", "$13–$18/sq ft", "7-10″ wide, character-grade"),
      ("Custom Herringbone Pattern", "$15–$22/sq ft", "Labor-intensive, premium look"),
      ("Custom Chevron Pattern", "$17–$24/sq ft", "Most premium hardwood install"),
      ("Subfloor Prep (per room)", "$200–$600", "If self-leveling required"),
      ("Old Flooring Removal", "$1.50–$3/sq ft", "Carpet/laminate/tile demo"),
    ],
    "faqs": [
      ("Can I install solid hardwood in a Florida slab home?", "Solid hardwood is not recommended for direct installation on concrete slabs in Florida. The combination of slab moisture and coastal humidity makes solid hardwood prone to cupping and gapping. We strongly recommend <strong>engineered hardwood</strong> for slab installs — it has a multi-ply core that's far more dimensionally stable. If you really want solid hardwood on a slab, we'd need to install plywood underlayment first (raises floor height ~3/4″)."),
      ("How long does hardwood acclimate before installation?", "We require a minimum of 48–72 hours of on-site acclimation before installation begins. The hardwood is delivered to your home, the boxes are opened (so air circulates around each plank), and we monitor with a digital hygrometer until the wood's moisture content matches your home's interior climate. This is the single most important step in preventing future buckling and gapping."),
      ("What's the difference between engineered and solid hardwood?", "Solid hardwood is one piece of wood, 3/4″ thick, that can be sanded and refinished up to 8 times over its lifetime. Engineered hardwood has a top veneer of real hardwood (typically 2-6mm) bonded to a multi-ply substrate, making it more dimensionally stable in humid climates. Quality engineered hardwood can be sanded 1–3 times. For Florida homes, <strong>we recommend engineered hardwood 90% of the time</strong> — better moisture performance for the same look."),
      ("How long does a hardwood installation take?", "A typical 1,200–1,800 sqft hardwood install takes 3–5 working days: Day 1 demolition + subfloor prep, Days 2–3 acclimation + initial install, Day 4 finishing rooms + transitions, Day 5 quarter-round + final touches. Larger or more complex projects (herringbone patterns, multiple staircases) can take 5–10 days."),
    ],
  },
  "vinyl-plank-flooring": {
    "name": "Luxury Vinyl Plank (LVP) Flooring",
    "short": "Vinyl Plank",
    "h1_phrase": "Vinyl Plank Flooring",
    "intro_lead": "100% waterproof luxury vinyl plank — the smartest flooring investment for Florida kitchens, baths, beach condos, and short-term rentals.",
    "card_image": "card-vinyl.webp",
    "hero_image": "hero-bg.jpg",
    "intro_long": """Luxury vinyl plank (LVP) and stone-plastic composite (SPC) flooring are the fastest-growing flooring categories in Tampa Bay — and for good reason. They're <strong>100% waterproof</strong>, scratch-resistant enough for pets and rental properties, dimensionally stable in Florida humidity, and they look remarkably close to real hardwood at a fraction of the cost.

Triangle Flooring installs both <strong>click-lock floating LVP</strong> (no glue, faster install, easy to replace single planks) and <strong>glue-down LVP</strong> (more permanent, no flex, ideal for high-traffic areas and large open-plan spaces over 800 sqft). For most Florida homes, click-lock SPC at 6.5mm or thicker with a 22-mil wear layer is the sweet spot for residential use.

We're particularly skilled at LVP installations in <strong>short-term rental properties</strong> across Anna Maria Island, Siesta Key, and Lido Key — where waterproof, easy-to-clean flooring that looks great in listing photos drives nightly rates. We've completed 100+ STR reflooring projects in the last three years, and we know how to coordinate around peak booking seasons to minimize lost revenue.""",
    "scope_items": ["Click-lock LVP installation (floating)","Glue-down LVP installation","SPC (Stone Plastic Composite) plank installation","WPC (Wood Plastic Composite) plank installation","Underlayment installation (when needed)","Subfloor moisture testing","Concrete slab leveling","Old flooring removal &amp; haul-away","Transition strip installation","Flush-mount transitions to tile/carpet","Stair nosing &amp; LVP stair treads","Quarter-round &amp; shoe molding","Toilet pull &amp; reset","Appliance moves (washer/dryer/fridge)"],
    "pricing_rows": [
      ("Standard LVP (4mm, 12-mil wear)", "$3.50–$5/sq ft", "Builder-grade, rental-friendly"),
      ("Mid-Range LVP/SPC (6mm, 20-mil)", "$4.50–$7/sq ft", "Most popular for residential"),
      ("Premium SPC (8mm, 22+mil wear)", "$6–$9/sq ft", "Pet-proof, lifetime residential warranty"),
      ("Luxury Wide-Plank LVP (9″+)", "$7–$11/sq ft", "Premium look, hardwood-mimicking"),
      ("Glue-Down LVP (commercial)", "$5–$8/sq ft", "STRs, AirBnBs, high-traffic"),
      ("LVP Stair Treads", "$45–$85/tread", "Custom-cut bullnose"),
      ("Subfloor Self-Leveling", "$200–$700", "Per room, if needed"),
      ("Old Flooring Removal", "$1.50–$3/sq ft", "Includes haul-away"),
    ],
    "faqs": [
      ("Is LVP really 100% waterproof?", "Quality SPC and rigid-core LVP are <strong>100% waterproof on the surface</strong> — meaning standing water won't damage the plank itself. However, water can still seep <em>through</em> the seams of click-lock LVP if it sits there long enough, so we always recommend wiping spills promptly. For bathrooms and rental properties, we often suggest glue-down installation, which seals the seams completely."),
      ("How long does LVP last in Florida?", "Quality residential LVP/SPC has a 20–30 year manufacturer warranty when properly installed. In Florida's humidity, the failure mode is rarely the LVP itself — it's almost always inadequate subfloor prep (uneven slab, untested moisture, or cheap underlayment). When we install LVP with proper moisture testing and a flat subfloor, we expect it to last the full warranty period."),
      ("Can LVP be installed over existing tile?", "In some cases, yes — if the tile is well-bonded, level, and the floor height increase is acceptable for door clearance. We assess each situation: small grout lines (1/8″ or less) usually don't telegraph through quality SPC; larger grout lines may need to be filled with self-leveling compound first. Removing the tile is often cleaner and gives a better long-term result, but it's significantly more expensive."),
      ("Is LVP good for short-term rentals?", "LVP is the #1 choice for STRs across Tampa Bay. It handles spills, sand, suitcases, and turnover cleaning without scratching or staining. For rentals, we recommend a 22-mil wear layer minimum (commercial-grade), in lighter colors that don't show pet hair or sand. We can typically install 1,200 sqft in 2-3 days, perfect for the gap between bookings."),
    ],
  },
  "tile-installation": {
    "name": "Tile Installation",
    "short": "Tile",
    "h1_phrase": "Tile Installation",
    "intro_lead": "Porcelain, ceramic, and large-format tile — installed with Schluter-certified waterproofing systems for showers, kitchens, and floors that last decades.",
    "card_image": "card-tile.webp",
    "hero_image": "hero-bg.jpg",
    "intro_long": """Tile is the most demanding flooring installation we do — and the one where shortcuts show up fastest. A poorly installed tile floor will crack at the grout lines within a year. A poorly installed shower will leak behind the wall. We take tile work seriously because we've been called to fix too many botched jobs from other contractors.

Triangle Flooring installs <strong>large-format porcelain</strong> (24×48, 32×32, 48×48), traditional ceramic, mosaic, marble-look porcelain, and natural stone. For wet areas, we use <strong>Schluter-Kerdi</strong> waterproofing membranes — the only system we trust for Florida shower installations where humidity and salt air make moisture management critical.

We're also one of the few crews in Tampa Bay willing to take on <strong>curbless shower</strong> installations, which require precise slope, drain placement, and waterproofing detail. These are the high-end shower installs you see in luxury Lakewood Ranch and Sarasota waterfront builds — and they have to be done right the first time.""",
    "scope_items": ["Porcelain tile installation (any size)","Large-format tile (24×48, 32×32, 48×48)","Natural stone installation (marble, travertine)","Mosaic &amp; decorative tile work","Curbless shower construction","Schluter-Kerdi waterproofing systems","Pre-formed shower pan installation","Linear drain installation","Custom shower niches","Bullnose &amp; edge trim","Schluter Strip transitions (Reno, Jolly, Quadec)","Backsplash installation","Tile floor demolition","Subfloor preparation &amp; leveling"],
    "pricing_rows": [
      ("Standard Ceramic Tile", "$8–$12/sq ft", "12×12, 12×24, basic install"),
      ("Porcelain Tile (12×24, 24×24)", "$10–$15/sq ft", "Most common residential size"),
      ("Large-Format Porcelain (24×48+)", "$13–$20/sq ft", "Requires perfectly flat substrate"),
      ("Natural Stone (marble, travertine)", "$15–$25/sq ft", "Includes sealing"),
      ("Mosaic / Decorative Tile", "$18–$30/sq ft", "Labor-intensive layout"),
      ("Curbless Shower (waterproofing only)", "$1,800–$3,200", "Schluter-Kerdi + pan"),
      ("Tile Backsplash", "$15–$28/sq ft", "Kitchen or bathroom"),
      ("Tile Removal", "$2.50–$5/sq ft", "Includes thinset removal"),
    ],
    "faqs": [
      ("Why is large-format tile more expensive to install?", "Large-format tiles (24×48 and bigger) require an extremely flat substrate — within 1/8″ of variation per 10 feet, which is much tighter than smaller tile. This often means self-leveling compound on the entire floor before tile goes down. The tiles themselves are also heavier (some 24×48 porcelains weigh 30+ lbs each), require two installers to lift, and use specialized large-format mortars and leveling clip systems to prevent lippage."),
      ("Is grout color permanent?", "Standard cementitious grout absorbs water and can stain over time. We strongly recommend <strong>epoxy grout</strong> for showers and kitchens (color-stable, stain-proof, no sealing needed), or sealed cementitious grout with annual resealing. Color choice is personal — but we always advise clients away from pure white grout in high-traffic areas because it shows dirt within months."),
      ("How long does a tile shower take to install?", "A standard tile shower (60×36 with one accent wall and a niche) takes 4-6 days when done correctly: Day 1 demo, Day 2 framing &amp; backer board, Day 3 Schluter-Kerdi waterproofing &amp; flood test, Day 4-5 tile install, Day 6 grout &amp; silicone. We never rush waterproofing — a missed step here means leaks behind the wall later."),
      ("Can you match existing tile if I just want a repair?", "We can match existing tile if it's a current product line still in production. We'll need a sample (or a few extra tiles you saved from the original install). For discontinued tiles, we can usually find very close matches at boutique tile suppliers in Sarasota and Tampa, but exact color matches are rare. We'll always show you samples before committing."),
    ],
  },
  "laminate-flooring": {
    "name": "Laminate Flooring",
    "short": "Laminate",
    "h1_phrase": "Laminate Flooring",
    "intro_lead": "Affordable, scratch-resistant laminate that mimics real hardwood — perfect for rental properties, bedrooms, and budget-conscious renovations.",
    "card_image": "card-laminate.webp",
    "hero_image": "hero-bg.jpg",
    "intro_long": """Laminate flooring is the budget-friendly alternative to hardwood — a high-density fiberboard core topped with a photographic decorative layer and a clear wear layer. Modern laminate (AC4 or AC5 rated) is highly scratch-resistant and can convincingly imitate hardwood, stone, and even tile.

For Florida homes, laminate has one significant limitation: <strong>it's not waterproof</strong>. Standing water can cause the HDF core to swell, creating permanent damage. We don't recommend laminate for kitchens, bathrooms, or laundry rooms in Florida — for those rooms, we suggest LVP or porcelain tile instead. But for bedrooms, living rooms, hallways, and rental properties, quality laminate installed correctly can deliver a hardwood look at 40-60% less cost.

Triangle Flooring installs name-brand laminate from Pergo, Mohawk, Shaw, and Mannington. We also install <strong>water-resistant laminate</strong> (a newer category that handles spills better than traditional laminate, though still not fully waterproof like LVP).""",
    "scope_items": ["Click-lock laminate installation (floating)","Underlayment installation","Vapor barrier on concrete subfloors","Subfloor moisture testing","Old flooring demolition","Transition strip installation","T-molding for long runs","Reducer strips at height transitions","Quarter-round &amp; shoe molding","Threshold transitions","Pet-friendly water-resistant laminate","Furniture removal &amp; reset","Laminate stair treads","Subfloor leveling (when needed)"],
    "pricing_rows": [
      ("Builder-Grade Laminate (AC3, 7mm)", "$2.50–$4/sq ft", "Bedroom/closet rentals"),
      ("Mid-Range Laminate (AC4, 8-10mm)", "$3.50–$5.50/sq ft", "Most common residential"),
      ("Premium Laminate (AC5, 12mm)", "$5–$7/sq ft", "Commercial-grade scratch resistance"),
      ("Water-Resistant Laminate", "$5.50–$8/sq ft", "Newer technology, splash-tolerant"),
      ("Underlayment (foam)", "$0.50–$1/sq ft", "Standard, included in most installs"),
      ("Underlayment (premium with vapor barrier)", "$1–$1.75/sq ft", "Required on slab"),
      ("Subfloor Prep", "$150–$500", "Per room, varies by condition"),
      ("Old Flooring Removal", "$1.50–$3/sq ft", "Carpet/vinyl/old laminate"),
    ],
    "faqs": [
      ("How is laminate different from LVP?", "Laminate has a <strong>high-density fiberboard (HDF) core</strong> with a photographic decorative layer — it looks like wood, but the core is essentially compressed wood pulp. Vinyl plank (LVP) has a <strong>plastic-based core</strong> (PVC or SPC stone-plastic composite). The big practical differences: <strong>LVP is waterproof, laminate isn't.</strong> LVP is softer underfoot. Laminate generally looks more textured and 'real' (better embossing technology), but LVP wins for kitchens and baths. For bedrooms and living rooms, both work great."),
      ("Will laminate scratch from pets?", "Quality AC4 or AC5-rated laminate is highly scratch-resistant — actually <em>more</em> scratch-resistant than most hardwood. We've installed laminate in homes with multiple large dogs and seen no scratches after years of use. The wear layer is the determining factor: AC3 is residential moderate use, AC4 is residential heavy / commercial light, AC5 is commercial heavy."),
      ("Can you install laminate over existing tile?", "Yes, in most cases — if the existing tile is well-bonded, the floor is reasonably flat, and the height increase is acceptable for door clearance. We use a thicker underlayment (cork or rubber) to mask the grout lines. If the tile has wide grout lines (over 1/4″) or is uneven, we'd recommend either tile demolition or a self-leveling pour first."),
      ("How long does a laminate installation take?", "A typical 1,200–1,500 sqft laminate install takes 1.5–2.5 days: Day 1 demo + subfloor prep + underlayment + start install, Day 2 finish install + transitions + quarter-round. Laminate is the fastest install of any flooring type because it's a floating click-lock system — no glue cure time, no acclimation requirement (some manufacturers do recommend 24-48 hr acclimation, which we follow)."),
    ],
  },
  "stair-treads": {
    "name": "Stair Treads &amp; Risers",
    "short": "Stair Treads",
    "h1_phrase": "Stair Treads",
    "intro_lead": "Custom hardwood, vinyl, and tile stair treads with matching risers — precision miter joints, slip-resistant finishes, and bullnose detail.",
    "card_image": "card-stairs.webp",
    "hero_image": "hero-bg.jpg",
    "intro_long": """Stair treads are the highest-skill flooring work we do. Every tread is a custom-cut piece — measured, scribed to fit, mitered at the nosing, and finished to match your existing flooring. There's no margin for error: a 1/16″ gap on a stair tread is glaringly visible, where the same gap on a bedroom floor would never be noticed.

Triangle Flooring installs <strong>solid hardwood treads</strong> (typically 1″ thick White Oak, Red Oak, Maple, or Brazilian Cherry), <strong>engineered hardwood treads</strong> (matching engineered floor systems), <strong>LVP-clad treads</strong> with custom-cut bullnose, and <strong>porcelain tile treads</strong> for outdoor stairs and modern interior installations. We also do matching risers, stringers, skirt boards, and starting/landing nosing.

Common stair tread projects in Tampa Bay include: replacing carpet on existing wood stairs (the most popular request), matching new hardwood floors to existing stairs, modernizing builder-grade oak stairs with new white oak, and refinishing weathered exterior tile stairs. Most stair projects take 2–4 days depending on the number of risers and finish complexity.""",
    "scope_items": ["Solid hardwood stair treads (1″ thick)","Engineered hardwood treads (matching floor)","LVP-clad treads with custom bullnose","Porcelain tile treads","Matching risers (paint or wood)","Skirt board installation","Starting nosing","Landing nosing","Stringer trim","Carpet removal &amp; tack strip cleanup","Squeak elimination","Tread leveling &amp; shimming","Custom miter returns","Slip-resistant tread finishes (where required)"],
    "pricing_rows": [
      ("Hardwood Tread (red/white oak)", "$95–$165/tread", "Stained or natural"),
      ("Hardwood Tread (premium species)", "$125–$220/tread", "Brazilian cherry, walnut, etc."),
      ("LVP-Clad Tread (custom bullnose)", "$45–$85/tread", "Matches LVP floor"),
      ("Porcelain Tile Tread", "$80–$150/tread", "With non-slip nosing strip"),
      ("Matching Risers (painted)", "$25–$45/riser", "Primed and painted white"),
      ("Matching Risers (wood)", "$45–$85/riser", "Same species as treads"),
      ("Skirt Board / Stringer Trim", "$35–$70/linear ft", "Wall-side staircase trim"),
      ("Carpet Demolition (per stair)", "$15–$30/tread", "Includes tack strip removal"),
    ],
    "faqs": [
      ("Can you replace carpet on stairs with hardwood?", "This is our most common stair project. We remove the existing carpet, padding, and tack strips; check the existing pine/plywood treads for level and squeaks; install solid hardwood treads on top with matching wood or painted risers. If the existing pine treads are warped or damaged, we replace them entirely. The whole conversion typically takes 2-3 days for a standard 14-step staircase and looks completely transformed."),
      ("Why are hardwood stair treads so much more expensive than regular flooring?", "Each tread is a custom-cut piece: scribed to fit the wall, mitered at the nosing, often with a return on the open side. The labor per square foot is 4-5x what it costs to install regular flooring. The treads themselves are also more expensive — a quality 1″ thick solid hardwood tread costs $40-90 just for the material, before labor. Risers are simpler but still need precision miters. A 14-step staircase is essentially 14 mini custom carpentry projects."),
      ("Do I need slip-resistant nosing?", "For interior residential stairs, slip resistance is mostly about finish choice (matte/satin = better grip than gloss). For exterior stairs, pool-side stairs, and commercial properties, we install proper non-slip nosing strips — either Schluter-TREP for tile, or aluminum/brass strips for hardwood. Florida building code may require non-slip nosing in some commercial situations; we follow whatever is appropriate for your property."),
      ("Can you match my existing flooring on the treads?", "Yes — this is one of our most common requests. If your existing floor is engineered hardwood, we'll order matching solid stair treads from the same manufacturer (most major brands like Anderson, Mirage, and Mohawk offer matching treads). If your floor is LVP, we'll use the LVP planks themselves to clad pre-fabricated wood treads with a custom-cut bullnose. The result is a continuous look from floor to stairs."),
    ],
  },
  "floor-repair": {
    "name": "Floor Repair &amp; Replacement",
    "short": "Repair",
    "h1_phrase": "Flooring Repair &amp; Replacement",
    "intro_lead": "Hurricane and water damage restoration, plank replacement, subfloor repair, and partial reflooring — without redoing the whole space.",
    "card_image": "card-repair.webp",
    "hero_image": "hero-bg.jpg",
    "intro_long": """Not every flooring problem requires a full replacement. Triangle Flooring specializes in <strong>partial repair work</strong> that saves you thousands compared to ripping out a whole room. Whether you've got a few water-damaged planks, a section of buckled hardwood under a window leak, or post-storm damage from Hurricane Ian or Helene — we can usually fix what's broken without touching what's still good.

We've completed <strong>80+ post-hurricane reflooring projects</strong> across Manatee and Sarasota counties since 2022. We know how to work with insurance adjusters, document damage progressions for claims, prioritize the rooms that need to be livable first, and source matching replacement materials for older flooring. If you're navigating an insurance claim right now, we can quote based on your adjuster's scope or provide our own detailed estimate with photo documentation.

Common repair scenarios we handle: <strong>plank replacement</strong> (single damaged boards in hardwood, LVP, or laminate), <strong>tile crack repair</strong> (cracked tiles and grout line damage), <strong>subfloor repair</strong> (rot, soft spots, squeaks under existing flooring), <strong>transition strip replacement</strong> (worn or damaged thresholds), and <strong>partial-room reflooring</strong> (water damage in one section of a larger floor).""",
    "scope_items": ["Hurricane &amp; storm damage restoration","Water damage flooring removal","Insurance claim documentation","Single plank replacement (hardwood/LVP/laminate)","Cracked tile replacement","Grout line repair &amp; recoloring","Subfloor rot repair","Subfloor squeak elimination","Soft spot diagnosis &amp; repair","Toilet flange repair (water-damaged)","Transition strip replacement","Threshold repair","Partial-room reflooring","Color-matching to existing materials"],
    "pricing_rows": [
      ("Single Plank Replacement (LVP/laminate)", "$85–$150/plank", "Includes labor &amp; matching"),
      ("Single Plank Replacement (hardwood)", "$120–$220/plank", "Higher difficulty - blending"),
      ("Cracked Tile Replacement (per tile)", "$95–$175/tile", "Includes matching grout"),
      ("Subfloor Repair (small soft spot)", "$280–$650", "Per spot, includes patch"),
      ("Subfloor Replacement (per room)", "$3.50–$7/sq ft", "Plywood replacement"),
      ("Water-Damaged Section (10-50 sqft)", "$450–$1,500", "Includes drying, prep, replacement"),
      ("Hurricane Insurance Claim Project", "Based on scope", "We work with your adjuster"),
      ("Diagnosis Visit (waived if hired)", "$95", "On-site assessment + written quote"),
    ],
    "faqs": [
      ("Can you match my existing flooring for a repair?", "We can match most flooring installed in the last 10 years if you have either (a) a few extra planks/tiles saved from the original install, (b) a manufacturer name and product code from old paperwork, or (c) a sample we can take to a tile or flooring supplier. For older or discontinued products, we can usually find very close matches but exact-match is rare. We always show you samples before committing to materials."),
      ("Will my insurance cover post-hurricane flooring damage?", "It depends on your specific policy and the cause. Generally: <strong>flood damage is covered only by separate flood insurance</strong> (NFIP), <strong>wind-driven rain damage</strong> through a damaged roof or windows is usually covered by standard homeowners, and <strong>storm surge</strong> is flood insurance only. We're not insurance adjusters, but we have experience documenting damage in claim-friendly format and have worked with most major Florida insurers post-Ian and post-Helene."),
      ("How fast can you get to a water emergency?", "For active water emergencies (burst pipes, fresh storm damage), we can usually get a crew to your home within 24 hours for damage assessment and stabilization. Full repairs depend on materials availability and the extent of damage — typically we can begin repair work within 3-7 days of initial assessment. For scheduled repairs (cracked tile, single plank replacement, etc.), our standard 24-hour estimate response applies."),
      ("Can you tell me if my whole floor needs replacement, or just part?", "Yes — that's exactly what our diagnosis visit is for. We come out, assess the damaged area, test moisture in surrounding flooring (to see if hidden water has spread), and give you a written recommendation for either partial repair or full replacement with a clear cost comparison. In our experience, 70% of damage that 'looks bad' can actually be repaired for less than half the cost of full replacement."),
    ],
  },
}

# ============================================================================
# RENDER FUNCTIONS
# ============================================================================
def render_pricing_table(rows, service_short, city=""):
    title = f"{service_short} Prices in {city} (2026)" if city else f"{service_short} Prices (2026)"
    rows_html = "".join(f'<tr><td>{a}</td><td class="price">{b}</td><td>{c}</td></tr>' for a,b,c in rows)
    return f"""<section class="pricing">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Transparent Pricing</span>
      <h2>{title}</h2>
      <p>Free custom estimate — call <a href="tel:{PHONE}">{PHONE_DISPLAY}</a></p>
    </div>
    <div class="pricing-table">
      <table>
        <thead><tr><th>Material / Service</th><th>Price Range</th><th>Notes</th></tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>
    <p class="pricing-note">* Prices reflect 2026 Tampa Bay market rates and assume standard subfloor conditions. <a href="/contact/">Get a free custom estimate →</a></p>
  </div>
</section>"""

def render_neighborhoods_section(city_data, service_short):
    nb = "".join(f'<div class="neighborhood-pill">{n}</div>' for n in city_data["neighborhoods"])
    zips = "".join(f'<div class="zip-pill">{z}</div>' for z in city_data["zips"])
    return f"""<section class="neighborhoods">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Local Coverage</span>
      <h2>{service_short} in {city_data['name']} Neighborhoods</h2>
      <p>We serve all of {city_data['county']} — {len(city_data['neighborhoods'])}+ neighborhoods and counting.</p>
    </div>
    <div class="neighborhood-grid">{nb}</div>
    <h3 style="text-align:center;margin:2.5rem 0 1rem;font-size:1.05rem;color:var(--gray);font-weight:600;letter-spacing:.06em;text-transform:uppercase">ZIP Codes Served</h3>
    <div class="zip-grid">{zips}</div>
  </div>
</section>"""

def render_scope_section(items):
    items_html = "".join(f'<li style="padding:9px 0 9px 28px;position:relative;border-bottom:1px solid var(--gray-border);font-size:.95rem"><span style="position:absolute;left:0;top:9px;color:var(--success);font-weight:700">✓</span>{i}</li>' for i in items)
    return f"""<section style="background:#fff">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">What's Included</span>
      <h2>Full Scope of Work</h2>
      <p>Everything covered when Triangle Flooring takes on your project — itemized and transparent.</p>
    </div>
    <ul style="list-style:none;max-width:780px;margin:0 auto;columns:2;column-gap:2.5rem;padding:0">{items_html}</ul>
  </div>
</section>"""

def render_stat_badge():
    return """<div class="stat-badge">
  <span class="stat-badge-icon">⭐</span>
  <div>
    <p>300+ Projects Completed Across Tampa Bay — Triangle Flooring</p>
    <p>6 verified Google reviews · 5.0 ★ rating · Insured · Same-crew installations</p>
  </div>
</div>"""

# ============================================================================
# BUILD: SERVICE HUB PAGES (6 pages)
# ============================================================================
def build_service_hub(slug, svc):
    PATH = f"/{slug}/"
    title_short = svc["short"]
    TITLE = f"{svc['h1_phrase']} in Bradenton FL | Triangle Flooring"
    if len(TITLE) > 65:
        TITLE = f"{title_short} Flooring Bradenton FL | Triangle Flooring"
    DESC = f"{svc['h1_phrase']} installation across Bradenton, Sarasota, Lakewood Ranch & Tampa Bay. {svc['intro_lead'][:80]} Free estimate."
    if len(DESC) > 158: DESC = DESC[:155] + "..."

    bc_items = [("Home", "/"), (svc['name'].replace("&amp;", "&"), None)]
    bc_schema = render_breadcrumb_schema(bc_items)

    checklist_html, total_pts = render_checklist()
    business_schema = render_local_business_schema(svc["name"].replace("&amp;","&"), svc["intro_lead"][:160], PATH, image=svc["card_image"])
    business_schema["hasOfferCatalog"] = {
        "@type":"OfferCatalog","name":svc["name"].replace("&amp;","&"),
        "itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":i.replace("&amp;","&")}} for i in svc["scope_items"][:8]]
    }

    faq_html, faq_schema = render_faq(svc["faqs"])
    pricing = render_pricing_table(svc["pricing_rows"], title_short)
    scope = render_scope_section(svc["scope_items"])

    # City links section
    city_links_html = ""
    if slug in ["hardwood-flooring","vinyl-plank-flooring"]:
        cards = []
        for cs, cd in CITIES.items():
            cards.append(f'<a href="/{slug}/{cs}/" class="related-card"><strong>{title_short} in {cd["name"]} →</strong><span>{cd["county"]} · {len(cd["neighborhoods"])}+ neighborhoods</span></a>')
        city_links_html = f"""<section class="related">
  <div class="container">
    <div class="section-head"><span class="eyebrow">By City</span><h2>{title_short} Service Areas</h2></div>
    <div class="related-grid">{"".join(cards)}</div>
  </div>
</section>"""

    related_services = [s for s in SERVICES if s != slug][:3]
    related_html = "".join(f'<a href="/{s}/" class="related-card"><strong>{SERVICES[s]["name"].replace("&amp;","&")} →</strong><span>{SERVICES[s]["intro_lead"][:80]}</span></a>' for s in related_services)

    content = f"""{page_head(TITLE, DESC, PATH, og_image=svc["card_image"])}
{header()}
{breadcrumbs(bc_items)}

<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Our Service</span>
    <h1>{svc['h1_phrase']} in <span>Tampa Bay, FL</span></h1>
    <p>{svc['intro_lead']}</p>
    <div class="page-hero-trust">
      <span>300+ projects</span>
      <span>5★ Google rated</span>
      <span>1-year warranty</span>
      <span>Free estimates</span>
    </div>
  </div>
</section>

<section class="intro">
  <div class="container">
    <div class="intro-content">
      {''.join(f'<p>{p}</p>' for p in svc['intro_long'].split(chr(10)+chr(10)))}
      {render_stat_badge()}
    </div>
  </div>
</section>

{pricing}

{scope}

<section style="background:var(--gray-light)">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">The Triangle Standard</span>
      <h2>Our 42-Point {title_short} Installation Checklist</h2>
      <p>Every install — no matter the size — must pass all {total_pts} points before we sign off. You get a printed copy at handover.</p>
    </div>
    {checklist_html}
  </div>
</section>

{city_links_html}

{render_common_mistakes_section(title_short)}

<section class="intro" style="background:#fff">
  <div class="container">
    <div class="intro-content">
      <h2 style="margin-bottom:1.4rem">How to Choose the Right {title_short} for Your Florida Home</h2>
      <p>After 300+ installs, here's the framework we walk every client through during in-home consultations. It's the same logic we use to recommend products, simplified into something you can use yourself before you ever talk to a contractor.</p>

      <h3 style="margin:2rem 0 .9rem;font-size:1.2rem;color:var(--text)">Step 1 — Understand your home's actual conditions</h3>
      <p>Before looking at materials, look at your home. <strong>Is your home on slab or wood subfloor?</strong> Slab homes have moisture migration risk; wood subfloors have flex and squeak risk. <strong>What's your indoor humidity range?</strong> A whole-house dehumidifier or properly sized AC keeps it stable; without those, materials work harder. <strong>Where does water risk exist?</strong> Kitchens, baths, laundry rooms, and rooms adjacent to lanai sliders all face higher moisture exposure than bedrooms or living rooms.</p>

      <h3 style="margin:2rem 0 .9rem;font-size:1.2rem;color:var(--text)">Step 2 — Match the material to the room</h3>
      <p>The single biggest mistake homeowners make is choosing one material for the whole house. <strong>Different rooms have different demands.</strong> A premium hardwood that's perfect in your living room is a disaster in your bathroom. A waterproof vinyl plank that's perfect in your kitchen feels less luxurious in your formal foyer. The smartest installs use different materials in different zones — connected with thoughtful transitions — to optimize each space.</p>

      <h3 style="margin:2rem 0 .9rem;font-size:1.2rem;color:var(--text)">Step 3 — Plan for the long term</h3>
      <p>Are you in a forever home, a 5-7 year stop, or an investment property? Each scenario points toward different choices. <strong>Forever homes</strong> justify premium materials with longer lifespans (engineered hardwood, porcelain tile) — the per-year cost actually drops as ownership extends. <strong>Mid-term homes</strong> usually favor mid-range SPC, which delivers most of the visual appeal of hardwood at lower cost and faster ROI at sale. <strong>Investment properties</strong> almost always favor premium SPC — waterproof, scratch-resistant, easy to repair when tenants damage planks.</p>

      <h3 style="margin:2rem 0 .9rem;font-size:1.2rem;color:var(--text)">Step 4 — Get itemized written quotes (plural)</h3>
      <p>Always get at least 2-3 quotes. Always require itemized line items: material cost, labor cost, removal/disposal, subfloor prep, transition strips, baseboards, waste percentage. Compare apples to apples. The cheapest quote almost always becomes the most expensive job (because of the line items hidden out of the initial bid). The right contractor explains what every line is for.</p>

      <h3 style="margin:2rem 0 .9rem;font-size:1.2rem;color:var(--text)">Step 5 — Ask the questions that filter contractors</h3>
      <p>These five questions reveal more about a contractor than any sales pitch:</p>
      <ol style="margin:0 0 1rem 1.4rem;padding:0">
        <li><strong>"Will the same crew that quotes my job install it?"</strong> If they subcontract, quality varies wildly.</li>
        <li><strong>"Do you test subfloor moisture before install? Can you show me the meter reading?"</strong> If they don't, your floor is at risk before it's even installed.</li>
        <li><strong>"How long do you acclimate materials on-site?"</strong> Anything under 48 hours is too short for Florida.</li>
        <li><strong>"Can I see your written labor warranty?"</strong> If it's verbal-only or under 12 months, that's a red flag.</li>
        <li><strong>"What's your contingency for finding subfloor damage mid-install?"</strong> A good contractor has a documented process; a bad one says "we'll figure it out."</li>
      </ol>
    </div>
  </div>
</section>

{render_why_triangle_section(title_short)}

<section class="faq-section">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Common Questions</span><h2>{title_short} FAQ</h2></div>
    {faq_html}
  </div>
</section>

<section class="related">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Related</span><h2>Other Flooring Services</h2></div>
    <div class="related-grid">{related_html}</div>
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

    out_path = f"{OUT_DIR}/{slug}/index.html"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f: f.write(content)
    print(f"  ✓ /{slug}/index.html ({len(content)//1024} KB)")

# ============================================================================
# BUILD: SERVICE+CITY PAGES
# ============================================================================
def build_service_city(svc_slug, city_slug):
    svc = SERVICES[svc_slug]
    city = CITIES[city_slug]
    PATH = f"/{svc_slug}/{city_slug}/"
    title_short = svc["short"]
    TITLE = f"{title_short} {city['name']} FL | Triangle Flooring 5★"
    if len(TITLE) > 65: TITLE = f"{title_short} in {city['name']} FL | Triangle Flooring"
    DESC = f"{svc['h1_phrase']} in {city['name']}, FL. Hardwood-quality install in {len(city['neighborhoods'])}+ neighborhoods. 5★ rated · 1-yr warranty · Free estimate in 24h."
    if len(DESC) > 158: DESC = DESC[:155] + "..."

    bc_items = [("Home","/"),(svc['name'].replace("&amp;","&"),f"/{svc_slug}/"),(city['name'],None)]
    bc_schema = render_breadcrumb_schema(bc_items)

    checklist_html, total_pts = render_checklist()
    business_schema = render_local_business_schema(f"{svc['short']} in {city['name']}", f"{svc['h1_phrase']} installation in {city['name']}, FL — serving {city['county']}.", PATH, city=city['name'], image=svc["card_image"])

    # City-specific FAQs
    city_faqs = [
      (f"How much does {svc['short'].lower()} flooring cost in {city['name']}, FL?",
       f"<p>{svc['short']} flooring in {city['name']} typically ranges from <strong>{svc['pricing_rows'][0][1]}</strong> for entry-level options up to <strong>{svc['pricing_rows'][-3][1]}</strong> for premium installations. Final pricing depends on subfloor condition, square footage, material grade, and any custom work like patterns or stair treads. Triangle Flooring provides free, itemized written estimates within 24 hours of your call.</p>"),
      (f"Do you serve all of {city['name']}?",
       f"<p>Yes — we cover all of {city['name']} and surrounding {city['county']}, including {', '.join(city['neighborhoods'][:6])}, and {len(city['neighborhoods'])-6}+ other neighborhoods. ZIP codes served: {', '.join(city['zips'][:6])}{' and more' if len(city['zips'])>6 else ''}. Free in-home estimates anywhere in our service area.</p>"),
      (f"How long does a {svc['short'].lower()} installation take in {city['name']}?",
       f"<p>Most residential {svc['short'].lower()} projects (under 1,500 sq ft) take 2 to 5 working days from start to finish in {city['name']}. This includes acclimation, demolition of existing flooring, subfloor preparation, installation, and finish work like baseboards and transitions. Larger projects or custom patterns can extend this timeline. We provide a clear daily schedule when you sign off on the quote.</p>"),
      (f"Do you offer warranties on {svc['short'].lower()} installation?",
       f"<p>Yes. Triangle Flooring provides a written <strong>1-year labor warranty</strong> on every {svc['short'].lower()} installation in {city['name']}, in addition to the manufacturer's product warranty (which typically ranges from 15 years to lifetime depending on the specific product you choose). If a plank lifts, a tile cracks at the grout, or a tread squeaks within 12 months, we come back and fix it.</p>"),
    ]
    faq_html, faq_schema = render_faq(city_faqs)

    pricing = render_pricing_table(svc["pricing_rows"], title_short, city["name"])

    # City context paragraph
    city_intro = f"""<p><strong>{svc['h1_phrase']} in {city['name']}, Florida</strong> requires a contractor who understands the unique demands of {city['county']}. {city['context']}</p>

<p>Triangle Flooring has installed {svc['short'].lower()} flooring in {len(city['neighborhoods'])}+ neighborhoods across {city['name']}, including {', '.join(city['neighborhoods'][:5])}, and many more. Whether you're in a beachfront condo, a 1990s ranch, or a brand-new Lakewood Ranch luxury build, we know how to spec the right material and install it to last decades — not seasons.</p>

<p>Local landmarks we work near regularly: {city['landmarks']}. We typically respond to {city['name']} estimate requests within 24 hours and can begin most projects within 1–2 weeks of contract sign-off.</p>"""

    # Related: link to other services in this city + same service in other cities
    related_cards = []
    for other_svc_slug, other_svc in SERVICES.items():
        if other_svc_slug == svc_slug: continue
        if other_svc_slug in ["hardwood-flooring","vinyl-plank-flooring"]:
            related_cards.append(f'<a href="/{other_svc_slug}/{city_slug}/" class="related-card"><strong>{other_svc["short"]} in {city["name"]} →</strong><span>{other_svc["intro_lead"][:75]}</span></a>')
        else:
            related_cards.append(f'<a href="/{other_svc_slug}/" class="related-card"><strong>{other_svc["short"]} →</strong><span>{other_svc["intro_lead"][:75]}</span></a>')
    related_html = "".join(related_cards[:4])

    # Same service in OTHER cities
    other_city_cards = []
    for other_city_slug, other_city in CITIES.items():
        if other_city_slug == city_slug: continue
        other_city_cards.append(f'<a href="/{svc_slug}/{other_city_slug}/" class="related-card"><strong>{svc["short"]} in {other_city["name"]} →</strong><span>{other_city["county"]} · {len(other_city["neighborhoods"])}+ neighborhoods</span></a>')
    other_cities_html = f"""<section class="related" style="background:var(--gray-light)">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Other Service Areas</span><h2>{svc['short']} in Other Cities</h2></div>
    <div class="related-grid">{"".join(other_city_cards)}</div>
  </div>
</section>"""

    content = f"""{page_head(TITLE, DESC, PATH, og_image=svc["card_image"])}
{header()}
{breadcrumbs(bc_items)}

<section class="page-hero">
  <div class="container">
    <span class="eyebrow">📍 {city['county']}</span>
    <h1>{svc['h1_phrase']} in <span>{city['name']}, FL</span></h1>
    <p>{svc['intro_lead']}</p>
    <div class="page-hero-trust">
      <span>{len(city['neighborhoods'])}+ neighborhoods served</span>
      <span>300+ projects</span>
      <span>5★ Google rated</span>
      <span>Free estimates</span>
    </div>
  </div>
</section>

<section class="intro">
  <div class="container">
    <div class="intro-content">
      {city_intro}
      {render_stat_badge()}
    </div>
  </div>
</section>

{pricing}

{render_scope_section(svc["scope_items"])}

<section style="background:var(--gray-light)">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">The Triangle Standard</span>
      <h2>Our 42-Point Installation Checklist for {city['name']} Homes</h2>
      <p>Every install — no matter the size — must pass all {total_pts} points before we sign off. You get a printed copy at handover.</p>
    </div>
    {checklist_html}
  </div>
</section>

{render_neighborhoods_section(city, svc['short'])}

{render_common_mistakes_section(svc['short'])}

<section class="intro" style="background:#fff">
  <div class="container">
    <div class="intro-content">
      <h2 style="margin-bottom:1.4rem">How {city['name']} Homeowners Should Choose {svc['short']}</h2>
      <p>{city['name']} has its own dynamics — different neighborhoods, different home ages, different humidity exposures. Here's how we help local clients think through the choice.</p>

      <h3 style="margin:2rem 0 .9rem;font-size:1.2rem;color:var(--text)">Match the material to your specific {city['name']} home</h3>
      <p>If you're in a beachfront or waterfront home (think Anna Maria Island, Siesta Key, Lido Key, Longboat Key), salt-air exposure and elevated humidity push the recommendation toward <strong>SPC vinyl plank or porcelain tile</strong>. If you're in a newer Lakewood Ranch or East Manatee build (built 2010+), modern slab construction generally handles engineered hardwood very well. If you're in a 1980s-1990s {city['name']} home, expect older subfloor conditions that may need more prep — both for hardwood and for vinyl plank.</p>

      <h3 style="margin:2rem 0 .9rem;font-size:1.2rem;color:var(--text)">Consider how you actually live in your {city['name']} home</h3>
      <p>Are you full-time residents, snowbirds, vacation rentals? Each scenario changes the math. <strong>Full-time families</strong> need durable, easy-maintenance flooring that handles daily traffic — premium SPC is often the smartest pick. <strong>Snowbirds</strong> who close up the home for summer face indoor humidity spikes when AC is set high — moisture-tolerant materials (SPC, tile) protect against this. <strong>Vacation rentals</strong> need waterproof, scratch-resistant flooring that photographs well in listings and survives turnover cleaning — SPC dominates this category.</p>

      <h3 style="margin:2rem 0 .9rem;font-size:1.2rem;color:var(--text)">Get itemized quotes from local installers</h3>
      <p>The {city['name']} flooring market includes everyone from one-truck handymen to nationally-franchised chains. The pricing varies wildly — but so does the quality. Always require: itemized line items (material, labor, removal, prep, transitions, baseboards, waste), written 1-year minimum labor warranty, documented subfloor moisture testing, and 48-72 hour on-site acclimation. Anyone unwilling to commit to all four in writing is not the right contractor.</p>

      <h3 style="margin:2rem 0 .9rem;font-size:1.2rem;color:var(--text)">Plan for the {city['name']} climate, not the showroom climate</h3>
      <p>That gorgeous wide-plank European white oak you saw at Floor &amp; Decor in air-conditioned 70°F showroom climate? It will move in your {city['name']} home, where indoor humidity swings 10-15 points seasonally. <strong>The product matters; the install matters more.</strong> Florida-experienced contractors plan for our climate — generic national install protocols don't.</p>

      <p>If you'd like a free in-home consultation in {city['name']}, we cover all of {city['county']} including {', '.join(city['neighborhoods'][:5])} and {len(city['neighborhoods'])-5}+ other neighborhoods. We measure, test your subfloor, and provide written itemized quotes within 24 hours.</p>
    </div>
  </div>
</section>

{render_why_triangle_section(svc['short'])}

<section class="faq-section">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Common Questions</span><h2>{svc['short']} FAQ — {city['name']}</h2></div>
    {faq_html}
  </div>
</section>

{other_cities_html}

<section class="related">
  <div class="container">
    <div class="section-head"><span class="eyebrow">More in {city['name']}</span><h2>Other Triangle Flooring Services</h2></div>
    <div class="related-grid">{related_html}</div>
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

    out_path = f"{OUT_DIR}/{svc_slug}/{city_slug}/index.html"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f: f.write(content)
    print(f"  ✓ /{svc_slug}/{city_slug}/index.html ({len(content)//1024} KB)")

# ============================================================================
# RUN
# ============================================================================
print("\n→ Building service hub pages:")
for slug, svc in SERVICES.items():
    build_service_hub(slug, svc)

print("\n→ Building service+city pages (hardwood + vinyl plank × 3 cities):")
for svc_slug in ["hardwood-flooring","vinyl-plank-flooring"]:
    for city_slug in CITIES:
        build_service_city(svc_slug, city_slug)

print("\n✓ All pages built")
