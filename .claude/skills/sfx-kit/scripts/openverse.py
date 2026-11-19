#!/usr/bin/env python3
"""Busca áudio (ou imagem) de licença aberta no Openverse (Freesound, Jamendo, Wikimedia...), sem chave.
Use quando o SFX Kit não tiver o som: ambiências, sons reais específicos, trilhas.

  python3 openverse.py buscar "rain on window" [--n 10] [--imagem] [--todas-licencas]
  python3 openverse.py baixar <url> <arquivo-destino>

Por padrão só lista o que permite uso comercial (license_type=commercial). CC0 e PDM dispensam crédito;
CC BY e CC BY-SA exigem crédito (a linha 'crédito' já sai pronta para a legenda ou descrição do vídeo).
API anônima: limite de requisições baixo, então busque com termos certeiros.
"""
import json
import shutil
import sys
import urllib.parse
import urllib.request

API = 'https://api.openverse.org/v1/'
UA = {'User-Agent': 'aivacs-skills/1.0'}


def buscar(q, n=10, imagem=False, todas=False):
    params = {'q': q, 'page_size': n}
    if not todas:
        params['license_type'] = 'commercial'
    url = API + ('images/' if imagem else 'audio/') + '?' + urllib.parse.urlencode(params)
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        data = json.load(r)
    print(f"{data['result_count']} resultados para '{q}'")
    for x in data['results']:
        lic = f"{x['license'].upper()} {x.get('license_version') or ''}".strip()
        dur = f"{x['duration'] / 1000:.1f}s" if x.get('duration') else ''
        print(f"- {x['title'][:60]} · {lic} · {x.get('creator') or '?'} · {x.get('provider')} {dur}")
        print(f"  arquivo: {x['url']}")
        print(f"  página: {x['foreign_landing_url']}")
        if x['license'] not in ('cc0', 'pdm'):
            print(f"  crédito: \"{x['title']}\" de {x.get('creator') or 'autor desconhecido'} ({lic}, {x['license_url']})")


def baixar(url, dst):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r, open(dst, 'wb') as f:
        shutil.copyfileobj(r, f)
    print(dst)


if __name__ == '__main__':
    a = sys.argv[1:]
    if len(a) >= 2 and a[0] == 'buscar':
        n = int(a[a.index('--n') + 1]) if '--n' in a else 10
        termos = [x for i, x in enumerate(a[1:], 1) if not x.startswith('--') and a[i - 1] != '--n']
        buscar(' '.join(termos), n, '--imagem' in a, '--todas-licencas' in a)
    elif len(a) == 3 and a[0] == 'baixar':
        baixar(a[1], a[2])
    else:
        sys.exit(__doc__)
