"""Shared building blocks for the AIVACS carousel slides (1080x1350)."""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))


def icon(name):
    si = name.startswith('si:')
    fn = f"si-{name[3:]}.svg" if si else f"lucide-{name}.svg"
    svg = open(os.path.join(HERE, 'icons', fn), encoding='utf-8').read()
    svg = re.sub(r'<!--.*?-->', '', svg, flags=re.S).strip()
    head, rest = svg.split('>', 1)
    head = re.sub(r'\s(class|width|height)="[^"]*"', '', head)
    svg = head + '>' + rest
    if si:
        svg = svg.replace('<svg ', '<svg fill="currentColor" ', 1)
    return svg


LOGO = ('<svg viewBox="0 0 100 100" fill="none"><path d="M50 7 L93 79 Q95 85 89 85 L11 85 Q5 85 7 79 Z" '
        'stroke="#4BBFEF" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>'
        '<line x1="17" y1="96" x2="83" y2="96" stroke="#4BBFEF" stroke-width="7" stroke-linecap="round"/></svg>')


def top(n, total):
    return (f'<div class="top"><div class="brand">{LOGO}AIVACS</div>'
            f'<div class="count">{n:02d} / {total:02d}</div></div>')


def bot(last=False, text='Desliza'):
    right = '' if last else f'<span class="next">{text} {icon("arrow-right")}</span>'
    return f'<div class="bot"><span>@aivacses</span>{right}</div>'


def person(src, left, top_, width, rim=False, z=6, extra=''):
    rim_html = (f'<div class="rim" style="-webkit-mask-image:url({src})"></div>' if rim else '')
    return (f'<div class="person" style="left:{left}px;top:{top_}px;width:{width}px;z-index:{z};{extra}">'
            f'<img src="{src}" alt="">{rim_html}</div>')


def tile(name, x, y, size, rot=0, label=None, extra=''):
    si = ' si' if name.startswith('si:') else ''
    lab = f'<small>{label}</small>' if label else ''
    return (f'<div class="tile{si}" style="left:{x}px;top:{y}px;width:{size}px;height:{size}px;'
            f'transform:rotate({rot}deg);{extra}">{icon(name)}{lab}</div>')


def chip(html, name, x, y, extra=''):
    ic = icon(name) if name else ''
    return f'<div class="chip" style="left:{x}px;top:{y}px;{extra}">{ic}<span>{html}</span></div>'


def glow(cx, cy, r, op=1):
    return f'<div class="glow" style="left:{cx - r}px;top:{cy - r}px;width:{2 * r}px;height:{2 * r}px;opacity:{op}"></div>'


def ring(cx, cy, r, thin=False):
    c = ' thin' if thin else ''
    return f'<div class="ring{c}" style="left:{cx - r}px;top:{cy - r}px;width:{2 * r}px;height:{2 * r}px"></div>'


def streak(d1, d2, sid='s', z=8):
    return f'''<svg class="streak" style="z-index:{z}" viewBox="0 0 1080 1350"><defs>
<linearGradient id="{sid}g" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#4BBFEF" stop-opacity="0"/>
<stop offset=".35" stop-color="#4BBFEF"/><stop offset=".62" stop-color="#F2FBFF"/><stop offset=".85" stop-color="#4BBFEF"/>
<stop offset="1" stop-color="#4BBFEF" stop-opacity="0"/></linearGradient>
<filter id="{sid}b" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="16"/></filter>
<filter id="{sid}b2" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="4"/></filter></defs>
<path d="{d1}" stroke="url(#{sid}g)" stroke-width="46" fill="none" filter="url(#{sid}b)" opacity=".75"/>
<path d="{d1}" stroke="url(#{sid}g)" stroke-width="10" fill="none" filter="url(#{sid}b2)"/>
<path d="{d1}" stroke="url(#{sid}g)" stroke-width="3.5" fill="none"/>
<path d="{d2}" stroke="url(#{sid}g)" stroke-width="2.5" fill="none" opacity=".8"/>
<path d="{d2}" stroke="url(#{sid}g)" stroke-width="14" fill="none" filter="url(#{sid}b)" opacity=".5"/></svg>'''


def doodle_arrow(x, y, w, rot=0, flip=False):
    sx = -1 if flip else 1
    return (f'<svg class="doodle" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg) scaleX({sx})" '
            'viewBox="0 0 200 120" fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M10 20 C 40 95, 110 110, 175 80"/><path d="M150 62 L178 79 L152 100"/></svg>')


def slide(out, inner, cls=''):
    return f'<section class="slide {cls}" data-out="{out}">{inner}</section>'


def page(title, slides):
    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{title}</title>'
            f'<link rel="stylesheet" href="style.css"></head><body>{"".join(slides)}</body></html>')


BUST = 'img/jhony-bust-rim.png'
FACE = 'img/jhony-bust.png'


def avatar(size, x, y, z=12):
    scale = size * 2.8 / 753
    bw = 753 * scale
    fx, fy = 310 * scale, 330 * scale
    return (f'<div class="avatar abs" style="left:{x}px;top:{y}px;width:{size}px;height:{size}px;'
            f'background-image:url({FACE});background-size:{bw:.0f}px auto;'
            f'background-position:{size / 2 - fx:.0f}px {size / 2 - fy:.0f}px;z-index:{z}"></div>')


def header(n, total, eyebrow, title, width=950, extra=''):
    return (f'{top(n, total)}<div class="abs" style="left:64px;top:170px;width:{width}px;z-index:12">'
            f'<div class="eyebrow">{eyebrow}</div><h2 class="h2" style="margin-top:22px">{title}</h2>{extra}</div>')
