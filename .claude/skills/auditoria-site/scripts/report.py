#!/usr/bin/env python3
"""Monta o relatório HTML (um arquivo só, pronto para mandar ao cliente ou imprimir em PDF).

Uso: python3 report.py --dir pasta/  (lê findings.json, crawl-summary.json, lighthouse-summary.json, keywords.json)
Gera: relatorio.html
"""
import argparse, html, json, os, sys

L = {
    "es": dict(t="Auditoría web", res="Resumen", notas="Puntuación por área", prio="Prioridades", imp="Impacto", esf="Esfuerzo",
               area="Área", ev="Qué vimos", rec="Qué hacer", vel="Velocidad (Lighthouse, móvil)", kw="Oportunidades de palabras clave",
               preg="Preguntas reales de la gente", lac="Búsquedas sin página que las responda", acc="Lo que necesitamos de vosotros",
               pas="Próximos pasos", anexo="Anexo técnico", pag="páginas analizadas", prob="Problema", tot="Total", ej="Ejemplos",
               glob="Nota global", gen="Generado por AIVACS", met="Métricas", opp="Mayores mejoras posibles", ahorro="ahorro", a11y="Accesibilidad", busca="Búsqueda", intent="Intención", pagsug="Página sugerida",
               area_names=dict(tecnico="Técnico", contenido="Contenido", rendimiento="Velocidad", local="SEO local",
                               datos_estructurados="Datos estructurados", conversion="Conversión"),
               lvl=dict(alto="Alto", medio="Medio", bajo="Bajo")),
    "pt": dict(t="Auditoria de site", res="Resumo", notas="Nota por área", prio="Prioridades", imp="Impacto", esf="Esforço",
               area="Área", ev="O que vimos", rec="O que fazer", vel="Velocidade (Lighthouse, celular)", kw="Oportunidades de palavras-chave",
               preg="Perguntas reais das pessoas", lac="Buscas sem página que as responda", acc="O que precisamos de vocês",
               pas="Próximos passos", anexo="Anexo técnico", pag="páginas analisadas", prob="Problema", tot="Total", ej="Exemplos",
               glob="Nota geral", gen="Gerado pela AIVACS", met="Métricas", opp="Maiores melhorias possíveis", ahorro="ganho", a11y="Acessibilidade", busca="Busca", intent="Intenção", pagsug="Página sugerida",
               area_names=dict(tecnico="Técnico", contenido="Conteúdo", rendimiento="Velocidade", local="SEO local",
                               datos_estructurados="Dados estruturados", conversion="Conversão"),
               lvl=dict(alto="Alto", medio="Médio", bajo="Baixo")),
}
CSS = """
:root{--ink:#1b1d26;--muted:#5c6070;--line:#e4e6ec;--bg:#fff;--soft:#f6f7f9;--accent:#ff9400;--good:#1f9d55;--mid:#e3a008;--bad:#d64545}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:980px;margin:0 auto;padding:32px 20px 64px}h1{font-size:30px;margin:0 0 4px}h2{font-size:20px;margin:40px 0 12px;padding-top:8px;border-top:2px solid var(--ink)}
.sub{color:var(--muted)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px}
.card{background:var(--soft);border:1px solid var(--line);border-radius:10px;padding:14px}.score{font-size:30px;font-weight:700}
.ring{width:96px;height:96px;border-radius:50%;display:grid;place-items:center;font-size:28px;font-weight:800}
table{width:100%;border-collapse:collapse;font-size:14px}th,td{text-align:left;vertical-align:top;padding:8px;border-bottom:1px solid var(--line)}
th{font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}.pill{display:inline-block;padding:1px 8px;border-radius:99px;font-size:12px;font-weight:600}
.alto{background:#fde2e2;color:#9b1c1c}.medio{background:#fdf0cf;color:#8a5a00}.bajo{background:#dcf2e4;color:#14532d}
ul{padding-left:20px}code,.u{font-size:12px;color:var(--muted);word-break:break-all}.cols{columns:2;column-gap:24px}@media(max-width:640px){.cols{columns:1}}
.top{display:flex;gap:20px;align-items:center;flex-wrap:wrap}footer{margin-top:48px;color:var(--muted);font-size:12px}
@media print{h2{break-after:avoid}tr{break-inside:avoid}}
"""


def col(v):
    return "var(--good)" if v >= 80 else "var(--mid)" if v >= 50 else "var(--bad)"


