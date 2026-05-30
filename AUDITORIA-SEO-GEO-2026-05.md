# Auditoria SEO + GEO + Internal Linking + Concorrentes — Triangle Flooring

**Data:** 2026-05-29 · **Domínio:** https://triangle-floor.com · **Páginas:** 132 HTML (129 no sitemap)
**Método:** auditoria multi-agente (34 agentes) — 12 templates linha-a-linha, 5 checks site-wide, 6 mercados de concorrentes (SERP ao vivo), 6 verticais de keyword, 5 queries de GEO.
**Volume de achados:** ~188 (19 críticos, 54 high, 71 medium, 44 low) + 61 keyword gaps + ~60 ideias de página nova.

---

## 0. Veredito em uma frase

> O site é **excelente on-page** (schema rico, conteúdo profundo, internal linking hub-spoke, llms.txt) mas está **invisível off-page**: não aparece em SERP não-branded nem no map pack de **nenhum** dos 6 mercados, e a Cloudflare está **bloqueando os crawlers de IA**. O gargalo NÃO é qualidade de conteúdo — é **autoridade, indexação e presença externa**.

Prova: nas 5 queries de teste de IA, o Triangle só foi citado em **1** ("best flooring for Florida humidity"), e mesmo assim de forma instável. Nas 6 cidades, os agentes acharam o Triangle ausente do orgânico comercial e do map pack — só rankeia conteúdo branded/Palmetto (ex.: o post "Hardwood Cost in Palmetto" rankeia #1 e é citado por IA — prova de que a fórmula funciona; só não foi escalada).

---

## P0 — CRÍTICOS (consertar primeiro, alto impacto)

### P0.1 — 🚨 Cloudflare bloqueando crawlers de IA + 403 a bots (mata o GEO)
**Confirmado ao vivo.** O `robots.txt` de produção tem DOIS blocos conflitantes. No topo, um bloco **"Cloudflare Managed Content"**:
- `Content-Signal: search=yes, ai-train=no`
- `User-agent: ClaudeBot → Disallow: /` (idem GPTBot, Google-Extended)

Como o crawler aplica o **primeiro** bloco de user-agent que casa, o `Disallow` da Cloudflare provavelmente **vence** a seção aberta do Triangle. Além disso, o site retornou **HTTP 403** a user-agents não-browser (ChatGPT-User, Perplexity-User, ClaudeBot fazem fetch em tempo real para citar).

**Efeito:** llms.txt + robots aberto são inúteis se a Cloudflare bloqueia. ChatGPT/Claude/Perplexity/Gemini não conseguem ler nem citar o site.

**Fix (no dashboard Cloudflare, NÃO no repo):**
1. Desligar **"Block AI Scrapers and Crawlers" / "AI Audit"** (Managed robots.txt) — ou permitir os bots desejados.
2. Trocar Content-Signal para `search=yes, ai-input=yes` (`ai-input` controla o uso em RAG/respostas de IA — exatamente o que queremos).
3. Criar exceção no **WAF / Bot Fight Mode** para não devolver 403 a ChatGPT-User, Perplexity-User, ClaudeBot, GPTBot, OAI-SearchBot, PerplexityBot.
4. Reconfirmar com `curl -A "ClaudeBot" https://triangle-floor.com/` → deve dar 200.

### P0.2 — 🚨 Confusão de entidade geográfica (Google acha que é "Triangle Area, NC")
Em St. Petersburg, a busca interpretou a marca como **"Triangle Flooring – Triangle Area, North Carolina"** — geo-mismatch que torna a marca **invisível** em Tampa Bay/Pinellas. "Triangle" + flooring colide com a região do Triangle (Raleigh-Durham, NC).
**Fix:** reforçar entidade FL em TUDO — Organization `@id` único com `areaServed` explícito (8 cidades FL), `sameAs` (GBP, Yelp, FB, IG), NAP idêntico em todo lugar, e tagline/title sempre com "Tampa Bay / Bradenton–Sarasota, FL". Considerar disambiguação no GBP e nos diretórios.

### P0.3 — 🚨 Número de reviews bagunçado (visível ≠ schema, em ambas direções)
Três números circulando (6, 13, "300+ projects") e contradições **dentro da mesma página**:
- Páginas serviço+cidade (62): texto visível **"13 verified Google reviews"** mas schema `reviewCount: "6"`.
- Homepage: texto visível **"6 Google Reviews"** mas schema `"13"` (em 2 entidades).
- Hub Bradenton: diz **"13"** na linha 312 E **"Six"** na linha 461 E schema "6".

Google **ignora/penaliza** AggregateRating quando visível ≠ schema. **Fix:** definir **1 fonte de verdade = contagem real do GBP hoje**, e alinhar 100% das páginas (texto + schema). Eu faço isso via patch Python site-wide.

### P0.4 — 🚨 AggregateRating self-serving em 110 páginas (risco de manual action)
5.0★ + 6/13 reviews marcado em 110 LocalBusiness quase idênticas (48 blog cost + 48 serviço+cidade + hubs). Padrão clássico que dispara ação manual do Google e some com os rich snippets.
**Fix:** remover AggregateRating de **todas as sub-páginas** (especialmente dos blog posts — rating em Article é violação). Manter review markup **só** numa entidade Organization central, idealmente com nós `Review` reais (não só agregado).

### P0.5 — Páginas indexáveis fora do sitemap + órfãs
`/thanks/` indexável mas fora do sitemap; sitemap tem 129 vs 132 HTML. `/financing/` é página-pilar com **1 só link interno** (praticamente órfã).
**Fix:** revisar sitemap (incluir o que deve indexar, `noindex` no /thanks/ se for página de conversão), e linkar /financing/ contextualmente (contact, home, about, footer).

---

## P1 — VISIBILIDADE / OFF-PAGE (a causa-raiz dos rankings)

Isto é o que mais move a agulha e **não** está no código — é trabalho de presença. Os concorrentes ganham aqui, não no on-page.

1. **Google Business Profile + volume de reviews.** O rating 5.0 é a maior força real, mas o **volume** perde feio: Footprints 50-80+ (4.8), 50Floor 12.000+ (4.9). Map pack premia volume + proximidade. **Ação:** campanha agressiva de reviews (manter 5.0, crescer volume), GBP em modo Service-Area otimizado por cidade.
2. **Diretórios/aggregators que dominam a página 1 E alimentam a IA.** Triangle **não está** em Angi, Yelp, Houzz, Thumbtack, HomeAdvisor, BBB, Expertise, Porch, HomeGuide. Essas listas "Best/Top 10" são o que a IA cita para "best flooring contractor in [cidade]". **Ação:** criar/verificar perfis com NAP idêntico (SAB, sem rua) e semear reviews.
3. **Páginas service-area reais por cidade (silos).** TODOS os concorrentes rodam página dedicada por cidade. Triangle tem hubs de cidade mas precisa de mais profundidade/entidade local e de city pages para Lakewood Ranch (seu mercado de maior valor, hoje invisível lá).

---

## P1 — INTERNAL LINKING (autoridade interna mal distribuída)

Achado transversal a TODAS as páginas-dinheiro:

1. **Pilares/guides só no dropdown do header — zero links contextuais no corpo.** Guides, FAQ, Glossary, Warranty, Blog não recebem link no texto de nenhuma money page. Autoridade tópica não flui para os pilares (chave de ranking + GEO). **Fix:** injetar links contextuais (ex.: seção de aclimatação → guide; discussão de qualidade → warranty; comparações → guide engineered-vs-solid).
2. **/financing/ órfã** (1 inbound) — ver P0.5.
3. **Glossary sem links bidirecionais:** 30+ termos, só 3 linkam para serviço. Deveria linkar AC Rating→laminate, Janka→hardwood, Porcelain→tile, Vapor Barrier→hardwood, etc. E receber link de volta das money pages.
4. **Distribuição desigual:** hardwood concentra ~419 inbounds vs floor-repair ~281; blog posts fragmentados (muitos com 1-5 inbounds). **Fix:** blocos "related" mais densos e cross-links cost-guide ↔ service page ↔ city hub.
5. **Cost guides órfãos do funil:** ex. /blog/hardwood-flooring-cost-sarasota/ é ótimo asset mas pouco linkado de /sarasota/ e /hardwood-flooring/sarasota/. **Fix:** link proeminente cidade↔custo.

---

## P1 — ON-PAGE / SCHEMA (corrigíveis via template/patch Python)

1. **`geo.placename` = "Palmetto, Florida" em TODAS as páginas** — contradiz title/H1 da cidade-alvo. **Fix:** setar para a cidade da página (Bradenton, Sarasota...). Patch site-wide.
2. **Canibalização de intenção dentro da própria página:** páginas de hardwood (e o warranty) empurram SPC/tile contra o próprio produto ("SPC dominates", "premium SPC is often the smartest pick"). Honesto, mas mata foco de keyword e conversão. **Fix:** reposicionar — hardwood é premium *para casas adequadas* (Lakewood Ranch, Heritage Harbour, builds 2010+); mandar quem quer waterproof para a página de LVP via link, sem desqualificar a própria página.
3. **Schema a consolidar:**
   - Organization/LocalBusiness `@id` único e referenciado (ContactPage e AboutPage têm `mainEntity`/ref **pendente** apontando para Organization que não existe na página).
   - `areaServed` muito estreito (só a City) — virar array com condado + ZIPs.
   - Formatação mista `"@type":` vs `"@type": ` (533 vs 479) → padronizar (sinal de geradores diferentes).
   - OfferCatalog com 8 ofertas **sem `price`/`priceCurrency`** (campos obrigatórios).
   - FAQPage com perguntas duplicadas em 120+ páginas (só muda o nome da cidade) — diferenciar ou reduzir.
   - Glossary sem `DefinedTerm` schema (oportunidade de rich result + GEO).
4. **Titles/metas:** alguns titles >60 chars; metas duplicadas em grupos de páginas; FAQ/Glossary com geo genérico ("Florida") em vez de Tampa Bay/cidade. **Fix:** patch de titles/metas únicos.
5. **Alt text faltando** em imagens de produto/hero (hardwood, water-damage). **Fix:** alt com cidade+material.
6. **Headings answer-ready mas em prosa** — converter seções "How to choose" em listas/tabelas (featured snippet + extração por IA).

---

## P2 — EXPANSÃO DE KEYWORD (61 gaps de alto valor → novas páginas)

A fórmula programática serviço×cidade + cost guide já funciona; **escalar** para o que não existe:

**Hardwood/refinishing:** hub `/hardwood-refinishing/` + `/hardwood-refinishing/[cidade]/` · `/engineered-hardwood/` · herringbone/chevron/parquet · guia condo flooring.
**LVP:** ângulo "waterproof" por cidade · guide SPC vs WPC · LVP para condo/HOA · herringbone vinyl · página "marcas que instalamos" (COREtec/LifeProof/Shaw).
**Tile:** `/tile-installation/shower-tile/` · pool-deck/lanai · backsplash · `/tile-installation/repair/` (regrout) · padrões · comercial.
**Laminate:** guides comparativos (laminate vs LVP, laminate vs hardwood) · waterproof laminate · buying guide (AC rating).
**Stair treads:** `/stair-treads/carpet-to-hardwood/` (+ cost por cidade) · vinyl plank treads · non-slip para idosos · `/stair-railings/`.
**Floor repair (vertical mais sub-atendida e alto ticket):** `/floor-repair/emergency/` (same-day) · `/floor-repair/hurricane-damage/` + flood · subfloor repair · guide buckling/cupping · guide de **seguro** (water-damage insurance claim) · `/commercial-flooring/`.

> Nicho mais lucrativo e menos disputado: **floor repair / water-damage / refinishing**. Demanda alta, ticket alto, e os grandes cobrem mal. Priorizar.

---

## GEO — específico para citação por IA

Além do P0.1 (desbloquear Cloudflare, o pré-requisito):
1. **llms.txt:** remover o vazamento de rua ("8737 Royal Acacia Ave") — inconsistente com SAB.
2. **Trocar AggregateRating por nós `Review` reais** (mais críveis para IA).
3. **`author` Person nomeada** (o instalador-dono) com `jobTitle`, `knowsAbout`, `experiência 300+ installs`, `reviewedBy`/`lastReviewed` — E-E-A-T que a IA valoriza.
4. **Blocos de resposta direta** ("Best flooring contractor in Bradenton: criteria + answer") e `speakable` schema nos guides/cost pages.
5. **De-orfanar os cost assets** e cross-linkar (ver internal linking) — ajuda a IA a corroborar.
6. **Footprint de citação externa** (diretórios/Reddit) — a IA monta "best of" a partir de terceiros; sem isso, conteúdo bom não basta.

---

## Sequência recomendada

| Fase | O quê | Quem | Esforço |
|------|-------|------|---------|
| **Semana 1** | Desbloquear Cloudflare (P0.1); decidir nº real de reviews; patch Python: reviewCount unificado, remover AggregateRating das sub-páginas, geo.placename por cidade, /thanks/+sitemap | Eu (patch) + você (Cloudflare/GBP) | Médio |
| **Semana 1-2** | Internal linking: links contextuais pros pilares, de-orfanar /financing/ e cost guides, glossary bidirecional (patch Python) | Eu | Médio |
| **Semana 2-3** | Off-page: GBP otimizado + campanha de reviews + perfis em diretórios (Angi/Yelp/Houzz/BBB/Thumbtack) | Você | Alto/contínuo |
| **Semana 2-4** | Schema consolidation (Organization @id, areaServed, Offer price, DefinedTerm) + reposicionar copy anti-canibalização | Eu | Médio |
| **Mês 2+** | Novas páginas: floor-repair/water-damage cluster, refinishing hub, Lakewood Ranch city pages, tile sub-serviços | Eu (gerar) | Alto |

> **Regra de ouro (memória do projeto):** aplicação global = **patch cirúrgico em Python** lendo os HTMLs de produção. **Nunca** rerodar `_build_*.py` (regride GA/Ads/Resources/SAB). Sempre `git diff --stat` antes de commitar.
