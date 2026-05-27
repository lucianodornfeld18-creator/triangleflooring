# Triangle Flooring — Production Website

Production website for **Triangle Flooring**, a flooring contractor serving Bradenton, Sarasota, Lakewood Ranch, Tampa Bay, and surrounding areas.

🌐 **Live:** [triangle-floor.com](https://triangle-floor.com/)

## 🏗️ Stack

- **Static HTML/CSS/JS** — no framework, no build step
- **Cloudflare Pages** for hosting + CDN + SSL
- **Outfit + Lato** via Google Fonts
- **Schema.org JSON-LD** for SEO (Organization, LocalBusiness, FAQ, Breadcrumb, WebSite)

## 📁 Structure

```
/
├── index.html                    # Homepage
├── 404.html                      # Branded 404
├── sitemap.xml                   # SEO sitemap
├── robots.txt                    # Crawler directives (AI bots allowed)
├── _headers                      # Cloudflare Pages security + cache
├── _redirects                    # 301 redirects for keyword variations
├── images/                       # Logos, OG, hero, project photos
├── about/                        # About page (Phase 2)
├── contact/                      # Contact + free quote (Phase 2)
├── hardwood-flooring/            # Hardwood service hub (Phase 2)
│   ├── bradenton/
│   ├── sarasota/
│   └── lakewood-ranch/
├── vinyl-plank-flooring/         # LVP service hub (Phase 2)
│   ├── bradenton/
│   ├── sarasota/
│   └── lakewood-ranch/
├── tile-installation/            # Tile service (Phase 2)
├── laminate-flooring/            # Laminate service (Phase 2)
├── stair-treads/                 # Stair treads service (Phase 2)
├── floor-repair/                 # Repair & replacement (Phase 2)
└── blog/                         # SEO blog (Phase 3)
```

## 🚀 Cloudflare Pages Setup

1. Connect this GitHub repo to Cloudflare Pages
2. **Build command:** *(leave blank — static site)*
3. **Build output directory:** `/`
4. **Root directory:** `/`
5. Click **Save and Deploy**

After first deploy:
- Add custom domain `triangle-floor.com` in Cloudflare Pages settings
- Verify SSL is active (auto-handled by Cloudflare)

## 🔍 SEO Submissions Checklist

After domain is live, submit to:

- [ ] **Google Search Console** → submit `sitemap.xml`
- [ ] **Bing Webmaster Tools** → submit `sitemap.xml` + IndexNow API key
- [ ] **Apple Business Connect** → claim & verify
- [ ] **Google Business Profile** → already exists, link site URL
- [ ] **Yelp Business** → create profile (currently missing)
- [ ] **Angi**, **Thumbtack**, **HomeAdvisor** → list business
- [ ] **Houzz** → flooring contractor profile
- [ ] **Better Business Bureau** → claim listing
- [ ] **NextDoor Business** → local visibility

## 📊 Performance Targets

- **PageSpeed (Mobile):** 90+
- **PageSpeed (Desktop):** 95+
- **LCP:** < 1.8s
- **FID:** < 100ms
- **CLS:** < 0.1

## 📞 Business Info

- **Phone:** (941) 402-6861
- **Email:** trianglefloor@gmail.com
- **Address:** 8737 Royal Acacia Ave, Palmetto, FL 34221
- **Service Area:** Bradenton, Sarasota, Lakewood Ranch, Palmetto, Parrish, Venice, St. Petersburg, Tampa
- **Instagram:** [@flooringtriangle](https://www.instagram.com/flooringtriangle)
- **Facebook:** [Triangle Flooring](https://www.facebook.com/people/Triangle-Flooring/61567334333950/)

## 🛠️ Development

This site is plain HTML/CSS/JS. No build step needed.

To preview locally:
```bash
python3 -m http.server 8000
# Then visit http://localhost:8000
```

## 📄 License

© 2026 Triangle Flooring. All rights reserved.
