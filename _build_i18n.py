#!/usr/bin/env python3
"""Build the PT + ES core page clusters (the trilingual AEO brecha, B1/D9).
Reuses SHARED_STYLES from _gen.py at runtime (no CSS duplication). Emits
pt/** and es/** with reciprocal hreflang + LocalBusiness/Breadcrumb/FAQPage/
Service schema. Idempotent (overwrites its own output).
"""
import os, re, json

ROOT = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "triangle-floor.com"
PHONE = "+19414026861"
PHONE_DISP = "(941) 402-6861"
EMAIL = "trianglefloor@gmail.com"
WA = "https://wa.me/19414026861"
SAME_AS = [
    "https://www.facebook.com/people/Triangle-Flooring/61567334333950/",
    "https://www.instagram.com/flooringtriangle",
    "https://share.google/TVRjAYdnZR3TS8Kzq",
    "https://www.yelp.com/biz/triangle-flooring-palmetto",
    "https://www.houzz.com/pro/trianglefloorus/__public",
    "https://nextdoor.com/pages/triangle-flooring/",
]

gen_src = open(os.path.join(ROOT, "_gen.py"), encoding="utf-8").read()
m = re.search(r'SHARED_STYLES\s*=\s*"""(.*?)"""', gen_src, re.S)
SHARED_STYLES = m.group(1)

CITIES = ["Bradenton", "Sarasota", "Lakewood Ranch", "Palmetto", "Parrish", "Venice", "Tampa", "St. Petersburg"]

SERVICES = [
    {"en":"hardwood-flooring","pt":"pisos-de-madeira","es":"pisos-de-madera","price":"$7.35–$20.70/sq ft",
     "pt_name":"Pisos de Madeira","es_name":"Pisos de Madera",
     "pt_desc":"Madeira maciça e engenheirada (carvalho, hickory, maple). Na umidade da Flórida, a madeira engenheirada costuma ser a melhor escolha sobre laje.",
     "es_desc":"Madera sólida y de ingeniería (roble, nogal, arce). En la humedad de Florida, la madera de ingeniería suele ser la mejor opción sobre losa."},
    {"en":"vinyl-plank-flooring","pt":"piso-vinilico","es":"piso-vinilico","price":"$3.91–$11.11/sq ft",
     "pt_name":"Piso Vinílico (LVP)","es_name":"Piso Vinílico (LVP)",
     "pt_desc":"SPC/WPC 100% à prova d'água — a melhor opção para a umidade da Flórida, cozinhas, banheiros e aluguéis de temporada.",
     "es_desc":"SPC/WPC 100% impermeable — la mejor opción para la humedad de Florida, cocinas, baños y alquileres vacacionales."},
    {"en":"tile-installation","pt":"instalacao-de-azulejos","es":"instalacion-de-azulejos","price":"$7.50–$22.00/sq ft",
     "pt_name":"Instalação de Azulejos","es_name":"Instalación de Azulejos",
     "pt_desc":"Porcelanato e cerâmica (metrô, espinha de peixe, grande formato, mosaico). O melhor desempenho a longo prazo na umidade da Flórida.",
     "es_desc":"Porcelanato y cerámica (metro, espiga, gran formato, mosaico). El mejor rendimiento a largo plazo en la humedad de Florida."},
    {"en":"laminate-flooring","pt":"piso-laminado","es":"piso-laminado","price":"$3.50–$8.50/sq ft",
     "pt_name":"Piso Laminado","es_name":"Piso Laminado",
     "pt_desc":"Visual de madeira com bom custo (classificação AC4–AC5). Não impermeável — use vinílico em áreas molhadas.",
     "es_desc":"Aspecto de madera económico (clasificación AC4–AC5). No impermeable — use vinílico en áreas húmedas."},
    {"en":"stair-treads","pt":"degraus-de-escada","es":"peldanos-de-escalera","price":"$80–$220",
     "pt_name":"Degraus de Escada","es_name":"Peldaños de Escalera",
     "pt_desc":"Substituição de degraus em madeira maciça (carvalho, maple, hickory, nogal) — troca de carpete ou degraus de construtora.",
     "es_desc":"Reemplazo de peldaños en madera sólida (roble, arce, nogal) — cambio de alfombra o peldaños de constructora."},
    {"en":"floor-repair","pt":"reparo-de-pisos","es":"reparacion-de-pisos","price":"$250–$1,500+",
     "pt_name":"Reparo de Pisos","es_name":"Reparación de Pisos",
     "pt_desc":"Tábuas, dano por água, rangidos, frestas e transições. Reparo pós-vazamento e pós-furacão.",
     "es_desc":"Tablas, daño por agua, crujidos, huecos y transiciones. Reparación tras fugas y huracanes."},
]

