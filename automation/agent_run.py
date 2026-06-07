#!/usr/bin/env python3
"""
agent_run.py - autonomous post generator for the GitHub Actions cron.

Runs ONCE per invocation (Mon/Wed/Fri). Picks the next topic from
_content_queue.json (backlog_new -> topic_ideas_pool fallback), has the Claude
API write the CONTENT as JSON (with web search for real 2026 data), then the
deterministic scripts render + validate + wire it so the model can't break the
site:

    pick topic -> Claude API (web search) -> queue/<slug>.json
               -> render_post.py -> validate_post.py (HARD GATE) -> update_site.py

On autonomous push there is NO human review, so validate_post.py is the only
gate: if it fails, NOTHING is published that day (the workflow's `git diff`
check then commits nothing).

Env:  ANTHROPIC_API_KEY (required)
      TODAY=YYYY-MM-DD   (optional; set by the workflow, defaults to system date)
Usage: python automation/agent_run.py [--dry]
"""
import os, re, sys, json, subprocess, datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
HERE = Path(__file__).parent
QUEUE_DIR = HERE / "queue"
RUNBOOK = HERE / "RUNBOOK.md"
EXAMPLE = QUEUE_DIR / "_example.json"
CQUEUE = ROOT / "_content_queue.json"
CMAP = ROOT / "_content_map.json"
PUBLOG = HERE / "published_log.json"
MODEL = "claude-opus-4-8"
MAX_TRIES = 2  # regenerate this many times if the validator rejects the draft


def today():
    return datetime.date.fromisoformat(os.environ.get("TODAY") or datetime.date.today().isoformat())


def existing_urls():
    try:
        cmap = json.load(open(CMAP, encoding="utf-8"))
        return [e["url"] for e in cmap.get("entries", [])]
    except (OSError, ValueError):
        return []


def published_slugs():
    try:
        return {p["slug"] for p in json.load(open(PUBLOG, encoding="utf-8"))}
    except (OSError, ValueError):
        return set()


def slugify(s):
    s = re.sub(r"\(20\d\d[^)]*\)", "", s).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:70]


def pick_topic(q):
    """Next un-built item from backlog_new, else a topic from the idea pool."""
    done = published_slugs()
    existing = set(existing_urls())
    for item in q.get("backlog_new", []):
        slug = item["slug"].strip("/").replace("blog/", "")
        if item.get("status") == "published":
            continue
        if item["slug"] in existing or slug in done:
            continue
        if (ROOT / "blog" / slug / "index.html").exists():
            continue
        if item.get("canibal_check") not in (None, "clear"):
            continue
        return {
            "slug": slug, "title": item["title"], "intent": item.get("intent", ""),
            "funnel_to": item.get("funnel_to"), "supports": item.get("supports", []),
            "service": item.get("service"),
        }
    # fallback: rotate through the free-form idea pool by ordinal day
    pool = q.get("topic_ideas_pool", [])
    if pool:
        idx = today().toordinal() % len(pool)
        idea = pool[idx]
        return {"slug": slugify(idea), "title": idea, "intent": "informational",
                "funnel_to": None, "supports": [], "service": None}
    return None


def build_messages(topic, d, correction=None):
    runbook = RUNBOOK.read_text(encoding="utf-8")
    example = EXAMPLE.read_text(encoding="utf-8")
    existing = existing_urls()
    funnel = topic.get("funnel_to") or "(choose the most relevant service hub)"
    supports = ", ".join(topic.get("supports") or []) or "(choose 3-5 relevant existing URLs)"
    system = (
        runbook
        + "\n\n## OUTPUT CONTRACT\n"
        "You are the autonomous generator for Triangle Flooring (Tampa Bay, FL). Produce ONE blog "
        "post as a single JSON object matching automation/queue/_example.json EXACTLY (same keys).\n"
        "- ~1200-1500 words across `sections[].html`, >=6 question-style H2 sections, >=2 comparison "
        "tables (HTML <table> inside section html), >=6 FAQs, a 40-60 word `answer_first` (may use "
        "<strong>/<em>).\n"
        "- INFORMATIONAL intent only. NEVER target a transactional '{service} cost {city}' or "
        "'{service} {city}' query — those 96 pages already exist and must not be cannibalized.\n"
        "- `interlinks` (3-6) and `related_cards` (3) MUST point to REAL existing URLs from the list "
        "below, reciprocal where possible. ALWAYS include the funnel target.\n"
        "- `og_image`/card image MUST be an existing /images/ card (e.g. card-repair.webp, card-tile.webp, "
        "card-hardwood.webp, card-vinyl.webp).\n"
        "- title < 60 chars, meta_desc < 155 chars, both UNIQUE vs every existing page.\n"
        "- NAP must stay consistent: Triangle Flooring, +1 941-402-6861, Palmetto FL. Do NOT invent other phones/addresses.\n"
        "- Output ONLY the JSON inside one ```json fenced block. No prose before/after.\n\n"
        "## SITE URLS (link only to these)\n" + "\n".join("- " + u for u in existing) + "\n\n"
        "## EXAMPLE SCHEMA (copy the shape, not the content)\n```json\n" + example + "\n```\n"
    )
    user = (
        f"Today is {d.isoformat()} ({d.strftime('%A')}).\n"
        f"TOPIC TO WRITE: {topic['title']}\n"
        f"Suggested slug: {topic['slug']}\n"
        f"Primary funnel target (must interlink): {funnel}\n"
        f"Supporting pages to interlink: {supports}\n\n"
        "Research real 2026 Florida pricing, methods, and the questions homeowners actually ask about "
        "this topic with web search, then output the post JSON. Set `date` to today and `slug` to the "
        "suggested slug."
    )
    if correction:
        user += "\n\n## CORRECTION - your previous draft was REJECTED by the validator. Fix it now:\n" + correction
    return system, user


