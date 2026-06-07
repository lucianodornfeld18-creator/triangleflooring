# Handoff — Automação de Blog Triangle Flooring (GEO/AEO)
_Última sessão: 2026-06-07 · branch `main` sincronizada com `origin/main`_

## O que foi feito nesta sessão (✅ commitado e pushado)
- **Post novo:** `/blog/water-damaged-hardwood-floor-repair-florida/` — guia how-to AEO "How to Fix Water-Damaged Hardwood Floors in Florida" (1.773 palavras, answer-first/speakable, 2 tabelas, FAQ 6Q, schema Breadcrumb+Article+FAQPage+LocalBusiness, autor E-E-A-T Jose Mauricio). Pilar comercial = `/floor-repair/water-damage/`; o post é suporte informacional e linka pra ele (sem canibalizar).
- **Ledger anti-canibalização criado:** `_content_map.json` (132 URLs classificadas). É a **memória entre execuções** — base de qualquer automação futura. Gerado por `_build_content_map.py` (lê o sitemap + taxonomia de cidades/serviços).
- **Scripts:** `_build_water_damage_post.py` (gera o post fatiando boilerplate de um post exemplar), `_validate_post.py` (22 checagens: JSON-LD, FAQ==schema, links, unicidade title/meta, GA não-duplicado).
- **Integração:** card no índice do blog (53→54), sitemap (nova URL + lastmod das 4 páginas que passaram a linkar), interlinks reversos em `/floor-repair/water-damage/`, `/floor-repair/`, `/blog/hardwood-floor-refinishing-tampa-bay/`.
- **Commits:** `9844016` (blog) + `bd95331` (homepage: hero full-bleed + form inline Web3Forms, que estava pendente de antes).

## Fatos do repo que NÃO são óbvios (ler antes de mexer)
- **Não existe `_data.py` nem `CLAUDE.md`.** Config (NAP, schema, telefone) vive em `_gen.py`; cidades/serviços em `_build_services.py` (`CITIES`, `SERVICES`).
- **Build roda em sandbox na nuvem:** `OUT_DIR=/home/claude/triangle`. NÃO roda local. O repo guarda só o HTML de saída. Por isso o método adotado é **escrever HTML direto no padrão `_gen.py`** (paridade byte-a-byte) + validar — não rodar `_build_*.py` local.
- **`_gen.py` está DEFASADO vs HTML publicado** (header/footer renderizados têm "Hardwood Refinishing", dropdown "Resources", `/directories/`, autor "Jose Mauricio"). Para criar páginas novas, **fatiar boilerplate de um post recente** (ex. `blog/best-flooring-florida-humidity/index.html`), não usar `_gen.header()/footer()`.
- **Cidades:** Tier 1 = bradenton, sarasota, lakewood-ranch, palmetto, parrish, venice · Tier 2 = tampa, st-petersburg.
- **Custo-por-cidade está SATURADO** (48 posts). Não criar mais nada nessa intenção.
- Deploy: Cloudflare Pages (push no `main` publica). RSS não existe (só sitemap.xml).

## AUTOMAÇÃO — cadência DECIDIDA (2026-06-07)
Arquitetura = **routine agendado** (`/schedule`) que clona o repo do GitHub, roda o pipeline lendo `_content_map.json` (o que existe) + `_content_queue.json` (o que falta + ordem), gera+valida+integra, e commita/PR. Cloudflare publica no push. Não dá cron "burro" (exige julgamento de IA). Pré-requisito: token GitHub pro agente na nuvem pushar.

**✅ DECISÃO 2 — Cadência:** cliente fechou em **3x/semana, mix híbrido = 2 novos + 1 refresh**. Encodada em `_content_queue.json` (`_meta.cadence`).
- Motivo: o eixo "{serviço} cost {cidade}" e "{serviço}/{cidade}" está **saturado** (96 slots cheios). Espaço seguro = informacional/how-to/guia + vertical **hardwood-refinishing** (intocada: faltam 8 cidade + 8 cost). Refresh dos 48 cost = runway infinito p/ sinal de frescor.
- Fila semeada: 12 posts novos em `backlog_new` + `topic_ideas_pool` (12) + `backlog_new_secondary` (refinishing) → ~3-4 meses de conteúdo novo, indefinido com refresh.

