#!/usr/bin/env python3
"""
Triangle Flooring - Phase 2 Page Generator
Generates 13 production-ready HTML pages with consistent SEO/schema/design.
"""
import os, json, re

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "triangle-floor.com"
PHONE = "+19414026861"
PHONE_DISPLAY = "(941) 402-6861"
EMAIL = "trianglefloor@gmail.com"

# ============================================================================
# SHARED COMPONENTS (used by every page)
# ============================================================================

SHARED_STYLES = """
:root{--navy:#1A4F8C;--navy-dark:#0F3A6E;--navy-light:#E8F2FB;--cerulean:#2E8DD9;--cerulean-light:#5BAEEB;--orange:#E07A2B;--orange-dark:#C56619;--text:#1B2939;--gray:#5B6B7E;--gray-light:#F7F9FC;--gray-border:#E2E8F0;--white:#fff;--success:#10B981;--whatsapp:#25D366;--radius:12px;--radius-lg:18px;--shadow-sm:0 1px 3px rgba(15,58,110,.08);--shadow:0 4px 12px rgba(15,58,110,.10);--shadow-lg:0 14px 36px rgba(15,58,110,.14);--font-head:'Outfit',sans-serif;--font-body:'Lato',-apple-system,BlinkMacSystemFont,sans-serif;--container:1180px;--transition:.25s cubic-bezier(.4,0,.2,1)}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%;scroll-padding-top:90px}
body{font-family:var(--font-body);font-size:16px;line-height:1.65;color:var(--text);background:var(--white);overflow-x:hidden}
img{max-width:100%;height:auto;display:block}
a{color:var(--navy);text-decoration:none;transition:color var(--transition)}
a:hover{color:var(--orange)}
h1,h2,h3,h4,h5{font-family:var(--font-head);font-weight:700;line-height:1.2;letter-spacing:-.02em;color:var(--text)}
h1{font-size:clamp(2rem,5vw,3.2rem)}
h2{font-size:clamp(1.5rem,3.2vw,2.1rem)}
h3{font-size:clamp(1.1rem,1.9vw,1.3rem)}
p{margin:0 0 1rem}
.container{max-width:var(--container);margin:0 auto;padding:0 20px}
.eyebrow{display:inline-block;font-size:.78rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--navy);background:var(--navy-light);padding:5px 14px;border-radius:50px;margin-bottom:.85rem}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:14px 26px;font-family:var(--font-head);font-weight:600;font-size:.98rem;border-radius:50px;text-decoration:none;cursor:pointer;border:none;transition:all var(--transition);white-space:nowrap}
.btn-primary{background:var(--orange);color:#fff;box-shadow:0 4px 16px rgba(224,122,43,.32)}
.btn-primary:hover{background:var(--orange-dark);color:#fff;transform:translateY(-2px)}
.btn-secondary{background:#fff;color:var(--navy);border:2px solid var(--navy)}
.btn-secondary:hover{background:var(--navy);color:#fff}
.btn-ghost{background:transparent;color:#fff;border:2px solid rgba(255,255,255,.5)}
.btn-ghost:hover{background:#fff;color:var(--navy);border-color:#fff}
.site-header{position:sticky;top:0;z-index:100;background:rgba(255,255,255,.96);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border-bottom:1px solid var(--gray-border)}
.nav-bar{display:flex;align-items:center;justify-content:space-between;padding:14px 20px;max-width:var(--container);margin:0 auto;gap:1rem}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;flex-shrink:0}
.brand img{height:46px;width:auto}
.brand-text{display:flex;flex-direction:column;line-height:1}
.brand-name{font-family:var(--font-head);font-weight:800;font-size:1.18rem;color:var(--navy);letter-spacing:-.02em;white-space:nowrap}
.brand-tag{font-size:.7rem;letter-spacing:.16em;color:var(--cerulean);text-transform:uppercase;margin-top:2px;white-space:nowrap}
.nav-menu{display:flex;align-items:center;gap:1.25rem;list-style:none;flex-wrap:nowrap}
.nav-menu li{position:relative}
.nav-menu a{font-family:var(--font-head);font-weight:500;color:var(--text);font-size:.94rem;padding:8px 4px;white-space:nowrap}
.nav-menu a:hover{color:var(--navy)}
.dropdown{position:absolute;top:calc(100% + 6px);left:50%;transform:translateX(-50%) translateY(-8px);background:#fff;min-width:240px;border-radius:var(--radius);box-shadow:var(--shadow-lg);padding:.6rem 0;opacity:0;visibility:hidden;transition:all var(--transition);z-index:99;border:1px solid var(--gray-border)}
.nav-menu li:hover .dropdown{opacity:1;visibility:visible;transform:translateX(-50%) translateY(0)}
.dropdown a{display:block;padding:9px 18px;font-size:.92rem;font-weight:400;border-radius:0;white-space:nowrap}
.dropdown a:hover{background:var(--navy-light);color:var(--navy)}
.nav-cta{display:flex;align-items:center;gap:.85rem;flex-shrink:0}
.nav-phone{display:flex;align-items:center;gap:6px;color:var(--navy);font-family:var(--font-head);font-weight:600;font-size:.95rem;white-space:nowrap}
.nav-phone svg{width:16px;height:16px;flex-shrink:0}
.menu-toggle{display:none;background:none;border:none;cursor:pointer;padding:8px;color:var(--navy)}
.menu-toggle svg{width:26px;height:26px}
.breadcrumbs{background:var(--gray-light);padding:14px 0;font-size:.85rem;border-bottom:1px solid var(--gray-border)}
.breadcrumbs ol{list-style:none;display:flex;flex-wrap:wrap;align-items:center;gap:8px;color:var(--gray)}
.breadcrumbs li{display:flex;align-items:center;gap:8px}
.breadcrumbs li::after{content:"/";color:var(--gray-border);margin-left:8px}
.breadcrumbs li:last-child::after{display:none}
.breadcrumbs a{color:var(--cerulean);font-weight:500}
.breadcrumbs li:last-child{color:var(--text);font-weight:600}
.page-hero{padding:3.5rem 0 2.5rem;background:linear-gradient(135deg,#0F3A6E 0%,#1A4F8C 70%,#2E8DD9 100%);color:#fff;text-align:center}
.page-hero h1{color:#fff;margin-bottom:.85rem}
.page-hero h1 span{background:linear-gradient(90deg,#FFC993,#E07A2B);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.page-hero p{font-size:1.05rem;color:rgba(255,255,255,.92);max-width:720px;margin:0 auto 1.5rem}
.page-hero .eyebrow{background:rgba(255,255,255,.14);color:#fff}
.page-hero-trust{display:flex;justify-content:center;flex-wrap:wrap;gap:.7rem 1.6rem;margin-top:1.4rem;font-size:.88rem;color:rgba(255,255,255,.95)}
.page-hero-trust span{display:inline-flex;align-items:center;gap:6px;font-weight:600;font-family:var(--font-head)}
.page-hero-trust span::before{content:"✓";color:#FFC993;font-weight:700}
section{padding:4rem 0}
.section-head{text-align:center;max-width:740px;margin:0 auto 3rem}
.section-head p{color:var(--gray);font-size:1.05rem;margin-top:.6rem}
.intro{padding:3rem 0;background:#fff}
.intro-content{max-width:780px;margin:0 auto;font-size:1.05rem;line-height:1.75;color:var(--text)}
.intro-content p{margin-bottom:1.2rem}
.intro-content strong{color:var(--navy)}
.stat-badge{background:linear-gradient(135deg,#FFF4E0,#FFE4C2);border:1.5px solid #F4B069;border-radius:14px;padding:1.1rem 1.4rem;margin:1.8rem 0;display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.stat-badge-icon{font-size:2.2rem}
.stat-badge p{margin:0;color:#7A4310;font-weight:600;font-size:.96rem}
.stat-badge p:nth-child(2){color:#9E5A1A;font-size:.82rem;font-weight:500}
.pricing{background:var(--gray-light)}
.pricing-table{background:#fff;border-radius:14px;overflow:hidden;box-shadow:var(--shadow);border:1px solid var(--gray-border);max-width:920px;margin:0 auto}
.pricing-table table{width:100%;border-collapse:collapse;font-size:.95rem}
.pricing-table thead{background:linear-gradient(135deg,var(--navy-dark),var(--navy))}
.pricing-table th{padding:14px 18px;text-align:left;color:#fff;font-family:var(--font-head);font-weight:600;font-size:.88rem;letter-spacing:.04em;text-transform:uppercase}
.pricing-table tbody tr{border-bottom:1px solid var(--gray-border);transition:background var(--transition)}
.pricing-table tbody tr:last-child{border-bottom:none}
.pricing-table tbody tr:nth-child(even){background:var(--gray-light)}
.pricing-table tbody tr:hover{background:var(--navy-light)}
.pricing-table td{padding:13px 18px}
.pricing-table td:first-child{font-weight:600;color:var(--text)}
.pricing-table td.price{font-weight:700;color:var(--navy);white-space:nowrap;font-family:var(--font-head)}
.pricing-note{text-align:center;font-size:.85rem;color:var(--gray);margin-top:1rem}
.pricing-note a{color:var(--cerulean);font-weight:600}
.checklist-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1.3rem;margin-top:2rem}
.checklist-card{background:#fff;border:1.5px solid var(--gray-border);border-radius:14px;overflow:hidden;box-shadow:var(--shadow-sm)}
.checklist-card-head{background:linear-gradient(135deg,var(--navy),var(--cerulean));padding:.95rem 1.2rem;color:#fff}
.checklist-card-head strong{font-family:var(--font-head);font-weight:700;font-size:1rem;display:block}
.checklist-card-head span{font-size:.75rem;opacity:.85;letter-spacing:.04em;text-transform:uppercase;margin-top:2px;display:block}
.checklist-card ol{list-style:none;counter-reset:item;padding:.85rem 1.2rem;font-size:.92rem}
.checklist-card li{counter-increment:item;padding:5px 0 5px 24px;position:relative;color:var(--text);line-height:1.45}
.checklist-card li::before{content:counter(item);position:absolute;left:0;top:6px;width:18px;height:18px;background:var(--navy-light);color:var(--navy);border-radius:50%;font-size:.7rem;font-weight:700;display:grid;place-items:center;font-family:var(--font-head)}
.neighborhoods{background:#fff}
.zip-grid{display:flex;flex-wrap:wrap;gap:.6rem;justify-content:center;max-width:920px;margin:1.5rem auto 0}
.zip-pill{background:var(--gray-light);border:1.5px solid var(--gray-border);padding:8px 16px;border-radius:50px;font-family:var(--font-head);font-weight:600;color:var(--navy);font-size:.88rem}
.neighborhood-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:.7rem;max-width:920px;margin:2rem auto 0}
.neighborhood-pill{background:var(--navy-light);color:var(--navy);padding:11px 16px;border-radius:10px;text-align:center;font-weight:600;font-size:.92rem;font-family:var(--font-head);transition:all var(--transition)}
.neighborhood-pill:hover{background:var(--navy);color:#fff;transform:translateY(-2px)}
.faq-section{background:var(--gray-light)}
.faq-list{max-width:820px;margin:0 auto}
.faq-item{background:#fff;border:1.5px solid var(--gray-border);border-radius:12px;margin-bottom:1rem;overflow:hidden;transition:all var(--transition)}
.faq-item[open]{border-color:var(--cerulean);box-shadow:var(--shadow)}
.faq-item summary{padding:1.1rem 1.4rem;font-family:var(--font-head);font-weight:600;font-size:1.02rem;color:var(--text);cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:1rem}
.faq-item summary::-webkit-details-marker{display:none}
.faq-item summary::after{content:"+";font-size:1.5rem;color:var(--cerulean);font-weight:300;transition:transform var(--transition);flex-shrink:0;line-height:1}
.faq-item[open] summary::after{content:"−"}
.faq-item summary:hover{color:var(--navy)}
.faq-content{padding:0 1.4rem 1.2rem;color:var(--gray);line-height:1.7;font-size:.96rem}
.faq-content p{margin-bottom:.7rem}
.faq-content p:last-child{margin-bottom:0}
.related{background:#fff}
.related-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1.2rem;margin-top:2rem}
.related-card{background:var(--gray-light);padding:1.4rem;border-radius:14px;border:1px solid var(--gray-border);text-decoration:none;color:inherit;transition:all var(--transition);display:block}
.related-card:hover{transform:translateY(-3px);box-shadow:var(--shadow);background:#fff;border-color:var(--cerulean);color:inherit}
.related-card strong{font-family:var(--font-head);font-size:1.02rem;color:var(--navy);display:block;margin-bottom:.3rem}
.related-card span{font-size:.88rem;color:var(--gray)}
.whatsapp-banner{background:linear-gradient(135deg,#128C7E,#25D366);border-radius:var(--radius-lg);padding:1.6rem 2rem;margin:3rem 0;display:flex;align-items:center;justify-content:space-between;gap:1.5rem;flex-wrap:wrap;box-shadow:0 14px 30px rgba(37,211,102,.25)}
.whatsapp-banner-text strong{font-family:var(--font-head);color:#fff;font-size:1.15rem;font-weight:700;display:block}
.whatsapp-banner-text span{color:rgba(255,255,255,.92);font-size:.9rem}
.whatsapp-banner-btn{background:#fff;color:#128C7E;padding:13px 24px;border-radius:50px;font-family:var(--font-head);font-weight:700;text-decoration:none;font-size:.95rem;display:inline-flex;align-items:center;gap:8px}
.final-cta{background:linear-gradient(135deg,#0F3A6E 0%,#1A4F8C 100%);color:#fff;text-align:center;padding:4.5rem 0}
.final-cta-content{position:relative;max-width:680px;margin:0 auto;padding:0 20px}
.final-cta h2{color:#fff;font-size:clamp(1.7rem,3.6vw,2.4rem);margin-bottom:.85rem}
.final-cta p{color:rgba(255,255,255,.92);font-size:1.02rem;margin-bottom:1.6rem}
.final-cta-buttons{display:flex;justify-content:center;gap:1rem;flex-wrap:wrap}
.cta-phone-large{font-family:var(--font-head);font-size:1.6rem;font-weight:800;color:#fff;display:inline-block;margin:.85rem 0;letter-spacing:-.01em}
.cta-phone-large:hover{color:#FFC993}
footer{background:#0A2342;color:rgba(255,255,255,.85);padding:3.5rem 0 0;font-size:.92rem}
.footer-grid{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:2.5rem;margin-bottom:2.5rem}
.footer-col h4{color:#fff;font-size:.92rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;margin-bottom:1rem;font-family:var(--font-head)}
.footer-brand{display:flex;align-items:center;gap:10px;margin-bottom:1rem}
.footer-brand img{height:42px;filter:brightness(0) invert(1)}
.footer-brand strong{font-family:var(--font-head);font-size:1.2rem;color:#fff}
.footer-col p{color:rgba(255,255,255,.7);line-height:1.65;font-size:.9rem}
.footer-col ul{list-style:none}
.footer-col li{margin-bottom:.6rem}
.footer-col a{color:rgba(255,255,255,.75);font-size:.9rem;transition:color var(--transition)}
.footer-col a:hover{color:#FFC993}
.footer-contact-item{display:flex;gap:8px;margin-bottom:.7rem;font-size:.9rem;color:rgba(255,255,255,.78);align-items:flex-start}
.footer-contact-item svg{width:15px;height:15px;color:#5BAEEB;flex-shrink:0;margin-top:3px}
.social-icons{display:flex;gap:10px;margin-top:1rem}
.social-icons a{width:38px;height:38px;background:rgba(255,255,255,.1);border-radius:50%;display:grid;place-items:center;color:#fff;transition:all var(--transition)}
.social-icons a:hover{background:var(--orange);transform:translateY(-2px)}
.social-icons svg{width:17px;height:17px}
.footer-bottom{border-top:1px solid rgba(255,255,255,.1);padding:1.4rem 0;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;font-size:.84rem;color:rgba(255,255,255,.6)}
.footer-bottom a{color:rgba(255,255,255,.6)}
.footer-bottom a:hover{color:#FFC993}
.whatsapp-float{position:fixed;bottom:22px;right:22px;z-index:9999;background:var(--whatsapp);color:#fff;padding:13px 20px;border-radius:50px;font-family:var(--font-head);font-weight:600;font-size:.92rem;display:inline-flex;align-items:center;gap:8px;box-shadow:0 6px 22px rgba(37,211,102,.45);text-decoration:none;transition:all var(--transition)}
.whatsapp-float:hover{transform:translateY(-3px) scale(1.04);color:#fff}
.whatsapp-float svg{width:20px;height:20px}
@media(max-width:1200px){
  .brand-tag{display:none}
  .nav-menu{gap:1rem}
  .nav-menu a{font-size:.9rem}
  .nav-phone{font-size:.9rem}
  .brand-name{font-size:1.08rem}
}
@media(max-width:960px){
  .footer-grid{grid-template-columns:1fr 1fr;gap:1.8rem}
  .nav-menu{display:none;position:absolute;top:100%;left:0;right:0;flex-direction:column;background:#fff;padding:.5rem 0;box-shadow:var(--shadow-lg);align-items:stretch;border-top:1px solid var(--gray-border);max-height:calc(100vh - 80px);overflow-y:auto}
  .nav-menu.open{display:flex}
  .nav-menu li{width:100%;border-bottom:1px solid var(--gray-border)}
  .nav-menu li:last-child{border-bottom:none}
  .nav-menu>li>a{padding:14px 20px;display:flex;align-items:center;justify-content:space-between;font-weight:500;font-size:1rem}
  .nav-menu>li>a[data-toggle]::after{content:"+";font-size:1.4rem;font-weight:300;color:var(--cerulean);transition:transform var(--transition);line-height:1}
  .nav-menu>li.expanded>a[data-toggle]::after{content:"−"}
  .dropdown{position:static;transform:none;opacity:1;visibility:visible;box-shadow:none;background:var(--gray-light);margin:0;padding:0;border-radius:0;border:none;display:none;max-height:none;min-width:0}
  .nav-menu>li.expanded .dropdown{display:block}
  .dropdown a{padding:11px 20px 11px 36px;font-size:.94rem;color:var(--text);border-bottom:1px solid rgba(0,0,0,.04)}
  .nav-phone span{display:none}
  .menu-toggle{display:block}
  .nav-cta .btn{display:none}
  .whatsapp-float{padding:11px 16px;font-size:.85rem}
  .whatsapp-float span{display:none}
  .footer-grid{grid-template-columns:1fr 1fr}
  section{padding:3rem 0}
  .checklist-grid{grid-template-columns:1fr}
  .pricing-table{font-size:.85rem}
  .pricing-table th,.pricing-table td{padding:10px 12px}
  .whatsapp-banner{flex-direction:column;text-align:center}
}
@media(max-width:560px){
  .footer-grid{grid-template-columns:1fr}
  .pricing-table{overflow-x:auto;display:block}
  .pricing-table table{min-width:520px}
}
"""

