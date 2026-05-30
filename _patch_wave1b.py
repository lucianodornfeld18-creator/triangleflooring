import glob,os,re
# 1) add /financing/ to sitemap
sm=open("sitemap.xml",encoding="utf-8").read()
if "financing/</loc>" not in sm:
    entry='  <url>\n    <loc>https://triangle-floor.com/financing/</loc>\n    <lastmod>2026-05-29</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n'
    sm=sm.replace("</urlset>",entry+"</urlset>")
    open("sitemap.xml","w",encoding="utf-8").write(sm)
    print("sitemap: /financing/ adicionado")
else:
    print("sitemap: /financing/ ja presente")

# 2) inject "Helpful Guides & Resources" block before final-cta on service pages
GUIDES={
 "hardwood-flooring":[("/guides/engineered-vs-solid-hardwood-florida/","Engineered vs Solid Hardwood","Which wins in Florida humidity"),
                      ("/guides/hardwood-vs-vinyl-plank-florida/","Hardwood vs Vinyl Plank","Cost, durability &amp; resale compared")],
 "vinyl-plank-flooring":[("/guides/waterproof-flooring-florida/","Waterproof Flooring Options","LVP, tile &amp; laminate compared"),
                      ("/guides/hardwood-vs-vinyl-plank-florida/","Hardwood vs Vinyl Plank","Cost, durability &amp; resale compared")],
 "tile-installation":[("/guides/waterproof-flooring-florida/","Waterproof Flooring Options","LVP, tile &amp; laminate compared"),
                      ("/guides/pet-friendly-flooring-florida/","Pet &amp; Kid-Friendly Flooring","Scratch &amp; stain resistance ranked")],
 "laminate-flooring":[("/guides/waterproof-flooring-florida/","Waterproof Flooring Options","LVP, tile &amp; laminate compared"),
                      ("/guides/hardwood-vs-vinyl-plank-florida/","Hardwood vs Vinyl Plank","Cost, durability &amp; resale compared")],
 "stair-treads":[("/guides/engineered-vs-solid-hardwood-florida/","Engineered vs Solid Hardwood","Which wins in Florida humidity"),
                      ("/guides/pet-friendly-flooring-florida/","Pet &amp; Kid-Friendly Flooring","Scratch &amp; stain resistance ranked")],
 "floor-repair":[("/guides/waterproof-flooring-florida/","Waterproof Flooring Options","LVP, tile &amp; laminate compared"),
                      ("/guides/pet-friendly-flooring-florida/","Pet &amp; Kid-Friendly Flooring","Scratch &amp; stain resistance ranked")],
}
def block(svc):
    g=GUIDES[svc]
    cards="".join('<a href="%s" class="related-card"><strong>%s →</strong><span>%s</span></a>'%(u,t,d) for u,t,d in g)
    cards+='<a href="/glossary/" class="related-card"><strong>Flooring Glossary →</strong><span>Plain-English flooring terms explained</span></a>'
    cards+='<a href="/financing/" class="related-card"><strong>Flooring Financing →</strong><span>Flexible payment options for your project</span></a>'
    return ('<section class="related" style="background:var(--gray-light)">\n  <div class="container">\n'
            '    <div class="section-head"><span class="eyebrow">Before You Buy</span><h2>Helpful Guides &amp; Resources</h2></div>\n'
            '    <div class="related-grid">'+cards+'</div>\n  </div>\n</section>\n\n')

n=0
for svc in GUIDES:
    for f in glob.glob(svc+"/**/index.html",recursive=True):
        s=open(f,encoding="utf-8").read()
        if "Helpful Guides &amp; Resources" in s:  continue
        if '<section class="final-cta">' not in s:  continue
        s=s.replace('<section class="final-cta">', block(svc)+'<section class="final-cta">',1)
        open(f,"w",encoding="utf-8").write(s); n+=1
print("bloco 'Helpful Guides' injetado em",n,"paginas de servico")
