#!/usr/bin/env python3
"""
Generate /blog/[service]-cost-[city]/ pricing pages.
6 services × 8 cities = 48 combinations, but skips 2 existing
(/blog/vinyl-plank-flooring-cost-bradenton-2026/ and /blog/tile-installation-cost-sarasota/)
producing 46 NEW articles. Each is 2,200-2,500 words with city-specific
pricing computed from labor multipliers, real neighborhood scenarios,
inline WhatsApp + quote form, and FAQPage/Article/BreadcrumbList schemas.
"""
import sys, json, os, re, hashlib
sys.path.insert(0, '/home/claude/triangle')
from _gen import *
from _build_services import CITIES, SERVICES

# ============================================================================
# PRICING DATA — 2026 Florida rates
# ============================================================================

# Labor multipliers per city (applied to labor portion only)
CITY_LABOR_MULT = {
    "palmetto":         0.95,  # HQ market
    "parrish":          0.95,  # newer growth area
    "bradenton":        1.00,  # baseline
    "venice":           1.05,  # snowbird/retiree premium
    "sarasota":         1.07,  # affluent
    "st-petersburg":    1.08,  # urban + waterfront
    "tampa":            1.10,  # urban premium
    "lakewood-ranch":   1.10,  # luxury master-planned
    "ellenton":         0.97,  # next to HQ, value market
    "ruskin":           0.97,  # fast-growth, builder-grade upgrades
    "north-port":       0.98,  # high-growth value market
    "sun-city-center":  1.02,  # 55+ retiree, carpet-replacement heavy
    "apollo-beach":     1.08,  # affluent waterfront
    "nokomis":          1.08,  # affluent coastal
}