def header(active_path=""):
    return f"""<header class="site-header">
  <nav class="nav-bar" aria-label="Main navigation">
    <a href="/" class="brand" aria-label="Triangle Flooring home">
      <img src="/images/logo.png" alt="Triangle Flooring logo" width="46" height="46" loading="eager">
      <div class="brand-text"><span class="brand-name">Triangle Flooring</span><span class="brand-tag">Bradenton · Sarasota · Tampa</span></div>
    </a>
    <ul class="nav-menu" id="navMenu">
      <li><a href="/">Home</a></li>
      <li><a href="/hardwood-flooring/" data-toggle>Services</a>
        <div class="dropdown">
          <a href="/hardwood-flooring/">Hardwood Flooring</a>
          <a href="/vinyl-plank-flooring/">Vinyl Plank (LVP)</a>
          <a href="/tile-installation/">Tile Installation</a>
          <a href="/laminate-flooring/">Laminate Flooring</a>
          <a href="/stair-treads/">Stair Treads</a>
          <a href="/floor-repair/">Repair & Replacement</a>
        </div>
      </li>
      <li><a href="/bradenton/" data-toggle>Service Areas</a>
        <div class="dropdown">
          <a href="/bradenton/">📍 Bradenton, FL</a>
          <a href="/sarasota/">📍 Sarasota, FL</a>
          <a href="/lakewood-ranch/">📍 Lakewood Ranch</a>
          <a href="/palmetto/">📍 Palmetto, FL</a>
          <a href="/parrish/">📍 Parrish, FL</a>
          <a href="/venice/">📍 Venice, FL</a>
          <a href="/tampa/">📍 Tampa, FL</a>
          <a href="/st-petersburg/">📍 St. Petersburg, FL</a>
        </div>
      </li>
      <li><a href="/blog/">Blog</a></li>
      <li><a href="/about/">About</a></li>
      <li><a href="/contact/">Contact</a></li>
    </ul>
    <div class="nav-cta">
      <a href="tel:{PHONE}" class="nav-phone" aria-label="Call us">
        <svg fill="currentColor" viewBox="0 0 24 24"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.28-.28.67-.36 1.02-.25 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
        <span>{PHONE_DISPLAY}</span>
      </a>
      <a href="/contact/#quote" class="btn btn-primary">Free Quote</a>
      <button class="menu-toggle" id="menuToggle" aria-label="Toggle menu" aria-expanded="false">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
      </button>
    </div>
  </nav>
</header>"""

