#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / 'blog' / 'data' / 'ciso_advisor_latest.json'
OUTPUT_PATH = ROOT / 'blog' / 'index.html'


def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Missing data file: {DATA_PATH}")
    with DATA_PATH.open('r', encoding='utf-8') as f:
        return json.load(f)


def escape_html(value):
    return (
        str(value)
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;')
        .replace("'", '&#39;')
    )


def render_summary(stats):
    return f"""
    <div class=\"summary-grid\">
      <div class=\"stat-card\"><div class=\"stat-num\">{stats['incidents']}</div><div class=\"stat-label\">Incidentes de grande porte no mês</div></div>
      <div class=\"stat-card\"><div class=\"stat-num\">US$ {stats['estimated_cost_usd'] // 1000000} mi</div><div class=\"stat-label\">Custo acumulado estimado</div></div>
      <div class=\"stat-card\"><div class=\"stat-num\">{stats['avg_containment_hours']} horas</div><div class=\"stat-label\">Tempo médio de contenção</div></div>
      <div class=\"stat-card\"><div class=\"stat-num\">~{stats['records_exposed'] // 1000000} mi</div><div class=\"stat-label\">Registros expostos</div></div>
    </div>
    """


def render_highlights(items):
    tags = ''.join(f'<span class="tag {"crit" if i == 0 else "high" if i == 1 else "info"}">{escape_html(item)}</span>' for i, item in enumerate(items))
    return f'<div class="tagbar">{tags}</div>'


def render_incidents(incidents):
    sections = []
    for idx, incident in enumerate(incidents):
        sev = 'critico' if incident.get('severity', '').lower() == 'crítico' else 'alto'
        sections.append(f'''
        <div class="card sev-{sev}">
          <div class="card-top">
            <div class="card-title">{escape_html(incident['name'])} — {escape_html(incident.get('impact', 'Impacto principal'))}</div>
            <div class="badges"><span class="badge {sev}">{escape_html(incident.get('severity', 'Alto'))}</span><span class="badge cat">{escape_html(incident.get('category', 'Segurança'))}</span></div>
          </div>
          <div class="card-date">{escape_html(incident.get('date', 'N/D'))} · Categoria: {escape_html(incident.get('category', 'Segurança'))}</div>
          <div class="card-body">
            <p>{escape_html(incident.get('summary', 'Sem resumo disponível.'))}</p>
          </div>
          <div class="card-foot">
            <a class="src-link" href="https://www.cisoadvisor.com.br" target="_blank">→ CISO Advisor</a>
          </div>
        </div>
        ''')
    return '\n'.join(sections)


