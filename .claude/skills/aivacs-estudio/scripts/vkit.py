"""Kit for the AIVACS vertical Reels (HyperFrames, 1080x1920), with motion craft taken from the motionmaxxing docs:
living ground (no dead frame), word-level captions at speech rhythm, accelerating exits, short living end card.
Every time given to the kit is absolute (seconds from the start of the video)."""
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))   # .claude/skills/aivacs-estudio/scripts -> repo root
sys.path.insert(0, HERE)
from lib import icon  # noqa: E402,F401

VO_OFF = 0.15
CY = '#4BBFEF'
SFX_LIB = os.path.join(REPO, '.claude', 'skills', 'media-use', 'audio', 'assets', 'sfx')
SFX_FILES = {'pop': 'pop.mp3', 'click': 'click-soft.mp3', 'whoosh': 'whoosh-short.mp3', 'impact': 'impact-bass-1.mp3', 'notify': 'notification.mp3', 'chime': 'chime.mp3'}
SFX_LEN = {'pop': 0.7, 'click': 0.37, 'whoosh': 0.57, 'impact': 2.1, 'notify': 1.2, 'chime': 1.4}

# GSAP stand-ins for the measured eases (motionmaxxing references/motion.md section 2)
E = {'softLand': 'power3.out', 'snapSettle': 'expo.out', 'glide': 'sine.out', 'accelExit': 'power3.in', 'crashOut': 'power4.in',
     'gentleIn': 'power2.in', 'softInOut': 'power2.inOut', 'cruise': 'none', 'popOver': 'back.out(1.4)'}

FONTS = """@font-face { font-family: "Jakarta"; src: url('assets/fonts/plus-jakarta-sans.woff2') format('woff2'); font-weight: 200 800; }
@font-face { font-family: "DMSans"; src: url('assets/fonts/dm-sans.woff2') format('woff2'); font-weight: 100 1000; }
@font-face { font-family: "JBMono"; src: url('assets/fonts/jetbrains-mono.woff2') format('woff2'); font-weight: 100 800; }"""

BASE = FONTS + """
#root { position: absolute; inset: 0; font-family: "DMSans", sans-serif; color: #F0F4F8; overflow: hidden; }
.ic svg { width: 100%; height: 100%; display: block; }
.glass { background: linear-gradient(160deg, rgba(110,210,250,.16), rgba(17,24,33,.86) 42%, rgba(9,14,19,.94)); border: 2px solid rgba(110,210,250,.45);
  border-radius: 30px; box-shadow: 0 30px 60px rgba(0,0,0,.5), 0 0 36px rgba(75,191,239,.16), inset 0 1px 0 rgba(255,255,255,.08); }
.chip { position: absolute; display: flex; align-items: center; gap: 22px; padding: 0 30px; height: 118px; font: 700 40px "Jakarta"; color: #fff; white-space: nowrap; }
.chip .ic { width: 58px; height: 58px; flex: none; color: #BDEBFF; filter: drop-shadow(0 0 12px rgba(75,191,239,.75)); }
.hx { font-family: "Jakarta"; font-weight: 800; letter-spacing: -.035em; line-height: 1.0; }
.cy { color: #4BBFEF; text-shadow: 0 0 36px rgba(75,191,239,.45); }
"""

LOGO_SVG = ('<svg viewBox="0 0 100 100" width="{w}" height="{w}" fill="none" style="filter:drop-shadow(0 0 22px rgba(75,191,239,.8))">'
            '<path id="{p}-tri" d="M50 7 L93 79 Q95 85 89 85 L11 85 Q5 85 7 79 Z" stroke="#4BBFEF" stroke-width="7" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/>'
            '<line id="{p}-base" x1="17" y1="96" x2="83" y2="96" stroke="#4BBFEF" stroke-width="7" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/></svg>')


def norm(x):
    return re.sub(r'[^a-záéíóúñ0-9]', '', x.lower())