def breadcrumbs(items):
    """items: list of (name, url|None)"""
    lis = []
    for name, url in items:
        if url:
            lis.append(f'<li><a href="{url}">{name}</a></li>')
        else:
            lis.append(f'<li>{name}</li>')
    return f'<nav class="breadcrumbs" aria-label="Breadcrumb"><div class="container"><ol>{"".join(lis)}</ol></div></nav>'

def whatsapp_banner():
    return f"""<div class="whatsapp-banner">
  <div class="whatsapp-banner-text"><strong>Free estimate within 24 hours.</strong><span>Call, text, or WhatsApp — 7 days a week.</span></div>
  <a href="https://wa.me/19414026861?text=Hi%20Triangle%20Flooring%2C%20I%27d%20like%20a%20free%20flooring%20estimate." target="_blank" rel="noopener" class="whatsapp-banner-btn">
    <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.71.306 1.263.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
    WhatsApp Us
  </a>
</div>"""

def final_cta():
    return f"""<section class="final-cta">
  <div class="final-cta-content">
    <span class="eyebrow" style="background:rgba(255,255,255,.15);color:#fff">Ready to Get Started?</span>
    <h2>Get Your Free Flooring Estimate Today</h2>
    <p>From first call to last baseboard — Triangle Flooring delivers Florida-tough installations across Tampa Bay. Free measurement. Locked-in pricing. 1-year warranty.</p>
    <a href="tel:{PHONE}" class="cta-phone-large">📞 {PHONE_DISPLAY}</a>
    <div class="final-cta-buttons">
      <a href="/contact/#quote" class="btn btn-primary">Get My Free Quote</a>
      <a href="https://wa.me/19414026861?text=Hi%2C%20I%27d%20like%20a%20free%20flooring%20estimate." target="_blank" rel="noopener" class="btn btn-ghost">💬 WhatsApp Us</a>
    </div>
  </div>
</section>"""

