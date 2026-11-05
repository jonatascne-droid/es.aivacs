#!/usr/bin/env python3
"""Rastreia um site (como um Screaming Frog simples) e aponta os problemas de SEO técnico e on-page.

Uso: python3 crawl.py https://exemplo.com --max 300 --out pasta/
Gera: crawl.json (tudo), crawl-summary.json (contagens + até 5 exemplos por problema) e pages.csv.
"""
import argparse, csv, json, re, sys, time
from collections import Counter, defaultdict, deque
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urldefrag, urlparse
from urllib import robotparser

import requests
from bs4 import BeautifulSoup

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0 Safari/537.36 AIVACS-Audit")
SKIP_EXT = re.compile(r"\.(jpe?g|png|gif|webp|svg|ico|pdf|zip|rar|mp4|mp3|webm|avi|mov|docx?|xlsx?|pptx?|css|js|json|xml|woff2?|ttf|eot)(\?|$)", re.I)
PHONE = re.compile(r"(?:\+34[\s.-]?)?(?:[6789]\d{2}[\s.-]?\d{2,3}[\s.-]?\d{2,3}[\s.-]?\d{0,3})")


def norm(url):
    url, _ = urldefrag(url)
    p = urlparse(url)
    path = p.path or "/"
    return f"{p.scheme}://{p.netloc.lower()}{path}" + (f"?{p.query}" if p.query else "")


def same_site(url, host):
    h = urlparse(url).netloc.lower()
    return h == host or h == "www." + host or "www." + h == host


def fetch(sess, url, timeout=20):
    t = time.time()
    try:
        r = sess.get(url, timeout=timeout, allow_redirects=True)
        return r, round(r.elapsed.total_seconds(), 2), None
    except requests.RequestException as e:
        return None, round(time.time() - t, 2), str(e)[:200]


def parse_sitemaps(sess, start, robots_txt):
    urls, todo, seen = set(), [], set()
    for line in robots_txt.splitlines():
        if line.lower().startswith("sitemap:"):
            todo.append(line.split(":", 1)[1].strip())
    if not todo:
        todo = [urljoin(start, "/sitemap.xml"), urljoin(start, "/sitemap_index.xml"), urljoin(start, "/wp-sitemap.xml")]
    found_any = []
    while todo and len(seen) < 60:
        sm = todo.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        r, _, err = fetch(sess, sm)
        if not r or r.status_code != 200 or "<" not in r.text[:500]:
            continue
        found_any.append(sm)
        soup = BeautifulSoup(r.content, "xml")
        for loc in soup.find_all("loc"):
            u = loc.get_text(strip=True)
            parent = loc.parent.name if loc.parent else ""
            if parent == "sitemap":
                todo.append(u)
            elif parent == "url" and not loc.prefix:
                urls.add(norm(u))
    return found_any, urls


