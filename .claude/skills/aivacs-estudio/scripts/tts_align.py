"""One Gemini TTS request for a whole script, then split into per-line WAVs using Whisper word timings aligned to the script.
Writes assets/voice/<id>.wav and voice_meta.json with per-line word timings (one entry per script token, relative to the clip).
Usage: TTS_MODEL=... tts_align.py PROJECT_DIR [--reuse]   (--reuse skips the TTS request and re-splits assets/voice/full.wav)"""
import base64
import difflib
import json
import os
import re
import subprocess
import sys
import time
import unicodedata
import urllib.error
import urllib.request
import wave

import numpy as np

P = sys.argv[1]
reuse = '--reuse' in sys.argv
model = os.environ.get('TTS_MODEL', 'gemini-2.5-flash-preview-tts')
req = json.load(open(os.path.join(P, 'audio_request.json'), encoding='utf-8'))
lines = req['lines']
vdir = os.path.join(P, 'assets', 'voice'); os.makedirs(vdir, exist_ok=True)
full = os.path.join(vdir, 'full.wav')

if not reuse:
    prompt = f"{req.get('style', '')}\nLee exactamente este texto, con una pausa clara entre cada frase:\n" + '\n'.join(l.get('say', l['text']) for l in lines)
    body = {'contents': [{'parts': [{'text': prompt}]}],
            'generationConfig': {'responseModalities': ['AUDIO'], 'speechConfig': {'voiceConfig': {'prebuiltVoiceConfig': {'voiceName': req.get('voice', 'Charon')}}}}}
    r = urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent',
                               data=json.dumps(body).encode(), headers={'Content-Type': 'application/json', 'x-goog-api-key': 'dummy'})
    for attempt in range(6):
        try:
            res = json.load(urllib.request.urlopen(r, timeout=300)); break
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 5:
                print(e.read()[:400]); raise
            print('429, waiting', flush=True); time.sleep(40)
    part = res['candidates'][0]['content']['parts'][0]['inlineData']
    mt = part.get('mimeType', '')
    rate = int(mt.split('rate=')[1].split(';')[0]) if 'rate=' in mt else 24000
    raw = os.path.join(vdir, 'full.pcm')
    open(raw, 'wb').write(base64.b64decode(part['data']))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 's16le', '-ar', str(rate), '-ac', '1', '-i', raw, '-ar', '48000', '-ac', '1', full], check=True)
    os.remove(raw)

with wave.open(full) as w:
    sr = w.getframerate(); audio = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
dur = len(audio) / sr
print('full', round(dur, 2), 's', flush=True)

# ---------- helpers ----------
def whisper(path):
    o = subprocess.run(['npx', 'hyperframes', 'transcribe', path, '--model', 'small', '--language', 'es', '--json'], cwd=P, capture_output=True, text=True, timeout=900)
    words = []
    for ln in (o.stdout + '\n' + o.stderr).splitlines():
        ln = ln.strip()
        if ln.startswith('{"type":"words"'):
            words += json.loads(ln)['words']
    return words


def norm(s):
    s = unicodedata.normalize('NFD', s.lower())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]', '', s)


def align(toks, ww, total):
    """script tokens -> (start, end) using Whisper words; misses interpolated by character length."""
    times = [None] * len(toks)
    A = [norm(t) for t in toks]; B = [norm(w['text']) for w in ww]
    sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
    hit = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            for k in range(i2 - i1):
                times[i1 + k] = (ww[j1 + k]['start'], ww[j1 + k]['end']); hit += 1
        elif tag == 'replace':
            s0, e0 = ww[j1]['start'], ww[j2 - 1]['end']
            tot = sum(len(t) for t in toks[i1:i2]) or 1; acc = 0
            for k in range(i1, i2):
                a = s0 + (e0 - s0) * acc / tot; acc += len(toks[k]); times[k] = (a, s0 + (e0 - s0) * acc / tot)
    k = 0
    while k < len(toks):
        if times[k] is not None:
            k += 1; continue
        j = k
        while j < len(toks) and times[j] is None:
            j += 1
        s0 = times[k - 1][1] if k > 0 else 0.0
        e0 = times[j][0] if j < len(toks) else total
        tot = sum(len(t) for t in toks[k:j]) or 1; acc = 0
        for m in range(k, j):
            a = s0 + (e0 - s0) * acc / tot; acc += len(toks[m]); times[m] = (a, s0 + (e0 - s0) * acc / tot)
        k = j
    return times, hit