L = {
  "pt": {
    "lang":"pt-BR","locale":"pt_BR",
    "nav":{"home":"Início","services":"Serviços","areas":"Regiões","blog":"Blog","about":"Sobre","contact":"Contato","quote":"Orçamento Grátis"},
    "free_quote":"Orçamento grátis em 24h","call":"Ligar","whatsapp":"WhatsApp",
    "trust":["300+ obras concluídas","Avaliação 5★ no Google","Licenciada e segurada","Garantia de 1 ano"],
    "hero_home_h1":"Empresa de Pisos em Bradenton, Sarasota e Tampa Bay",
    "hero_home_sub":"Madeira, vinílico, porcelanato e laminado instalados por um profissional que fala português. 300+ obras na Flórida · orçamento itemizado em 24 horas.",
    "intro_home":"A Triangle Flooring é uma empresa de pisos licenciada e segurada, com sede em Palmetto (FL), atendendo Bradenton, Sarasota, Lakewood Ranch, Palmetto, Parrish, Venice, Tampa e St. Petersburg. Fundada por um instalador com mais de 5 anos de experiência na Flórida, já concluímos mais de 300 obras com nota 5,0 no Google. Atendemos em português, espanhol e inglês.",
    "services_h":"Nossos Serviços de Piso","areas_h":"Onde Atendemos","faq_h":"Perguntas Frequentes",
    "cta_h":"Peça seu orçamento grátis hoje","cta_p":"Da primeira ligação ao último rodapé — instalação à prova da Flórida em toda Tampa Bay. Medição grátis. Preço travado. Garantia de 1 ano.",
    "cta_btn":"Quero meu orçamento grátis","speak":"Falamos português",
    "from":"A partir de","learn":"Saiba mais","price_note":"Todos os orçamentos são itemizados por escrito — sem preço de pacote opaco. Preços 2026, por sq ft instalado.",
    "contact_h1":"Contato — Orçamento Grátis de Piso","contact_sub":"Resposta no mesmo dia em português. Ligue, mande mensagem ou WhatsApp.",
    "contact_intro":"Peça seu orçamento grátis e itemizado em até 24 horas. Atendemos Bradenton, Sarasota, Tampa Bay e toda a região — em português, espanhol e inglês.",
    "hours":"Seg–Sáb · 7h–19h",
  },
  "es": {
    "lang":"es","locale":"es_US",
    "nav":{"home":"Inicio","services":"Servicios","areas":"Áreas","blog":"Blog","about":"Acerca","contact":"Contacto","quote":"Presupuesto Gratis"},
    "free_quote":"Presupuesto gratis en 24h","call":"Llamar","whatsapp":"WhatsApp",
    "trust":["300+ proyectos completados","Calificación 5★ en Google","Con licencia y seguro","Garantía de 1 año"],
    "hero_home_h1":"Compañía de Pisos en Bradenton, Sarasota y Tampa Bay",
    "hero_home_sub":"Madera, vinílico, porcelanato y laminado instalados por un profesional que habla español. 300+ proyectos en Florida · presupuesto detallado en 24 horas.",
    "intro_home":"Triangle Flooring es una compañía de pisos con licencia y seguro, con sede en Palmetto (FL), que atiende Bradenton, Sarasota, Lakewood Ranch, Palmetto, Parrish, Venice, Tampa y St. Petersburg. Fundada por un instalador con más de 5 años de experiencia en Florida, hemos completado más de 300 proyectos con calificación 5.0 en Google. Atendemos en español, portugués e inglés.",
    "services_h":"Nuestros Servicios de Pisos","areas_h":"Dónde Trabajamos","faq_h":"Preguntas Frecuentes",
    "cta_h":"Pida su presupuesto gratis hoy","cta_p":"De la primera llamada al último zócalo — instalación a prueba de Florida en todo Tampa Bay. Medición gratis. Precio fijo. Garantía de 1 año.",
    "cta_btn":"Quiero mi presupuesto gratis","speak":"Hablamos español",
    "from":"Desde","learn":"Más información","price_note":"Todos los presupuestos son detallados por escrito — sin precios de paquete opacos. Precios 2026, por sq ft instalado.",
    "contact_h1":"Contacto — Presupuesto Gratis de Pisos","contact_sub":"Respuesta el mismo día en español. Llame, escriba o WhatsApp.",
    "contact_intro":"Pida su presupuesto gratis y detallado en 24 horas. Atendemos Bradenton, Sarasota, Tampa Bay y toda la región — en español, portugués e inglés.",
    "hours":"Lun–Sáb · 7am–7pm",
  }
}