def footer():
    return f"""<footer>
  <div class="container">
    <div class="footer-grid">
      <div class="footer-col">
        <div class="footer-brand"><img src="/images/logo.png" alt="Triangle Flooring"><strong>Triangle Flooring</strong></div>
        <p>Professional flooring contractor serving Bradenton, Sarasota, Lakewood Ranch, Tampa Bay & all of Manatee, Sarasota, Hillsborough, and Pinellas counties. Hardwood, vinyl, tile, laminate, stair treads, and repair.</p>
        <div class="social-icons">
          <a href="https://www.instagram.com/flooringtriangle" target="_blank" rel="noopener" aria-label="Instagram"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg></a>
          <a href="https://www.facebook.com/people/Triangle-Flooring/61567334333950/" target="_blank" rel="noopener" aria-label="Facebook"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg></a>
          <a href="https://share.google/TVRjAYdnZR3TS8Kzq" target="_blank" rel="noopener" aria-label="Google Business"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg></a>
          <a href="https://br.pinterest.com/trianglefloor/" target="_blank" rel="noopener" aria-label="Pinterest"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M12.017 0C5.396 0 .029 5.367.029 11.987c0 5.079 3.158 9.417 7.618 11.162-.105-.949-.199-2.403.041-3.439.219-.937 1.406-5.957 1.406-5.957s-.359-.72-.359-1.781c0-1.668.967-2.914 2.171-2.914 1.023 0 1.518.769 1.518 1.69 0 1.029-.655 2.568-.994 3.995-.283 1.194.599 2.169 1.777 2.169 2.133 0 3.772-2.249 3.772-5.495 0-2.873-2.064-4.882-5.012-4.882-3.414 0-5.418 2.561-5.418 5.207 0 1.031.397 2.138.893 2.738.098.119.112.224.083.345-.09.375-.293 1.199-.334 1.363-.053.225-.172.271-.402.165-1.495-.696-2.433-2.879-2.433-4.646 0-3.785 2.75-7.262 7.929-7.262 4.163 0 7.398 2.967 7.398 6.931 0 4.136-2.607 7.464-6.227 7.464-1.216 0-2.359-.631-2.75-1.378l-.748 2.853c-.271 1.043-1.002 2.35-1.492 3.146C9.57 23.812 10.763 24 12.017 24c6.624 0 11.99-5.367 11.99-11.988C24.007 5.367 18.641.001 12.017.001z"/></svg></a>
          <a href="https://www.houzz.com/pro/triangleflooring79" target="_blank" rel="noopener" aria-label="Houzz"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M24 24v-7.451l-6.461-3.726V24H24zM0 0v7.451l6.461 3.726V0H0zm0 24h6.461v-7.451L0 12.823V24zm9.269-10.908L24 7.451V0L9.269 5.176v7.916z"/></svg></a>
          <a href="https://www.bbb.org/us/fl/palmetto/profile/flooring-contractors/triangle-flooring-llc-0653-90463364" target="_blank" rel="noopener" aria-label="BBB Accredited"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M12 1 3 5v6c0 5.25 3.84 9.74 9 11 5.16-1.26 9-5.75 9-11V5l-9-4zm-1.2 15.2-4-4 1.4-1.4 2.6 2.6 5.2-5.2 1.4 1.4-6.6 6.6z"/></svg></a>
        </div>
      </div>
      <div class="footer-col">
        <h4>Services</h4>
        <ul>
          <li><a href="/hardwood-flooring/">Hardwood Flooring</a></li>
          <li><a href="/vinyl-plank-flooring/">Luxury Vinyl Plank</a></li>
          <li><a href="/tile-installation/">Tile Installation</a></li>
          <li><a href="/laminate-flooring/">Laminate Flooring</a></li>
          <li><a href="/stair-treads/">Stair Treads</a></li>
          <li><a href="/floor-repair/">Repair & Replacement</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Service Areas</h4>
        <ul>
          <li><a href="/bradenton/">Bradenton, FL</a></li>
          <li><a href="/sarasota/">Sarasota, FL</a></li>
          <li><a href="/lakewood-ranch/">Lakewood Ranch</a></li>
          <li><a href="/palmetto/">Palmetto, FL</a></li>
          <li><a href="/parrish/">Parrish, FL</a></li>
          <li><a href="/venice/">Venice, FL</a></li>
          <li><a href="/tampa/">Tampa, FL</a></li>
          <li><a href="/st-petersburg/">St. Petersburg, FL</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Contact</h4>
        <div class="footer-contact-item"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/></svg><a href="tel:{PHONE}">{PHONE_DISPLAY}</a></div>
        <div class="footer-contact-item"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg><a href="mailto:{EMAIL}">{EMAIL}</a></div>
        <div class="footer-contact-item"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg><span>8737 Royal Acacia Ave<br>Palmetto, FL 34221</span></div>
        <div class="footer-contact-item"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg><span>Mon–Sat · 7 AM – 7 PM</span></div>
      </div>
    </div>
    <div class="footer-bottom">
      <div>© 2026 Triangle Flooring. All rights reserved. · Locally owned & operated.</div>
      <div><a href="/about/">About</a> · <a href="/blog/">Blog</a> · <a href="/faq/">FAQ</a> · <a href="/warranty/">Warranty</a> · <a href="/contact/">Contact</a></div>
    </div>
  </div>
</footer>"""