def analyse(url, r, secs, host):
    d = {"url": url, "final_url": norm(r.url), "status": r.status_code, "secs": secs,
         "redirects": [h.status_code for h in r.history], "bytes": len(r.content),
         "type": r.headers.get("content-type", "").split(";")[0]}
    if "html" not in d["type"] or r.status_code >= 400 or (r.history and d["final_url"] != norm(url)):
        return d, []
    soup = BeautifulSoup(r.text, "lxml")
    meta = lambda n: (soup.find("meta", attrs={"name": re.compile(f"^{n}$", re.I)}) or {}).get("content", "")
    t = soup.title.get_text(" ", strip=True) if soup.title else ""
    canon = soup.find("link", rel=lambda v: v and "canonical" in v)
    d.update({
        "title": t, "title_len": len(t),
        "desc": meta("description").strip(), "robots": meta("robots").lower(),
        "viewport": bool(meta("viewport")),
        "canonical": norm(urljoin(r.url, canon["href"])) if canon and canon.get("href") else "",
        "lang": (soup.html.get("lang", "") if soup.html else ""),
        "h1": [h.get_text(" ", strip=True)[:120] for h in soup.find_all("h1")],
        "h2": len(soup.find_all("h2")),
        "hreflang": [l.get("hreflang") for l in soup.find_all("link", hreflang=True)],
        "og_image": bool(soup.find("meta", property="og:image")),
    })
    d["desc_len"] = len(d["desc"])
    types = []
    for s in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(s.string or "")
        except Exception:
            types.append("JSON-LD inválido")
            continue
        stack = data if isinstance(data, list) else [data]
        while stack:
            x = stack.pop()
            if isinstance(x, dict):
                tp = x.get("@type")
                types += tp if isinstance(tp, list) else ([tp] if tp else [])
                stack += x.get("@graph", []) if isinstance(x.get("@graph"), list) else []
    types += [i.get("itemtype", "").rsplit("/", 1)[-1] for i in soup.find_all(itemtype=True)]
    d["schema"] = sorted({str(x) for x in types if x})
    imgs = soup.find_all("img")
    d["imgs"] = len(imgs)
    d["imgs_no_alt"] = sum(1 for i in imgs if not (i.get("alt") or "").strip())
    d["mixed"] = sum(1 for tag, att in (("img", "src"), ("script", "src"), ("link", "href"), ("iframe", "src"))
                     for e in soup.find_all(tag) if (e.get(att) or "").startswith("http://")) if r.url.startswith("https") else 0
    for s in soup(["script", "style", "noscript", "svg"]):
        s.decompose()
    text = soup.get_text(" ", strip=True)
    d["words"] = len(text.split())
    d["phones"] = sorted({re.sub(r"\D", "", m)[-9:] for m in PHONE.findall(text) if len(re.sub(r"\D", "", m)) >= 9})[:5]
    d["tel_links"] = sorted({a["href"][4:].replace(" ", "") for a in soup.find_all("a", href=True) if a["href"].startswith("tel:")})[:5]
    links, ext = [], 0
    for a in soup.find_all("a", href=True):
        h = a["href"].strip()
        if h.startswith(("mailto:", "tel:", "javascript:", "#", "whatsapp:")):
            continue
        u = norm(urljoin(r.url, h))
        if not u.startswith("http"):
            continue
        if same_site(u, host):
            links.append(u)
        else:
            ext += 1
    d["links_int"] = len(set(links))
    d["links_ext"] = ext
    return d, links


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--max", type=int, default=300)
    ap.add_argument("--out", default=".")
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()
    start = norm(a.url if a.url.startswith("http") else "https://" + a.url)
    host = urlparse(start).netloc.lower().removeprefix("www.")
    sess = requests.Session()
    sess.headers.update({"User-Agent": UA, "Accept-Language": "es-ES,es;q=0.9,pt;q=0.8,en;q=0.7"})

    rr, _, _ = fetch(sess, urljoin(start, "/robots.txt"))
    robots_txt = rr.text if rr is not None and rr.status_code == 200 else ""
    rp = robotparser.RobotFileParser()
    rp.parse(robots_txt.splitlines())
    sitemaps, sm_urls = parse_sitemaps(sess, start, robots_txt)
    sm_urls = {u for u in sm_urls if same_site(u, host)}

    pages, inlinks, seen = {}, defaultdict(set), set()
    queue = deque([start] + sorted(sm_urls))
    seen.update(queue)
    blocked = []

    def work(u):
        r, secs, err = fetch(sess, u)
        if r is None:
            return u, {"url": u, "status": 0, "error": err, "secs": secs}, []
        return (u, *analyse(u, r, secs, host))

    with ThreadPoolExecutor(a.workers) as ex:
        while queue and len(pages) < a.max:
            batch = []
            while queue and len(batch) < a.workers * 2 and len(pages) + len(batch) < a.max:
                u = queue.popleft()
                if SKIP_EXT.search(u):
                    continue
                if robots_txt and not rp.can_fetch(UA, u):
                    blocked.append(u)
                    continue
                batch.append(u)
            for u, d, links in ex.map(work, batch):
                pages[u] = d
                for l in links:
                    inlinks[l].add(u)
                    if l not in seen and not SKIP_EXT.search(l):
                        seen.add(l)
                        queue.append(l)
    unvisited = [u for u in seen if u not in pages and not SKIP_EXT.search(u)]

    # problemas
    html = [p for p in pages.values() if p.get("title") is not None and p.get("status") == 200]
    final_of = {u: p.get("final_url", u) for u, p in pages.items()}
    inlinks_final = defaultdict(set)
    for u, srcs in inlinks.items():
        inlinks_final[final_of.get(u, u)] |= srcs
    issues = defaultdict(list)
    add = lambda k, u, extra="": issues[k].append(u + (f" — {extra}" if extra else ""))
    for p in pages.values():
        s = p.get("status", 0)
        if s == 0:
            add("erro_conexao", p["url"], p.get("error", ""))
        elif s >= 400:
            add(f"http_{s}", p["url"], f"{len(inlinks.get(p['url'], []))} link(s) apontam para cá")
        if len(p.get("redirects", [])) > 1:
            add("cadeia_redirecionamento", p["url"], "→".join(map(str, p["redirects"])))
        if p.get("redirects") and p.get("final_url") != p["url"] and inlinks.get(p["url"]):
            add("links_internos_para_redirecionamento", p["url"], f"→ {p['final_url']} ({len(inlinks[p['url']])} página(s) linkam a versão antiga)")
        if p.get("secs", 0) > 2.0 and s == 200 and not p.get("redirects"):
            add("servidor_lento_>2s_ate_responder", p["url"], f"{p['secs']}s (medido daqui; confirme no Lighthouse)")
        if p.get("bytes", 0) > 600_000 and "html" in p.get("type", ""):
            add("html_pesado_>600KB", p["url"], f"{p['bytes']//1024} KB")
    titles = Counter(p["title"] for p in html if p.get("title"))
    descs = Counter(p["desc"] for p in html if p.get("desc"))
    for p in html:
        u = p["url"]
        if "noindex" in p.get("robots", ""):
            add("noindex", u)
            continue
        if not p["title"]:
            add("sem_title", u)
        elif titles[p["title"]] > 1:
            add("title_duplicado", u, p["title"][:70])
        if p["title"] and p["title_len"] > 65:
            add("title_longo_>65", u, f"{p['title_len']} caracteres")
        if p["title"] and p["title_len"] < 25:
            add("title_curto_<25", u, p["title"])
        if not p["desc"]:
            add("sem_meta_description", u)
        elif descs[p["desc"]] > 1:
            add("description_duplicada", u)
        elif p["desc_len"] > 165 or p["desc_len"] < 70:
            add("description_tamanho_ruim", u, f"{p['desc_len']} caracteres")
        if not p["h1"]:
            add("sem_h1", u)
        elif len(p["h1"]) > 1:
            add("varios_h1", u, " | ".join(p["h1"][:3]))
        if not p["canonical"]:
            add("sem_canonical", u)
        elif p["canonical"] != p["final_url"]:
            add("canonical_aponta_outra_url", u, p["canonical"])
        if p["words"] < 250:
            add("conteudo_fino_<250_palavras", u, f"{p['words']} palavras")
        if p["imgs_no_alt"]:
            add("imagens_sem_alt", u, f"{p['imgs_no_alt']} de {p['imgs']}")
        if not p["lang"]:
            add("sem_atributo_lang", u)
        if not p["viewport"]:
            add("sem_meta_viewport", u)
        if p["mixed"]:
            add("conteudo_misto_http", u, f"{p['mixed']} recurso(s)")
        if not p["og_image"]:
            add("sem_og_image", u)
        if "JSON-LD inválido" in p["schema"]:
            add("json_ld_invalido", u)
    home = pages.get(start) or (html[0] if html else {})
    if home and not {"Organization", "LocalBusiness", "HVACBusiness", "HomeAndConstructionBusiness", "Plumber"} & set(home.get("schema", [])):
        add("home_sem_schema_organizacao_ou_negocio_local", start, ", ".join(home.get("schema", [])) or "nenhum schema")
    crawled_ok = {p["final_url"] for p in html}
    for u in sorted(sm_urls):
        p = pages.get(u)
        if p and p.get("status") != 200:
            add("sitemap_url_nao_200", u, str(p.get("status")))
        if p and not inlinks_final.get(p.get("final_url", u)) and u != start:
            add("orfa_no_sitemap_sem_links_internos", u)
    for u in sorted(crawled_ok - sm_urls):
        if sm_urls:
            add("fora_do_sitemap", u)
    if not robots_txt:
        add("sem_robots_txt", urljoin(start, "/robots.txt"))
    if not sitemaps:
        add("sem_sitemap", start)
    phones = Counter(ph for p in html for ph in p.get("phones", []))

    data = {"start": start, "host": host, "pages": list(pages.values()), "sitemaps": sitemaps,
            "sitemap_urls": len(sm_urls), "blocked_by_robots": blocked[:50], "unvisited": len(unvisited),
            "issues": {k: v for k, v in issues.items()}}
    summary = {
        "site": start, "paginas_rastreadas": len(pages), "html_200": len(html),
        "status": dict(Counter(str(p.get("status")) for p in pages.values())),
        "sitemaps": sitemaps, "urls_no_sitemap": len(sm_urls), "robots_txt": bool(robots_txt),
        "bloqueadas_robots": len(blocked), "nao_visitadas_limite": len(unvisited),
        "tempo_medio_resposta_s": round(sum(p.get("secs", 0) for p in html) / max(1, len(html)), 2),
        "palavras_media": round(sum(p["words"] for p in html) / max(1, len(html))),
        "schema_encontrado": dict(Counter(t for p in html for t in p.get("schema", [])).most_common(15)),
        "idiomas": dict(Counter(p.get("lang", "") for p in html)),
        "hreflang_usado": any(p.get("hreflang") for p in html),
        "telefones_no_texto": dict(phones.most_common(5)),
        "home": {k: home.get(k) for k in ("title", "desc", "h1", "canonical", "schema", "words", "secs")} if home else {},
        "problemas": {k: {"total": len(v), "exemplos": v[:5]} for k, v in sorted(issues.items(), key=lambda kv: -len(kv[1]))},
    }
    import os
    os.makedirs(a.out, exist_ok=True)
    json.dump(data, open(os.path.join(a.out, "crawl.json"), "w"), ensure_ascii=False, indent=1)
    json.dump(summary, open(os.path.join(a.out, "crawl-summary.json"), "w"), ensure_ascii=False, indent=1)
    cols = ["url", "status", "secs", "title", "title_len", "desc_len", "h1", "canonical", "words", "imgs_no_alt", "schema"]
    with open(os.path.join(a.out, "pages.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for p in pages.values():
            w.writerow([" | ".join(p[c]) if isinstance(p.get(c), list) else p.get(c, "") for c in cols])
    print(f"✓ {len(pages)} páginas ({len(html)} HTML 200) · {len(sm_urls)} no sitemap · {sum(len(v) for v in issues.values())} ocorrências em {len(issues)} tipos de problema")
    for k, v in summary["problemas"].items():
        print(f"  {v['total']:>4}  {k}")


if __name__ == "__main__":
    sys.exit(main())
