#!/usr/bin/env python3
"""Radar de nicho: acha os vídeos que passaram muito da média do próprio canal (outliers), no YouTube e no TikTok.
Sem chave e sem login: usa o yt-dlp em modo lista (não baixa vídeo).

  python3 radar.py canais <url> [<url> ...] [--n 40] [--aba shorts|videos|ambas] [--top 20] [--min 2] [--out pasta]
  python3 radar.py buscar "marketing para dentistas" [--canais 8] [--idioma es] [mesmas opções]

<url>: canal do YouTube (https://www.youtube.com/@handle) ou perfil do TikTok (https://www.tiktok.com/@user).
'buscar' encontra canais do YouTube pelo termo e depois faz o mesmo que 'canais'.

Para cada canal, pega os últimos --n vídeos, calcula a mediana de visualizações e o múltiplo de cada vídeo
(visualizações ÷ mediana). Lista os que passam de --min vezes a mediana, do maior múltiplo para o menor.
Saída: tabela no terminal + <out>/radar.md e <out>/radar.json.
"""
import argparse
import json
import statistics
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


IDIOMA = 'es'


def ytdlp_json(url, n):
    # títulos no idioma pedido (o YouTube traduz títulos conforme o idioma de quem acessa)
    extra = ['--extractor-args', f'youtube:lang={IDIOMA}'] if ('youtube' in url or url.startswith('ytsearch')) else []
    r = subprocess.run(['yt-dlp', '--flat-playlist', '--playlist-end', str(n), '-J', '--no-warnings', *extra, url],
                       capture_output=True, text=True, timeout=240)
    if r.returncode:
        print(f'  ! {url}: {r.stderr.strip()[-200:]}', file=sys.stderr)
        return None
    return json.loads(r.stdout)


def tabs(url, aba):
    if 'youtube.com' not in url:
        return [url]
    base = url.rstrip('/')
    for t in ('/shorts', '/videos', '/streams', '/featured'):
        if base.endswith(t):
            base = base[: -len(t)]
    return {'shorts': [base + '/shorts'], 'videos': [base + '/videos'], 'ambas': [base + '/shorts', base + '/videos']}[aba]


def analisar(url, n, aba):
    linhas = []
    for u in tabs(url, aba):
        d = ytdlp_json(u, n)
        if not d:
            continue
        canal = d.get('channel') or d.get('uploader') or d.get('title') or u
        seguidores = d.get('channel_follower_count')
        ents = [e for e in d.get('entries') or [] if e and e.get('view_count')]
        if len(ents) < 5:
            print(f'  ! {canal} ({u}): só {len(ents)} vídeos com visualizações; pulei', file=sys.stderr)
            continue
        med = statistics.median(e['view_count'] for e in ents)
        for e in ents:
            ts = e.get('timestamp')
            linhas.append({
                'canal': canal, 'seguidores': seguidores, 'aba': u.rsplit('/', 1)[-1] if 'youtube.com' in u else 'tiktok',
                'titulo': (e.get('title') or '').replace('\n', ' ').strip(),
                'views': e['view_count'], 'mediana_canal': int(med), 'multiplo': round(e['view_count'] / med, 1),
                'likes': e.get('like_count'), 'duracao': e.get('duration'),
                'data': datetime.fromtimestamp(ts, timezone.utc).strftime('%Y-%m-%d') if ts else None,
                'url': e.get('url') if str(e.get('url', '')).startswith('http') else f"https://www.youtube.com/watch?v={e.get('id')}",
            })
        print(f'  {canal} · {u.rsplit("/", 1)[-1]} · {len(ents)} vídeos · mediana {int(med):,}'.replace(',', '.'), file=sys.stderr)
        time.sleep(1)
    return linhas


def buscar_canais(termo, k, idioma):
    q = f'ytsearch{k * 4}:{termo}'
    d = ytdlp_json(q, k * 4) or {}
    vistos, canais = set(), []
    for e in d.get('entries') or []:
        cu = e.get('channel_url')
        if cu and cu not in vistos:
            vistos.add(cu)
            canais.append(cu)
        if len(canais) >= k:
            break
    print(f'canais encontrados para "{termo}": {len(canais)}', file=sys.stderr)
    return canais


def fmt(n):
    return f'{n:,}'.replace(',', '.') if isinstance(n, int) else '—'


def main():
    a = argparse.ArgumentParser()
    a.add_argument('modo', choices=['canais', 'buscar'])
    a.add_argument('alvos', nargs='+')
    a.add_argument('--n', type=int, default=40)
    a.add_argument('--aba', default='ambas', choices=['shorts', 'videos', 'ambas'])
    a.add_argument('--top', type=int, default=20)
    a.add_argument('--min', type=float, default=2.0)
    a.add_argument('--canais', type=int, default=8)
    a.add_argument('--idioma', default='es')
    a.add_argument('--out', default='radar')
    args = a.parse_args()
    global IDIOMA
    IDIOMA = args.idioma

    urls = args.alvos if args.modo == 'canais' else buscar_canais(' '.join(args.alvos), args.canais, args.idioma)
    todas = []
    for u in urls:
        todas += analisar(u, args.n, args.aba)
    hits = sorted([l for l in todas if l['multiplo'] >= args.min], key=lambda l: -l['multiplo'])[: args.top]

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'radar.json').write_text(json.dumps({'gerado': datetime.now(timezone.utc).isoformat(), 'alvos': urls,
                                                'outliers': hits, 'todos': todas}, ensure_ascii=False, indent=1))
    md = [f'# Radar de nicho · {datetime.now():%d/%m/%Y}', '',
          f'Canais analisados: {len(urls)} · vídeos lidos: {len(todas)} · outliers (≥ {args.min:g}× a mediana do canal): {len(hits)}', '',
          '| # | Múltiplo | Views | Mediana do canal | Canal | Título | Data | Link |', '|---|---|---|---|---|---|---|---|']
    for i, h in enumerate(hits, 1):
        md.append(f"| {i} | {h['multiplo']}× | {fmt(h['views'])} | {fmt(h['mediana_canal'])} | {h['canal']} | {h['titulo'][:70]} | {h['data'] or '—'} | {h['url']} |")
    (out / 'radar.md').write_text('\n'.join(md) + '\n')
    print('\n'.join(md))
    print(f'\nsalvo em {out}/radar.md e {out}/radar.json', file=sys.stderr)


if __name__ == '__main__':
    main()