# Service pricing: each tier has material range + base labor range
# Computed final = material + (labor × city_mult)
SVC_PRICING = {
    "hardwood-flooring": {
        "name": "Hardwood Flooring",
        "short": "Hardwood",
        "card_image": "card-hardwood.webp",
        "unit": "sq ft",
        "tiers": [
            ("Engineered Hardwood (entry-level)",   4.50,  6.50, 3.00, 4.50),
            ("Engineered Hardwood (mid-range)",     7.00, 10.00, 3.25, 5.00),
            ("Engineered Hardwood (premium wide-plank)", 10.00, 15.00, 4.00, 6.00),
            ("Solid Hardwood (with subfloor prep)",  8.00, 12.00, 4.00, 7.00),
        ],
        "premium_factor": "wide-plank European white oak",
        "cost_factors": [
            ("Wood species and grade",
             "White oak and red oak are most affordable, $4.50-$8/sq ft for material. Walnut, hickory, maple add $1-3/sq ft. Brazilian cherry, teak, and other exotics push material above $12/sq ft. Within each species, 'Select' grade (clear, uniform) costs more than 'Character' grade (knots, mineral streaks)."),
            ("Plank width and length",
             "Standard 3-5 inch planks are the most affordable. Wide-plank (7 inches and wider) costs $2-4/sq ft more. Random-length planks (mix of 12-72 inch lengths) add another premium because they reduce visual repetition. Extra-wide (9 inch+) and extra-long (84 inch+) are luxury-tier pricing."),
            ("Engineered vs solid construction",
             "Engineered hardwood (multi-ply with hardwood top layer) is what we install in most Florida homes — better dimensional stability in humidity. Solid 3/4-inch hardwood requires plywood underlayment over slab construction, adding $3-5/sq ft to the project. Engineered is usually the smarter choice for Florida."),
            ("Finish type",
             "Pre-finished hardwood (factory finish, ready to walk on) costs more upfront but installs faster. Site-finished (raw wood, finished after install) costs less in materials but doubles labor time (sanding + 3 finish coats). Pre-finished is the dominant choice in 2026."),
            ("Subfloor preparation",
             "If your subfloor needs self-leveling compound, vapor barrier, or repair, expect $1-3/sq ft added. We always test slab moisture before any hardwood install — if readings exceed manufacturer limits, additional moisture management is required."),
        ],
        "hidden_costs": [
            ("Self-leveling compound (concrete slab)",      "$300 – $900 per room"),
            ("Subfloor moisture testing & documentation",   "$95 – $180"),
            ("Plywood underlayment (for solid hardwood)",   "$1.80 – $3/sq ft"),
            ("Vapor barrier (over slab)",                    "$0.40 – $0.80/sq ft"),
            ("Existing flooring removal (carpet)",          "$1.50 – $2.50/sq ft"),
            ("Existing flooring removal (tile)",            "$2.50 – $5/sq ft"),
            ("Furniture moving (per room)",                  "$200 – $600"),
            ("Quarter-round / shoe molding",                "$2.50 – $4.50/linear ft"),
            ("Stair noses (matching wood)",                 "$45 – $85 each"),
            ("Manufacturer's transition strips",             "$25 – $65 each"),
        ],
        "money_tips": [
            "Choose engineered hardwood over solid for Florida slab homes — saves $3-5/sq ft on substrate prep without sacrificing visual quality.",
            "Move your own furniture before the crew arrives. $200-600 per room saved.",
            "Schedule during the slow season (January-February or August-September). Many contractors offer 5-10% off labor or upgrade you to better material at the same price.",
            "Buy through your installer rather than retail. Distributor pricing is typically 15-30% below Floor & Decor or Lumber Liquidators retail.",
            "Don't skimp on acclimation. Skipping the 48-72 hour acclimation period costs nothing upfront — but failing planks within 18 months costs $5,000-15,000 in rework.",
        ],
    },
    "vinyl-plank-flooring": {
        "name": "Vinyl Plank Flooring (LVP/SPC)",
        "short": "Vinyl Plank",
        "card_image": "card-vinyl.webp",
        "unit": "sq ft",
        "tiers": [
            ("Builder-Grade LVP (12-mil wear)",     0.30, 1.20, 1.80, 2.50),
            ("Mid-Range SPC (20-mil wear)",          1.20, 3.00, 2.00, 3.00),
            ("Premium SPC (22-30 mil wear)",         3.00, 5.50, 2.20, 3.20),
            ("Luxury Wide-Plank LVP/SPC",            5.50, 9.00, 2.50, 3.50),
        ],
        "premium_factor": "premium SPC with 22-mil+ wear layer",
        "cost_factors": [
            ("LVP vs SPC core construction",
             "LVP has a flexible PVC core; SPC (Stone Plastic Composite) has a rigid mineral-filled core. SPC is more dimensionally stable in Florida humidity and more forgiving of subfloor imperfections — we recommend SPC over standard LVP for nearly all Florida installs. SPC typically costs $0.50-1.50/sq ft more for material."),
            ("Wear layer thickness (mils)",
             "The clear protective top layer determines durability. 12-mil wear handles light residential use (rentals, low-traffic rooms). 20-mil wear is the residential sweet spot. 22-30 mil wear is needed for pets, kids, and high-traffic homes. Premium SPC products with 30+ mil wear carry lifetime residential warranties."),
            ("Plank dimensions",
             "Wider planks (7-9 inch) and longer planks (60-72 inch) cost more but install faster per square foot. Counterintuitively, this means luxury wide-plank can sometimes be cheaper to install per square foot than standard 5-6 inch planks."),
            ("Installation method",
             "Click-lock floating installs are fastest ($2-2.80/sq ft labor in 2026). Glue-down installs cost more ($2.80-3.80/sq ft labor) due to glue prep, trowel work, and adhesive cure time. Glue-down is essential for areas with significant temperature swings (lanai conversions, sunrooms)."),
            ("Subfloor condition",
             "Clean, flat slab? Standard install. Slab needs self-leveling? Add $0.50-1.50/sq ft. Wood subfloor with squeaks? Add $200-500 for fastener pass before LVP goes down. Excessive moisture readings? Vapor barrier adds $0.40-0.80/sq ft."),
        ],
        "hidden_costs": [
            ("Self-leveling compound (concrete slab)",      "$200 – $700 per room"),
            ("Subfloor moisture testing",                    "$95 – $180"),
            ("Underlayment (when not built-in)",            "$0.50 – $1.75/sq ft"),
            ("Vapor barrier on concrete slab",              "$0.40 – $0.80/sq ft"),
            ("Existing flooring removal",                    "$1.50 – $3/sq ft"),
            ("Furniture moving",                             "$200 – $600 per room"),
            ("Toilet pull and reset",                        "$120 – $200 per toilet"),
            ("Quarter-round / shoe molding",                "$2.50 – $4.50/linear ft"),
            ("Transition strips (T-mold, reducer)",          "$25 – $65 each"),
            ("Stair tread custom bullnose",                  "$45 – $85 per stair"),
        ],
        "money_tips": [
            "Choose mid-range SPC over builder-grade LVP. The $1-2/sq ft material upgrade lasts 3x longer and avoids the 'cheap floor → cheap repair → cheap replacement' cycle.",
            "Avoid 'premium underlayment' upcharges if your SPC has attached padding. You're paying for something the product already has.",
            "Click-lock SPC over glue-down when possible. Faster install, lower labor cost, and easier single-plank repairs years later.",
            "Buy in bulk. Most distributors offer 5-10% discounts on orders over 1,000 sq ft — relevant for whole-home reflooring projects.",
            "Don't skip subfloor moisture testing. A $150 test prevents $5,000 of plank failures in year three.",
        ],
    },
    "tile-installation": {
        "name": "Tile Installation",
        "short": "Tile",
        "card_image": "card-tile.webp",
        "unit": "sq ft",
        "tiers": [
            ("Standard Ceramic Tile",                 0.50,  3.00, 5.00,  8.00),
            ("Standard Porcelain Tile (12×24)",       1.50,  5.00, 5.50,  9.00),
            ("Large-Format Porcelain (24×48+)",       3.00,  9.00, 8.00, 12.00),
            ("Natural Stone (marble, travertine)",    4.00, 14.00, 8.00, 12.00),
        ],
        "premium_factor": "large-format porcelain (24×48 or larger)",
        "cost_factors": [
            ("Tile size and format",
             "Standard 12×12 and 12×24 tiles install at standard rates. Large-format tiles (24×24, 24×48, 32×32, 48×48) require nearly perfect substrate flatness — usually self-leveling compound across the entire floor. Plus specialized large-format mortars and leveling-clip systems. Adds $2-3/sq ft to labor."),
            ("Material type and grade",
             "Ceramic tile is most affordable but more porous (can stain). Porcelain is denser, harder, and virtually waterproof — better for Florida floors. Natural stone (marble, travertine, slate) requires sealing and ongoing maintenance, but offers irreplaceable aesthetic character. Grade-1 porcelain is the standard for floors; grade-2 or 'wall tile' should never be used on floors."),
            ("Layout pattern complexity",
             "Straight-set installation is fastest. Diagonal layouts add 10-15% labor. Herringbone, basket-weave, or chevron patterns add 25-40%. Mixed-tile mosaics or custom medallions can double the labor cost on that section. Pattern choice is purely aesthetic and budget-driven."),
            ("Wet area waterproofing",
             "Showers, tub surrounds, and curbless walk-ins require Schluter-Kerdi or Hydro-Ban waterproofing membranes — non-negotiable for Florida humidity. Adds $5-8/sq ft for the waterproofing area, plus the labor to install correctly. A 40 sq ft shower waterproofing alone runs $400-800."),
            ("Substrate preparation",
             "Old tile removal averages $2.50-$5/sq ft (often more than new tile material). Existing wood subfloors may need backer board ($2.50-$4.50/sq ft) before tile goes down. Concrete slabs with cracks or unevenness need self-leveling compound ($0.50-$1.50/sq ft of repaired area)."),
        ],
        "hidden_costs": [
            ("Self-leveling compound",                       "$300 – $900 per room"),
            ("Backer board (shower walls)",                   "$2.50 – $4.50/sq ft"),
            ("Schluter-Kerdi waterproofing",                  "$5 – $8/sq ft"),
            ("Premium epoxy grout (vs cementitious)",         "$1.50 – $3/sq ft upcharge"),
            ("Existing tile demolition",                      "$2.50 – $5/sq ft"),
            ("Toilet pull and reset",                         "$120 – $200 per toilet"),
            ("Linear drain (curbless shower)",                "$400 – $900 each"),
            ("Schluter Strip transitions",                    "$25 – $95 each"),
            ("Custom shower niches",                          "$300 – $900 each"),
            ("Stone sealing (natural stone only)",            "$1 – $3/sq ft"),
        ],
        "money_tips": [
            "Choose porcelain over natural stone unless aesthetics are critical. Porcelain is more durable, doesn't need sealing, and costs 30-50% less.",
            "Standard 12×24 porcelain delivers 90% of the visual impact of large-format at 60% of the installed cost. Larger isn't always better.",
            "Keep showers as standard rectangular (curb shower) to avoid the linear drain + curbless premium ($1,500-2,500 added).",
            "Use epoxy grout in showers and high-stain areas. Costs $1.50-3/sq ft more upfront but never needs sealing — saves money long-term.",
            "Skip unnecessary backsplash mosaic accent strips. They look dated within 5 years and cost $30-80 per linear foot.",
        ],
    },
    "laminate-flooring": {
        "name": "Laminate Flooring",
        "short": "Laminate",
        "card_image": "card-laminate.webp",
        "unit": "sq ft",
        "tiers": [
            ("Builder-Grade Laminate (AC3)",         1.00, 2.00, 1.50, 2.50),
            ("Mid-Range Laminate (AC4)",              1.50, 3.00, 1.75, 2.75),
            ("Premium Water-Resistant Laminate (AC5)", 2.50, 4.00, 2.00, 3.00),
            ("Restoration-Grade Wood-Look Laminate",  3.00, 5.00, 2.25, 3.25),
        ],
        "premium_factor": "AC5 water-resistant laminate",
        "cost_factors": [
            ("AC rating (abrasion resistance class)",
             "AC3 is residential standard. AC4 is durable residential / light commercial — what we recommend for most Florida homes. AC5 is heavy commercial-rated and best for households with pets, kids, or high traffic. Higher AC ratings cost $0.50-1.50/sq ft more but last 2-3x longer."),
            ("Plank thickness and underlayment",
             "8mm laminate is entry-level; 10-12mm is standard residential; 14mm+ is premium. Thicker laminate dampens sound better and feels more solid underfoot. Some products include attached underlayment — saves $0.50-1/sq ft vs separately purchased underlayment."),
            ("Water resistance level",
             "Standard laminate is NOT waterproof. 'Water-resistant' laminate (typically AC4-AC5 with sealed edges) handles minor spills better but isn't waterproof either. For Florida homes with any water risk (kitchens, bathrooms, near sliding doors), we strongly recommend SPC vinyl over laminate."),
            ("Click-lock vs glue-down",
             "Click-lock (floating) laminate is the dominant install method — fast, clean, repairable. Glue-down laminate is rare in residential. Stick with click-lock unless you have specific reasons to glue."),
            ("Subfloor preparation",
             "Like all flooring, laminate needs flat substrate. Concrete slabs over 3/16-inch deviation per 10 feet need self-leveling compound. Wood subfloors with squeaks should be addressed before installation. Always include a vapor barrier on concrete slab."),
        ],
        "hidden_costs": [
            ("Underlayment (when not attached)",            "$0.50 – $1.20/sq ft"),
            ("Self-leveling compound",                       "$200 – $600 per room"),
            ("Vapor barrier on concrete slab",              "$0.40 – $0.80/sq ft"),
            ("Existing flooring removal",                    "$1.50 – $3/sq ft"),
            ("Furniture moving",                             "$200 – $600 per room"),
            ("Quarter-round / shoe molding",                "$2.50 – $4.50/linear ft"),
            ("Transition strips",                            "$25 – $55 each"),
            ("Toilet pull and reset",                        "$120 – $200 per toilet"),
        ],
        "money_tips": [
            "Skip laminate in kitchens, bathrooms, and laundry rooms. The cost difference vs SPC vinyl is $1-2/sq ft, and the water-damage risk reduction is enormous.",
            "Choose AC4 minimum for any common-area room. The $0.75/sq ft upgrade from AC3 to AC4 doubles the floor's lifespan.",
            "Look for products with attached underlayment. Typically saves $0.50-1/sq ft vs separately purchased underlayment.",
            "Avoid promotional 'lifetime warranty' marketing on cheap laminate. Read the warranty fine print — most exclude residential humidity outside 35-55% (which Florida exceeds for most of the year).",
            "Consider mid-range SPC instead. For $1-2/sq ft more, you get 100% waterproof + 2-3x lifespan vs laminate.",
        ],
    },
    "stair-treads": {
        "name": "Stair Tread Replacement",
        "short": "Stair Treads",
        "card_image": "card-stairs.webp",
        "unit": "tread",
        "tiers": [
            ("LVP-Clad Treads",                       25,  40, 40,  65),
            ("Solid Oak Hardwood Treads",             50,  90, 55,  85),
            ("Premium Hardwood (walnut, hickory)",    80, 130, 60,  90),
            ("Porcelain Tile Treads",                 45,  80, 50,  80),
        ],
        "premium_factor": "premium hardwood treads with custom mitered returns",
        "cost_factors": [
            ("Tread material",
             "LVP-clad treads are most affordable — pre-fab pine treads clad with LVP planks. Solid hardwood treads in oak run $50-90/each, premium species (walnut, hickory) $80-130. Porcelain tile treads need non-slip nosing strips. Each material has trade-offs in durability, sound, and refinishability."),
            ("Open vs closed staircase",
             "Closed staircases (walls on both sides) install fastest. Open staircases (one or both sides exposed to a railing) require custom mitered returns on every visible tread end — adds $45-95 per affected tread."),
            ("Riser style and material",
             "Painted white risers (with stained wood treads) is popular and affordable ($25-45/each). Wood risers matching the treads add $20-40/each. Wallpapered or specialty-finished risers add $30-80/each."),
            ("Bullnose style and finish",
             "Standard rounded bullnose is included in tread pricing. Square (modern), beveled (contemporary), or custom-routed bullnoses add $15-50 per tread. Matching stain to existing flooring is typically included; custom color matching adds $20-40 per tread."),
            ("Demolition and substrate prep",
             "Carpet removal: $15-30 per stair. Existing tile or laminate removal: $25-50 per stair. Substrate squeak repair (screwing existing pine treads to stringers): $10-25 per stair. Skirt board / stringer trim work: $35-70 per linear foot."),
        ],
        "hidden_costs": [
            ("Carpet removal (per stair)",                   "$15 – $30"),
            ("Existing tread removal (wood/tile)",           "$25 – $50 per stair"),
            ("Custom mitered returns (open side)",           "$45 – $95 per tread"),
            ("Substrate squeak repair",                       "$10 – $25 per stair"),
            ("Skirt board / stringer trim",                  "$35 – $70 per linear ft"),
            ("Wood risers (vs painted)",                      "$20 – $40 per riser upcharge"),
            ("Custom stain matching",                         "$20 – $40 per tread"),
            ("Quarter-round at wall edges",                  "$3 – $5 per linear ft"),
            ("Newel post or railing repair",                 "$200 – $800 each"),
        ],
        "money_tips": [
            "Choose LVP-clad treads if your main floor is LVP — costs $1,200-1,800 for a typical 14-step staircase vs $3,000-5,500 for solid hardwood.",
            "Painted risers vs wood risers saves $300-600 on a typical staircase without sacrificing aesthetic.",
            "Skip custom bullnose styling unless you have a strong design reason. Standard rounded bullnose looks great in 95% of homes.",
            "If your stairs have an open side, expect 30-40% higher labor cost than closed. Factor this into budgeting upfront.",
            "Address subfloor squeaks before new treads go on. A $200 squeak fix prevents $1,500 of tread loosening over the next 5 years.",
        ],
    },
    "floor-repair": {
        "name": "Floor Repair & Replacement",
        "short": "Floor Repair",
        "card_image": "card-repair.webp",
        "unit": "project",
        "tiers": [
            ("Single-plank or single-tile repair",   50, 150,  150,  300),
            ("Multi-plank or section repair",       200, 500,  300,  900),
            ("Subfloor repair (water/structural)",  300, 800,  500, 1500),
            ("Whole-room partial reflooring",       600,1800, 1000, 3500),
        ],
        "premium_factor": "post-hurricane water damage restoration",
        "cost_factors": [
            ("Type and extent of damage",
             "Single-plank scratches or cracked tiles are quick fixes ($150-450 total). Multi-plank water damage with subfloor involvement runs $1,500-4,500. Whole-room reflooring after major water events runs $3,000-9,000+. Always start with damage assessment ($200-500 — usually credited toward repair if you proceed)."),
            ("Material matching",
             "If your existing flooring is from a major manufacturer (Mohawk, Shaw, COREtec, Daltile, Anderson), we can usually source matching planks or tiles. If the floor is 10+ years old, exact matches may be impossible — expect color variation or partial reflooring of the visible section."),
            ("Subfloor involvement",
             "Surface-only damage is cheapest. Damage that's penetrated to the subfloor (water events, prolonged leaks) requires subfloor repair: removing damaged plywood or OSB, drying any remaining moisture, replacing the substrate, then refloating the new top layer. Subfloor work runs $300-1,500 per affected room."),
            ("Insurance vs cash projects",
             "If the repair is insurance-related (water damage, hurricane), the scope is often defined by your adjuster's quote. We work directly with adjusters and can quote against their scope. Cash projects offer more flexibility but require the homeowner to cover all costs upfront."),
            ("Urgency",
             "Standard repair scheduling is 1-2 weeks out. Emergency scheduling (active water damage, mold growth risk) typically requires 24-48 hour response and adds 15-25% to labor cost. We prioritize emergencies in our schedule."),
        ],
        "hidden_costs": [
            ("Initial damage assessment fee",                "$200 – $500 (often credited)"),
            ("Material sourcing for matching",                "$50 – $200"),
            ("Subfloor moisture remediation",                "$300 – $900 per room"),
            ("Mold testing (if needed)",                      "$200 – $400"),
            ("Disposal/haul-away of damaged material",       "$150 – $400"),
            ("Furniture moving",                              "$200 – $600 per room"),
            ("Toilet pull and reset (bathroom repairs)",     "$120 – $200"),
            ("Insurance documentation report",                "$150 – $300"),
        ],
        "money_tips": [
            "Address damage early. A $300 single-plank repair becomes a $3,000 multi-room project if water spreads to subfloor.",
            "Document everything for insurance. Photos before, during, and after repair. We help with this for insurance-related work.",
            "Get the assessment first, then decide. The $200-500 assessment fee is often credited if you proceed with repair through us.",
            "Match-and-replace beats whole-room reflooring when possible. Saves 60-80% over full replacement when matching material is available.",
            "For partial water damage, consider strategic transitions instead of perfect matching. A clean transition strip between repaired and original sections looks intentional, not patched.",
        ],
    },
}