class Kit:
    def __init__(self, P, gap=0.25, tail=1.9):
        self.P = P
        self.meta = json.load(open(os.path.join(P, 'voice_meta.json'), encoding='utf-8'))
        self.ids = sorted(self.meta, key=lambda s: int(s[1:]))
        self.ls, self.ld = {}, {}
        t = 0.0
        for i, sid in enumerate(self.ids):
            d = VO_OFF + self.meta[sid]['duration_s'] + (tail if i == len(self.ids) - 1 else gap)
            self.ls[sid] = round(t, 3); self.ld[sid] = round(d, 3); t += d
        self.total = round(t, 3)
        self.scenes, self.sfx = [], []
        os.makedirs(os.path.join(P, 'compositions'), exist_ok=True)
        for sub in ('fonts', 'img', 'sfx'):
            os.makedirs(os.path.join(P, 'assets', sub), exist_ok=True)
        for f in ('plus-jakarta-sans.woff2', 'dm-sans.woff2', 'jetbrains-mono.woff2'):
            shutil.copy(os.path.join(REPO, 'assets', 'fonts', f), os.path.join(P, 'assets', 'fonts', f))
        for n, f in SFX_FILES.items():
            shutil.copy(os.path.join(SFX_LIB, f), os.path.join(P, 'assets', 'sfx', f'{n}.mp3'))
        open(os.path.join(P, 'assets', 'sfx', 'CREDITS.md'), 'w').write('# Sound effects\n\nBundled HyperFrames library, from Pixabay under the Pixabay Content License: commercial use, no attribution required.\n')

    # ---- timing ----
    def start(self, sid):
        return self.ls[sid]

    def end(self, sid):
        return round(self.ls[sid] + self.ld[sid], 3)

    def words(self, sid):
        base = self.ls[sid] + VO_OFF
        return [(w['text'], round(base + w['start'], 3), round(base + w['end'], 3)) for w in self.meta[sid]['words']]

    def at(self, sid, prefix, which='start', nth=0):
        hits = [w for w in self.words(sid) if norm(w[0]).startswith(norm(prefix))]
        w = hits[nth]
        return round(w[1] if which == 'start' else w[2], 3)

    def last_word(self, sid):
        return self.words(sid)[-1][2]

    # ---- scenes ----
    def add_scene(self, sid, start, end, css, html, js):
        dur = round(end - start, 3)
        self.scenes.append((sid, round(start, 3), dur))
        content = f"""<template>
<style>
{BASE}
{css}
</style>
<div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
{html}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{js}
window.__timelines["{sid}"] = tl;
</script>
</template>
"""
        open(os.path.join(self.P, 'compositions', f'{sid}.html'), 'w', encoding='utf-8').write(content)

    def fx(self, name, t):
        self.sfx.append((name, round(t, 3)))

    def image(self, src, name):
        shutil.copy(src, os.path.join(self.P, 'assets', 'img', name))
        return f'assets/img/{name}'

    # ---- word-level captions ----
    def captions(self, keys, skip=(), until=None, top=1250):
        FUNC = {'y', 'que', 'al', 'en', 'a', 'se', 'la', 'el', 'tu', 'lo', 'con', 'de', 'por', 'e', 'un', 'una'}
        groups = []
        for sid in self.ids:
            if sid in skip:
                continue
            ws = [w for w in self.words(sid) if until is None or w[1] < until]
            cur = []
            for j, w in enumerate(ws):
                rest = 0
                for x in ws[j:]:
                    rest += 1
                    if x[0][-1] in '.,!?:':
                        break
                if cur and len(cur) >= 2 and rest > 2 and norm(w[0]) in FUNC and len(cur) + 1 > 3 and norm(cur[-1][0]) not in FUNC:
                    groups.append(cur); cur = []
                cur.append(w)
                if len(cur) >= 5 or w[0][-1] in '.,!?:' or j == len(ws) - 1:
                    groups.append(cur); cur = []
        html, js = '', ''
        for k, g in enumerate(groups):
            n_chars = sum(len(w[0]) for w in g) + len(g)
            fs = min(68, int(900 / (n_chars * 0.6)))
            spans = ' '.join(f'<span class="w" id="c{k}w{i}">{w[0]}</span>' for i, w in enumerate(g))
            html += f'<div class="cg" id="c{k}" style="font-size:{fs}px">{spans}</div>\n'
            st = max(0.05, g[0][1] - 0.06)
            nxt = groups[k + 1][0][1] - 0.06 if k + 1 < len(groups) else self.total - 0.2
            en = min(g[-1][2] + 0.35, nxt, until if until else 1e9)
            js += f'tl.set("#c{k}", {{ visibility: "visible" }}, {st:.3f});\n'
            for i, w in enumerate(g):
                t0 = max(0.02, w[1] - 0.05)
                final = CY if norm(w[0]) in keys else '#FFFFFF'
                js += f'tl.set("#c{k}w{i}", {{ y: 18 }}, 0);\n'
                js += f'tl.to("#c{k}w{i}", {{ opacity: 1, y: 0, duration: 0.3, ease: "{E["softLand"]}" }}, {t0:.3f});\n'
                if final != CY:
                    js += f'tl.to("#c{k}w{i}", {{ color: "{final}", duration: 0.25, ease: "power1.out" }}, {t0 + 0.14:.3f});\n'
            js += (f'tl.to("#c{k}", {{ y: -18, opacity: 0, duration: 0.12, ease: "{E["accelExit"]}" }}, {en - 0.12:.3f});\n'
                   f'tl.set("#c{k}", {{ visibility: "hidden" }}, {en:.3f});\n')
        cap = f"""<template>
<style>
{FONTS}
#root {{ position: absolute; inset: 0; }}
.cg {{ position: absolute; left: 0; right: 0; top: {top}px; text-align: center; font-family: "Jakarta"; font-weight: 800; line-height: 1.12;
  letter-spacing: -.01em; padding: 0 64px; visibility: hidden; text-shadow: 0 4px 18px rgba(0,0,0,.9), 0 0 3px rgba(0,0,0,.9); }}
.w {{ display: inline-block; opacity: 0; color: {CY}; }}
</style>
<div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{html}</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{js}
window.__timelines["captions"] = tl;
</script>
</template>
"""
        open(os.path.join(self.P, 'compositions', 'captions.html'), 'w', encoding='utf-8').write(cap)
        return [(' '.join(w[0] for w in g), round(g[0][1], 2)) for g in groups]

    # ---- root: living ground, scene hosts, captions, audio ----
    def write_index(self, bgm_volume=0.2, bgm_media_start=0, glow_path=((-140, -80, 160, 140), (180, 260, -160, -60))):
        T = self.total
        drift = int(T * 30 / 60) * 60        # about 1 px per frame, whole 60 px tiles
        (a0x, a0y, a1x, a1y), (b0x, b0y, b1x, b1y) = glow_path
        hosts = ''.join(f'<div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{st}" data-duration="{du}" data-track-index="{i + 1}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:{i + 5}"></div>\n'
                        for i, (sid, st, du) in enumerate(self.scenes))
        voices = ''.join(f'<audio id="vo-{sid}" class="clip" src="{self.meta[sid]["path"]}" data-start="{self.ls[sid] + VO_OFF:.3f}" data-duration="{self.meta[sid]["duration_s"]}" data-track-index="20" data-volume="1"></audio>\n'
                         for sid in self.ids)
        sfx = ''.join(f'<audio id="fx{k}" class="clip" src="assets/sfx/{n}.mp3" data-start="{max(0, t0):.3f}" data-duration="{SFX_LEN[n]}" data-track-index="{(21, 22, 24)[k % 3]}" data-volume="0.3" data-fade-out="0.1"></audio>\n'
                      for k, (n, t0) in enumerate(self.sfx))
        bgm = ''
        if os.path.exists(os.path.join(self.P, 'assets', 'bgm', 'track.mp3')):
            bgm = f'<audio id="bgm" class="clip" src="assets/bgm/track.mp3" data-start="0" data-duration="{T}" data-track-index="23" data-volume="{bgm_volume}" data-media-start="{bgm_media_start}" data-fade-in="0.3" data-fade-out="1.4"></audio>\n'
        index = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #080C10; }}