env = np.sqrt(np.convolve(audio ** 2, np.ones(int(sr * 0.02)) / int(sr * 0.02), mode='same'))
thr = max(0.008, float(np.percentile(env, 30)) * 2.5)
quiet = env < thr

# ---------- rough line boundaries from the full transcription ----------
ww = whisper(full)
if not ww:
    sys.exit('no whisper words')
toks, owner = [], []
for li, l in enumerate(lines):
    for t in l['text'].split():
        toks.append(t); owner.append(li)
times, hit = align(toks, ww, dur)
print(f'full transcription: {len(ww)} words, {hit}/{len(toks)} script words matched', flush=True)
first = [times[owner.index(li)][0] for li in range(len(lines))]

# ---------- cut at the N-1 longest silences (the sentence pauses), checked against the transcription ----------
step = int(sr * 0.001)
qs = quiet[::step]
runs_, s_ = [], None
for i, v in enumerate(qs):
    if v and s_ is None:
        s_ = i
    if (not v or i == len(qs) - 1) and s_ is not None:
        if i - s_ >= 250:
            runs_.append((s_ / 1000, i / 1000))
        s_ = None
need = len(lines) - 1
last_end = [times[max(i for i, o in enumerate(owner) if o == li)][1] for li in range(len(lines))]
cuts, prev = [0.0], 0.0
for li in range(1, len(lines)):
    exp = first[li] - 0.3
    cands = [r for r in runs_ if r[0] > prev + 0.3 and last_end[li - 1] - 0.8 <= (r[0] + r[1]) / 2 <= first[li] + 1.0]
    if not cands:
        cands = [r for r in runs_ if r[0] > prev + 0.3 and abs((r[0] + r[1]) / 2 - exp) <= 2.0]
    if not cands:
        sys.exit(f'no pause found near line {li + 1} ({first[li]:.2f}s)')
    best = max(cands, key=lambda r: (r[1] - r[0]) - 0.35 * abs((r[0] + r[1]) / 2 - exp))
    cuts.append((best[0] + best[1]) / 2); prev = best[1]
    print(f'boundary {li}: pause {best[0]:.2f}-{best[1]:.2f}s (transcription: line {li + 1} near {first[li]:.2f}s)', flush=True)
cuts.append(dur)

tempo = float(os.environ.get('TEMPO', '1.0'))
meta = {}
for li, l in enumerate(lines):
    a, b = int(cuts[li] * sr), int(cuts[li + 1] * sr)
    loud = np.where(~quiet[a:b])[0]
    s0 = (a + loud[0]) / sr if len(loud) else cuts[li]
    e0 = (a + loud[-1]) / sr if len(loud) else cuts[li + 1]
    c0, c1 = max(cuts[li], s0 - 0.05), min(cuts[li + 1], e0 + 0.14)
    wav = os.path.join(vdir, f"{l['id']}.wav")
    af = 'afade=t=in:d=0.02,areverse,afade=t=in:d=0.05,areverse' + (f',atempo={tempo}' if tempo != 1.0 else '') + ',loudnorm=I=-16:TP=-1.5:LRA=11'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{c0:.3f}', '-t', f'{c1 - c0:.3f}', '-i', full, '-af', af, '-ar', '48000', wav], check=True)
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', wav], capture_output=True, text=True).stdout)
    lt = l['text'].split()
    lw = whisper(wav)
    t2, h2 = align(lt, lw, d - 0.08)
    words = [{'text': lt[i], 'start': round(max(0, t2[i][0]), 3), 'end': round(min(d, t2[i][1]), 3)} for i in range(len(lt))]
    meta[l['id']] = {'path': f"assets/voice/{l['id']}.wav", 'duration_s': round(d, 3), 'text': l['text'], 'words': words, 'model': model, 'tempo': tempo}
    print(f"{l['id']} {d:.2f}s  matched {h2}/{len(lt)} | heard: " + ' '.join(w['text'] for w in lw), flush=True)
json.dump(meta, open(os.path.join(P, 'voice_meta.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('speech total', round(sum(v['duration_s'] for v in meta.values()), 2), 's')