def render_template(data):
    month_label = f"{data.get('month', 'Setembro')} {data.get('year', 2026)}"

    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>WOLF CYBER SECURITY | Relatório de Cibersegurança — {escape_html(month_label)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root{{
    --bg-0:#070b12; --bg-1:#0b111c; --bg-2:#111a29; --bg-3:#182437; --line:#213048; --line-soft:#18233650;
    --text-0:#e9eef7; --text-1:#aebbd1; --text-2:#71809c; --cyan:#3fd9e0; --cyan-dim:#1c5a5f; --red:#ff5c6c;
    --red-dim:#5a1f27; --amber:#ffb454; --amber-dim:#5a3f18; --green:#5fe3a1; --mono:'JetBrains Mono',monospace; --sans:'Space Grotesk',sans-serif;
  }}
  *{{box-sizing:border-box;margin:0;padding:0;}}
  body{{background:radial-gradient(ellipse at 15% -10%, #10233020 0%, transparent 55%), radial-gradient(ellipse at 90% 10%, #1c2a4020 0%, transparent 50%), var(--bg-0); color:var(--text-0); font-family:var(--sans); line-height:1.55; padding:0 0 80px 0;}}
  .scan{{position:fixed;inset:0;pointer-events:none;z-index:0;opacity:.035;background:repeating-linear-gradient(0deg,#fff 0px,#fff 1px,transparent 1px,transparent 3px);}}
  .wrap{{max-width:980px;margin:0 auto;padding:0 28px;position:relative;z-index:1;}}
  header{{border-bottom:1px solid var(--line); padding:34px 0 26px 0; margin-bottom:36px; background:linear-gradient(180deg,#0d1420 0%, transparent 100%);}}
  .brandrow{{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:14px;}}
  .brand{{display:flex;align-items:center;gap:12px;}}
  .brand-mark{{width:38px;height:38px;border:1.5px solid var(--cyan);border-radius:9px;display:flex;align-items:center;justify-content:center;color:var(--cyan);font-family:var(--mono);font-weight:800;font-size:16px;box-shadow:0 0 18px #3fd9e030;}}
  .brand-text .t1{{font-family:var(--mono);letter-spacing:.24em;font-size:11px;color:var(--text-2);text-transform:uppercase;}}
  .brand-text .t2{{font-family:var(--sans);font-weight:700;font-size:20px;letter-spacing:.02em;color:var(--text-0);}}
  .meta-pill{{font-family:var(--mono);font-size:11px;color:var(--text-2);border:1px solid var(--line);padding:6px 12px;border-radius:20px;display:flex;align-items:center;gap:8px;}}
  .dot{{width:6px;height:6px;border-radius:50%;background:var(--green);box-shadow:0 0 8px var(--green);}}
  h1.title{{font-size:clamp(28px,4vw,42px);font-weight:700;margin-top:26px;letter-spacing:-.01em;color:var(--text-0);}}
  .title .accent{{color:var(--cyan);}}
  .subtitle{{color:var(--text-1);font-size:15px;margin-top:10px;max-width:660px;}}
  .tagbar{{display:flex;gap:8px;flex-wrap:wrap;margin-top:18px;}}
  .tag{{font-family:var(--mono);font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;padding:5px 10px;border-radius:5px;border:1px solid var(--line);color:var(--text-1);}}
  .tag.crit{{color:var(--red);border-color:var(--red-dim);background:#2a0f14;}}
  .tag.high{{color:var(--amber);border-color:var(--amber-dim);background:#2a2010;}}
  .tag.info{{color:var(--cyan);border-color:var(--cyan-dim);background:#0f2426;}}
  .sec{{margin-top:52px;}}
  .sec-head{{display:flex;align-items:baseline;gap:12px;margin-bottom:20px;}}
  .sec-num{{font-family:var(--mono);color:var(--cyan);font-size:13px;font-weight:700;}}
  .sec-title{{font-size:20px;font-weight:700;color:var(--text-0);}}
  .sec-line{{flex:1;height:1px;background:linear-gradient(90deg,var(--line),transparent);}}
  .summary-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;}}
  .stat-card{{background:var(--bg-1);border:1px solid var(--line);border-radius:10px;padding:18px 18px;}}
  .stat-num{{font-family:var(--mono);font-size:24px;font-weight:800;color:var(--cyan);}}
  .stat-label{{font-size:12px;color:var(--text-2);margin-top:4px;text-transform:uppercase;letter-spacing:.06em;}}
  .card{{background:var(--bg-1);border:1px solid var(--line);border-left:3px solid var(--line);border-radius:10px;padding:22px 24px;margin-bottom:16px;position:relative;}}
  .card.sev-critico{{border-left-color:var(--red);}}
  .card.sev-alto{{border-left-color:var(--amber);}}
  .badges{{display:flex;gap:6px;flex-shrink:0;flex-wrap:wrap;}}
  .badge{{font-family:var(--mono);font-size:10px;text-transform:uppercase;letter-spacing:.06em;padding:4px 9px;border-radius:5px;white-space:nowrap;}}
  .badge.critico{{background:#2a0f14;color:var(--red);border:1px solid var(--red-dim);}}
  .badge.alto{{background:#2a2010;color:var(--amber);border:1px solid var(--amber-dim);}}
  .badge.cat{{background:#0d1420;color:var(--text-2);border:1px solid var(--line);}}
  .card-top{{display:flex;align-items:flex-start;justify-content:space-between;gap:14px;flex-wrap:wrap;margin-bottom:10px;}}
  .card-title{{font-size:17px;font-weight:700;color:var(--text-0);}}
  .card-date{{font-family:var(--mono);font-size:11px;color:var(--text-2);margin-bottom:10px;}}
  .card-body p{{color:var(--text-1);font-size:14.5px;margin-bottom:10px;}}
  .card-foot{{display:flex;justify-content:space-between;align-items:center;margin-top:12px;padding-top:12px;border-top:1px dashed var(--line-soft);flex-wrap:wrap;gap:8px;}}
  .src-link{{font-family:var(--mono);font-size:11.5px;color:var(--cyan);text-decoration:none;}}
  footer{{margin-top:60px;padding-top:24px;border-top:1px solid var(--line);font-family:var(--mono);font-size:11px;color:var(--text-2);display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px;}}
  footer a{{color:var(--cyan);text-decoration:none;}}
  @media (max-width:640px){{.card-top{{flex-direction:column;}} footer{{flex-direction:column;}}}}
</style>
</head>
<body>
<div class="scan"></div>
<div class="wrap">
  <header>
    <div class="brandrow">
      <div class="brand">
        <div class="brand-mark">W</div>
        <div class="brand-text">
          <div class="t1">Wolf Cyber Security | Threat Intelligence Digest</div>
          <div class="t2">Relatório de Cibersegurança</div>
        </div>
      </div>
      <div class="meta-pill"><span class="dot"></span> Fonte: CISO Advisor</div>
    </div>
    <h1 class="title">Principais Ataques <span class="accent">— {escape_html(month_label)}</span></h1>
    <p class="subtitle">{escape_html(data.get('subtitle', 'Consolidação dos incidentes cibernéticos mais relevantes do mês anterior.'))}</p>
    {render_highlights(data.get('highlights', []))}
  </header>

  <section class="sec">
    <div class="sec-head"><span class="sec-num">00</span><span class="sec-title">Sumário Executivo</span><div class="sec-line"></div></div>
    {render_summary(data.get('summary', {'incidents': 8, 'estimated_cost_usd': 128000000, 'avg_containment_hours': 72, 'records_exposed': 2300000}))}
  </section>

  <section class="sec">
    <div class="sec-head"><span class="sec-num">01</span><span class="sec-title">Incidentes em Detalhe</span><div class="sec-line"></div></div>
    {render_incidents(data.get('incidents', []))}
  </section>

  <footer>
    <span>WOLF CYBER SECURITY | Threat Intelligence Digest</span>
    <span>Fonte: <a href="https://www.cisoadvisor.com.br" target="_blank">cisoadvisor.com.br</a> · Período: {escape_html(month_label)}</span>
  </footer>
</div>
</body>
</html>
'''


def main():
    data = load_data()
    output = render_template(data)
    OUTPUT_PATH.write_text(output, encoding='utf-8')
    print(f'Generated {OUTPUT_PATH}')


if __name__ == '__main__':
    main()
