"""Render review: our own implementation of the gate criteria described in the motionmaxxing docs
(G0 render exists, G2 no empty frame, G3 end hold / final-shot share, motion band, longest static stretch, contact sheet).
Usage: mogcheck.py VIDEO.mp4 OUTDIR [--expect SECONDS]"""
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

AW, AH = 96, 54
FLAT_STD, FLAT_RNG, FLAT_MAX_OK = 1.5, 8, 3
HOLD_EPS, HOLD_MAX = 0.35, 1.4
HUMAN = (6.8, 4.4, 9.8)

video, out = sys.argv[1], sys.argv[2]
expect = float(sys.argv[sys.argv.index('--expect') + 1]) if '--expect' in sys.argv else None
os.makedirs(out, exist_ok=True)


def probe():
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type,r_frame_rate:format=duration', '-of', 'json', video],
                       capture_output=True, text=True)
    j = json.loads(r.stdout)
    fps = 30.0
    for s in j['streams']:
        if s['codec_type'] == 'video':
            a, b = s['r_frame_rate'].split('/')
            fps = float(a) / float(b)
    return float(j['format']['duration']), fps, any(s['codec_type'] == 'audio' for s in j['streams'])


dur, fps, has_audio = probe()
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', video, '-an', '-vf', f'scale={AW}:{AH}:flags=area,format=gray', '-f', 'rawvideo', '-'],
                     capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, AH, AW).astype(np.float32)
n = len(fr)
std = fr.reshape(n, -1).std(1)
rng = fr.reshape(n, -1).max(1) - fr.reshape(n, -1).min(1)
diff = np.concatenate([[0.0], np.abs(fr[1:] - fr[:-1]).reshape(n - 1, -1).mean(1)])
flat_c = fr.reshape(n, -1) - fr.reshape(n, -1).mean(1, keepdims=True)
den = np.sqrt((flat_c ** 2).sum(1))
corr = np.concatenate([[1.0], (flat_c[1:] * flat_c[:-1]).sum(1) / np.maximum(den[1:] * den[:-1], 1e-6)])


def runs(mask):
    out_, s = [], None
    for i, m in enumerate(mask):
        if m and s is None:
            s = i
        elif not m and s is not None:
            out_.append((s, i - 1)); s = None
    if s is not None:
        out_.append((s, len(mask) - 1))
    return out_


gates = []
why, st = [], 'PASS'
if (std >= FLAT_STD).sum() < max(1, 0.05 * n):
    why.append('BLANK'); st = 'FAIL'
if (diff[1:] >= HOLD_EPS).sum() < max(2, 0.05 * (n - 1)):
    why.append('NO MOTION'); st = 'FAIL'
if expect is not None and abs(dur - expect) > 1.0:
    why.append(f'duration {dur:.2f}s vs expected {expect:.2f}s'); st = 'FAIL'
why.append(f'duration {dur:.2f}s, {n} frames @ {fps:.0f}fps, audio {"yes" if has_audio else "NO"}')
if not has_audio:
    st = 'FAIL'
gates.append(('G0 render exists', st, '; '.join(why)))

flat_runs = [r for r in runs((std < FLAT_STD) & (rng < FLAT_RNG)) if r[1] - r[0] + 1 > FLAT_MAX_OK]
gates.append(('G2 no empty frame', 'FAIL' if flat_runs else 'PASS',
              '; '.join(f'{s / fps:.2f}-{(e + 1) / fps:.2f}s' for s, e in flat_runs) or f'no run of > {FLAT_MAX_OK} flat frames'))

still = runs(diff < HOLD_EPS)
hold = (n - still[-1][0]) / fps if still and still[-1][1] == n - 1 else 0.0
cuts = [i for i in range(2, n) if corr[i] < 0.6 and diff[i] >= 5 and diff[i] >= 2.5 * np.median(diff[max(1, i - 6):i + 6])]
final = (n - cuts[-1]) / fps if cuts else dur
st = 'PASS'
why = [f'end hold {hold:.2f}s (limit {HOLD_MAX}s{"; under 0.6s = ends mid-motion" if hold < 0.6 else ""})']
if hold > HOLD_MAX:
    st = 'FAIL'
why.append(f'final shot {final:.2f}s = {100 * final / dur:.0f}% of the film' + (' (> 25%)' if cuts and final / dur > 0.25 else ''))
if cuts and final / dur > 0.25:
    st = 'FAIL'
gates.append(('G3 end hold, final shot', st, '; '.join(why)))

inner = [(s, e) for s, e in still if e < n - 1]
longest = max(inner, key=lambda r: r[1] - r[0]) if inner else None
# dark footage: a word landing on a near-black ground moves the mean luma far less than on a bright frame,
# so also measure the longest stretch with no visible event against this film's own living-ground floor
eps_ev = max(0.12, 3 * float(np.percentile(diff[1:], 20)))
quiet_ev = [r for r in runs(diff < eps_ev) if r[1] < n - 1]
longest_ev = max(quiet_ev, key=lambda r: r[1] - r[0]) if quiet_ev else None
mm = float(diff[1:].mean())
band = 'inside' if HUMAN[1] <= mm <= HUMAN[2] else ('below' if mm < HUMAN[1] else 'above')

# contact sheet: 15 frames evenly spaced, 3 rows x 5
cols, rows_ = 5, 3
times = [dur * (i + 0.5) / (cols * rows_) for i in range(cols * rows_)]
tw, th = 216, 384
sheet = Image.new('RGB', (cols * tw, rows_ * (th + 22)), (20, 20, 20))
d = ImageDraw.Draw(sheet)
for k, t in enumerate(times):
    png = os.path.join(out, f'_f{k}.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', video, '-frames:v', '1', '-vf', f'scale={tw}:{th}', png])
    if os.path.exists(png):
        sheet.paste(Image.open(png), ((k % cols) * tw, (k // cols) * (th + 22)))
        os.remove(png)
    d.text(((k % cols) * tw + 6, (k // cols) * (th + 22) + th + 4), f'{t:.1f}s', fill=(230, 230, 230))
sheet.save(os.path.join(out, 'sheet.jpg'), quality=85)

report = {'gates': gates, 'motion_mean': round(mm, 2), 'human_band': HUMAN, 'motion_vs_band': band,
          'longest_static': [round(longest[0] / fps, 2), round((longest[1] + 1) / fps, 2)] if longest else None,
          'cuts_s': [round(c / fps, 2) for c in cuts], 'event_eps': round(eps_ev, 3),
          'longest_no_event': [round(longest_ev[0] / fps, 2), round((longest_ev[1] + 1) / fps, 2)] if longest_ev else None}
json.dump(report, open(os.path.join(out, 'report.json'), 'w'), indent=1)
for g in gates:
    print(f'{g[1]:4s}  {g[0]}: {g[2]}')
print(f'MOTION mean frame-to-frame luma change {mm:.1f}/255 ({band} the human band {HUMAN[1]}-{HUMAN[2]}, median {HUMAN[0]})')
if longest:
    print(f'STATIC longest still stretch inside the film: {longest[0] / fps:.2f}-{(longest[1] + 1) / fps:.2f}s ({(longest[1] - longest[0] + 1) / fps:.2f}s)')
if longest_ev:
    print(f'EVENTS longest stretch with no visible event (diff < {eps_ev:.2f}, 3x this film\'s ground floor): {longest_ev[0] / fps:.2f}-{(longest_ev[1] + 1) / fps:.2f}s ({(longest_ev[1] - longest_ev[0] + 1) / fps:.2f}s)')
print(f'CUTS {len(cuts)} detected; sheet: {os.path.join(out, "sheet.jpg")}')