def esc(x):
    return html.escape(str(x if x is not None else ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    a = ap.parse_args()
    ld = lambda n, d=None: json.load(open(os.path.join(a.dir, n))) if os.path.exists(os.path.join(a.dir, n)) else d
    f = ld("findings.json")
    if not f:
        print("✗ findings.json não encontrado"); return 1
    cs, lh, kw = ld("crawl-summary.json", {}), ld("lighthouse-summary.json", []), ld("keywords.json", {})
    t = L.get(f.get("idioma", "es"), L["es"])
    g = int(f.get("nota_global", 0))
    o = [f"<!doctype html><html lang='{esc(f.get('idioma','es'))}'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>",
         f"<title>{esc(t['t'])} · {esc(f.get('cliente', f.get('site','')))}</title><style>{CSS}</style></head><body><div class='wrap'>",
         f"<div class='top'><div class='ring' style='background:conic-gradient({col(g)} {g*3.6}deg,var(--line) 0)'><div class='ring' style='width:76px;height:76px;background:#fff'>{g}</div></div>",
         f"<div><h1>{esc(t['t'])}: {esc(f.get('cliente',''))}</h1><div class='sub'>{esc(f.get('site',''))} · {esc(f.get('fecha',''))} · {cs.get('paginas_rastreadas','?')} {t['pag']}</div></div></div>",
         f"<h2>{t['res']}</h2><p>{esc(f.get('resumen','')).replace(chr(10),'<br>')}</p>"]
    notas = f.get("notas", {})
    if notas:
        o.append(f"<h2>{t['notas']}</h2><div class='grid'>")
        for k, v in notas.items():
            o.append(f"<div class='card'><div class='sub'>{esc(t['area_names'].get(k,k))}</div><div class='score' style='color:{col(int(v))}'>{int(v)}</div></div>")
        o.append("</div>")
    o.append(f"<h2>{t['prio']}</h2><table><tr><th>#</th><th>{t['prob']}</th><th>{t['imp']}</th><th>{t['esf']}</th><th>{t['rec']}</th></tr>")
    for i, p in enumerate(f.get("prioridades", []), 1):
        urls = "".join(f"<div class='u'>{esc(u)}</div>" for u in p.get("urls", [])[:3])
        o.append(f"<tr><td>{i}</td><td><b>{esc(p.get('titulo'))}</b><div class='sub'>{esc(t['area_names'].get(p.get('area'),p.get('area','')))} · {esc(p.get('evidencia'))}</div>{urls}</td>"
                 f"<td><span class='pill {esc(p.get('impacto'))}'>{esc(t['lvl'].get(p.get('impacto'),p.get('impacto')))}</span></td>"
                 f"<td>{esc(t['lvl'].get(p.get('esfuerzo'),p.get('esfuerzo')))}</td><td>{esc(p.get('recomendacion'))}</td></tr>")
    o.append("</table>")
    mob = [r for r in lh if r.get("form") == "mobile" and r.get("notas")]
    if mob:
        o.append(f"<h2>{t['vel']}</h2><table><tr><th>URL</th><th>Performance</th><th>SEO</th><th>{t['a11y']}</th><th>{t['met']}</th></tr>")
        for r in mob:
            n, m = r["notas"], r["metricas"]
            o.append(f"<tr><td class='u'>{esc(r['url'])}</td><td style='color:{col(n.get('performance') or 0)}'><b>{n.get('performance')}</b></td>"
                     f"<td>{n.get('seo')}</td><td>{n.get('accessibility')}</td><td>LCP {esc(m['LCP'])} · TBT {esc(m['TBT'])} · CLS {esc(m['CLS'])}</td></tr>")
        o.append("</table>")
        opp = mob[0].get("oportunidades", [])[:6]
        if opp:
            o.append(f"<p><b>{t['opp']}</b> ({esc(mob[0]['url'])})</p><ul>" + "".join(f"<li>{esc(x['audit'])} — {t['ahorro']} ~{x['ganho_ms']/1000:.1f} s</li>" for x in opp) + "</ul>")
    pk = f.get("palabras_clave", [])
    if pk or kw:
        o.append(f"<h2>{t['kw']}</h2>")
        if pk:
            o.append(f"<table><tr><th>{t['busca']}</th><th>{t['intent']}</th><th>{t['pagsug']}</th></tr>" +
                     "".join(f"<tr><td><b>{esc(k.get('termino'))}</b></td><td>{esc(k.get('intencion'))}</td><td>{esc(k.get('pagina_sugerida'))}</td></tr>" for k in pk) + "</table>")
        if kw.get("perguntas"):
            o.append(f"<p><b>{t['preg']}</b></p><ul class='cols'>" + "".join(f"<li>{esc(q)}</li>" for q in kw["perguntas"][:30]) + "</ul>")
    for key, title in (("accesos_pendientes", t["acc"]), ("proximos_pasos", t["pas"])):
        if f.get(key):
            o.append(f"<h2>{title}</h2><ol>" + "".join(f"<li>{esc(x)}</li>" for x in f[key]) + "</ol>")
    if cs.get("problemas"):
        o.append(f"<h2>{t['anexo']}</h2><table><tr><th>{t['prob']}</th><th>{t['tot']}</th><th>{t['ej']}</th></tr>")
        for k, v in cs["problemas"].items():
            o.append(f"<tr><td><code>{esc(k)}</code></td><td>{v['total']}</td><td>" + "".join(f"<div class='u'>{esc(e)}</div>" for e in v["exemplos"][:3]) + "</td></tr>")
        o.append("</table>")
    o.append(f"<footer>{t['gen']} · {esc(f.get('fecha',''))}</footer></div></body></html>")
    open(os.path.join(a.dir, "relatorio.html"), "w").write("\n".join(o))
    print("✓ relatorio.html")


if __name__ == "__main__":
    sys.exit(main())