**✅ DECISÃO 1 — Autonomia:** cliente fechou em **push direto autônomo** (publica no main sem revisão humana).
- ⚠️ IMPLICAÇÃO CRÍTICA: `_validate_post.py` vira o ÚNICO portão de qualidade. No pipeline ele DEVE ser *hard-fail* — se qualquer das 22 checagens falhar, ABORTA o commit/push (não publica conteúdo quebrado no site ao vivo).
- Regra extra recomendada no pipeline: também abortar se `canibal_check != 'clear'` no item da fila.

## AUTOMAÇÃO CONSTRUÍDA (2026-06-07) — GitHub Actions, igual ao brazacleaningnovo
Método escolhido: **GitHub Actions** (não `/schedule`), espelhando `brazacleaningnovo/.github/workflows/blog-auto.yml`. Roda na nuvem do GitHub, 100% hands-off. Repo já está no GitHub: `github.com/lucianodornfeld18-creator/triangleflooring`.

**Arquivos criados (testados localmente, compilam + render/validate passam):**
- `.github/workflows/blog-auto.yml` — cron seg/qua/sex 13:00 UTC (~9h FL) + botão manual. Roda `agent_run.py`, commita e dá push. Cloudflare publica no push.
- `automation/agent_run.py` — orquestrador: pega próximo tópico de `_content_queue.json` (backlog_new → topic_ideas_pool fallback) → chama Claude API (`claude-opus-4-8` + web_search) p/ escrever o CONTEÚDO em JSON → render → validate (GATE) → update_site. Guard anti-canibalização: nunca sobrescreve página existente.
- `automation/render_post.py` — fatia o chrome byte-a-byte de `blog/best-flooring-florida-humidity/` (método provado do `_build_water_damage_post.py`) e injeta só o conteúdo.
- `automation/validate_post.py` — porta parametrizável do `_validate_post.py` (22 checagens). É o ÚNICO gate (push autônomo). Exit≠0 = nada publicado.
- `automation/update_site.py` — injeta card no `blog/index.html`, add `<url>` no `sitemap.xml`, marca item `published` na fila. Idempotente.
- `automation/queue/_example.json` (schema), `automation/RUNBOOK.md` (system prompt/qualidade), `automation/published_log.json` (log).

**Teste local (2026-06-07):** `py automation/agent_run.py --dry` → seleciona Kerdi vs RedGard, lê 132 URLs. Self-test render+validate = 21/22 OK (única falha = word-count no fixture fino, gate funcionando). Sem vazamento.

## FALTA LIGAR — 2 passos manuais únicos (só o dono do repo pode)
1. **Push destes arquivos pro GitHub** (automation/ + .github/ + _content_queue.json + handoff). Sem isso o workflow não existe na nuvem.
2. **Adicionar o secret `ANTHROPIC_API_KEY`** no GitHub: repo → Settings → Secrets and variables → Actions → New repository secret. (Não dá pra eu fazer — exige a API key + a UI do GitHub.)
Depois: Actions → "Auto Blog Post" → Run workflow p/ testar na hora; daí roda sozinho seg/qua/sex.

## Próximos passos para retomar
1. ✅ Decisões 1 e 2 fechadas. ✅ Automação construída e testada localmente.
2. Push + secret `ANTHROPIC_API_KEY` (os 2 passos acima).
3. (opcional) Implementar o REFRESH (a cadência híbrida previa 1 refresh/semana dos 48 posts de custo). v1 publica só conteúdo NOVO da fila (24+ tópicos = ~2 meses de runway). Refresh = v2 documentada.
3. **Gerar Post #2 (1º da fila):** `shower-waterproofing-kerdi-vs-redgard-florida` — `status: approved` no `_content_queue.json`. Alto ticket, funil p/ `/tile-installation/`. Gerar na mesma linha do #1 (fatiar boilerplate de post recente + `_validate_post.py`).

## Dívida técnica registrada (não corrigida — só reportar/atacar quando pedirem)
- **Canibalização:** 3 URLs disputando "hardwood vs vinyl" → pilar = `/guides/hardwood-vs-vinyl-plank-florida/`; suporte = `/blog/hardwood-vs-vinyl-plank-lakewood-ranch/` e `/blog/best-flooring-florida-humidity/`. Resolver com canonical/hierarquia pilar→suporte.
