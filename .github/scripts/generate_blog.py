#!/usr/bin/env python3
from __future__ import annotations

import html
import json
from collections import Counter
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "blog" / "data"
LATEST_PATH = DATA_DIR / "news_latest.json"
HISTORY_PATH = DATA_DIR / "news_history.json"
OUTPUT_PATH = ROOT / "blog" / "index.html"
RSS_PATH = ROOT / "blog" / "feed.xml"
LOCAL_TZ = ZoneInfo("America/Sao_Paulo")
MAX_RENDERED_ITEMS = 90

CATEGORY_CLASS = {"Cyber": "cyber", "GRC": "grc", "CISO": "ciso"}


def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def esc(value) -> str:
    return html.escape(str(value or ""), quote=True)


def parse_dt(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except Exception:
        return datetime.now(timezone.utc)


def local_label(value: str) -> str:
    dt = parse_dt(value).astimezone(LOCAL_TZ)
    return dt.strftime("%d/%m/%Y %H:%M")


def why_it_matters(categories: list[str]) -> str:
    messages = []
    if "Cyber" in categories:
        messages.append("relevância operacional para prevenção, detecção ou resposta a ameaças")
    if "GRC" in categories:
        messages.append("impacto potencial em governança, risco, conformidade ou resiliência")
    if "CISO" in categories:
        messages.append("interesse para liderança, estratégia e tomada de decisão executiva em segurança")
    if not messages:
        return "selecionada automaticamente por aderência ao radar de cibersegurança"
    if len(messages) == 1:
        return messages[0]
    return "; ".join(messages[:-1]) + "; e " + messages[-1]


def render_badges(categories: list[str]) -> str:
    parts = []
    for category in categories:
        css = CATEGORY_CLASS.get(category, "cyber")
        parts.append(f'<span class="badge {css}">{esc(category)}</span>')
    return "".join(parts)


def render_tags(tags: list[str]) -> str:
    if not tags:
        return ""
    return '<div class="tags">' + "".join(f'<span>#{esc(tag.replace(" ", "-"))}</span>' for tag in tags[:5]) + "</div>"


def render_card(item: dict) -> str:
    categories = item.get("categories", [])
    return f'''
    <article class="news-card">
      <div class="news-top">
        <div class="badges">{render_badges(categories)}</div>
        <time>{esc(local_label(item.get("published_at", "")))}</time>
      </div>
      <h2>{esc(item.get("title", "Sem título"))}</h2>
      <p class="context"><strong>Por que entrou no radar:</strong> {esc(why_it_matters(categories))}.</p>
      {render_tags(item.get("tags", []))}
      <div class="news-foot">
        <span class="source">Fonte: {esc(item.get("source", item.get("feed", "Fonte externa")))}</span>
        <a href="{esc(item.get("url", "#"))}" target="_blank" rel="noopener noreferrer nofollow">Ler na fonte →</a>
      </div>
    </article>
    '''


def recent_stats(items: list[dict], latest: dict) -> dict:
    categories = Counter()
    sources = set()
    for item in items[:MAX_RENDERED_ITEMS]:
        categories.update(item.get("categories", []))
        sources.add(item.get("source") or item.get("feed"))

    source_status = latest.get("sources", []) if isinstance(latest, dict) else []
    healthy = sum(1 for source in source_status if source.get("status") == "ok")
    return {
        "total": len(items[:MAX_RENDERED_ITEMS]),
        "cyber": categories.get("Cyber", 0),
        "grc": categories.get("GRC", 0),
        "ciso": categories.get("CISO", 0),
        "sources": healthy or len({x for x in sources if x}),
    }


def render_blog(history: dict, latest: dict) -> str:
    items = history.get("items", []) if isinstance(history, dict) else []
    items = sorted(items, key=lambda x: (x.get("published_at", ""), x.get("score", 0)), reverse=True)[:MAX_RENDERED_ITEMS]
    stats = recent_stats(items, latest)
    generated = latest.get("generated_at") or history.get("updated_at") or datetime.now(timezone.utc).isoformat()
    generated_label = local_label(generated)

    cards = "\n".join(render_card(item) for item in items)
    if not cards:
        cards = '<div class="empty">O radar ainda não possui notícias processadas. Execute o workflow <code>Daily Cyber GRC CISO Blog</code> pelo GitHub Actions.</div>'

    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="Radar diário da WOLF CYBER SECURITY com notícias selecionadas sobre cibersegurança, GRC e liderança CISO.">
<title>WOLF CYBER SECURITY | Radar Diário Cyber, GRC & CISO</title>
<link rel="alternate" type="application/rss+xml" title="WOLF Cyber News RSS" href="./feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#070b12;--panel:#0b111c;--panel2:#111a29;--line:#213048;--text:#e9eef7;--muted:#8b9ab4;--cyan:#3fd9e0;--amber:#ffb454;--green:#5fe3a1;--red:#ff5c6c;--mono:'JetBrains Mono',monospace;--sans:'Space Grotesk',sans-serif;}}
*{{box-sizing:border-box}} body{{margin:0;background:radial-gradient(circle at 15% 0,#10233055,transparent 32%),var(--bg);color:var(--text);font-family:var(--sans);line-height:1.55}} a{{color:var(--cyan)}} .wrap{{max-width:1120px;margin:auto;padding:0 24px 80px}} header{{padding:38px 0 28px;border-bottom:1px solid var(--line)}} .brand{{display:flex;justify-content:space-between;gap:18px;align-items:center;flex-wrap:wrap}} .brand-left{{display:flex;gap:12px;align-items:center}} .mark{{width:42px;height:42px;border:1px solid var(--cyan);border-radius:10px;display:grid;place-items:center;font:800 17px var(--mono);color:var(--cyan);box-shadow:0 0 24px #3fd9e028}} .eyebrow{{font:600 10px var(--mono);letter-spacing:.18em;text-transform:uppercase;color:var(--muted)}} .brand-name{{font-size:20px;font-weight:700}} .status{{font:11px var(--mono);color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:7px 12px}} h1{{font-size:clamp(32px,5vw,54px);line-height:1.04;margin:34px 0 12px;letter-spacing:-.03em}} h1 span{{color:var(--cyan)}} .subtitle{{max-width:760px;color:#b5c0d4}} .navlinks{{display:flex;gap:16px;margin-top:18px;font:12px var(--mono)}} .stats{{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px;margin:28px 0 34px}} .stat{{background:linear-gradient(180deg,var(--panel2),var(--panel));border:1px solid var(--line);border-radius:12px;padding:18px}} .stat strong{{display:block;font:800 25px var(--mono);color:var(--cyan)}} .stat span{{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}} .section-head{{display:flex;align-items:center;gap:12px;margin:38px 0 18px}} .section-head h2{{font-size:20px;margin:0}} .section-head:after{{content:'';height:1px;background:linear-gradient(90deg,var(--line),transparent);flex:1}} .feed{{display:grid;gap:14px}} .news-card{{background:linear-gradient(180deg,#0d1522,var(--panel));border:1px solid var(--line);border-radius:13px;padding:20px 22px;box-shadow:0 10px 30px #00000016}} .news-top,.news-foot{{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}} .news-top time,.source{{font:11px var(--mono);color:var(--muted)}} .badges{{display:flex;gap:7px;flex-wrap:wrap}} .badge{{font:700 10px var(--mono);letter-spacing:.06em;padding:4px 8px;border-radius:5px;border:1px solid}} .badge.cyber{{color:var(--cyan);border-color:#1c5a5f;background:#0f2426}} .badge.grc{{color:var(--amber);border-color:#5a3f18;background:#2a2010}} .badge.ciso{{color:var(--green);border-color:#22573e;background:#10251b}} .news-card h2{{font-size:19px;line-height:1.25;margin:14px 0 10px}} .context{{margin:0;color:#aebbd1;font-size:14px}} .tags{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px;font:10px var(--mono);color:#71809c}} .news-foot{{margin-top:16px;padding-top:14px;border-top:1px dashed #21304888}} .news-foot a{{font:12px var(--mono);text-decoration:none}} .empty{{border:1px dashed var(--line);padding:24px;border-radius:12px;color:var(--muted)}} footer{{margin-top:44px;padding-top:22px;border-top:1px solid var(--line);color:var(--muted);font:11px var(--mono);display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}}
@media(max-width:760px){{.stats{{grid-template-columns:repeat(2,minmax(0,1fr))}}.stat:last-child{{grid-column:span 2}}}} @media(max-width:480px){{.stats{{grid-template-columns:1fr}}.stat:last-child{{grid-column:auto}}}}
</style>
</head>
<body>
<div class="wrap">
<header>
  <div class="brand">
    <div class="brand-left"><div class="mark">W</div><div><div class="eyebrow">Wolf Cyber Security</div><div class="brand-name">Threat & Governance Intelligence</div></div></div>
    <div class="status">Atualizado em {esc(generated_label)} · America/Sao_Paulo</div>
  </div>
  <h1>Radar Diário <span>Cyber · GRC · CISO</span></h1>
  <p class="subtitle">Curadoria automatizada de manchetes e metadados públicos. O radar prioriza fontes de segurança, governança, risco, conformidade e liderança executiva, sempre direcionando o leitor ao conteúdo original.</p>
  <div class="navlinks"><a href="./feed.xml">RSS</a><a href="../">Portfólio</a></div>
</header>
<section class="stats">
  <div class="stat"><strong>{stats['total']}</strong><span>itens no radar</span></div>
  <div class="stat"><strong>{stats['cyber']}</strong><span>Cyber</span></div>
  <div class="stat"><strong>{stats['grc']}</strong><span>GRC</span></div>
  <div class="stat"><strong>{stats['ciso']}</strong><span>CISO</span></div>
  <div class="stat"><strong>{stats['sources']}</strong><span>fontes ativas</span></div>
</section>
<div class="section-head"><h2>Últimas notícias selecionadas</h2></div>
<section class="feed">{cards}</section>
<footer><span>WOLF CYBER SECURITY · Radar automatizado</span><span>Sem republicação integral: título, metadados e link para a fonte original.</span></footer>
</div>
</body>
</html>
'''


def render_rss(history: dict) -> str:
    items = sorted(history.get("items", []), key=lambda x: x.get("published_at", ""), reverse=True)[:40]
    entries = []
    for item in items:
        dt = parse_dt(item.get("published_at", ""))
        categories = ", ".join(item.get("categories", [])) or "Cybersecurity"
        entries.append(f'''<item>
<title>{html.escape(str(item.get("title", "")))}</title>
<link>{html.escape(str(item.get("url", "")))}</link>
<guid isPermaLink="false">{html.escape(str(item.get("id", "")))}</guid>
<pubDate>{format_datetime(dt)}</pubDate>
<description>{html.escape(f"Categorias: {categories}. Fonte: {item.get('source', item.get('feed', 'Fonte externa'))}.")}</description>
</item>''')
    build_date = format_datetime(datetime.now(timezone.utc))
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
<title>WOLF CYBER SECURITY — Radar Cyber, GRC & CISO</title>
<link>https://w3bscr4p3r.github.io/blog/</link>
<description>Curadoria automatizada de notícias sobre cibersegurança, GRC e liderança CISO.</description>
<language>pt-BR</language>
<lastBuildDate>{build_date}</lastBuildDate>
{''.join(entries)}
</channel></rss>
'''


def main() -> None:
    latest = load_json(LATEST_PATH, {})
    history = load_json(HISTORY_PATH, {"items": []})
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(render_blog(history, latest), encoding="utf-8")
    RSS_PATH.write_text(render_rss(history), encoding="utf-8")
    print(f"Generated {OUTPUT_PATH}")
    print(f"Generated {RSS_PATH}")


if __name__ == "__main__":
    main()