def whatsapp_float():
    return """<a href="https://wa.me/19414026861?text=Hi%20Triangle%20Flooring%2C%20I%27d%20like%20a%20free%20flooring%20estimate." target="_blank" rel="noopener" class="whatsapp-float" aria-label="Chat on WhatsApp">
  <svg fill="currentColor" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.71.306 1.263.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
  <span>Free Quote</span>
</a>"""

def menu_script():
    return """<script>
(function(){var t=document.getElementById('menuToggle'),m=document.getElementById('navMenu');if(!t||!m)return;t.addEventListener('click',function(){var o=m.classList.toggle('open');t.setAttribute('aria-expanded',o);if(!o)m.querySelectorAll('li.expanded').forEach(function(l){l.classList.remove('expanded')})});m.querySelectorAll('a[data-toggle]').forEach(function(a){a.addEventListener('click',function(e){if(window.innerWidth>960)return;e.preventDefault();var l=a.parentElement,w=l.classList.contains('expanded');m.querySelectorAll('li.expanded').forEach(function(x){x.classList.remove('expanded')});if(!w)l.classList.add('expanded')})});m.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){if(a.hasAttribute('data-toggle')&&window.innerWidth<=960)return;m.classList.remove('open');t.setAttribute('aria-expanded','false');m.querySelectorAll('li.expanded').forEach(function(l){l.classList.remove('expanded')})})});window.addEventListener('resize',function(){if(window.innerWidth>960){m.classList.remove('open');t.setAttribute('aria-expanded','false');m.querySelectorAll('li.expanded').forEach(function(l){l.classList.remove('expanded')})}})})();
/* Anchor scroll handler — guarantees correct positioning even when arriving from another page with #hash in URL.
   Browser native anchor scrolling sometimes triggers before sticky header is laid out; this fixes that timing issue. */
(function(){function scrollToAnchor(hash){if(!hash||hash.length<2)return;var el=document.getElementById(hash.slice(1));if(!el)return;var rect=el.getBoundingClientRect();var scrollTop=window.pageYOffset||document.documentElement.scrollTop;var headerOffset=window.innerWidth<=960?70:90;window.scrollTo({top:rect.top+scrollTop-headerOffset,behavior:'smooth'})}
if(window.location.hash){setTimeout(function(){scrollToAnchor(window.location.hash)},80);window.addEventListener('load',function(){setTimeout(function(){scrollToAnchor(window.location.hash)},150)})}
document.querySelectorAll('a[href*="#"]').forEach(function(link){var href=link.getAttribute('href');if(!href||href==='#')return;var hashIndex=href.indexOf('#');if(hashIndex<0)return;var path=href.substring(0,hashIndex);var hash=href.substring(hashIndex);if(path===''||path===window.location.pathname){link.addEventListener('click',function(e){var el=document.getElementById(hash.slice(1));if(el){e.preventDefault();history.pushState(null,'',hash);scrollToAnchor(hash)}})}})})();
</script>
<script>
/* Lead-to-WhatsApp notification: on any Web3Forms submit, POST the lead to the same-origin
   /wa-lead Pages Function, which calls CallMeBot server-side (apikey hidden, CSP-safe). */
(function(){function g(f,n){var e=f.querySelector('[name="'+n+'"]');return e?(''+e.value).trim():''}document.querySelectorAll('form[action*="web3forms"]').forEach(function(f){f.addEventListener('submit',function(){try{if(g(f,'botcheck'))return;var d={};['name','phone','email','city','service','sqft','message'].forEach(function(n){d[n]=g(f,n)});var data=JSON.stringify(d);if(navigator.sendBeacon){navigator.sendBeacon('/wa-lead',data)}else{fetch('/wa-lead',{method:'POST',body:data,keepalive:true})}}catch(e){}})})})();
</script>"""