# Existing posts to skip (already have these slug paths)
EXISTING_POSTS = {
    ("vinyl-plank-flooring", "bradenton"),  # /blog/vinyl-plank-flooring-cost-bradenton-2026/
    ("tile-installation", "sarasota"),       # /blog/tile-installation-cost-sarasota/
}

# ============================================================================
# CITY-SPECIFIC SCENARIO DATA — for project examples
# ============================================================================

# 3 project example scenarios per city, with realistic neighborhood + scope.
# Each scenario template gets parametrized for the specific service.
CITY_SCENARIOS = {
    "bradenton": [
        {"area": "West Bradenton", "type": "1,400 sqft single-family ranch home",
         "context": "1990s slab-built family home with carpet in bedrooms and living areas, original tile in entry and bathrooms. Family of four, two dogs."},
        {"area": "Heritage Harbour", "type": "1,950 sqft golf-community home",
         "context": "2008-built two-story with hardwood throughout main floor showing wear, kitchen tile in good condition. Active retired couple."},
        {"area": "Anna Maria Island (Bradenton Beach)", "type": "1,100 sqft beachfront condo",
         "context": "1970s converted condo, currently used as vacation rental, existing laminate failing from humidity exposure. Year-round STR booking."},
    ],
    "sarasota": [
        {"area": "West of Trail (Cherokee Park)", "type": "2,200 sqft mid-century home",
         "context": "1958-built ranch with original solid hardwood under carpet (discovered during renovation). Owner committed to historic preservation aesthetic."},
        {"area": "Siesta Key", "type": "1,450 sqft beachfront condo",
         "context": "Direct Gulf-front condo with elevated humidity, original 1980s tile worn but well-bonded. Owner uses property full-time December–April."},
        {"area": "Palmer Ranch", "type": "2,650 sqft luxury single-family",
         "context": "2015-built home with builder-grade carpet and tile, owner wants premium upgrade for resale-positioning within 3 years."},
    ],
    "lakewood-ranch": [
        {"area": "Country Club East", "type": "3,200 sqft luxury home",
         "context": "2018 custom build with original wide-plank engineered hardwood in living areas; owner wants matching staircase and bedroom floors to extend the seamless look."},
        {"area": "Star Farms", "type": "2,400 sqft new-build",
         "context": "Brand-new 2024 home with builder-grade vinyl plank and tile; owner upgrading to premium throughout before move-in."},
        {"area": "The Lake Club", "type": "4,100 sqft estate home",
         "context": "2020 luxury build with herringbone hardwood in great room; owner extending similar premium materials to bedroom suites."},
    ],
    "palmetto": [
        {"area": "Riviera Dunes", "type": "2,000 sqft waterfront townhome",
         "context": "2008-built three-story townhouse on the Manatee River, original tile and carpet, owner wants water-tolerant materials throughout."},
        {"area": "Esplanade at Artisan Lakes", "type": "1,750 sqft retirement community home",
         "context": "2019-built single-story home in active-adult community; owners are snowbirds who close up the home from May–October each year."},
        {"area": "Snead Island", "type": "1,300 sqft historic cottage",
         "context": "1955-built waterfront cottage with original hardwood under carpet; owner restoring as a vacation rental investment."},
    ],
    "parrish": [
        {"area": "North River Ranch", "type": "2,200 sqft new-construction",
         "context": "Brand-new 2025 build with builder-grade carpet and basic LVP; family of four upgrading before move-in."},
        {"area": "Silverleaf", "type": "1,950 sqft single-family",
         "context": "2020-built home with builder vinyl plank starting to show wear after 5 years of family use, two large dogs."},
        {"area": "Forest Creek", "type": "2,850 sqft executive home",
         "context": "2017 luxury build with original carpet in bedrooms and living areas; owner upgrading to premium hardwood throughout."},
    ],
    "venice": [
        {"area": "Wellen Park (IslandWalk)", "type": "1,850 sqft retirement community villa",
         "context": "2022-built attached villa with builder LVP throughout; snowbird owners upgrading to premium SPC for full-time conversion."},
        {"area": "Venice Island (Historic District)", "type": "1,100 sqft 1950s cottage",
         "context": "Restored 1955 cottage near downtown Venice; owner replacing original tile with period-appropriate hardwood and adding modern bathroom tile."},
        {"area": "Pelican Pointe", "type": "2,150 sqft golf-community home",
         "context": "2003-built home with worn carpet in living areas, original tile in baths and kitchen still good; family of three."},
    ],
    "tampa": [
        {"area": "Hyde Park", "type": "2,800 sqft historic home",
         "context": "1924-built craftsman bungalow with original heart-pine floors under 1980s carpet; restoration project bringing back original character."},
        {"area": "Wesley Chapel", "type": "2,350 sqft suburban home",
         "context": "2019-built family home with builder-grade laminate failing from kitchen water exposure; owners switching to SPC throughout main floor."},
        {"area": "Channelside (downtown condo)", "type": "1,200 sqft luxury condo",
         "context": "2007-built downtown condo with original tile in great condition; owner adding hardwood-look to bedrooms while preserving entry tile."},
    ],
    "st-petersburg": [
        {"area": "Old Northeast", "type": "2,100 sqft 1920s historic home",
         "context": "1922 Mediterranean-revival with original mosaic tile in foyer and bath; owner restoring original wood floors and adding modern bathroom tile."},
        {"area": "Snell Isle", "type": "3,400 sqft waterfront luxury home",
         "context": "1985-built waterfront home extensively renovated; owner upgrading to premium wide-plank hardwood and large-format porcelain."},
        {"area": "St. Pete Beach", "type": "1,500 sqft Gulf-front condo",
         "context": "1979 oceanfront condo used as vacation rental; existing floors damaged by salt-air exposure, full reflooring with waterproof materials."},
    ],
    "ellenton": [
        {"area": "Colony Cove", "type": "1,400 sqft 55+ resort-community home",
         "context": "Manufactured/resort-community home with original carpet throughout; retired owners want easy-clean, allergy-friendly waterproof vinyl plank for full-time living."},
        {"area": "East Ellenton (riverfront)", "type": "1,800 sqft single-family home",
         "context": "1990s deed-restricted home near the Manatee River with worn carpet in bedrooms and living areas, original tile in baths; family of three replacing carpet with LVP."},
        {"area": "Covered Bridge Estates", "type": "2,100 sqft two-story home",
         "context": "2006-built family home with builder-grade carpet and laminate showing wear after years of use; owner upgrading main floor to porcelain tile and SPC."},
    ],
    "ruskin": [
        {"area": "Hawks Point", "type": "2,200 sqft new-construction home",
         "context": "2022-built family home with builder-grade carpet and basic LVP; young family upgrading to premium waterproof vinyl plank throughout main floor."},
        {"area": "Mira Lago", "type": "1,950 sqft single-family home",
         "context": "2018 home with builder carpet in bedrooms wearing fast with two kids and a dog; owners switching to scratch-resistant SPC and tile."},
        {"area": "Bahia Lakes", "type": "2,600 sqft two-story home",
         "context": "2015-built home with original carpet on stairs and second floor; owner adding matching engineered hardwood and stair treads for a seamless look."},
    ],
    "apollo-beach": [
        {"area": "MiraBay", "type": "2,800 sqft waterfront single-family home",
         "context": "2016 canal-front home with builder tile and carpet; affluent owners upgrading to wide-plank engineered hardwood and large-format porcelain, with attention to canal humidity."},
        {"area": "Waterset", "type": "2,400 sqft new-build home",
         "context": "Brand-new 2024 home with builder-grade LVP and carpet; family upgrading to premium SPC and tile before fully moving in."},
        {"area": "Bimini Bay", "type": "1,600 sqft waterfront condo",
         "context": "Older waterfront condo near the marina with laminate failing from salt-air humidity; owner reflooring with fully waterproof vinyl plank."},
    ],
    "sun-city-center": [
        {"area": "Kings Point", "type": "1,500 sqft 55+ gated-community villa",
         "context": "Original 1990s carpet throughout; retired owners want slip-resistant, easy-clean waterproof vinyl plank with low-profile transitions for safe, accessible aging-in-place."},
        {"area": "The Preserve at La Paloma", "type": "1,900 sqft single-story home",
         "context": "2015-built home with builder carpet in bedrooms and living areas; snowbird owners replacing all carpet with allergy-friendly SPC before full-time retirement."},
        {"area": "Renaissance", "type": "2,200 sqft golf-community home",
         "context": "Active-adult home with worn carpet and dated tile; owners upgrading to premium wood-look porcelain and luxury vinyl plank throughout."},
    ],
    "north-port": [
        {"area": "Wellen Park (West Villages)", "type": "2,300 sqft new-construction home",
         "context": "2023-built home with builder-grade carpet and basic LVP; growing family upgrading to premium waterproof vinyl plank and tile throughout main floor."},
        {"area": "Bobcat Trail", "type": "2,000 sqft golf-community home",
         "context": "2004-built home with original carpet in bedrooms and living areas, tile in wet areas; owners replacing carpet with scratch-resistant SPC."},
        {"area": "Heron Creek", "type": "2,650 sqft executive home",
         "context": "2008 luxury build with worn carpet on stairs and second floor; owner adding matching engineered hardwood and stair treads throughout."},
    ],
    "nokomis": [
        {"area": "Calusa Lakes", "type": "2,500 sqft Mediterranean golf-community home",
         "context": "Deed-restricted home with original tile and carpet; affluent owners upgrading to wide-plank European white oak and large-format porcelain."},
        {"area": "Sorrento East", "type": "1,900 sqft single-family home",
         "context": "1990s home near the water with worn carpet and dated tile; owner reflooring with premium waterproof vinyl plank and porcelain tile."},
        {"area": "Casey Key", "type": "2,800 sqft barrier-island luxury home",
         "context": "Gulf-front home with elevated salt-air humidity; owner installing premium herringbone hardwood in living areas and waterproof materials in coastal-exposed rooms."},
    ],
}

