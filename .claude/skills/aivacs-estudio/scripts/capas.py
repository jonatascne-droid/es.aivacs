"""Helpers for 1080x1920 Reel covers in the AIVACS identity: brand row, eyebrow and big title, glow and bottom fade.
Key content stays inside the 4:5 feed crop (y 285-1635). See examples/capas_reels.py."""
from lib import icon, LOGO, person, tile, chip, glow, ring

CSS = """<style>
.slide.cover { height: 1920px; }
.slide.cover::before { -webkit-mask-image: radial-gradient(circle at 55% 52%, #000 18%, transparent 70%); }
.cv-brand { position: absolute; left: 64px; top: 318px; z-index: 20; display: flex; align-items: center; gap: 14px; font-family: "Jakarta"; font-weight: 800; font-size: 34px; letter-spacing: .04em; }
.cv-brand svg { width: 50px; height: 50px; filter: drop-shadow(0 0 10px rgba(75, 191, 239, .6)); }
.cv-tag { position: absolute; right: 64px; top: 322px; z-index: 20; display: inline-flex; align-items: center; gap: 10px; padding: 10px 20px; border-radius: 999px; border: 1.5px solid rgba(110, 210, 250, .45); background: rgba(13, 22, 31, .7); font-family: "Mono"; font-size: 24px; letter-spacing: .08em; color: var(--cyl); }
.cv-tag i { width: 0; height: 0; border-left: 16px solid #4BBFEF; border-top: 10px solid transparent; border-bottom: 10px solid transparent; }
.cv-head { position: absolute; left: 64px; right: 64px; top: 420px; z-index: 20; }
.cv-title { font-family: "Jakarta"; font-weight: 800; font-size: 112px; line-height: 1.0; letter-spacing: -.035em; text-wrap: balance; margin-top: 18px; text-shadow: 0 6px 30px rgba(0, 0, 0, .6); }
.cv-title em { font-style: normal; color: var(--cy); text-shadow: 0 0 34px rgba(75, 191, 239, .5); }
.cv-fade { position: absolute; left: 0; right: 0; bottom: 0; height: 420px; z-index: 15; background: linear-gradient(0deg, #06090C 10%, rgba(6, 9, 12, .75) 45%, transparent); }
.step { display: flex; align-items: center; gap: 16px; padding: 16px 24px; border-radius: 20px; background: rgba(13, 22, 31, .86); border: 1.5px solid rgba(110, 210, 250, .4); box-shadow: 0 16px 40px rgba(0, 0, 0, .5); font-family: "Jakarta"; font-weight: 700; font-size: 32px; white-space: nowrap; }
.step b { font-family: "Mono"; font-weight: 700; font-size: 26px; color: var(--cy); }
.bubble { position: absolute; z-index: 12; max-width: 470px; padding: 20px 26px 16px; border-radius: 26px; font-family: "DM"; font-size: 31px; line-height: 1.3; box-shadow: 0 18px 44px rgba(0, 0, 0, .55); }
.bubble small { display: block; text-align: right; font-size: 20px; opacity: .65; margin-top: 6px; }
.bubble.in { background: #1F2C34; color: #E9EDEF; border-top-left-radius: 8px; }
.bubble.out { background: #005C4B; color: #E9EDEF; border-top-right-radius: 8px; }
svg.wire { position: absolute; inset: 0; width: 1080px; height: 1920px; z-index: 8; pointer-events: none; }
</style>"""


def head(tag, eyebrow, title):
    return (f'<div class="cv-brand">{LOGO}AIVACS</div><div class="cv-tag"><i></i>{tag}</div>'
            f'<div class="cv-head"><div class="eyebrow">{eyebrow}</div><div class="cv-title">{title}</div></div>')


def cover(out, inner):
    return f'<section class="slide cover" data-out="{out}">{glow(880, 90, 430, .32)}{inner}<div class="cv-fade"></div></section>'


def wire(points, dash=False):
    d = ' '.join(('M' if i == 0 else 'L') + f' {x} {y}' for i, (x, y) in enumerate(points))
    da = ' stroke-dasharray="10 12"' if dash else ''
    return (f'<svg class="wire" viewBox="0 0 1080 1920"><path d="{d}" fill="none" stroke="#4BBFEF" stroke-width="4" '
            f'stroke-linecap="round" stroke-linejoin="round" opacity=".7"{da} style="filter:drop-shadow(0 0 8px rgba(75,191,239,.8))"/></svg>')


