#!/usr/bin/env python3
"""Roda o Lighthouse (o motor do PageSpeed Insights) localmente com o Chromium e resume o resultado.

Uso: python3 lighthouse.py --out pasta/ https://site/ https://site/pagina [--desktop]
Gera: lighthouse-summary.json (notas, Core Web Vitals, maiores oportunidades e falhas de SEO/acessibilidade).
"""
import argparse, glob, json, os, re, subprocess, sys


def chrome_path():
    for p in [os.environ.get("CHROME_PATH", "")] + sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux*/chrome")) + \
             sorted(glob.glob(os.path.expanduser("~/.cache/ms-playwright/chromium-*/chrome-*/chrome"))) + \
             ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/usr/bin/google-chrome", "/usr/bin/chromium"]:
        if p and os.path.exists(p):
            return p
    return ""


def run(url, form, out_json):
    flags = "--headless=new --no-sandbox --disable-gpu"
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if proxy:
        flags += f" --proxy-server={proxy} --ignore-certificate-errors"
    cmd = ["npx", "--yes", "lighthouse@12", url, "--quiet", f"--chrome-flags={flags}",
           "--only-categories=performance,seo,accessibility,best-practices", "--output=json", f"--output-path={out_json}"]
    cmd += ["--preset=desktop"] if form == "desktop" else ["--form-factor=mobile"]
    env = dict(os.environ, CHROME_PATH=chrome_path())
    p = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=420)
    if p.returncode != 0 or not os.path.exists(out_json):
        return {"url": url, "form": form, "erro": (p.stderr or p.stdout)[-400:]}
    r = json.load(open(out_json))
    a = r["audits"]
    val = lambda k: a.get(k, {}).get("displayValue", "")
    opp = []
    for k, x in a.items():
        det = x.get("details") or {}
        sav = det.get("overallSavingsMs") or x.get("metricSavings", {}).get("LCP") or 0
        if (x.get("score") is not None and x["score"] < 0.9) and sav and sav >= 150:
            opp.append({"audit": x.get("title"), "ganho_ms": round(sav), "detalhe": re.sub(r"\[.*?\]\(.*?\)", "", x.get("displayValue", ""))[:80]})
    opp.sort(key=lambda o: -o["ganho_ms"])
    fails = lambda cat: [a[ref["id"]]["title"] for ref in r["categories"][cat]["auditRefs"]
                         if ref.get("weight", 0) > 0 and a.get(ref["id"], {}).get("score") is not None and a[ref["id"]]["score"] < 0.9]
    field = (r.get("loadingExperience") or {}).get("metrics", {})
    return {
        "url": url, "form": form,
        "notas": {k: (round(v["score"] * 100) if v.get("score") is not None else None) for k, v in r["categories"].items()},
        "metricas": {"FCP": val("first-contentful-paint"), "LCP": val("largest-contentful-paint"), "TBT": val("total-blocking-time"),
                     "CLS": val("cumulative-layout-shift"), "Speed Index": val("speed-index")},
        "elemento_LCP": ((a.get("largest-contentful-paint-element", {}).get("details") or {}).get("items") or [{}])[0].get("items", [{}])[0].get("node", {}).get("snippet", "")[:160] if a.get("largest-contentful-paint-element") else "",
        "peso_total_KB": round((a.get("total-byte-weight", {}).get("numericValue") or 0) / 1024),
        "oportunidades": opp[:8],
        "falhas_seo": fails("seo"), "falhas_acessibilidade": fails("accessibility")[:10], "falhas_boas_praticas": fails("best-practices")[:8],
        "dados_reais_usuarios": bool(field),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="+")
    ap.add_argument("--out", default=".")
    ap.add_argument("--desktop", action="store_true", help="também roda a versão desktop da primeira URL")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    if not chrome_path():
        print("✗ Chromium/Chrome não encontrado (defina CHROME_PATH)"); return 1
    jobs = [(u, "mobile") for u in a.urls] + ([(a.urls[0], "desktop")] if a.desktop else [])
    res = []
    for i, (u, f) in enumerate(jobs):
        r = run(u, f, os.path.join(a.out, f"lh-{i}-{f}.json"))
        res.append(r)
        print(f"  {f:7} {r.get('notas', r.get('erro', ''))}  {u}")
    json.dump(res, open(os.path.join(a.out, "lighthouse-summary.json"), "w"), ensure_ascii=False, indent=1)
    print("✓ lighthouse-summary.json")


if __name__ == "__main__":
    sys.exit(main())