# City-specific bonus FAQs per city (added to the standard FAQ list)
CITY_BONUS_FAQS = {
    "bradenton": [
        ("Do you handle Bradenton beachfront condos differently?", "Yes — beachfront properties (Anna Maria Island, Bradenton Beach, Holmes Beach) have elevated humidity and salt-air exposure. We always specify SPC vinyl plank or porcelain tile for these projects, never laminate or solid hardwood. Subfloor moisture testing is more rigorous, and we use higher-grade adhesives rated for elevated moisture conditions."),
        ("How long does Bradenton labor scheduling take?", "Standard scheduling is 1-2 weeks from contract signing for residential projects. During hurricane season (June-November) we sometimes have shorter availability for emergency water-damage repairs that take priority. New-construction project scheduling typically runs 3-4 weeks out."),
    ],
    "sarasota": [
        ("Why does Sarasota flooring tend to cost more than Bradenton?", "Sarasota labor rates run roughly 5-7% higher than Bradenton due to market positioning and material expectations. Sarasota homeowners typically choose premium-tier materials (wide-plank hardwood, large-format porcelain) more often, which involves more labor per square foot. The actual labor delta is small — most of the price difference is product selection."),
        ("Do you work in Siesta Key, Lido Key, and Longboat Key?", "Yes — we work all of Sarasota County including the keys. Beach-area projects require more careful subfloor moisture management due to salt-air exposure and elevated humidity. We typically recommend SPC vinyl plank or porcelain tile for key properties."),
    ],
    "lakewood-ranch": [
        ("Is Lakewood Ranch flooring really more expensive?", "Slightly. Lakewood Ranch labor rates run 8-10% higher than Manatee County average, driven by neighborhood expectations and the prevalence of premium materials. The bigger driver of total project cost is material choice — Lakewood Ranch buyers typically choose wide-plank hardwood or large-format porcelain over standard products, which has bigger cost impact than the labor delta."),
        ("Which Lakewood Ranch villages do you serve?", "All of them. We work regularly in Country Club East, The Lake Club, Esplanade, Star Farms, Sweetwater, Polo Run, Del Webb, Cresswind, Greenbrook, Edgewater, Mallory Park, Lorraine Lakes, Indigo, and Waterside Place. We've completed flooring projects in 50+ Lakewood Ranch homes."),
    ],
    "palmetto": [
        ("Is Triangle Flooring really based in Palmetto?", "Yes — our headquarters is at 8737 Royal Acacia Ave, Palmetto, FL 34221. We've completed more flooring projects in Palmetto than in any other city. As locals, we know the neighborhoods, the older slab-construction homes, and the specific moisture characteristics of riverfront properties on the Manatee."),
        ("Do you offer same-day quotes in Palmetto?", "For Palmetto residents, often yes — we can sometimes do same-day in-home measurements and emailed written quotes within 24 hours. Call us first thing in the morning at (941) 402-6861 if you need fast turnaround."),
    ],
    "parrish": [
        ("Why is Parrish flooring labor 5% cheaper than Bradenton?", "Parrish has lower commercial real estate costs and less market premium than coastal Bradenton, which translates to slightly lower labor rates. The actual quality of work is identical — we use the same crew with the same 42-Point Standard regardless of which city the project is in."),
        ("Do you serve all of North River Ranch and Star Farms?", "Yes — both communities are growing rapidly and we work there regularly. We've completed 30+ projects in Parrish master-planned communities including North River Ranch, Star Farms (Parrish portion), Crosscreek, Forest Creek, Silverleaf, and Aviary at Rutland Ranch."),
    ],
    "venice": [
        ("Do you handle Wellen Park new construction projects?", "Yes — Wellen Park has been one of our growth markets since 2022. We work directly with homeowners pre-closing to handle builder-grade flooring upgrades before move-in. Coordinating with builders requires specific scheduling, which we manage on your behalf."),
        ("Are Venice snowbird homes treated differently?", "Sometimes. Snowbird homes that close up for 4-6 months face elevated humidity spikes when AC is set high. We recommend SPC vinyl plank or porcelain tile in these properties — both handle the seasonal humidity swing without dimensional issues that could affect hardwood."),
    ],
    "tampa": [
        ("Tampa is a big metro — do you cover all of it?", "We cover most of Hillsborough County including South Tampa (Hyde Park, Davis Islands, Bayshore, Channelside, Westshore), the suburbs (Wesley Chapel, Brandon, Riverview, New Tampa), and northwestern areas (Carrollwood, Lutz, Westchase). For the few outer-county areas we don't cover routinely, we can usually accommodate larger projects with advance scheduling."),
        ("Do Tampa labor rates differ from suburban areas?", "Slightly. Urban Tampa (downtown, South Tampa) labor runs at our highest rates due to parking, access, and urban logistics. Suburban Tampa (Wesley Chapel, Riverview) is comparable to Bradenton/Sarasota suburban rates. The difference is usually 5-8% on labor only."),
    ],
    "st-petersburg": [
        ("Do you work on historic Old Northeast and Snell Isle homes?", "Yes — historic St. Pete restorations are some of our favorite projects. Old Northeast and Snell Isle homes from the 1920s-1940s often have original heart-pine or oak floors hidden under carpet. We can refinish these (when viable) or match new engineered hardwood to the original character."),
        ("Are St. Pete Beach and Treasure Island included?", "Yes. Beach area properties require more careful moisture management due to salt-air exposure, but we do beachfront work regularly. We typically recommend porcelain tile or premium SPC for direct waterfront/beachfront properties — not laminate or solid hardwood."),
    ],
}

# ============================================================================
# HELPERS
# ============================================================================

def compute_pricing_table(svc_slug, city_slug):
    """Build pricing table HTML with city-specific labor multiplier applied."""
    svc = SVC_PRICING[svc_slug]
    mult = CITY_LABOR_MULT[city_slug]
    unit = svc['unit']
    
    rows = []
    for tier_name, mat_low, mat_high, lab_low, lab_high in svc['tiers']:
        adj_lab_low = lab_low * mult
        adj_lab_high = lab_high * mult
        total_low = mat_low + adj_lab_low
        total_high = mat_high + adj_lab_high
        
        if unit == "tread":
            mat_str = f"${mat_low:.0f}–${mat_high:.0f}"
            lab_str = f"${adj_lab_low:.0f}–${adj_lab_high:.0f}"
            tot_str = f"${total_low:.0f}–${total_high:.0f}"
        elif unit == "project":
            mat_str = f"${mat_low:.0f}–${mat_high:.0f}"
            lab_str = f"${adj_lab_low:.0f}–${adj_lab_high:.0f}"
            tot_str = f"${total_low:.0f}–${total_high:.0f}"
        else:  # sq ft
            mat_str = f"${mat_low:.2f}–${mat_high:.2f}"
            lab_str = f"${adj_lab_low:.2f}–${adj_lab_high:.2f}"
            tot_str = f"${total_low:.2f}–${total_high:.2f}"
        
        rows.append(f"<tr><td><strong>{tier_name}</strong></td><td>{mat_str}</td><td>{lab_str}</td><td><strong>{tot_str}</strong></td></tr>")
    
    unit_label = {"sq ft": "/sq ft", "tread": "/tread", "project": "(per project)"}[unit]
    
    return f"""<div style="overflow-x:auto;margin:1.6rem 0">
  <table style="width:100%;border-collapse:collapse;background:#fff;border-radius:14px;overflow:hidden;box-shadow:var(--shadow-sm);min-width:560px;font-size:.95rem">
    <thead style="background:linear-gradient(135deg,var(--navy-dark),var(--navy));color:#fff">
      <tr>
        <th style="padding:13px 16px;text-align:left;font-family:var(--font-head);font-weight:600">Tier</th>
        <th style="padding:13px 16px;text-align:left;font-family:var(--font-head);font-weight:600">Material {unit_label}</th>
        <th style="padding:13px 16px;text-align:left;font-family:var(--font-head);font-weight:600">Labor {unit_label}</th>
        <th style="padding:13px 16px;text-align:left;font-family:var(--font-head);font-weight:600;background:rgba(224,122,43,.2)">Total {unit_label}</th>
      </tr>
    </thead>
    <tbody>
      {"".join(f'<tr style="border-bottom:1px solid var(--gray-border);' + ('background:var(--gray-light)' if i%2==1 else '') + '">' + r[4:] for i, r in enumerate(rows))}
    </tbody>
  </table>
</div>"""

def compute_min_max(svc_slug, city_slug):
    """Return (min_total, max_total) for the service in the city."""
    svc = SVC_PRICING[svc_slug]
    mult = CITY_LABOR_MULT[city_slug]
    
    all_lows, all_highs = [], []
    for tier_name, mat_low, mat_high, lab_low, lab_high in svc['tiers']:
        all_lows.append(mat_low + lab_low * mult)
        all_highs.append(mat_high + lab_high * mult)
    return (min(all_lows), max(all_highs))