def call_api(system, user):
    import anthropic
    client = anthropic.Anthropic()
    msgs = [{"role": "user", "content": user}]
    tools = [{"type": "web_search_20260209", "name": "web_search"}]
    for _ in range(6):  # allow pause_turn continuations
        with client.messages.stream(
            model=MODEL, max_tokens=16000,
            thinking={"type": "adaptive"},
            output_config={"effort": "high"},
            system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
            messages=msgs, tools=tools,
        ) as stream:
            msg = stream.get_final_message()
        if msg.stop_reason == "pause_turn":
            msgs.append({"role": "assistant", "content": msg.content})
            continue
        return "".join(b.text for b in msg.content if b.type == "text")
    raise SystemExit("API: too many pause_turn continuations")


def extract_json(text):
    m = re.search(r"```json\s*(\{.*?\})\s*```", text, re.S) or re.search(r"(\{.*\})", text, re.S)
    if not m:
        raise SystemExit("No JSON object found in the model response")
    return json.loads(m.group(1))


def py(*args):
    print("  $", " ".join(str(a) for a in args[1:]))
    return subprocess.run([sys.executable, *args[1:]], capture_output=True, text=True)


def main():
    d = today()
    q = json.load(open(CQUEUE, encoding="utf-8"))
    topic = pick_topic(q)
    if not topic:
        print("Queue empty and no idea pool. Nothing to do today.")
        return

    if "--dry" in sys.argv:
        print(f"[dry] {d.isoformat()} {d.strftime('%A')} -> would write '{topic['title']}' "
              f"(slug={topic['slug']}, funnel={topic.get('funnel_to')})")
        print(f"[dry] {len(existing_urls())} existing urls; model={MODEL} + web_search.")
        return

    print(f"== agent_run {d.isoformat()} ({d.strftime('%A')}) | topic: {topic['title']} ==")
    required = [l for l in ([topic.get("funnel_to")] + (topic.get("supports") or [])) if l][:2]
    correction = None
    for attempt in range(1, MAX_TRIES + 1):
        if correction:
            print(f"== retry {attempt}/{MAX_TRIES} after validator rejection ==")
        system, user = build_messages(topic, d, correction)
        data = extract_json(call_api(system, user))
        data.setdefault("date", d.isoformat())
        data["slug"] = (data.get("slug") or topic["slug"]).strip("/").replace("blog/", "")
        slug = data["slug"]

        # hard cannibalization guard: never overwrite an existing page
        if (ROOT / "blog" / slug / "index.html").exists() or f"/blog/{slug}/" in set(existing_urls()):
            raise SystemExit(f"BLOCKED: /blog/{slug}/ already exists (cannibalization). Nothing published.")

        QUEUE_DIR.mkdir(parents=True, exist_ok=True)
        json.dump(data, open(QUEUE_DIR / f"{slug}.json", "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print(f"  wrote queue/{slug}.json")

        r = py("", str(HERE / "render_post.py"), slug)
        sys.stdout.write(r.stdout); sys.stderr.write(r.stderr)
        if r.returncode != 0:
            raise SystemExit(f"render_post.py failed:\n{(r.stdout + r.stderr)[-800:]}")

        v = py("", str(HERE / "validate_post.py"), slug, *required)
        sys.stdout.write(v.stdout); sys.stderr.write(v.stderr)
        if v.returncode == 0:
            u = py("", str(HERE / "update_site.py"), slug)
            sys.stdout.write(u.stdout); sys.stderr.write(u.stderr)
            if u.returncode != 0:
                raise SystemExit(f"update_site.py failed:\n{(u.stdout + u.stderr)[-800:]}")
            # log it
            log = []
            if PUBLOG.exists():
                log = json.load(open(PUBLOG, encoding="utf-8"))
            log.append({"slug": slug, "date": d.isoformat(), "title": data["title"]})
            json.dump(log, open(PUBLOG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            gh_out = os.environ.get("GITHUB_OUTPUT")
            if gh_out:
                with open(gh_out, "a", encoding="utf-8") as f:
                    f.write(f"slug={slug}\n")
            print(f"PUBLISHED slug={slug}")
            return

        # validator rejected -> feed failures back and regenerate
        fails = "\n".join(l for l in (v.stdout + v.stderr).splitlines() if "FAIL" in l)
        correction = ("The validator rejected the draft with these failures. Fix EVERY one:\n" + fails)
        # discard the rejected page so a clean retry can't leave a half-built dir
        bad = ROOT / "blog" / slug / "index.html"
        try:
            bad.unlink()
        except OSError:
            pass

    raise SystemExit(f"Exhausted {MAX_TRIES} attempts; validator still failing. Nothing published today.")


if __name__ == "__main__":
    main()
