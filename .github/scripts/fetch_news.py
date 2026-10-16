#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
import unicodedata
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import feedparser
import requests
from dateutil import parser as date_parser

ROOT = Path(__file__).resolve().parents[2]
SOURCES_PATH = ROOT / ".github" / "news_sources.json"
DATA_DIR = ROOT / "blog" / "data"
LATEST_PATH = DATA_DIR / "news_latest.json"
HISTORY_PATH = DATA_DIR / "news_history.json"

LOOKBACK_HOURS = int(os.getenv("NEWS_LOOKBACK_HOURS", "72"))
MAX_ITEMS = int(os.getenv("NEWS_MAX_ITEMS", "24"))
MAX_HISTORY = int(os.getenv("NEWS_MAX_HISTORY", "600"))
USER_AGENT = os.getenv(
    "NEWS_USER_AGENT",
    "WolfCyberNewsBot/1.0 (+https://github.com/w3bscr4p3r/w3bscr4p3r.github.io)",
)

CATEGORY_KEYWORDS = {
    "Cyber": [
        "cyber", "ciber", "ransomware", "malware", "phishing", "zero-day", "0-day",
        "vulnerability", "vulnerabilidade", "cve", "exploit", "breach", "violacao",
        "incidente", "ataque", "threat", "ameaca", "soc", "siem", "soar", "edr",
        "xdr", "botnet", "ddos", "supply chain", "cadeia de suprimentos", "identity",
        "identidade", "cloud security", "seguranca em nuvem", "ot security", "ics", "scada",
    ],
    "GRC": [
        "grc", "governanca", "governance", "risk", "risco", "compliance", "conformidade",
        "iso 27001", "iso/iec 27001", "nist csf", "nist cybersecurity framework", "lgpd",
        "gdpr", "nis2", "dora", "eu ai act", "ai act", "cra", "cyber resilience act",
        "audit", "auditoria", "regulation", "regulacao", "policy", "politica de seguranca",
        "third-party risk", "risco de terceiros", "resilience", "resiliencia",
    ],
    "CISO": [
        "ciso", "chief information security officer", "security leader", "security leadership",
        "lideranca de seguranca", "board", "conselho", "executive", "executivo", "budget",
        "orcamento", "cyber strategy", "estrategia de ciberseguranca", "security strategy",
        "cyber risk", "risco cibernetico", "business risk", "risco de negocio",
    ],
}

HIGH_VALUE_TERMS = [
    "zero-day", "ransomware", "cve", "critical", "critico", "exploit", "breach",
    "nist", "iso 27001", "nis2", "dora", "lgpd", "gdpr", "ai act", "ciso",
    "supply chain", "third-party", "board", "regulation", "incident response",
]

SKIP_TERMS = ["sponsored", "patrocinado", "webinar", "evento patrocinado"]
TRACKING_PARAMS = {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid", "fbclid"}


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def ascii_fold(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value or "")
    return "".join(ch for ch in normalized if not unicodedata.combining(ch))


def norm_text(value: str) -> str:
    value = ascii_fold(value).lower()
    value = re.sub(r"https?://\S+", " ", value)
    value = re.sub(r"[^a-z0-9+.#/-]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def canonical_url(url: str) -> str:
    try:
        parts = urlsplit(url)
        query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if k.lower() not in TRACKING_PARAMS]
        return urlunsplit((parts.scheme, parts.netloc.lower(), parts.path, urlencode(query), ""))
    except Exception:
        return url


def parse_entry_date(entry) -> datetime:
    raw = entry.get("published") or entry.get("updated") or entry.get("created")
    if not raw:
        return now_utc()
    try:
        parsed = date_parser.parse(raw)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except Exception:
        return now_utc()


def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def save_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def classify(title: str, source_hints: list[str]) -> tuple[list[str], list[str]]:
    text = norm_text(title)
    categories: list[str] = []
    tags: list[str] = []

    for category, keywords in CATEGORY_KEYWORDS.items():
        matched = [kw for kw in keywords if norm_text(kw) in text]
        if matched:
            categories.append(category)
            tags.extend(matched[:4])

    if not categories:
        categories = list(source_hints[:1])

    for hint in source_hints:
        if hint not in categories and any(norm_text(k) in text for k in CATEGORY_KEYWORDS.get(hint, [])):
            categories.append(hint)

    return sorted(set(categories)), sorted(set(tags))[:8]


def score_item(title: str, published_at: datetime, weight: int, categories: list[str], tags: list[str]) -> float:
    text = norm_text(title)
    age_hours = max(0.0, (now_utc() - published_at).total_seconds() / 3600)
    freshness = max(0.0, 28.0 * (1.0 - min(age_hours, LOOKBACK_HOURS) / LOOKBACK_HOURS))
    category_score = min(18.0, len(categories) * 7.0 + len(tags) * 1.5)
    high_value = sum(2.0 for term in HIGH_VALUE_TERMS if norm_text(term) in text)
    return round(float(weight) + freshness + category_score + min(16.0, high_value), 2)


def fingerprint(title: str, url: str) -> str:
    material = f"{norm_text(title)}|{canonical_url(url)}"
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:24]