def build_project_examples(svc_slug, city_slug):
    """Build 3 realistic project example scenarios for this service+city."""
    svc = SVC_PRICING[svc_slug]
    mult = CITY_LABOR_MULT[city_slug]
    scenarios = CITY_SCENARIOS[city_slug]
    
    # Compute pricing for typical project sizes per service
    examples = []
    
    # Scenario 1: Mid-tier project
    s1 = scenarios[0]
    if svc['unit'] == 'sq ft':
        # use mid-range tier
        tier = svc['tiers'][1]  # mid-range
        mat = (tier[1] + tier[2]) / 2
        lab = (tier[3] + tier[4]) / 2 * mult
        # Estimate sqft based on home size
        sqft_est = int(re.search(r'(\d{1,3},?\d{3})', s1['type']).group(1).replace(',','')) * 0.7  # 70% of home size for flooring
        sqft_est = round(sqft_est / 50) * 50
        mat_total = sqft_est * mat
        lab_total = sqft_est * lab
        prep_total = round(sqft_est * 0.6) + 800  # subfloor + transitions
        if 'carpet' in s1['context'].lower() or 'tile' in s1['context'].lower():
            removal = sqft_est * 2
        else:
            removal = 0
        total = mat_total + lab_total + prep_total + removal
        examples.append({
            "title": f"Mid-Range {svc['short']} in {s1['area']}",
            "type": s1['type'],
            "context": s1['context'],
            "scope": f"Full project covering approximately {sqft_est:,} sq ft of mid-range {svc['short'].lower()}, including subfloor prep, all transitions, and quarter-round.",
            "breakdown": [
                ("Material",   f"${mat_total:,.0f}"),
                ("Labor",       f"${lab_total:,.0f}"),
                ("Subfloor prep & transitions", f"${prep_total:,.0f}"),
                ("Existing flooring removal", f"${removal:,.0f}" if removal else "Included"),
            ],
            "total": f"${total:,.0f}",
            "per_unit": f"~${total/sqft_est:.2f}/sq ft all-in",
        })
    elif svc['unit'] == 'tread':
        steps = 14
        tier = svc['tiers'][1]  # solid oak
        mat_per = (tier[1] + tier[2]) / 2
        lab_per = (tier[3] + tier[4]) / 2 * mult
        risers = 35 * steps  # painted risers
        demo = 22 * steps    # carpet removal
        total = (mat_per + lab_per) * steps + risers + demo
        examples.append({
            "title": f"Solid Hardwood Treads in {s1['area']}",
            "type": s1['type'],
            "context": s1['context'],
            "scope": f"Replacement of {steps}-step staircase: existing carpet removed, solid oak treads installed with painted risers, custom mitered returns where stair has open side.",
            "breakdown": [
                ("Treads (material + labor)",   f"${(mat_per+lab_per)*steps:,.0f}"),
                ("Painted risers",               f"${risers:,.0f}"),
                ("Carpet removal",                f"${demo:,.0f}"),
            ],
            "total": f"${total:,.0f}",
            "per_unit": f"~${total/steps:.0f}/step",
        })
    else:  # project
        # Repair scenario
        tier = svc['tiers'][2]  # subfloor repair
        mat_low = tier[1]
        lab_low = tier[3] * mult
        total = mat_low + lab_low + 250  # plus assessment
        examples.append({
            "title": f"Subfloor Water-Damage Repair in {s1['area']}",
            "type": s1['type'],
            "context": s1['context'],
            "scope": f"Damage assessment, removal of damaged plywood subfloor in affected area (approximately 60-90 sq ft), replacement and refloating of new top flooring layer to match existing floor.",
            "breakdown": [
                ("Damage assessment (credited)",   f"$250"),
                ("Material (subfloor + matching top)", f"${mat_low:,.0f}"),
                ("Labor",                          f"${lab_low:,.0f}"),
            ],
            "total": f"${total:,.0f}",
            "per_unit": f"Single-room repair",
        })

    # Scenario 2: Premium project
    s2 = scenarios[1]
    if svc['unit'] == 'sq ft':
        tier = svc['tiers'][2]  # premium
        mat = (tier[1] + tier[2]) / 2
        lab = (tier[3] + tier[4]) / 2 * mult
        sqft_est = int(re.search(r'(\d{1,3},?\d{3})', s2['type']).group(1).replace(',','')) * 0.65
        sqft_est = round(sqft_est / 50) * 50
        mat_total = sqft_est * mat
        lab_total = sqft_est * lab
        prep_total = round(sqft_est * 0.8) + 1100
        removal = sqft_est * 2.5
        total = mat_total + lab_total + prep_total + removal
        examples.append({
            "title": f"Premium {svc['short']} in {s2['area']}",
            "type": s2['type'],
            "context": s2['context'],
            "scope": f"Approximately {sqft_est:,} sq ft of premium {svc['short'].lower()} with substrate moisture testing, vapor barrier, custom transitions, and matching baseboards.",
            "breakdown": [
                ("Material (premium tier)", f"${mat_total:,.0f}"),
                ("Labor",                    f"${lab_total:,.0f}"),
                ("Subfloor prep + vapor barrier",  f"${prep_total:,.0f}"),
                ("Existing flooring removal",      f"${removal:,.0f}"),
            ],
            "total": f"${total:,.0f}",
            "per_unit": f"~${total/sqft_est:.2f}/sq ft all-in",
        })
    elif svc['unit'] == 'tread':
        steps = 16
        tier = svc['tiers'][2]  # premium hardwood
        mat_per = (tier[1] + tier[2]) / 2
        lab_per = (tier[3] + tier[4]) / 2 * mult
        risers = 65 * steps  # wood risers
        demo = 30 * steps    # tile/laminate removal
        miters = 70 * steps  # custom mitered returns
        total = (mat_per + lab_per) * steps + risers + demo + miters
        examples.append({
            "title": f"Premium Hardwood Treads in {s2['area']}",
            "type": s2['type'],
            "context": s2['context'],
            "scope": f"Replacement of {steps}-step open-side staircase: existing material removed, premium hardwood treads with custom mitered returns, matching wood risers, full skirt board work.",
            "breakdown": [
                ("Treads",                       f"${(mat_per+lab_per)*steps:,.0f}"),
                ("Wood risers",                  f"${risers:,.0f}"),
                ("Custom mitered returns",       f"${miters:,.0f}"),
                ("Demolition",                   f"${demo:,.0f}"),
            ],
            "total": f"${total:,.0f}",
            "per_unit": f"~${total/steps:.0f}/step (open-side premium)",
        })
    else:  # project
        tier = svc['tiers'][3]  # whole-room
        mat_avg = (tier[1] + tier[2]) / 2
        lab_avg = (tier[3] + tier[4]) / 2 * mult
        total = mat_avg + lab_avg + 800  # plus scope add-ons
        examples.append({
            "title": f"Partial Reflooring in {s2['area']}",
            "type": s2['type'],
            "context": s2['context'],
            "scope": f"Whole-room partial reflooring of approximately 250-350 sq ft after water damage to existing flooring. Includes substrate moisture remediation, transition strips to existing floor, and matching of original material.",
            "breakdown": [
                ("Material (matching existing)",   f"${mat_avg:,.0f}"),
                ("Labor",                          f"${lab_avg:,.0f}"),
                ("Substrate remediation + transitions", f"$800"),
            ],
            "total": f"${total:,.0f}",
            "per_unit": f"Whole-room partial",
        })

    # Scenario 3: Budget/practical project
    s3 = scenarios[2]
    if svc['unit'] == 'sq ft':
        tier = svc['tiers'][0]  # entry-level
        mat = (tier[1] + tier[2]) / 2
        lab = (tier[3] + tier[4]) / 2 * mult
        sqft_est = int(re.search(r'(\d{1,3},?\d{3})', s3['type']).group(1).replace(',','')) * 0.75
        sqft_est = round(sqft_est / 50) * 50
        mat_total = sqft_est * mat
        lab_total = sqft_est * lab
        prep_total = round(sqft_est * 0.4) + 500
        removal = sqft_est * 1.8
        total = mat_total + lab_total + prep_total + removal
        examples.append({
            "title": f"Budget-Friendly {svc['short']} in {s3['area']}",
            "type": s3['type'],
            "context": s3['context'],
            "scope": f"Approximately {sqft_est:,} sq ft of entry-level tier {svc['short'].lower()} with standard subfloor prep and transitions. Designed to maximize value over premium aesthetics.",
            "breakdown": [
                ("Material (entry-tier)",   f"${mat_total:,.0f}"),
                ("Labor",                    f"${lab_total:,.0f}"),
                ("Subfloor prep & transitions", f"${prep_total:,.0f}"),
                ("Existing flooring removal", f"${removal:,.0f}"),
            ],
            "total": f"${total:,.0f}",
            "per_unit": f"~${total/sqft_est:.2f}/sq ft all-in",
        })
    elif svc['unit'] == 'tread':
        steps = 13
        tier = svc['tiers'][0]  # LVP-clad
        mat_per = (tier[1] + tier[2]) / 2
        lab_per = (tier[3] + tier[4]) / 2 * mult
        risers = 35 * steps  # painted
        demo = 22 * steps
        total = (mat_per + lab_per) * steps + risers + demo
        examples.append({
            "title": f"LVP-Clad Treads in {s3['area']}",
            "type": s3['type'],
            "context": s3['context'],
            "scope": f"Replacement of {steps}-step closed-side staircase with LVP-clad treads matching the home's main-floor LVP, painted risers, and skirt board.",
            "breakdown": [
                ("LVP-clad treads",             f"${(mat_per+lab_per)*steps:,.0f}"),
                ("Painted risers",               f"${risers:,.0f}"),
                ("Carpet removal",                f"${demo:,.0f}"),
            ],
            "total": f"${total:,.0f}",
            "per_unit": f"~${total/steps:.0f}/step",
        })
    else:  # project
        tier = svc['tiers'][1]  # multi-plank
        mat_avg = (tier[1] + tier[2]) / 2
        lab_avg = (tier[3] + tier[4]) / 2 * mult
        total = mat_avg + lab_avg
        examples.append({
            "title": f"Multi-Plank Repair in {s3['area']}",
            "type": s3['type'],
            "context": s3['context'],
            "scope": f"Replacement of 6-12 damaged planks/tiles with matching material from same manufacturer batch when available, or color-coordinated alternatives.",
            "breakdown": [
                ("Material (matching)",   f"${mat_avg:,.0f}"),
                ("Labor",                  f"${lab_avg:,.0f}"),
            ],
            "total": f"${total:,.0f}",
            "per_unit": f"Multi-plank section",
        })
    
    return examples

