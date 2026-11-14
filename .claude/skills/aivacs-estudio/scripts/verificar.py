"""Checks what this session has for the AIVACS groups and says how to fix what is missing.
Usage: verificar.py [videos|instagram|ads|documentos|design|site|estrategia|tudo]
Connectors (Metricool, Meta Ads, Google Ads, Claude Docs) are not visible from here: the agent checks them by looking for their tools."""
import importlib.util
import os
import shutil
import subprocess
import sys
import urllib.request

grupo = sys.argv[1] if len(sys.argv) > 1 else 'tudo'
ok_all = True


def line(ok, what, fix=''):
    global ok_all
    ok_all &= ok
    print(f"{'OK   ' if ok else 'FALTA'} {what}" + ('' if ok or not fix else f'  ->  {fix}'))


def http(url, headers=None):
    try:
        req = urllib.request.Request(url, headers=headers or {})
        return urllib.request.urlopen(req, timeout=15).status
    except Exception as e:  # noqa: BLE001
        return getattr(e, 'code', 0)


def py(mod):
    return importlib.util.find_spec(mod) is not None


def node_has(mod):
    return subprocess.run(['node', '-e', f"require('{mod}')"], capture_output=True).returncode == 0


if grupo in ('videos', 'instagram', 'design', 'tudo'):
    for c in ('ffmpeg', 'ffprobe', 'node', 'npx'):
        line(shutil.which(c) is not None, c, 'apt-get install -y ffmpeg / instale o Node 22')
    line(node_has('playwright'), 'Playwright + Chromium (render de capas e carrosséis)', 'já vem nas sessões na nuvem; local: npm i playwright')
    line(http('https://generativelanguage.googleapis.com/v1beta/models', {'x-goog-api-key': 'dummy'}) == 200,
         'Gemini (narração, imagens, /watch)', 'credencial "Gemini" do ambiente (site generativelanguage.googleapis.com, cabeçalho x-goog-api-key)')
    cred = os.path.expanduser('~/.hyperframes/credentials')
    line(os.path.exists(cred) or bool(os.environ.get('HEYGEN_API_KEY')),
         'HeyGen (música do catálogo)', 'npx hyperframes auth login --device e mande o link ao Jhony aprovar (cota gratuita)')
    fotos = os.environ.get('AIVACS_FOTOS', '')
    line(bool(fotos) and os.path.isdir(fotos), 'fotos do Jhony (AIVACS_FOTOS)',
         'add_repo jonatascne-droid/Mi-auto-trading, clone e export AIVACS_FOTOS=<clone>/aivacs/fotos/recortes')
    line(py('rembg'), 'rembg (recorte de fotos)', 'pip install "rembg[cpu]" scipy (só quando for recortar)')
if grupo in ('videos', 'instagram', 'tudo'):
    line(shutil.which('yt-dlp') is not None, 'yt-dlp (baixar Reels para o /watch e /insta)', 'o hook de início instala; senão: pip install -U yt-dlp')
if grupo in ('ads', 'tudo'):
    for v in ('GOOGLE_ADS_CLIENT_ID', 'GOOGLE_ADS_CLIENT_SECRET', 'GOOGLE_ADS_REFRESH_TOKEN'):
        line(bool(os.environ.get(v)), f'{v} (conector Google Ads, só leitura)', 'variável do ambiente na nuvem')
if grupo in ('documentos', 'tudo'):
    line(py('pypdf') or py('fitz') or shutil.which('pdftotext') is not None, 'leitura de PDF', 'pip install pypdf')
print('\nTudo certo.' if ok_all else '\nCorrija o que falta antes de começar, ou avise o Jhony.')