def publisher_name(entry, fallback: str) -> str:
    src = entry.get("source")
    if isinstance(src, dict) and src.get("title"):
        return str(src["title"]).strip()
    return fallback


def fetch_feed(session: requests.Session, source: dict) -> list[dict]:
    response = session.get(source["url"], timeout=25)
    response.raise_for_status()
    parsed = feedparser.parse(response.content)
    cutoff = now_utc() - timedelta(hours=LOOKBACK_HOURS)
    items: list[dict] = []

    for entry in parsed.entries:
        title = re.sub(r"\s+", " ", str(entry.get("title", "")).strip())
        url = canonical_url(str(entry.get("link", "")).strip())
        if not title or not url:
            continue

        title_norm = norm_text(title)
        if any(norm_text(term) in title_norm for term in SKIP_TERMS):
            continue

        published_at = parse_entry_date(entry)
        if published_at < cutoff:
            continue

        hints = source.get("category_hint", [])
        categories, tags = classify(title, hints)
        if not categories:
            continue

        item = {
            "id": fingerprint(title, url),
            "title": title,
            "url": url,
            "source": publisher_name(entry, source["name"]),
            "feed": source["name"],
            "published_at": published_at.isoformat(),
            "collected_at": now_utc().isoformat(),
            "categories": categories,
            "tags": tags,
            "score": score_item(title, published_at, int(source.get("weight", 5)), categories, tags),
        }
        items.append(item)

    return items


def select_balanced(items: list[dict], max_items: int) -> list[dict]:
    ordered = sorted(items, key=lambda x: (x["score"], x["published_at"]), reverse=True)
    selected: list[dict] = []
    selected_ids: set[str] = set()

    for category in ("Cyber", "GRC", "CISO"):
        quota = max(2, max_items // 6)
        for item in ordered:
            if len([x for x in selected if category in x["categories"]]) >= quota:
                break
            if category in item["categories"] and item["id"] not in selected_ids:
                selected.append(item)
                selected_ids.add(item["id"])

    for item in ordered:
        if len(selected) >= max_items:
            break
        if item["id"] not in selected_ids:
            selected.append(item)
            selected_ids.add(item["id"])

    return sorted(selected, key=lambda x: (x["score"], x["published_at"]), reverse=True)


def main() -> None:
    config = load_json(SOURCES_PATH, {"sources": []})
    history = load_json(HISTORY_PATH, {"items": []})
    old_items = history.get("items", []) if isinstance(history, dict) else []
    known_ids = {item.get("id") for item in old_items if item.get("id")}

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml;q=0.9, */*;q=0.5"})

    collected: list[dict] = []
    source_status: list[dict] = []
    seen_run: set[str] = set()

    for source in config.get("sources", []):
        try:
            feed_items = fetch_feed(session, source)
            unique_count = 0
            for item in feed_items:
                if item["id"] in seen_run:
                    continue
                seen_run.add(item["id"])
                collected.append(item)
                unique_count += 1
            source_status.append({"name": source["name"], "status": "ok", "items": unique_count})
        except Exception as exc:
            source_status.append({"name": source.get("name", "unknown"), "status": "error", "error": str(exc)[:180]})

    selected = select_balanced(collected, MAX_ITEMS)
    new_items = [item for item in selected if item["id"] not in known_ids]

    merged_map = {item.get("id"): item for item in old_items if item.get("id")}
    for item in new_items:
        merged_map[item["id"]] = item

    merged = sorted(
        merged_map.values(),
        key=lambda x: (x.get("published_at", ""), x.get("score", 0)),
        reverse=True,
    )[:MAX_HISTORY]

    run_at = now_utc().isoformat()
    latest_payload = {
        "generated_at": run_at,
        "lookback_hours": LOOKBACK_HOURS,
        "selected_count": len(selected),
        "new_count": len(new_items),
        "sources": source_status,
        "items": selected,
    }
    history_payload = {"updated_at": run_at, "items": merged}

    save_json(LATEST_PATH, latest_payload)
    save_json(HISTORY_PATH, history_payload)

    ok_sources = sum(1 for x in source_status if x["status"] == "ok")
    print(f"Collected {len(collected)} candidates from {ok_sources}/{len(source_status)} sources")
    print(f"Selected {len(selected)} items; {len(new_items)} are new; history has {len(merged)} items")


if __name__ == "__main__":
    main()