#bg {{ position: absolute; inset: 0; z-index: 0; background: linear-gradient(180deg, #0A1016, #080C10 55%, #06090C); }}
.glow {{ position: absolute; z-index: 1; border-radius: 50%; pointer-events: none; }}
#glowA {{ left: -110px; top: 260px; width: 1300px; height: 1300px; background: radial-gradient(circle, rgba(42,139,191,.34), rgba(42,139,191,.10) 42%, transparent 68%); }}
#glowB {{ left: 240px; top: 980px; width: 900px; height: 900px; background: radial-gradient(circle, rgba(75,191,239,.16), transparent 66%); }}
#gridw {{ position: absolute; inset: 0; z-index: 2; overflow: hidden; -webkit-mask-image: radial-gradient(circle at 50% 44%, #000 18%, transparent 72%); mask-image: radial-gradient(circle at 50% 44%, #000 18%, transparent 72%); }}
#grid {{ position: absolute; left: 0; top: 0; width: 1080px; height: {1920 + drift}px;
  background-image: linear-gradient(rgba(75,191,239,.075) 1px, transparent 1px), linear-gradient(90deg, rgba(75,191,239,.075) 1px, transparent 1px); background-size: 60px 60px; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="1080" data-height="1920">
<div id="bg"></div><div id="glowA" class="glow"></div><div id="glowB" class="glow"></div><div id="gridw"><div id="grid"></div></div>
{hosts}<div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{T}" data-track-index="9" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:60"></div>
{voices}{sfx}{bgm}</div>
<script>
const tl = gsap.timeline({{ paused: true }});
tl.fromTo("#glowA", {{ x: {a0x}, y: {a0y}, scale: 1 }}, {{ x: {a1x}, y: {a1y}, scale: 1.18, duration: {T}, ease: "none" }}, 0);
tl.fromTo("#glowB", {{ x: {b0x}, y: {b0y}, scale: 1.1 }}, {{ x: {b1x}, y: {b1y}, scale: .92, duration: {T}, ease: "none" }}, 0);
tl.fromTo("#grid", {{ y: 0 }}, {{ y: -{drift}, duration: {T}, ease: "none" }}, 0);
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
        open(os.path.join(self.P, 'index.html'), 'w', encoding='utf-8').write(index)


