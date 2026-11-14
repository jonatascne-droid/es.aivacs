"""Gemini image generate/edit. Usage: gem.py OUT --prompt TEXT [--img IN ...] [--aspect 4:5] [--size 2K] [--model M]"""
import argparse, base64, json, mimetypes, sys, urllib.request

p = argparse.ArgumentParser()
p.add_argument('out')
p.add_argument('--prompt', required=True)
p.add_argument('--img', action='append', default=[])
p.add_argument('--aspect', default='4:5')
p.add_argument('--size', default='2K')
p.add_argument('--model', default='gemini-3-pro-image')
a = p.parse_args()

parts = []
for f in a.img:
    mt = mimetypes.guess_type(f)[0] or 'image/jpeg'
    parts.append({'inline_data': {'mime_type': mt, 'data': base64.b64encode(open(f, 'rb').read()).decode()}})
parts.append({'text': a.prompt})
body = {'contents': [{'parts': parts}],
        'generationConfig': {'responseModalities': ['IMAGE'], 'imageConfig': {'aspectRatio': a.aspect, 'imageSize': a.size}}}
req = urllib.request.Request(
    f'https://generativelanguage.googleapis.com/v1beta/models/{a.model}:generateContent',
    data=json.dumps(body).encode(), headers={'Content-Type': 'application/json', 'x-goog-api-key': 'dummy'})
try:
    res = json.load(urllib.request.urlopen(req, timeout=300))
except urllib.error.HTTPError as e:
    print('HTTP', e.code, e.read().decode()[:800]); sys.exit(1)
for c in res.get('candidates', []):
    for part in c.get('content', {}).get('parts', []):
        d = part.get('inlineData') or part.get('inline_data')
        if d:
            open(a.out, 'wb').write(base64.b64decode(d['data']))
            print('saved', a.out, d.get('mimeType') or d.get('mime_type'))
            sys.exit(0)
print('no image:', json.dumps(res)[:800]); sys.exit(2)