def page_head(title, description, canonical_path, og_image="hero-bg.jpg"):
    canonical = f"https://{DOMAIN}{canonical_path}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="geo.region" content="US-FL">
<meta name="geo.placename" content="Palmetto, Florida">
<meta name="geo.position" content="27.5214;-82.5721">
<meta name="ICBM" content="27.5214, -82.5721">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://{DOMAIN}/images/{og_image}">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="Triangle Flooring">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="https://{DOMAIN}/images/{og_image}">
<link rel="icon" type="image/png" sizes="32x32" href="/images/favicon.png">
<link rel="apple-touch-icon" sizes="180x180" href="/images/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Lato:wght@400;700&display=swap" rel="stylesheet">
<style>{SHARED_STYLES}</style>
</head>
<body>"""

def render_faq(faqs):
    """faqs: list of (question, answer_html)"""
    html_items = []
    schema_items = []
    for q, a in faqs:
        html_items.append(f'<details class="faq-item"><summary>{q}</summary><div class="faq-content">{a}</div></details>')
        # Strip HTML tags for schema answer
        plain_a = re.sub(r'<[^>]+>', '', a).strip()
        schema_items.append({"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":plain_a}})
    schema = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":schema_items}
    return f'<div class="faq-list">{"".join(html_items)}</div>', schema

def render_breadcrumb_schema(items):
    """items: list of (name, url|None)"""
    elements = []
    for i, (name, url) in enumerate(items, 1):
        item = {"@type":"ListItem","position":i,"name":name}
        if url: item["item"] = f"https://{DOMAIN}{url}"
        elements.append(item)
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":elements}

def render_local_business_schema(name_suffix, description, page_path, city=None, image=None):
    schema = {
        "@context":"https://schema.org",
        "@type":["LocalBusiness","HomeAndConstructionBusiness"],
        "@id":f"https://{DOMAIN}{page_path}#business",
        "name":f"Triangle Flooring{' — ' + name_suffix if name_suffix else ''}",
        "description":description,
        "url":f"https://{DOMAIN}{page_path}",
        "telephone":PHONE,
        "image":f"https://{DOMAIN}/images/{image or 'hero-bg.jpg'}",
        "address":{"@type":"PostalAddress","streetAddress":"8737 Royal Acacia Ave","addressLocality":"Palmetto","addressRegion":"FL","postalCode":"34221","addressCountry":"US"},
        "geo":{"@type":"GeoCoordinates","latitude":27.5214,"longitude":-82.5723},
        "aggregateRating":{"@type":"AggregateRating","ratingValue":"5.0","reviewCount":"23","bestRating":"5"},
        "priceRange":"$$",
        "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],"opens":"07:00","closes":"19:00"}]
    }
    if city:
        schema["areaServed"] = {"@type":"City","name":city,"containedInPlace":{"@type":"State","name":"Florida"}}
    else:
        schema["areaServed"] = [{"@type":"City","name":c} for c in ["Bradenton","Sarasota","Lakewood Ranch","Palmetto","Parrish","Venice","St. Petersburg","Tampa"]]
    return schema

def render_article_schema(headline, description, slug, image, date_published, date_modified, word_count, category="Flooring"):
    return {
        "@context":"https://schema.org",
        "@type":"Article",
        "@id":f"https://{DOMAIN}/blog/{slug}/#article",
        "headline":headline,
        "description":description,
        "image":[f"https://{DOMAIN}/images/{image}"],
        "datePublished":date_published,
        "dateModified":date_modified,
        "author":{"@type":"Organization","name":"Triangle Flooring","url":f"https://{DOMAIN}/about/"},
        "publisher":{"@type":"Organization","name":"Triangle Flooring","logo":{"@type":"ImageObject","url":f"https://{DOMAIN}/images/logo.png","width":200,"height":200}},
        "mainEntityOfPage":{"@type":"WebPage","@id":f"https://{DOMAIN}/blog/{slug}/"},
        "articleSection":category,
        "wordCount":word_count,
        "inLanguage":"en-US"
    }

def render_common_mistakes_section(service_short):
    return f"""<section style="background:#fff">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Avoid These Pitfalls</span>
      <h2>5 Common Mistakes {service_short} Buyers Make in Florida</h2>
      <p>After 300+ projects, here are the most expensive mistakes we see homeowners make — and how to avoid them.</p>
    </div>
    <div style="max-width:820px;margin:0 auto;display:flex;flex-direction:column;gap:1.4rem">
      <div style="background:var(--gray-light);padding:1.6rem;border-radius:14px;border-left:5px solid var(--orange)">
        <h3 style="margin:0 0 .5rem;color:var(--navy);font-size:1.1rem">1. Skipping the acclimation period</h3>
        <p style="margin:0;color:var(--gray);font-size:.95rem">Florida's outdoor humidity (70-85%) is dramatically different from your air-conditioned interior (45-55%). Materials installed without 48-72 hours of on-site acclimation will gap, buckle, or cup within 6-18 months. Always require documented hygrometer readings before install begins.</p>
      </div>
      <div style="background:var(--gray-light);padding:1.6rem;border-radius:14px;border-left:5px solid var(--orange)">
        <h3 style="margin:0 0 .5rem;color:var(--navy);font-size:1.1rem">2. Choosing the wrong product for the room</h3>
        <p style="margin:0;color:var(--gray);font-size:.95rem">Solid hardwood in a Florida bathroom. Laminate near a sliding door that catches rain. Tile in a bedroom. Each room has constraints — moisture, traffic, sound, comfort. A good contractor asks how you live in the space before recommending a product. Be skeptical of any rep who suggests one product for every room without questions.</p>
      </div>
      <div style="background:var(--gray-light);padding:1.6rem;border-radius:14px;border-left:5px solid var(--orange)">
        <h3 style="margin:0 0 .5rem;color:var(--navy);font-size:1.1rem">3. Choosing the cheapest quote</h3>
        <p style="margin:0;color:var(--gray);font-size:.95rem">Flooring labor varies wildly because installation quality varies wildly. The lowest bid usually means subcontracted crew, no acclimation, no real subfloor prep, and no warranty. The same job done right costs 25-40% more — but lasts 3x longer. We've been hired to redo 30+ floors that were installed by lowest bidders less than 2 years prior.</p>
      </div>
      <div style="background:var(--gray-light);padding:1.6rem;border-radius:14px;border-left:5px solid var(--orange)">
        <h3 style="margin:0 0 .5rem;color:var(--navy);font-size:1.1rem">4. Skipping subfloor preparation</h3>
        <p style="margin:0;color:var(--gray);font-size:.95rem">A perfect floor over a bad subfloor is still a bad floor. Concrete slabs in Florida can have moisture seepage, cracks, and slope issues. Wood subfloors in older homes have squeaks, soft spots, and uneven joists. Skipping prep saves $300-700 upfront and costs $3,000-8,000 in rework two years later. Always insist on documented subfloor moisture testing.</p>
      </div>
      <div style="background:var(--gray-light);padding:1.6rem;border-radius:14px;border-left:5px solid var(--orange)">
        <h3 style="margin:0 0 .5rem;color:var(--navy);font-size:1.1rem">5. Trusting verbal-only quotes</h3>
        <p style="margin:0;color:var(--gray);font-size:.95rem">"It'll be around $5,000" is not a quote — it's a guess. Insist on itemized written estimates: material, labor, removal, transitions, baseboards, subfloor prep, and waste percentage. This protects you from mid-project upcharges and helps you compare apples-to-apples between contractors. We provide every quote in writing within 24 hours of measurement.</p>
      </div>
    </div>
  </div>