def build_pricing_post(svc_slug, city_slug):
    """Generate one complete pricing post for a (service, city) combination."""
    if (svc_slug, city_slug) in EXISTING_POSTS:
        return None  # skip — already exists with different URL
    
    svc = SVC_PRICING[svc_slug]
    city = CITIES[city_slug]
    mult = CITY_LABOR_MULT[city_slug]
    min_total, max_total = compute_min_max(svc_slug, city_slug)
    
    slug = f"{svc_slug}-cost-{city_slug}"
    PATH = f"/blog/{slug}/"
    
    unit = svc['unit']
    if unit == 'sq ft':
        price_summary = f"${min_total:.2f}–${max_total:.2f} per square foot installed"
    elif unit == 'tread':
        price_summary = f"${min_total:.0f}–${max_total:.0f} per tread installed"
    else:
        price_summary = f"${min_total:.0f}–${max_total:.0f} per project"
    
    TITLE_RAW = f"{svc['short']} Cost in {city['name']}, FL (2026 Guide)"
    if len(TITLE_RAW) > 60:
        TITLE_RAW = f"{svc['short']} Cost {city['name']}, FL 2026"
    TITLE = f"{TITLE_RAW} | Triangle Flooring"
    if len(TITLE) > 65:
        TITLE = TITLE_RAW
    
    DESC = f"2026 {svc['short'].lower()} pricing in {city['name']}, FL. Material, labor, hidden costs, real project examples. Free quote 24h. {price_summary}."
    if len(DESC) > 158: DESC = DESC[:155] + "..."
    
    H1 = f"{svc['short']} Cost in {city['name']}, FL — 2026 Pricing Guide"
    
    bc_items = [("Home","/"),("Blog","/blog/"),(f"{svc['short']} Cost {city['name']}", None)]
    bc_schema = render_breadcrumb_schema(bc_items)
    
    # === Build pricing table ===
    pricing_table_html = compute_pricing_table(svc_slug, city_slug)
    
    # === Build cost factors section ===
    factors_html = ""
    for i, (factor_name, factor_desc) in enumerate(svc['cost_factors'], 1):
        factors_html += f"""<h3 style="margin:1.8rem 0 .8rem;font-size:1.2rem;color:var(--navy)">{i}. {factor_name}</h3>
        <p>{factor_desc}</p>"""
    
    # === Build city-specific labor justification ===
    if mult < 1.0:
        labor_note = f"Labor rates in {city['name']} run roughly {int((1-mult)*100)}% lower than the {city['county']} average — driven by lower commercial real estate costs and less premium market positioning compared to coastal Bradenton or Sarasota. The actual quality of work is identical."
    elif mult > 1.05:
        labor_note = f"Labor rates in {city['name']} run roughly {int((mult-1)*100)}% higher than the regional baseline. This reflects {city['name']}'s market positioning — homeowners here typically expect premium materials and more meticulous installation, which involves slightly more labor per project."
    else:
        labor_note = f"Labor rates in {city['name']} are at the regional baseline — neither the cheapest nor the most expensive market in our service area. Pricing is straightforward and predictable."
    
    # === Build project examples ===
    examples = build_project_examples(svc_slug, city_slug)
    examples_html = ""
    for ex in examples:
        breakdown_html = "".join(f'<li><strong>{label}:</strong> {val}</li>' for label, val in ex['breakdown'])
        examples_html += f"""<div style="background:var(--gray-light);padding:1.6rem 1.8rem;border-radius:14px;margin-bottom:1.5rem;border-left:5px solid var(--cerulean)">
          <h3 style="margin:0 0 .6rem;color:var(--navy);font-size:1.15rem">{ex['title']}</h3>
          <p style="font-size:.92rem;color:var(--gray);margin-bottom:.7rem"><strong>Property:</strong> {ex['type']} · {ex['context']}</p>
          <p style="font-size:.95rem;margin-bottom:.7rem"><strong>Scope:</strong> {ex['scope']}</p>
          <ul style="margin:0 0 .8rem 1.4rem;font-size:.93rem">{breakdown_html}</ul>
          <p style="margin:0;font-size:1.05rem;color:var(--navy);font-weight:700">Project total: {ex['total']} <span style="font-size:.85rem;color:var(--gray);font-weight:400">({ex['per_unit']})</span></p>
        </div>"""
    
    # === Build hidden costs table ===
    hidden_costs_html = "<tbody>"
    for i, (item, cost) in enumerate(svc['hidden_costs']):
        bg = 'background:var(--gray-light)' if i%2==1 else ''
        hidden_costs_html += f'<tr style="border-bottom:1px solid var(--gray-border);{bg}"><td style="padding:11px 16px;font-weight:600">{item}</td><td style="padding:11px 16px">{cost}</td></tr>'
    hidden_costs_html += "</tbody>"
    
    # === Money tips ===
    tips_html = "".join(f'<li style="margin-bottom:.7rem;line-height:1.65">{tip}</li>' for tip in svc['money_tips'])
    
    # === Inline embedded quote form (mid-article CTA) ===
    inline_form_html = f"""<div style="background:linear-gradient(135deg,#1A4F8C,#2E8DD9);color:#fff;padding:2rem;border-radius:18px;margin:2.5rem 0;box-shadow:var(--shadow-lg)">
  <h3 style="color:#fff;font-size:1.4rem;margin-bottom:.5rem;font-family:var(--font-head)">Get Your Free {svc['short']} Quote in {city['name']}</h3>
  <p style="color:rgba(255,255,255,.9);margin-bottom:1.4rem;font-size:.97rem">Itemized written quote within 24 hours · No obligation · Same crew that quotes does the install.</p>
  
  <form action="https://api.web3forms.com/submit" method="POST" style="display:grid;grid-template-columns:1fr 1fr;gap:.9rem;margin-bottom:1rem">
    <input type="hidden" name="access_key" value="d811c86f-d17c-4768-baaa-e6f55aceeb57">
    <input type="hidden" name="from_name" value="Triangle Flooring Pricing Post">
    <input type="hidden" name="redirect" value="https://triangle-floor.com/thanks/">
    <input type="checkbox" name="botcheck" style="display:none" tabindex="-1" autocomplete="off">
    <input type="text" name="name" placeholder="Your name" required style="padding:12px 14px;border-radius:10px;border:none;font-size:.95rem;font-family:inherit">
    <input type="tel" name="phone" placeholder="Phone number" required style="padding:12px 14px;border-radius:10px;border:none;font-size:.95rem;font-family:inherit">
    <input type="text" name="address" placeholder="{city['name']}, FL address (or neighborhood)" style="padding:12px 14px;border-radius:10px;border:none;font-size:.95rem;font-family:inherit;grid-column:1/-1">
    <input type="hidden" name="service" value="{svc['name']}">
    <input type="hidden" name="city" value="{city['name']}">
    <input type="hidden" name="source" value="pricing_post">
    <textarea name="message" placeholder="Tell us about your project (optional)" style="padding:12px 14px;border-radius:10px;border:none;font-size:.95rem;font-family:inherit;grid-column:1/-1;min-height:80px;resize:vertical"></textarea>
    <button type="submit" style="grid-column:1/-1;padding:14px 24px;border-radius:50px;background:#E07A2B;color:#fff;border:none;font-family:var(--font-head);font-weight:700;font-size:1rem;cursor:pointer;letter-spacing:.02em">Send My Free Quote Request →</button>
  </form>
  
  <div style="display:flex;align-items:center;gap:.8rem;justify-content:center;margin-top:1.2rem;padding-top:1.2rem;border-top:1px solid rgba(255,255,255,.2);flex-wrap:wrap">
    <span style="color:rgba(255,255,255,.85);font-size:.9rem">Or message us directly:</span>
    <a href="https://wa.me/19414026861?text=Hi%20Triangle%20Flooring%2C%20I%27m%20interested%20in%20a%20{svc['short'].replace(' ','%20')}%20quote%20in%20{city['name'].replace(' ','%20')}." target="_blank" rel="noopener" style="background:#25D366;color:#fff;padding:9px 18px;border-radius:50px;font-weight:600;font-size:.9rem;display:inline-flex;align-items:center;gap:6px;text-decoration:none">
      <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.71.306 1.263.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
      WhatsApp
    </a>
    <a href="tel:+19414026861" style="background:#fff;color:var(--navy);padding:9px 18px;border-radius:50px;font-weight:600;font-size:.9rem;text-decoration:none">📞 (941) 402-6861</a>
  </div>
</div>"""
    
    # === Build city-specific FAQs (mix generic + city-specific) ===
    bonus_faqs = CITY_BONUS_FAQS.get(city_slug, [])
    generic_faqs = [
        (f"How much does {svc['short'].lower()} installation cost in {city['name']} in 2026?",
         f"For 2026, {svc['short'].lower()} installation in {city['name']}, FL ranges from {price_summary}. Most residential projects fall in the mid-range tier. Material cost typically accounts for 40-55% of the total, labor 35-45%, and prep/transitions 10-15%."),
        (f"What's included in your {city['name']} {svc['short'].lower()} quote?",
         f"Every quote includes itemized line items: material cost, labor cost, removal/disposal, subfloor prep, transition strips, baseboards, and waste percentage. The number on your contract is the number on your final invoice — no surprise upcharges mid-project."),
        (f"How long does a typical {svc['short'].lower()} project take in {city['name']}?",
         f"Project timelines depend on size and complexity. Single-room projects take 1-3 days. 1,200-1,500 sq ft full-area installs take 2-5 working days for most {svc['short'].lower()} projects. We provide a clear daily schedule when you sign the quote."),
    ]
    all_faqs = generic_faqs + bonus_faqs
    
    faq_html = ""
    faq_schema_items = []
    for q, a in all_faqs:
        faq_html += f'<details class="faq-item"><summary>{q}</summary><div class="faq-content"><p>{a}</p></div></details>'
        plain_a = re.sub(r'<[^>]+>', '', a).strip()
        faq_schema_items.append({"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":plain_a}})
    
    faq_schema = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":faq_schema_items}
    
    # === Article schema ===
    body_for_word_count = factors_html + examples_html + faq_html  # rough estimate input
    word_count = 2300  # we'll estimate; actual computed after rendering
    
    article_schema = render_article_schema(
        H1, DESC, slug, svc['card_image'],
        "2026-05-04T08:00:00-04:00", "2026-05-04T08:00:00-04:00",
        word_count, "Pricing Guides"
    )
    
    # === Local business schema (geo) ===
    business_schema = render_local_business_schema(
        f"{svc['short']} Pricing in {city['name']}",
        f"2026 {svc['short'].lower()} cost guide for {city['name']}, FL homeowners.",
        PATH, city=city['name']
    )
    
    # === Service schema ===
    service_schema = {
        "@context": "https://schema.org",
        "@type": "Service",
        "@id": f"https://{DOMAIN}{PATH}#service",
        "serviceType": svc['name'],
        "name": f"{svc['name']} in {city['name']}, FL",
        "description": f"Professional {svc['short'].lower()} installation in {city['name']}, FL. {price_summary}.",
        "areaServed": {"@type": "City", "name": city['name'], "addressRegion": "FL", "addressCountry": "US"},
        "provider": {"@id": f"https://{DOMAIN}/#organization"},
        "offers": {
            "@type": "AggregateOffer",
            "lowPrice": f"{min_total:.2f}",
            "highPrice": f"{max_total:.2f}",
            "priceCurrency": "USD",
            "priceSpecification": {"@type": "UnitPriceSpecification", "unitText": svc['unit']},
        },
    }
    
    # === Related links ===
    # 3 same-service in nearby cities, 3 same-city other services, 2 main blog posts
    nearby_cities = [c for c in CITIES if c != city_slug][:3]
    other_services = [s for s in SVC_PRICING if s != svc_slug][:3]
    
    related_links = []
    for nc in nearby_cities:
        if (svc_slug, nc) in EXISTING_POSTS:
            # link to the existing custom URL instead
            if (svc_slug, nc) == ("vinyl-plank-flooring", "bradenton"):
                related_links.append((f"{svc['short']} Cost in {CITIES[nc]['name']}", "/blog/vinyl-plank-flooring-cost-bradenton-2026/", "Same service, different city"))
            elif (svc_slug, nc) == ("tile-installation", "sarasota"):
                related_links.append((f"{svc['short']} Cost in {CITIES[nc]['name']}", "/blog/tile-installation-cost-sarasota/", "Same service, different city"))
        else:
            related_links.append((f"{svc['short']} Cost in {CITIES[nc]['name']}", f"/blog/{svc_slug}-cost-{nc}/", "Same service, different city"))
    for os_ in other_services:
        if (os_, city_slug) in EXISTING_POSTS:
            if (os_, city_slug) == ("vinyl-plank-flooring", "bradenton"):
                related_links.append((f"{SVC_PRICING[os_]['short']} Cost in {city['name']}", "/blog/vinyl-plank-flooring-cost-bradenton-2026/", "Different service, same city"))
            elif (os_, city_slug) == ("tile-installation", "sarasota"):
                related_links.append((f"{SVC_PRICING[os_]['short']} Cost in {city['name']}", "/blog/tile-installation-cost-sarasota/", "Different service, same city"))
        else:
            related_links.append((f"{SVC_PRICING[os_]['short']} Cost in {city['name']}", f"/blog/{os_}-cost-{city_slug}/", "Different service, same city"))
    related_links.append(("Best Flooring for Florida Humidity", "/blog/best-flooring-florida-humidity/", "Material comparison guide"))
    related_links.append(("Hardwood vs Vinyl Plank Comparison", "/blog/hardwood-vs-vinyl-plank-lakewood-ranch/", "Side-by-side analysis"))
    
    related_html = ""
    for title, link, sub in related_links[:6]:
        related_html += f'<a href="{link}" class="related-card"><strong>{title} →</strong><span>{sub}</span></a>'
    
    # === Build comparison table — this city vs 4 reference cities ===
    ref_cities = ["bradenton","sarasota","lakewood-ranch","tampa"] if city_slug not in ["bradenton","sarasota","lakewood-ranch","tampa"] else \
                 [c for c in ["palmetto","sarasota","lakewood-ranch","tampa","st-petersburg"] if c != city_slug][:4]
    comp_rows = []
    for rc in ref_cities + [city_slug] if city_slug not in ref_cities else ref_cities:
        rc_min, rc_max = compute_min_max(svc_slug, rc)
        rc_mult = CITY_LABOR_MULT[rc]
        is_this = (rc == city_slug)
        if unit == 'sq ft':
            min_str = f"${rc_min:.2f}"
            max_str = f"${rc_max:.2f}"
        else:
            min_str = f"${rc_min:.0f}"
            max_str = f"${rc_max:.0f}"
        delta = (rc_mult - 1.0) * 100
        delta_str = f"baseline" if abs(delta) < 0.5 else (f"+{delta:.0f}%" if delta > 0 else f"{delta:.0f}%")
        row_style = "background:rgba(46,141,217,.08);font-weight:600" if is_this else ""
        marker = " ← <em>this guide</em>" if is_this else ""
        comp_rows.append(f'<tr style="border-bottom:1px solid var(--gray-border);{row_style}"><td style="padding:11px 16px">{CITIES[rc]["name"]}{marker}</td><td style="padding:11px 16px">{CITIES[rc]["county"]}</td><td style="padding:11px 16px">{min_str} – {max_str}</td><td style="padding:11px 16px">{delta_str}</td></tr>')
    
    comparison_table_html = f"""<div style="overflow-x:auto;margin:1.6rem 0">
    <table style="width:100%;border-collapse:collapse;background:#fff;border-radius:12px;overflow:hidden;box-shadow:var(--shadow-sm);min-width:560px;font-size:.95rem">
      <thead style="background:var(--navy);color:#fff">
        <tr><th style="padding:12px 16px;text-align:left;font-family:var(--font-head);font-weight:600">Market</th><th style="padding:12px 16px;text-align:left;font-family:var(--font-head);font-weight:600">County</th><th style="padding:12px 16px;text-align:left;font-family:var(--font-head);font-weight:600">{svc['short']} Range</th><th style="padding:12px 16px;text-align:left;font-family:var(--font-head);font-weight:600">Labor Index</th></tr>
      </thead>
      <tbody>{"".join(comp_rows)}</tbody>
    </table>
  </div>"""
    
    # Comparison paragraph adapts to where the city sits in the market spectrum
    if mult <= 0.97:
        comparison_paragraph = f"{city['name']} sits at the affordable end of our service area. Homeowners here typically save 5-10% on labor costs versus the most expensive markets (Lakewood Ranch, Tampa) without any compromise in installation quality — we use the same crew and the same 42-Point Standard regardless of which city you're in. The savings come from lower commercial overhead and less premium market positioning."
    elif mult >= 1.07:
        comparison_paragraph = f"{city['name']} runs at the premium end of our pricing spectrum. Labor rates here run 7-10% above Manatee County baseline — a function of {city['name']}'s market expectations, the prevalence of premium materials, and (in some neighborhoods) urban access logistics. The work itself is identical to what we do in lower-cost markets; the difference is mostly market-driven."
    else:
        comparison_paragraph = f"{city['name']} sits comfortably in the middle of our pricing spectrum — neither the cheapest nor the most expensive market we serve. Pricing is predictable and consistent with regional norms. Most homeowners find {city['name']} pricing aligns with their expectations after getting 2-3 quotes."
    
    # === City-specific climate / install considerations ===
    coastal_cities = {"bradenton","sarasota","venice","st-petersburg","palmetto"}
    inland_cities = {"lakewood-ranch","parrish"}
    urban_cities = {"tampa","st-petersburg"}
    
    if city_slug in coastal_cities:
        climate_intro = f"{city['name']}'s proximity to the Gulf of Mexico (or major bay/river systems) creates unique conditions that affect every {svc['short'].lower()} install we do. Salt-air exposure, elevated ambient humidity (typically 75-85% year-round outdoor), and storm-season risks all factor into our installation planning. Generic national installation protocols don't account for these conditions — and we've seen the consequences firsthand on too many failed floors installed by national-chain contractors who don't adapt their methodology."
        climate_protocol = f"For {svc['short'].lower()} projects in {city['name']}, our protocol differs from inland installs in several specific ways: we extend acclimation time to 72 hours minimum (versus the industry-standard 48), we always specify higher-grade adhesives rated for elevated humidity, we test substrate moisture more rigorously (calcium chloride or pin-style hygrometer with documented readings), and we install vapor barriers on slab construction even when manufacturer guides treat them as optional. These additional protocols add maybe $0.30-0.60/sq ft to the project — but they're the difference between a floor that lasts 25 years and one that fails in 3."
        climate_outcome = f"The result: every {svc['short'].lower()} project we complete in {city['name']} carries our 1-year written labor warranty, and our 5-year+ post-completion failure rate is essentially zero. We document the install conditions (humidity readings, substrate moisture, acclimation timeline) and provide that documentation to you at handover — which also helps you maintain manufacturer product warranties if any future issue arises."
    elif city_slug in inland_cities:
        climate_intro = f"{city['name']} is one of {city['county']}'s rapidly growing inland markets, with most homes built within the last 10-20 years on modern slab construction. The flooring conditions here are generally more forgiving than coastal markets — slab moisture migration is lower, salt-air exposure is minimal, and most subfloors are in excellent condition. But inland Florida humidity still averages 65-75% outdoor, and indoor AC swings still create dimensional movement in any wood-based flooring."
        climate_protocol = f"For {svc['short'].lower()} projects in {city['name']}, our protocol focuses on the dimensional movement issue that defines all Florida flooring work. Materials acclimate on-site for 48-72 hours minimum before installation. We test substrate moisture even on newer slabs (some new construction has elevated initial moisture from concrete cure). Expansion gaps at every wall are non-negotiable — even when manufacturer guides allow tighter spacing, we install to Florida-spec gaps because we know what happens otherwise."
        climate_outcome = f"The advantage of {city['name']}'s newer construction is that we can usually achieve excellent results with standard installation protocols — no special adhesives, no extra moisture barriers in most cases. This translates to reliable 25-30 year service life on quality materials, with our written 1-year labor warranty backing every install."
    else:  # urban (tampa, st-pete)
        climate_intro = f"{city['name']} is one of Florida's largest urban markets, with a wide mix of property types — from 1920s historic homes to 2020s downtown condos to suburban new construction. The {svc['short'].lower()} install considerations vary dramatically depending on which {city['name']} you're in. Historic neighborhoods often have wood subfloors with character (squeaks, slight variations) that need addressing. Downtown high-rises have specific freight-elevator and HOA requirements. Suburban {city['name']} (Wesley Chapel, Brandon, Riverview) is similar to standard Manatee/Sarasota suburban work."
        climate_protocol = f"For {svc['short'].lower()} projects in {city['name']}, we adapt our protocol to your specific property type. Historic {city['name']} homes get extra subfloor inspection time, fastener-pass squeak repairs, and careful matching of new flooring to existing era-appropriate aesthetics. Downtown condos get coordinated freight-elevator scheduling and HOA-compliant install timing. Suburban projects follow our standard {city['county']} protocols. In all cases, materials acclimate 48-72 hours, substrate moisture is tested, and Florida-spec expansion gaps are maintained."
        climate_outcome = f"The result: {city['name']} {svc['short'].lower()} installs that match the home's specific character and conditions, backed by our written 1-year labor warranty. We've completed projects in everything from Hyde Park craftsman bungalows to brand-new New Tampa subdivisions, and the consistent thread is that we adapt our methodology to the property — not the other way around."
    
    # === Build the page ===
    content = f"""{page_head(TITLE, DESC, PATH, og_image=svc['card_image'])}
<style>
.article-hero{{padding:3.5rem 0 2rem;background:linear-gradient(135deg,#0F3A6E 0%,#1A4F8C 70%,#2E8DD9 100%);color:#fff;text-align:center}}
.article-hero .eyebrow{{background:rgba(255,255,255,.14);color:#fff}}
.article-hero h1{{color:#fff;margin-bottom:.85rem;max-width:880px;margin-left:auto;margin-right:auto}}
.article-meta{{display:flex;justify-content:center;gap:1.2rem;flex-wrap:wrap;color:rgba(255,255,255,.85);font-size:.88rem;margin-top:1rem;font-family:var(--font-head);font-weight:500}}
.article-feature-img{{max-width:850px;margin:-1.5rem auto 0;padding:0 20px}}
.article-feature-img img{{width:100%;border-radius:14px;box-shadow:var(--shadow-lg);aspect-ratio:16/9;object-fit:cover;object-position:center 60%;max-height:430px}}
@media(max-width:768px){{.article-feature-img img{{aspect-ratio:16/10;max-height:240px}}}}
.article-body{{max-width:780px;margin:0 auto;padding:3rem 20px;font-size:1.05rem;line-height:1.8;color:var(--text)}}
.article-body p{{margin-bottom:1.3rem}}
.article-body h2{{font-size:1.7rem;margin:2.5rem 0 1rem;color:var(--navy);scroll-margin-top:80px}}
.article-body h3{{font-size:1.3rem;margin:2rem 0 .8rem;color:var(--text);scroll-margin-top:80px}}
.article-body strong{{color:var(--navy)}}
.article-body table{{width:100%;border-collapse:collapse;margin:1.8rem 0;font-size:.95rem;background:#fff;border-radius:12px;overflow:hidden;box-shadow:var(--shadow-sm)}}
.article-body table th{{background:var(--navy);color:#fff;padding:12px 16px;text-align:left;font-family:var(--font-head);font-weight:600;font-size:.88rem}}
.article-body table td{{padding:11px 16px}}
.article-body ul,.article-body ol{{margin:0 0 1.4rem 1.4rem;padding:0}}
.article-body li{{margin-bottom:.65rem;line-height:1.7}}
.article-body .key-callout{{background:linear-gradient(135deg,#FFF4E0,#FFE4C2);border:1.5px solid #F4B069;border-radius:14px;padding:1.4rem 1.6rem;margin:2rem 0;color:#7A4310}}
.article-body .key-callout strong{{color:#7A4310}}
.article-toc{{background:var(--gray-light);border:1px solid var(--gray-border);border-radius:14px;padding:1.4rem 1.6rem;margin:0 0 2rem}}
.article-toc strong{{display:block;font-family:var(--font-head);font-size:.85rem;text-transform:uppercase;letter-spacing:.08em;color:var(--gray);margin-bottom:.7rem}}
.article-toc ol{{margin:0;padding-left:1.2rem;font-size:.94rem}}
.article-toc li{{margin-bottom:.4rem}}
.article-toc a{{color:var(--cerulean);text-decoration:none;font-weight:500}}
.article-body a{{color:var(--cerulean);text-decoration:underline;text-decoration-color:rgba(46,141,217,.3);text-underline-offset:3px}}
.article-body a:hover{{color:var(--orange);text-decoration-color:currentColor}}
@media(max-width:600px){{
  div[style*="grid-template-columns:1fr 1fr"]{{grid-template-columns:1fr !important}}
}}
</style>
{header()}
{breadcrumbs(bc_items)}

<section class="article-hero">
  <div class="container">
    <span class="eyebrow">Pricing Guide · 2026</span>
    <h1>{H1}</h1>
    <div class="article-meta"><span>📅 Updated May 2026</span><span>📍 {city['county']}</span><span>📖 8 min read</span></div>
  </div>
</section>

<div class="article-feature-img">
  <img src="/images/{svc['card_image']}" alt="{svc['name']} in {city['name']} FL by Triangle Flooring" width="1100" height="688">
</div>

<article class="article-body">
  <div class="article-toc">
    <strong>What's in this guide</strong>
    <ol>
      <li><a href="#summary">Quick Answer: 2026 Pricing</a></li>
      <li><a href="#full-table">Detailed Pricing Table</a></li>
      <li><a href="#cost-factors">What Goes Into the Cost</a></li>
      <li><a href="#projects">Real {city['name']} Project Examples</a></li>
      <li><a href="#market-context">{city['name']} vs Other Tampa Bay Markets</a></li>
      <li><a href="#local-expertise">Why Local {city['name']} Expertise Matters</a></li>
      <li><a href="#hidden">Hidden Costs to Watch For</a></li>
      <li><a href="#savings">How to Get the Best Value</a></li>
      <li><a href="#faq">Frequently Asked Questions</a></li>
    </ol>
  </div>

  <p>If you're researching <strong>{svc['short'].lower()} cost in {city['name']}, FL</strong>, you've probably gotten quotes from 2-3 contractors that vary by hundreds (or thousands) of dollars. That's normal — pricing in this market is genuinely all over the map. Some of that is contractor pricing strategy; some is real differences in what's being installed and how.</p>

  <p>This guide breaks down 2026 {svc['short'].lower()} pricing in {city['name']} the way we'd want it explained if we were the homeowner: <strong>itemized, justified, and compared to real-world projects we've actually completed in your area</strong>. We're a {city['county']}-based flooring contractor with 300+ Tampa Bay projects under our belt, headquartered in Palmetto, FL.</p>

  <h2 id="summary">Quick Answer: {svc['short']} Cost in {city['name']}, FL (2026)</h2>
  
  <div class="key-callout">
    <p style="margin:0"><strong>Total installed cost in {city['name']}:</strong> {price_summary}, depending on material tier and project complexity. Most residential projects in {city['name']} land in the mid-range tier — see the full pricing table below for tier-by-tier details.</p>
  </div>

  <p>{labor_note}</p>

  <h2 id="full-table">Full 2026 {svc['short']} Pricing Table for {city['name']}, FL</h2>

  <p>Here's the complete breakdown by material tier, with material costs separated from labor costs (labor adjusted for {city['name']}'s specific market):</p>

  {pricing_table_html}

  <p style="font-size:.88rem;color:var(--gray)">Pricing reflects 2026 market rates for residential projects in {city['name']}, {city['county']}. Includes basic install but excludes major subfloor prep, demolition of existing flooring, and add-ons listed in the "Hidden Costs" section below. All quotes from Triangle Flooring are itemized in writing — we never use unitized "package" pricing that obscures what each line costs.</p>

  <h2 id="cost-factors">What Goes Into {svc['short']} Cost in {city['name']}?</h2>

  <p>The 5 biggest factors that drive {svc['short'].lower()} project pricing in {city['name']} are:</p>

  {factors_html}

  {inline_form_html}

  <h2 id="projects">Real {city['name']} Project Examples (2026)</h2>

  <p>Here are three real project examples representing the kinds of {svc['short'].lower()} jobs we quote in {city['name']} every month. Names and exact addresses are anonymized but pricing is representative of 2026 quotes:</p>

  {examples_html}

  <h2 id="market-context">How {city['name']} Pricing Compares to Other Tampa Bay Markets</h2>

  <p>{svc['short']} pricing in {city['name']} doesn't exist in a vacuum — it reflects {city['county']}'s broader market dynamics. Here's how {city['name']} stacks up against neighboring markets we serve:</p>

  {comparison_table_html}

  <p>{comparison_paragraph}</p>

  <h2 id="local-expertise">Why Local {city['name']} Expertise Matters for {svc['short']}</h2>

  <p>{climate_intro}</p>

  <p>{climate_protocol}</p>

  <p>{climate_outcome}</p>

  <h2 id="hidden">Hidden Costs Most {city['name']} Quotes Don't Mention</h2>

  <p>The "low quote" you got at $X/sq ft installed often becomes 30-50% higher after these line items get added mid-project. Always ask if the following are included <em>before</em> you sign:</p>

  <div style="overflow-x:auto;margin:1.5rem 0">
    <table style="width:100%;border-collapse:collapse;background:#fff;border-radius:12px;overflow:hidden;box-shadow:var(--shadow-sm);min-width:480px">
      <thead style="background:var(--navy);color:#fff">
        <tr><th style="padding:13px 16px;text-align:left;font-family:var(--font-head);font-weight:600">Hidden Cost Item</th><th style="padding:13px 16px;text-align:left;font-family:var(--font-head);font-weight:600">Typical {city['name']} Range</th></tr>
      </thead>
      {hidden_costs_html}
    </table>
  </div>

  <p>At Triangle Flooring, every {city['name']} quote includes all relevant line items — you see exactly what each component costs, and there are no surprise charges mid-project.</p>

  <h2 id="savings">How to Save Money on {svc['short']} in {city['name']} Without Sacrificing Quality</h2>

  <p>Most of the legitimate savings on a {svc['short'].lower()} project come from <em>scope decisions</em>, not from finding a cheaper installer. Here are the top ways to save:</p>

  <ol>
    {tips_html}
  </ol>

  <h2 id="faq">Frequently Asked Questions: {svc['short']} in {city['name']}</h2>

  <div class="faq-list">
    {faq_html}
  </div>

  <h2 style="margin-top:3rem">Ready to Get a Real {city['name']} Quote?</h2>

  <p>Triangle Flooring has completed {svc['short'].lower()} installations in {len(city['neighborhoods'])}+ {city['name']} neighborhoods including <strong>{', '.join(city['neighborhoods'][:5])}</strong>, and many others. Free in-home measurement, written itemized quote within 24 hours, no high-pressure sales.</p>

  <p>Three ways to start:</p>
  <ul>
    <li>📞 <strong>Call us:</strong> <a href="tel:+19414026861">(941) 402-6861</a> — same-day response, 7 days a week</li>
    <li>💬 <strong>WhatsApp:</strong> <a href="https://wa.me/19414026861" target="_blank" rel="noopener">Message us instantly</a> — typical response within 1 hour during business hours</li>
    <li>📝 <strong>Quote form:</strong> <a href="/contact/">Fill out our contact form</a> — itemized written quote within 24 hours</li>
  </ul>

  <p>Or learn more about {svc['short'].lower()} services in your area: <a href="/{svc_slug}/{city_slug}/">{svc['short']} services in {city['name']}, FL</a> — full details on our process, materials we work with, and warranty coverage.</p>
</article>

<section class="related" style="background:var(--gray-light)">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Continue Reading</span><h2>Related Pricing Guides</h2></div>
    <div class="related-grid">{related_html}</div>
  </div>
</section>

{final_cta()}
{footer()}
{whatsapp_float()}

<script type="application/ld+json">{json.dumps(bc_schema)}</script>
<script type="application/ld+json">{json.dumps(article_schema)}</script>
<script type="application/ld+json">{json.dumps(business_schema)}</script>
<script type="application/ld+json">{json.dumps(service_schema)}</script>
<script type="application/ld+json">{json.dumps(faq_schema)}</script>

{menu_script()}
</body>
</html>"""
    
    # Write file
    out = f"{OUT_DIR}/blog/{slug}/index.html"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f: f.write(content)
    
    # Word count
    text = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'&[a-z]+;', ' ', text)
    words = len(text.split())
    
    print(f"  ✓ /blog/{slug}/ ({len(content)//1024}KB · {words} words)")
    return slug

# ============================================================================
# RUN
# ============================================================================
print("\n→ Building 46 service×city pricing posts (skipping 2 existing):")
generated = []
for svc_slug in SVC_PRICING:
    for city_slug in CITIES:
        result = build_pricing_post(svc_slug, city_slug)
        if result: generated.append(result)

print(f"\n✓ Generated {len(generated)} pricing posts")
print(f"  Total blog: {len(generated)+7} articles (7 existing + {len(generated)} new)")