def endcard(K, sid, start, t_mark, jhony_src, jh_left, jh_top, jh_width, cta_title, cta_main):
    """Short, living end card: the AIVACS mark draws itself (arriving slightly oversize), the CTA lands, Jhony rises;
    then a light sweep crosses the WhatsApp pill on a fixed period and everything creeps, so no frame is dead. Times absolute."""
    L = lambda t: round(t - start, 3)
    end = K.total
    sweeps = ''
    t = t_mark + 1.25
    while t < end - 0.5:
        sweeps += f'tl.set("#{sid}-sw", {{ x: -220 }}, {L(t)});\ntl.to("#{sid}-sw", {{ x: 820, duration: 0.85, ease: "{E["softInOut"]}" }}, {L(t)});\n'
        t += 1.15
    html = f"""<div id="{sid}-all" style="position:absolute;inset:0">
<div id="{sid}-mark" style="position:absolute;left:0;right:0;top:330px;text-align:center">
  {LOGO_SVG.format(w=210, p=sid)}
  <div id="{sid}-word" style="font:800 84px 'Jakarta';letter-spacing:.06em;margin-top:4px;color:#F0F4F8">AIVACS</div></div>
<div id="{sid}-cta" style="position:absolute;left:0;right:0;top:700px;text-align:center">
  <div style="font:700 36px 'Jakarta';color:#C9D4DD">{cta_title}</div>
  <div id="{sid}-pill" style="position:relative;overflow:hidden;display:inline-flex;align-items:center;gap:16px;margin-top:20px;padding:22px 40px;border-radius:999px;background:#25D366;color:#04121B;font:800 48px 'Jakarta';box-shadow:0 0 50px rgba(37,211,102,.35)">
    <i class="ic" style="width:50px;height:50px">{icon('si:whatsapp')}</i>{cta_main}
    <span id="{sid}-sw" style="position:absolute;top:-20px;bottom:-20px;left:0;width:110px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.55),transparent)"></span></div></div>
<img id="{sid}-jh" src="{jhony_src}" alt="" style="position:absolute;left:{jh_left}px;top:{jh_top}px;width:{jh_width}px;filter:drop-shadow(0 14px 28px rgba(0,0,0,.55));-webkit-mask-image:linear-gradient(180deg,#000 70%,transparent 97%);mask-image:linear-gradient(180deg,#000 70%,transparent 97%)">
</div>"""
    css = f"#{sid}-mark, #{sid}-cta, #{sid}-jh {{ opacity: 0; }}\n"
    js = f"""tl.set("#{sid}-sw", {{ x: -220, skewX: -18 }}, 0);
tl.set("#{sid}-mark", {{ scale: 1.6 }}, 0);
tl.set("#{sid}-word", {{ y: 26 }}, 0);
tl.set("#{sid}-cta", {{ y: 60 }}, 0);
tl.set("#{sid}-jh", {{ y: 320, scale: 1, transformOrigin: "50% 100%" }}, 0);
tl.set("#{sid}-mark", {{ opacity: 1 }}, {L(t_mark - 0.3)});
tl.to("#{sid}-mark", {{ scale: 1, duration: 0.55, ease: "{E['snapSettle']}" }}, {L(t_mark - 0.3)});
tl.to("#{sid}-tri", {{ strokeDashoffset: 0, duration: 0.5, ease: "{E['softInOut']}" }}, {L(t_mark - 0.3)});
tl.to("#{sid}-base", {{ strokeDashoffset: 0, duration: 0.22, ease: "{E['softLand']}" }}, {L(t_mark + 0.12)});
tl.to("#{sid}-word", {{ y: 0, duration: 0.4, ease: "{E['softLand']}" }}, {L(t_mark)});
tl.to("#{sid}-cta", {{ opacity: 1, duration: 0.12, ease: "none" }}, {L(t_mark + 0.4)});
tl.to("#{sid}-cta", {{ y: 0, duration: 0.42, ease: "{E['softLand']}" }}, {L(t_mark + 0.4)});
tl.to("#{sid}-jh", {{ opacity: 1, duration: 0.12, ease: "none" }}, {L(t_mark + 0.2)});
tl.to("#{sid}-jh", {{ y: 0, duration: 0.6, ease: "{E['softLand']}" }}, {L(t_mark + 0.2)});
tl.fromTo("#{sid}-all", {{ scale: 1 }}, {{ scale: 1.035, duration: {round(end - t_mark, 3)}, ease: "none" }}, {L(t_mark)});
tl.to("#{sid}-jh", {{ scale: 1.05, duration: {round(end - t_mark - 0.8, 3)}, ease: "none" }}, {L(t_mark + 0.8)});
{sweeps}"""
    K.fx('impact', t_mark - 0.05)
    return css, html, js
