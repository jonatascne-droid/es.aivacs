"""Word-level transcript with local Whisper through the HyperFrames CLI (no API key, no paid service).
Writes {"words": [{"text", "start", "end"}]}, the shape cut-silences, cut-mistakes and short-form-edit read.
Usage: transcribe.py MEDIA [-o OUT.json] [--language es] [--model small]
Default output: MEDIA with the extension replaced by .json."""
import argparse
import json
import os
import subprocess
import sys

a = argparse.ArgumentParser()
a.add_argument('media')
a.add_argument('-o', '--out')
a.add_argument('--language', default='es')
a.add_argument('--model', default='small')
args = a.parse_args()

media = os.path.abspath(args.media)
out = args.out or os.path.splitext(media)[0] + '.json'
r = subprocess.run(['npx', '--yes', 'hyperframes', 'transcribe', media, '--model', args.model, '--language', args.language, '--json'],
                   capture_output=True, text=True, timeout=1800, cwd=os.path.dirname(media))
words = []
# the CLI prints its result in several {"type":"words"} chunks, on stdout or stderr depending on the version
for line in (r.stdout + '\n' + r.stderr).splitlines():
    line = line.strip()
    if line.startswith('{"type":"words"'):
        words += [{'text': w['text'].strip(), 'start': round(w['start'], 3), 'end': round(w['end'], 3)} for w in json.loads(line)['words']]
if not words:
    sys.exit('no words from hyperframes transcribe:\n' + (r.stderr or r.stdout)[-1500:])
json.dump({'words': words}, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'{len(words)} words, {words[-1]["end"]:.1f}s -> {out}')