FAQ = {
 "pt":[
  ("Vocês falam português?","Sim. Atendemos em português, espanhol e inglês — por telefone, WhatsApp, e-mail e pessoalmente."),
  ("Quanto custa instalar piso na Flórida?","Madeira $7,35–$20,70/sq ft · vinílico (LVP) $3,91–$11,11 · porcelanato $7,50–$22,00 · laminado $3,50–$8,50, instalados. Todo orçamento é itemizado por escrito."),
  ("Qual o melhor piso para a umidade da Flórida?","Porcelanato e vinílico (LVP) são os mais tolerantes à umidade; madeira engenheirada supera a maciça sobre laje. Evite madeira maciça e laminado em áreas molhadas."),
  ("O orçamento é grátis?","Sim — medição em casa, por escrito e itemizada, em até 24 horas."),
  ("Quais cidades vocês atendem?","Bradenton, Sarasota, Lakewood Ranch, Palmetto, Parrish, Venice, Tampa e St. Petersburg — cerca de 60 milhas de Palmetto."),
 ],
 "es":[
  ("¿Hablan español?","Sí. Atendemos en español, portugués e inglés — por teléfono, WhatsApp, correo y en persona."),
  ("¿Cuánto cuesta instalar pisos en Florida?","Madera $7.35–$20.70/sq ft · vinílico (LVP) $3.91–$11.11 · porcelanato $7.50–$22.00 · laminado $3.50–$8.50, instalados. Todo presupuesto es detallado por escrito."),
  ("¿Cuál es el mejor piso para la humedad de Florida?","Porcelanato y vinílico (LVP) son los más tolerantes a la humedad; la madera de ingeniería supera a la sólida sobre losa. Evite madera sólida y laminado en áreas húmedas."),
  ("¿El presupuesto es gratis?","Sí — medición en casa, por escrito y detallada, en 24 horas."),
  ("¿Qué ciudades atienden?","Bradenton, Sarasota, Lakewood Ranch, Palmetto, Parrish, Venice, Tampa y St. Petersburg — unas 60 millas de Palmetto."),
 ],
}

def hreflang_block(en_path, pt_path, es_path):
    return (f'<link rel="alternate" hreflang="en" href="https://{DOMAIN}{en_path}">\n'
            f'<link rel="alternate" hreflang="pt-BR" href="https://{DOMAIN}{pt_path}">\n'
            f'<link rel="alternate" hreflang="es" href="https://{DOMAIN}{es_path}">\n'
            f'<link rel="alternate" hreflang="x-default" href="https://{DOMAIN}{en_path}">')

