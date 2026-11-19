#!/usr/bin/env python3
"""AIVACS: word timings for a voiceover in Spanish (or Portuguese), in the format the /zach-d-films engine reads.
The kit's own words.py uses Parakeet, which only understands English. This one uses the local Whisper from our
aivacs-estudio kit (no key), then respells the heard words as the script has them when a script is given.

    python3 palavras_es.py <voiceover.wav|mp3|m4a> [script.json | script.txt] [--language es]

Writes <voiceover name>.words.json next to the audio: a list of {"w", "s", "e"} (word, start, end in seconds).
"""
import argparse
import difflib
import json
import os
import re
import subprocess
import sys
import tempfile
import unicodedata

HERE = os.path.dirname(os.path.realpath(__file__))
TRANSCRIBE = os.path.join(HERE, '..', 'skills', 'aivacs-estudio', 'scripts', 'transcribe.py')

a = argparse.ArgumentParser()
a.add_argument('audio'); a.add_argument('script', nargs='?')
a.add_argument('--language', default='es')
args = a.parse_args()

audio = os.path.abspath(args.audio)
base = re.sub(r'\.(wav|mp3|m4a|aac|flac|ogg)$', '', audio, flags=re.I)
with tempfile.TemporaryDirectory() as tmp:
    raw = os.path.join(tmp, 'w.json')
    r = subprocess.run([sys.executable, TRANSCRIBE, audio, '-o', raw, '--language', args.language])
    if r.returncode or not os.path.exists(raw):
        sys.exit('transcription failed (aivacs-estudio/scripts/transcribe.py)')
    heard = json.load(open(raw, encoding='utf-8'))['words']

words = [{'w': h['text'], 's': h['start'], 'e': h['end']} for h in heard if h['text']]

if args.script:
    txt = open(args.script, encoding='utf-8').read()
    try:
        data = json.loads(txt)
        txt = ' '.join(data if isinstance(data, list) else data.get('lines', []))
    except json.JSONDecodeError:
        pass
    target = txt.split()
    norm = lambda s: re.sub(r'[^\w]', '', unicodedata.normalize('NFKD', s.lower()).encode('ascii', 'ignore').decode())
    sm = difflib.SequenceMatcher(a=[norm(w['w']) for w in words], b=[norm(t) for t in target], autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ('equal', 'replace') and (i2 - i1) == (j2 - j1):
            for k in range(i2 - i1):
                words[i1 + k]['w'] = target[j1 + k]

out = base + '.words.json'
json.dump(words, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(' '.join(f"{w['w']}@{w['s']:.2f}" for w in words[:20]))
print('wrote', out)
