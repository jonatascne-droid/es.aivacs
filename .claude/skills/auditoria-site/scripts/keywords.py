#!/usr/bin/env python3
"""Ideias de palavras-chave e perguntas reais (substitui AnswerThePublic/Ubersuggest) usando o autocompletar do Google,
e confere quais o site já cobre.

Uso: python3 keywords.py --seeds "cambiar caldera" "caldera condensación" --hl es --gl es --crawl pasta/crawl.json --out pasta/
Gera: keywords.json (sugestões agrupadas, perguntas e lacunas de conteúdo).
"""
import argparse, json, os, re, sys, time, unicodedata
import requests

MOD = {
    "es": {"perguntas": ["qué", "cómo", "cuánto", "cuál", "dónde", "por qué", "cuándo", "es", "se puede"],
           "comercial": ["precio", "mejor", "barato", "ayudas", "opiniones", "cerca de mí", "vs", "instalación", "oferta"]},
    "pt": {"perguntas": ["o que", "como", "quanto", "qual", "onde", "por que", "quando", "é", "pode"],
           "comercial": ["preço", "melhor", "barato", "perto de mim", "vs", "avaliações", "promoção", "instalação"]},
}
STOP = set("de la el los las un una y o en para por con del al que a se es mi tu su lo como cuanto cuánto qué cómo cual cuál "
           "o as os um uma e em com do da dos das no na ao".split())


def suggest(q, hl, gl):
    try:
        r = requests.get("https://suggestqueries.google.com/complete/search",
                         params={"client": "firefox", "hl": hl, "gl": gl, "q": q}, timeout=15,
                         headers={"User-Agent": "Mozilla/5.0"})
        return r.json()[1] if r.status_code == 200 else []
    except Exception:
        return []


def plain(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", nargs="+", required=True)
    ap.add_argument("--hl", default="es")
    ap.add_argument("--gl", default="es")
    ap.add_argument("--city", default="", help="cidade/região para variações locais, ex.: madrid")
    ap.add_argument("--crawl", default="", help="crawl.json para medir cobertura")
    ap.add_argument("--out", default=".")
    a = ap.parse_args()
    mods = MOD.get(a.hl[:2], MOD["es"])
    out = {"seeds": a.seeds, "grupos": {}, "perguntas": [], "comerciais": [], "locais": []}
    allq = set()
    for s in a.seeds:
        g = set(suggest(s, a.hl, a.gl))
        for m in mods["perguntas"]:
            r = suggest(f"{m} {s}", a.hl, a.gl); g.update(r); out["perguntas"] += r; time.sleep(0.15)
        for m in mods["comercial"]:
            r = suggest(f"{s} {m}", a.hl, a.gl); g.update(r); out["comerciais"] += r; time.sleep(0.15)
        for ch in "abcdefghijlmnoprstuv":
            g.update(suggest(f"{s} {ch}", a.hl, a.gl)); time.sleep(0.1)
        if a.city:
            r = suggest(f"{s} {a.city}", a.hl, a.gl); g.update(r); out["locais"] += r
        out["grupos"][s] = sorted(g)
        allq |= g
    for k in ("perguntas", "comerciais", "locais"):
        out[k] = sorted(set(out[k]))
    if a.crawl and os.path.exists(a.crawl):
        pages = [p for p in json.load(open(a.crawl))["pages"] if p.get("title") is not None]
        corpus = [plain(" ".join([p.get("title", ""), p.get("desc", ""), " ".join(p.get("h1", []))])) for p in pages]
        gaps, covered = [], []
        for q in sorted(allq):
            terms = [t for t in re.findall(r"\w+", plain(q)) if t not in STOP and len(t) > 2]
            hit = any(sum(t in c for t in terms) >= max(1, round(len(terms) * 0.7)) for c in corpus) if terms else True
            (covered if hit else gaps).append(q)
        out["cobertas_em_titulo_ou_h1"] = covered
        out["lacunas"] = gaps
    os.makedirs(a.out, exist_ok=True)
    json.dump(out, open(os.path.join(a.out, "keywords.json"), "w"), ensure_ascii=False, indent=1)
    print(f"✓ {len(allq)} sugestões · {len(out['perguntas'])} perguntas · {len(out.get('lacunas', []))} lacunas → keywords.json")


if __name__ == "__main__":
    sys.exit(main())
