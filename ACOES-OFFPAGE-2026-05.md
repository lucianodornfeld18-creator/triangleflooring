# Ações Off-Page — Triangle Flooring (turnkey)

> Estas são as alavancas de **maior impacto** de SEO/GEO e **não dá pra fazer no código** — são ações suas (Luciano). A auditoria mostrou que o site é ótimo on-page mas invisível off-page; isto resolve o "invisível". Ordem = prioridade.

---

## 1. 🚨 Desbloquear crawlers de IA no Cloudflare (#1 — sem isso, GEO não existe)

**Problema confirmado:** o `robots.txt` ao vivo tem um bloco "Cloudflare Managed Content" com `ai-train=no` + `Disallow: /` pra ClaudeBot/GPTBot/Google-Extended, e o site dá **403 pra bots**. ChatGPT/Perplexity/Gemini não conseguem ler nem citar o site.

**Passos no dashboard Cloudflare** (conta do triangle-floor.com):
1. **SEO → Crawl Control** (ou **Security → Bots**): localizar **"Block AI Scrapers and Crawlers" / "AI Audit"** e **desligar** (ou allow para os bots desejados).
2. **robots.txt gerenciado:** se houver "Managed robots.txt"/"AI Crawl Control" injetando regras, **desativar** para o nosso `robots.txt` (aberto) prevalecer. Ou ajustar Content Signals para `search=yes, ai-input=yes` (`ai-input` = uso em respostas de IA/RAG — é o que queremos).
3. **WAF / Bot Fight Mode:** criar exceção (Skip) para não devolver 403 a: `ChatGPT-User`, `Perplexity-User`, `OAI-SearchBot`, `PerplexityBot`, `ClaudeBot`, `GPTBot`, `Google-Extended`, `Applebot`.
4. **Validar** (rodar no terminal com `!` na frente, ou em qualquer máquina):
   - `curl -A "ClaudeBot" -I https://triangle-floor.com/` → tem que dar **200** (não 403)
   - `curl https://triangle-floor.com/robots.txt` → o bloco do topo não pode ter `Disallow: /` pros bots de IA

---

## 2. 📍 Google Business Profile — volume de reviews + otimização (resolve map pack)

A nota 5.0 é sua maior força, mas **volume** perde (Footprints 50-80+, 50Floor 12k+). Map pack premia volume + proximidade.

- **Campanha de reviews:** pedir review a TODO cliente fechado (link curto do GBP por WhatsApp logo após o último rodapé instalado). Meta: +2-4/mês, mantendo 5.0. Já saiu de 13→20 — manter o ritmo.
- **GBP otimizado (Service-Area Business):** confirmar modo SAB (sem endereço público), categorias (Flooring contractor + Wood floor installer + Tile contractor), área de serviço = as 8 cidades, serviços listados com descrição, fotos de projetos reais com nome geográfico no arquivo.
- **Posts semanais** no GBP (projetos, antes/depois, dica) — sinal de atividade.
- **Q&A:** semear 5-8 perguntas/respostas no GBP (preço, garantia, áreas).

---

## 3. 📒 Diretórios / aggregators (página 1 + fontes que a IA cita)

As listas "Best/Top 10" (Angi, Yelp, Houzz, etc.) **são o que a IA cita** pra "best flooring contractor in [cidade]". Triangle não está em nenhuma. Criar/reivindicar perfis com **NAP idêntico** (abaixo).

| Diretório | Prioridade | Status |
|-----------|-----------|--------|
| Google Business Profile | ★★★ | (existe — otimizar) |
| Yelp for Business | ★★★ | criar/reivindicar |
| Angi (Angie's List) | ★★★ | criar |
| Houzz (Pro) | ★★★ | criar (ótimo p/ flooring) |
| Bing Places | ★★ | criar |
| BBB | ★★ | criar (sinal de confiança) |
| Thumbtack | ★★ | criar |
| HomeAdvisor | ★★ | criar |
| Apple Business Connect | ★★ | criar (Apple Maps/Siri) |
| Nextdoor Business | ★ | criar (local) |
| Facebook (página) | ★ | existe — manter ativa |

### NAP — copiar/colar IDÊNTICO em todo lugar (Service-Area, sem rua pública)
```
Nome:      Triangle Flooring
Telefone:  (941) 402-6861
Email:     trianglefloor@gmail.com
Área:      Palmetto, FL + Bradenton, Sarasota, Lakewood Ranch, Parrish, Venice, Tampa, St. Petersburg
Site:      https://triangle-floor.com
Categoria: Flooring Contractor
Horário:   Mon–Sat 7:00 AM–7:00 PM, Sun fechado
Descrição: Licensed & insured Florida flooring contractor. Hardwood, luxury vinyl plank,
           tile, laminate, stair treads, floor repair, water-damage restoration & hardwood
           refinishing. 300+ projects, 5.0 Google rating, 1-year labor warranty,
           free 24-hour estimates across Tampa Bay & Southwest Florida.
```
> ⚠️ Consistência de NAP é crítica — qualquer variação de nome/telefone confunde o Google e piora o problema de entidade "Triangle Area, NC".

---

## 4. 🏷️ Resolver a confusão de entidade (NC vs FL)

O Google interpreta a marca como "Triangle Flooring – Triangle Area, North Carolina". Combate:
- NAP idêntico em todos os diretórios (acima) sempre com **"Florida / Tampa Bay"**.
- GBP com área de serviço explícita nas 8 cidades FL.
- `sameAs` no schema já aponta IG/FB/Google (deployar o branch garante isso em contact/about).
- Quando possível, mencionar "Tampa Bay, FL" junto da marca em perfis e posts.

---

## 5. ⚙️ Deploy do branch `seo-geo-fixes-2026-05`

Nada do que implementei (Waves 1-3) vale até ir pro ar:
1. Revisar o branch (`git log`, `git diff main`).
2. Merge na `main` + push.
3. Deploy (Cloudflare Pages — `deploy.bat`/`deploy.ps1` ou o fluxo atual).
4. Após deploy: **resubmeter sitemap** no Google Search Console e Bing Webmaster Tools, e usar "URL Inspection" pra forçar indexação das páginas-chave (incluindo a nova `/hardwood-refinishing/`).