def head(title, desc, path, lang, locale, en_path, pt_path, es_path):
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://{DOMAIN}{path}">
{hreflang_block(en_path, pt_path, es_path)}
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="geo.region" content="US-FL">
<meta name="geo.placename" content="Palmetto, Florida">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://{DOMAIN}{path}">
<meta property="og:image" content="https://{DOMAIN}/images/hero-bg.jpg">
<meta property="og:locale" content="{locale}">
<meta property="og:site_name" content="Triangle Flooring">
<link rel="icon" type="image/png" sizes="32x32" href="/images/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Lato:wght@400;700&display=swap" rel="stylesheet">
<style>{SHARED_STYLES}
.lang-switch{{display:inline-flex;gap:6px;align-items:center;margin-left:8px}}
.lang-switch a{{font-size:.8rem;font-weight:700;color:var(--gray);padding:3px 7px;border-radius:6px}}
.lang-switch a.active{{background:var(--navy);color:#fff}}
.quick-answer{{background:var(--navy-light);border-left:4px solid var(--cerulean);padding:16px 20px;border-radius:0 10px 10px 0;margin:0 auto 1.6rem;max-width:780px;font-size:1.02rem;line-height:1.6;color:var(--navy-dark)}}
.svc-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1.3rem;margin-top:2rem}}
.svc-card{{background:#fff;border:1px solid var(--gray-border);border-radius:14px;padding:1.5rem;text-decoration:none;color:inherit;transition:all .25s;box-shadow:var(--shadow-sm)}}
.svc-card:hover{{transform:translateY(-4px);box-shadow:var(--shadow-lg);border-color:var(--cerulean)}}
.svc-card h3{{color:var(--navy);margin:0 0 .4rem;font-size:1.18rem}}
.svc-card .px{{color:var(--orange);font-weight:800;font-family:var(--font-head);font-size:.95rem;margin:.3rem 0}}
.svc-card p{{color:var(--gray);font-size:.92rem;margin:0}}
</style>
</head>
<body>"""

def header(lang, en_path, pt_path, es_path):
    t = L[lang]["nav"]
    sw = (f'<div class="lang-switch"><a href="{en_path}">EN</a>'
          f'<a href="{pt_path}" class="{"active" if lang=="pt" else ""}">PT</a>'
          f'<a href="{es_path}" class="{"active" if lang=="es" else ""}">ES</a></div>')
    base = f"/{lang}/"
    svc_links = "".join(f'<a href="/{lang}/{s[lang]}/">{s[lang+"_name"]}</a>' for s in SERVICES)
    return f"""<header class="site-header"><nav class="nav-bar" aria-label="Main">
  <a href="{base}" class="brand"><img src="/images/logo.png" alt="Triangle Flooring" width="46" height="46"><div class="brand-text"><span class="brand-name">Triangle Flooring</span><span class="brand-tag">Bradenton · Sarasota · Tampa</span></div></a>
  <ul class="nav-menu" id="navMenu">
    <li><a href="{base}">{t['home']}</a></li>
    <li><a href="/{lang}/{SERVICES[0][lang]}/" data-toggle>{t['services']}</a><div class="dropdown">{svc_links}</div></li>
    <li><a href="/bradenton/">{t['areas']}</a></li>
    <li><a href="/{lang}/contato/">{t['contact']}</a></li>
  </ul>
  <div class="nav-cta">
    <a href="tel:{PHONE}" class="nav-phone"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.28-.28.67-.36 1.02-.25 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg><span>{PHONE_DISP}</span></a>
    <a href="/{lang}/contato/" class="btn btn-primary">{t['quote']}</a>
    {sw}
    <button class="menu-toggle" id="menuToggle" aria-label="Menu" aria-expanded="false"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg></button>
  </div>
</nav></header>"""

def hero(eyebrow, h1, sub, lang):
    t = L[lang]
    trust = "".join(f'<span class="hero-trust-item">{x}</span>' for x in t["trust"])
    return f"""<section class="page-hero">
  <div class="container">
    <span class="eyebrow">{eyebrow}</span>
    <h1>{h1}</h1>
    <p>{sub}</p>
    <div class="final-cta-buttons">
      <a href="tel:{PHONE}" class="btn btn-primary btn-large">📞 {PHONE_DISP}</a>
      <a href="{WA}" target="_blank" rel="noopener" class="btn btn-ghost">💬 {t['whatsapp']}</a>
    </div>
    <div class="page-hero-trust">{trust}</div>
  </div>
</section>"""

def faq_section(lang):
    items = FAQ[lang]
    html = "".join(f'<details class="faq-item"><summary>{q}</summary><div class="faq-content"><p>{a}</p></div></details>' for q,a in items)
    schema = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in items]}
    return f'<section class="faq-section"><div class="container"><div class="section-head"><h2>{L[lang]["faq_h"]}</h2></div><div class="faq-list">{html}</div></div></section>', schema

def final_cta(lang):
    t = L[lang]
    return f"""<section class="final-cta"><div class="final-cta-content">
    <h2>{t['cta_h']}</h2><p>{t['cta_p']}</p>
    <a href="tel:{PHONE}" class="cta-phone-large">📞 {PHONE_DISP}</a>
    <div class="final-cta-buttons"><a href="/{lang}/contato/" class="btn btn-primary">{t['cta_btn']}</a>
    <a href="{WA}" target="_blank" rel="noopener" class="btn btn-ghost">💬 {t['whatsapp']}</a></div>
  </div></section>"""

def footer(lang):
    t = L[lang]
    svc = "".join(f'<li><a href="/{lang}/{s[lang]}/">{s[lang+"_name"]}</a></li>' for s in SERVICES)
    areas = "".join(f'<li><a href="/{c.lower().replace(". ","-").replace(" ","-")}/">{c}, FL</a></li>' for c in CITIES)
    return f"""<footer><div class="container"><div class="footer-grid">
    <div class="footer-col"><div class="footer-brand"><img src="/images/logo.png" alt="Triangle Flooring"><strong>Triangle Flooring</strong></div>
      <p>{t['intro_home'][:180]}…</p>
      <div class="social-icons">
        <a href="https://www.instagram.com/flooringtriangle" target="_blank" rel="noopener" aria-label="Instagram"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.2c3.2 0 3.6 0 4.85.07 3.25.15 4.77 1.69 4.92 4.92.06 1.27.07 1.65.07 4.85s0 3.58-.07 4.85c-.15 3.23-1.66 4.77-4.92 4.92-1.27.06-1.64.07-4.85.07s-3.58 0-4.85-.07c-3.26-.15-4.77-1.7-4.92-4.92C2.16 15.58 2.15 15.2 2.15 12s0-3.58.07-4.85C2.37 3.92 3.88 2.38 7.14 2.23 8.41 2.17 8.79 2.16 12 2.16z"/></svg></a>
        <a href="https://www.facebook.com/people/Triangle-Flooring/61567334333950/" target="_blank" rel="noopener" aria-label="Facebook"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.07C24 5.44 18.63.07 12 .07S0 5.44 0 12.07c0 5.99 4.39 10.95 10.13 11.85v-8.38H7.08v-3.47h3.05V9.43c0-3 1.79-4.67 4.53-4.67 1.31 0 2.69.24 2.69.24v2.95h-1.52c-1.49 0-1.96.93-1.96 1.87v2.25h3.33l-.53 3.47h-2.8v8.38C19.61 23.02 24 18.06 24 12.07z"/></svg></a>
        <a href="https://share.google/TVRjAYdnZR3TS8Kzq" target="_blank" rel="noopener" aria-label="Google"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/></svg></a>
      </div></div>
    <div class="footer-col"><h4>{t['nav']['services']}</h4><ul>{svc}</ul></div>
    <div class="footer-col"><h4>{t['nav']['areas']}</h4><ul>{areas}</ul></div>
    <div class="footer-col"><h4>{t['nav']['contact']}</h4>
      <div class="footer-contact-item"><a href="tel:{PHONE}">{PHONE_DISP}</a></div>
      <div class="footer-contact-item"><a href="mailto:{EMAIL}">{EMAIL}</a></div>
      <div class="footer-contact-item"><span>Palmetto, FL 34221</span></div>
      <div class="footer-contact-item"><span>{t['hours']}</span></div>
      <div class="footer-contact-item"><strong style="color:#FFC993">🗣️ {t['speak']}</strong></div>
    </div></div>
    <div class="footer-bottom"><div>© 2026 Triangle Flooring.</div><div><a href="/">English</a> · <a href="/pt/">Português</a> · <a href="/es/">Español</a></div></div>
  </div></footer>"""

def whatsapp_float(lang):
    return f'<a href="{WA}" target="_blank" rel="noopener" class="whatsapp-float" aria-label="WhatsApp"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.07-.3-.15-1.26-.46-2.39-1.48-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.61-.92-2.21-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48 0 1.46 1.07 2.88 1.21 3.07.15.2 2.1 3.2 5.08 4.49.71.3 1.26.49 1.69.62.71.23 1.36.2 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.18-1.41-.08-.13-.27-.2-.57-.35z"/></svg><span>{L[lang]["whatsapp"]}</span></a>'

def menu_script():
    return """<script>(function(){var t=document.getElementById('menuToggle'),m=document.getElementById('navMenu');if(!t)return;t.addEventListener('click',function(){var o=m.classList.toggle('open');t.setAttribute('aria-expanded',o)});m.querySelectorAll('a[data-toggle]').forEach(function(a){a.addEventListener('click',function(e){if(window.innerWidth>960)return;e.preventDefault();a.parentElement.classList.toggle('expanded')})})})();</script>"""

def local_business(path, name_suffix=None):
    return {"@context":"https://schema.org","@type":["LocalBusiness","HomeAndConstructionBusiness"],
         "@id":f"https://{DOMAIN}{path}#business",
         "name":"Triangle Flooring" + (f" — {name_suffix}" if name_suffix else ""),
         "url":f"https://{DOMAIN}{path}","telephone":PHONE,
         "image":f"https://{DOMAIN}/images/hero-bg.jpg",
         "address":{"@type":"PostalAddress","streetAddress":"8737 Royal Acacia Ave","addressLocality":"Palmetto","addressRegion":"FL","postalCode":"34221","addressCountry":"US"},
         "geo":{"@type":"GeoCoordinates","latitude":27.5214,"longitude":-82.5723},
         "priceRange":"$$","knowsLanguage":["en","pt","es"],"sameAs":SAME_AS,
         "areaServed":[{"@type":"City","name":c} for c in CITIES],
         "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],"opens":"07:00","closes":"19:00"}]}

def breadcrumb(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":i+1,"name":n,**({"item":f"https://{DOMAIN}{u}"} if u else {})} for i,(n,u) in enumerate(items)]}

def schema_block(*objs):
    return "".join(f'<script type="application/ld+json">{json.dumps(o,ensure_ascii=False,separators=(",",":"))}</script>' for o in objs)

def write(path_rel, html):
    full = os.path.join(ROOT, path_rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8", newline="").write(html)

built = []

# HOME
for lang in ("pt","es"):
    t = L[lang]; path = f"/{lang}/"
    en_p, pt_p, es_p = "/", "/pt/", "/es/"
    title = (t["hero_home_h1"] + " | Triangle Flooring")[:65]
    desc = t["hero_home_sub"][:158]
    svc_cards = "".join(f'<a class="svc-card" href="/{lang}/{s[lang]}/"><h3>{s[lang+"_name"]}</h3><div class="px">{t["from"]} {s["price"]}</div><p>{s[lang+"_desc"]}</p></a>' for s in SERVICES)
    area_links = "".join(f'<a class="svc-card" style="text-align:center" href="/{c.lower().replace(". ","-").replace(" ","-")}/"><h3 style="font-size:1rem;margin:0">📍 {c}, FL</h3></a>' for c in CITIES)
    faq_html, faq_schema = faq_section(lang)
    body = f"""{hero(t["speak"], t["hero_home_h1"], t["hero_home_sub"], lang)}
<section><div class="container"><div class="quick-answer">{t['intro_home'][:280]}</div>
  <div class="section-head"><h2>{t['services_h']}</h2></div>
  <div class="svc-grid">{svc_cards}</div>
  <p class="pricing-note">{t['price_note']}</p>
</div></section>
<section class="services"><div class="container"><div class="section-head"><h2>{t['areas_h']}</h2></div>
  <div class="svc-grid">{area_links}</div></div></section>
{faq_html}
{final_cta(lang)}"""
    sch = schema_block(local_business(path), breadcrumb([(t["nav"]["home"],None)]), faq_schema)
    html = head(title, desc, path, t["lang"], t["locale"], en_p, pt_p, es_p) + header(lang,en_p,pt_p,es_p) + body + footer(lang) + whatsapp_float(lang) + sch + menu_script() + "\n</body></html>"
    write(f"{lang}/index.html", html); built.append(path)

# SERVICE HUBS
for lang in ("pt","es"):
    t = L[lang]
    for s in SERVICES:
        slug = s[lang]; name = s[lang+"_name"]; desc_s = s[lang+"_desc"]
        path = f"/{lang}/{slug}/"
        en_p = f"/{s['en']}/"; pt_p = f"/pt/{s['pt']}/"; es_p = f"/es/{s['es']}/"
        title = (f"{name} em Bradenton & Sarasota FL | Triangle Flooring" if lang=="pt" else f"{name} en Bradenton & Sarasota FL | Triangle Flooring")[:65]
        desc = desc_s[:158]
        quick = (f"{name}: {desc_s} {t['from']} {s['price']} instalado. Orçamento itemizado grátis em 24h, atendimento em português." if lang=="pt"
                 else f"{name}: {desc_s} {t['from']} {s['price']} instalado. Presupuesto detallado gratis en 24h, atención en español.")
        others = "".join(f'<a class="svc-card" href="/{lang}/{o[lang]}/"><h3>{o[lang+"_name"]}</h3><div class="px">{t["from"]} {o["price"]}</div></a>' for o in SERVICES if o["en"]!=s["en"])
        faq_html, faq_schema = faq_section(lang)
        body = f"""{hero(t["speak"], name + (" na Flórida" if lang=="pt" else " en Florida"), desc_s, lang)}
<section><div class="container"><div class="quick-answer">{quick}</div>
  <div class="intro-content"><p>{t['intro_home']}</p><p><strong>{name}</strong> — {desc_s} {t['price_note']}</p></div>
  <div class="whatsapp-banner"><div class="whatsapp-banner-text"><strong>{t['free_quote']}.</strong><span>{t['speak']} · {t['hours']}</span></div>
    <a href="{WA}" target="_blank" rel="noopener" class="whatsapp-banner-btn">💬 {t['whatsapp']}</a></div>
  <div class="section-head" style="margin-top:1rem"><h2>{t['services_h']}</h2></div>
  <div class="svc-grid">{others}</div>
</div></section>
{faq_html}
{final_cta(lang)}"""
        sch = schema_block(local_business(path, name_suffix=name),
                           {"@context":"https://schema.org","@type":"Service","name":name,"serviceType":name,
                            "provider":{"@id":f"https://{DOMAIN}{path}#business"},
                            "areaServed":[{"@type":"City","name":c} for c in CITIES],
                            "offers":{"@type":"Offer","priceCurrency":"USD","price":s["price"]}},
                           breadcrumb([(t["nav"]["home"],f"/{lang}/"),(name,None)]), faq_schema)
        html = head(title, desc, path, t["lang"], t["locale"], en_p, pt_p, es_p) + header(lang,en_p,pt_p,es_p) + body + footer(lang) + whatsapp_float(lang) + sch + menu_script() + "\n</body></html>"
        write(f"{lang}/{slug}/index.html", html); built.append(path)

# CONTACT
for lang in ("pt","es"):
    t = L[lang]; path = f"/{lang}/contato/"
    en_p = "/contact/"; pt_p="/pt/contato/"; es_p="/es/contato/"
    title = (t["contact_h1"] + " | Triangle Flooring")[:65]
    desc = t["contact_sub"][:158]
    faq_html, faq_schema = faq_section(lang)
    body = f"""{hero(t["speak"], t["contact_h1"], t["contact_sub"], lang)}
<section><div class="container"><div class="quick-answer">{t['contact_intro']}</div>
  <div class="intro-content" style="text-align:center">
    <p style="font-size:1.3rem"><strong>📞 <a href="tel:{PHONE}">{PHONE_DISP}</a></strong></p>
    <p>✉️ <a href="mailto:{EMAIL}">{EMAIL}</a><br>💬 <a href="{WA}" target="_blank" rel="noopener">WhatsApp</a><br>📍 Palmetto, FL 34221 · {t['hours']}</p>
    <p><strong style="color:var(--orange)">🗣️ {t['speak']}</strong></p>
    <a href="{WA}" target="_blank" rel="noopener" class="btn btn-primary btn-large">💬 {t['whatsapp']}</a>
  </div></div></section>
{faq_html}
{final_cta(lang)}"""
    sch = schema_block(local_business(path),
                       {"@context":"https://schema.org","@type":"ContactPage","name":t["contact_h1"],"url":f"https://{DOMAIN}{path}"},
                       breadcrumb([(t["nav"]["home"],f"/{lang}/"),(t["nav"]["contact"],None)]), faq_schema)
    html = head(title, desc, path, t["lang"], t["locale"], en_p, pt_p, es_p) + header(lang,en_p,pt_p,es_p) + body + footer(lang) + whatsapp_float(lang) + sch + menu_script() + "\n</body></html>"
    write(f"{lang}/contato/index.html", html); built.append(path)

print(json.dumps({"built": len(built), "pages": built}, indent=2, ensure_ascii=False))
