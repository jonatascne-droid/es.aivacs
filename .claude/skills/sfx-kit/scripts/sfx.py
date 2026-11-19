#!/usr/bin/env python3
"""SFX Kit (wyzowl/sfx-kit, CC0): busca no catálogo e baixa só os sons que o vídeo usa.
O áudio (67 MB) não fica no repositório: cada .wav vem do GitHub, no commit fixado abaixo, e fica em cache.

  python3 sfx.py buscar "pop texto aparece" [--n 8]     # procura em nome, descrição, use_for e tags
  python3 sfx.py info pop-small-in                      # dados completos de um som (sync, duração, nível)
  python3 sfx.py baixar pop-small-in whoosh-fast-soft [--para assets/sfx]
  python3 sfx.py colocar pop-small-in 2.40              # em que segundo começar o som para o pico cair em 2.40 s

Cache: ~/.cache/sfx-kit (ou SFX_KIT_CACHE). 'baixar' copia do cache para --para quando dado.
"""
import json
import os
import shutil
import sys
import urllib.request
from pathlib import Path

COMMIT = '92780e7ab0cdfb557497a988089c47f46e8c7412'
RAW = f'https://raw.githubusercontent.com/wyzowl/sfx-kit/{COMMIT}/'
HERE = Path(__file__).resolve().parent.parent
CACHE = Path(os.environ.get('SFX_KIT_CACHE', Path.home() / '.cache' / 'sfx-kit'))
SOUNDS = {s['id']: s for s in json.loads((HERE / 'sounds.json').read_text())['sounds']}


def find(query, n=8):
    terms = [t for t in query.lower().split() if len(t) > 1]
    scored = []
    for s in SOUNDS.values():
        hay = ' '.join([s['id'], s['name'], s['description'], ' '.join(s.get('use_for', [])), ' '.join(s.get('tags', []))]).lower()
        score = sum(hay.count(t) for t in terms) + sum(3 for t in terms if t in s['id'])
        if score:
            scored.append((score, s))
    for _, s in sorted(scored, key=lambda x: -x[0])[:n]:
        print(f"{s['id']:<32} {s['duration']:.2f}s  sync {s['sync']['at']:.3f}s  sob voz {s.get('under_voiceover_db', 0):+d} dB  · {s['description']}")


def fetch(sid):
    s = SOUNDS.get(sid) or sys.exit(f'som desconhecido: {sid} (use buscar)')
    dst = CACHE / s['file']
    if not dst.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(RAW + s['file'], timeout=60) as r, open(dst, 'wb') as f:
            shutil.copyfileobj(r, f)
    return dst


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd, rest = sys.argv[1], sys.argv[2:]
    if cmd == 'buscar':
        n = int(rest[rest.index('--n') + 1]) if '--n' in rest else 8
        find(' '.join(r for r in rest if not r.isdigit() and r != '--n'), n)
    elif cmd == 'info':
        print(json.dumps(SOUNDS.get(rest[0]) or sys.exit(f'som desconhecido: {rest[0]}'), indent=1, ensure_ascii=False))
    elif cmd == 'baixar':
        para = Path(rest[rest.index('--para') + 1]) if '--para' in rest else None
        ids = [r for i, r in enumerate(rest) if r != '--para' and (i == 0 or rest[i - 1] != '--para')]
        for sid in ids:
            p = fetch(sid)
            if para:
                para.mkdir(parents=True, exist_ok=True)
                p = Path(shutil.copy(p, para / p.name))
            print(p)
    elif cmd == 'colocar':
        s = SOUNDS.get(rest[0]) or sys.exit(f'som desconhecido: {rest[0]}')
        t = float(rest[1])
        print(f"comece {s['id']} em {max(0, t - s['sync']['at']):.3f}s ({s['sync']['meets']}; {s['sync'].get('how', '')})")
    else:
        sys.exit(__doc__)


if __name__ == '__main__':
    main()