</section>"""

def render_why_triangle_section(service_short):
    return f"""<section style="background:var(--gray-light)">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Local vs Big Box</span>
      <h2>Why Choose Triangle Flooring Over Big Box Stores?</h2>
      <p>Big box stores sell flooring. We install it. The difference matters more than people realize.</p>
    </div>
    <div style="max-width:980px;margin:0 auto;overflow-x:auto">
      <table style="width:100%;border-collapse:collapse;font-size:.95rem;background:#fff;border-radius:14px;overflow:hidden;box-shadow:var(--shadow);min-width:640px">
        <thead style="background:linear-gradient(135deg,var(--navy-dark),var(--navy));color:#fff">
          <tr>
            <th style="padding:14px 18px;text-align:left;font-family:var(--font-head);font-weight:600;font-size:.88rem;letter-spacing:.04em;text-transform:uppercase">Factor</th>
            <th style="padding:14px 18px;text-align:left;font-family:var(--font-head);font-weight:600;font-size:.88rem;letter-spacing:.04em;text-transform:uppercase">Big Box Stores</th>
            <th style="padding:14px 18px;text-align:left;font-family:var(--font-head);font-weight:600;font-size:.88rem;letter-spacing:.04em;text-transform:uppercase;background:rgba(224,122,43,.2)">Triangle Flooring</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom:1px solid var(--gray-border)"><td style="padding:13px 18px;font-weight:600;color:var(--text)">Who installs your floor?</td><td style="padding:13px 18px;color:var(--gray)">Subcontracted crew (lowest bidder)</td><td style="padding:13px 18px;color:var(--navy);font-weight:600">Same crew, in-house, owner-supervised</td></tr>
          <tr style="border-bottom:1px solid var(--gray-border);background:var(--gray-light)"><td style="padding:13px 18px;font-weight:600;color:var(--text)">Florida-specific protocols?</td><td style="padding:13px 18px;color:var(--gray)">Generic national install spec</td><td style="padding:13px 18px;color:var(--navy);font-weight:600">42-Point Standard built for Gulf humidity</td></tr>
          <tr style="border-bottom:1px solid var(--gray-border)"><td style="padding:13px 18px;font-weight:600;color:var(--text)">Acclimation enforcement?</td><td style="padding:13px 18px;color:var(--gray)">Often skipped to hit schedule</td><td style="padding:13px 18px;color:var(--navy);font-weight:600">48-72 hr minimum, hygrometer-logged</td></tr>
          <tr style="border-bottom:1px solid var(--gray-border);background:var(--gray-light)"><td style="padding:13px 18px;font-weight:600;color:var(--text)">Subfloor moisture testing?</td><td style="padding:13px 18px;color:var(--gray)">Visual check only</td><td style="padding:13px 18px;color:var(--navy);font-weight:600">Calcium chloride / digital meter, documented</td></tr>
          <tr style="border-bottom:1px solid var(--gray-border)"><td style="padding:13px 18px;font-weight:600;color:var(--text)">Labor warranty?</td><td style="padding:13px 18px;color:var(--gray)">30-90 days typical, fine-print exclusions</td><td style="padding:13px 18px;color:var(--navy);font-weight:600">1-year written, no fine print</td></tr>
          <tr style="border-bottom:1px solid var(--gray-border);background:var(--gray-light)"><td style="padding:13px 18px;font-weight:600;color:var(--text)">Hidden upcharges?</td><td style="padding:13px 18px;color:var(--gray)">Common (subfloor, haul-away, prep)</td><td style="padding:13px 18px;color:var(--navy);font-weight:600">All-in itemized written quote</td></tr>
          <tr style="border-bottom:1px solid var(--gray-border)"><td style="padding:13px 18px;font-weight:600;color:var(--text)">Response time?</td><td style="padding:13px 18px;color:var(--gray)">3-7 days for callbacks</td><td style="padding:13px 18px;color:var(--navy);font-weight:600">Same-day, 7 days a week</td></tr>
          <tr><td style="padding:13px 18px;font-weight:600;color:var(--text)">Local accountability?</td><td style="padding:13px 18px;color:var(--gray)">Corporate hotline (offshore)</td><td style="padding:13px 18px;color:var(--navy);font-weight:600">Direct line to the owner</td></tr>
        </tbody>
      </table>
    </div>
    <p style="text-align:center;font-size:.85rem;color:var(--gray);margin-top:1.2rem;max-width:720px;margin-left:auto;margin-right:auto">We're not knocking the big box stores — they're great for materials. But for {service_short.lower()} <em>installation</em>, the crew that actually nails down your floor makes all the difference.</p>
  </div>
</section>"""

print("Page generator module loaded.")
print("Available helpers: page_head, header, breadcrumbs, whatsapp_banner, final_cta, footer, whatsapp_float, menu_script, render_faq, render_breadcrumb_schema, render_local_business_schema")
