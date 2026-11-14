"""Design-only covers 1080x1920 for the Tuesday/Thursday Reels (no photo): the theme written large plus one graphic.
Key content stays inside the 4:5 feed crop (y 285-1635)."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
from lib import icon, glow, ring, tile
from capas import CSS, head, cover

EXTRA = """<style>
.lbl { position: absolute; font-family: "Jakarta"; font-weight: 800; font-size: 44px; letter-spacing: -.02em; text-align: center; width: 300px; }
.node { position: absolute; width: 56px; height: 56px; border-radius: 50%; background: #0B1117; border: 5px solid #4BBFEF; box-shadow: 0 0 26px rgba(75,191,239,.85); z-index: 9; }
.path { position: absolute; height: 6px; border-radius: 3px; z-index: 8; background: linear-gradient(90deg, rgba(75,191,239,.1), #4BBFEF 14%, #4BBFEF 86%, rgba(75,191,239,.1)); box-shadow: 0 0 20px rgba(75,191,239,.85); }
.dot { position: absolute; width: 92px; height: 92px; border-radius: 50%; z-index: 10; display: grid; place-items: center; color: #04121B;
  background: radial-gradient(circle, #E9F8FF, #4BBFEF 60%); box-shadow: 0 0 44px rgba(75,191,239,.95); }
.dot svg { width: 48px; height: 48px; }
.sale { position: absolute; z-index: 10; display: inline-flex; align-items: center; gap: 12px; padding: 16px 30px; border-radius: 999px; background: #25D366; color: #04121B;
  font-family: "Jakarta"; font-weight: 800; font-size: 40px; box-shadow: 0 0 40px rgba(37,211,102,.45); }
.row { position: absolute; left: 64px; right: 64px; height: 150px; z-index: 10; display: flex; align-items: center; gap: 26px; padding: 0 40px; border-radius: 30px;
  background: linear-gradient(160deg, rgba(110,210,250,.14), rgba(17,24,33,.88) 42%, rgba(9,14,19,.95)); border: 2px solid rgba(110,210,250,.4); box-shadow: 0 26px 50px rgba(0,0,0,.5); }
.row .old { font-family: "Jakarta"; font-weight: 700; font-size: 50px; color: #6B7682; text-decoration: line-through; text-decoration-color: #4BBFEF; text-decoration-thickness: 7px; white-space: nowrap; }
.row .arrow { width: 52px; height: 52px; color: #4BBFEF; flex: none; }
.row .new { font-family: "Jakarta"; font-weight: 800; font-size: 56px; color: #4BBFEF; letter-spacing: -.02em; white-space: nowrap; text-shadow: 0 0 30px rgba(75,191,239,.45); }
.row .brand { margin-left: auto; font-family: "Mono"; font-size: 24px; letter-spacing: .1em; color: #9AA5B1; text-transform: uppercase; }
.cv-title s { color: #6B7682; text-decoration-color: #4BBFEF; text-decoration-thickness: 14px; }
.sub2 { position: absolute; left: 64px; right: 64px; z-index: 20; font-family: "Jakarta"; font-weight: 800; font-size: 60px; letter-spacing: -.02em; }
.sub2 em { font-style: normal; color: #4BBFEF; text-shadow: 0 0 30px rgba(75,191,239,.45); }
.pcard { position: absolute; width: 200px; height: 262px; border-radius: 28px; z-index: 10;
  background: linear-gradient(160deg, rgba(110,210,250,.18), rgba(17,24,33,.92) 42%, rgba(9,14,19,.96)); border: 2px solid rgba(110,210,250,.5); box-shadow: 0 26px 50px rgba(0,0,0,.55), 0 0 30px rgba(75,191,239,.18); }
.pcard b { position: absolute; left: 18px; top: 14px; font-family: "Mono"; font-size: 24px; color: #4BBFEF; }
.pcard i { position: absolute; left: 55px; top: 62px; width: 90px; height: 90px; color: #E9F8FF; filter: drop-shadow(0 0 14px rgba(75,191,239,.9)); }
.pcard i svg { width: 100%; height: 100%; }
.pcard span { position: absolute; left: 6px; right: 6px; bottom: 26px; text-align: center; font-family: "Jakarta"; font-weight: 800; font-size: 25px; letter-spacing: -.02em; }
</style>"""

# R1 · acquisition channels
cats = [('search', 'Búsqueda'), ('share-2', 'Redes'), ('megaphone', 'Publicidad'), ('users-round', 'Terceros'), ('map-pin', 'Presencia'), ('radio', 'Medios')]
grid = ''
for i, (ic, lab) in enumerate(cats):
    cx, cy = (240, 540, 840)[i % 3], (1030, 1330)[i // 3]
    grid += tile(ic, cx - 85, cy - 85, 170, (-5, 3, -3, 4, -4, 5)[i], lab)
r1 = cover('cover-r1', head('REEL', '6 canales de adquisición', '¿Por dónde te llegan <em>tus clientes?</em>') + f"""
{glow(540, 1180, 520, .7)}{ring(540, 1180, 400, thin=True)}{grid}""")

# R2 · every channel needs a function
X = [200, 540, 880]
r2g = f'<div class="path" style="left:70px;width:940px;top:1257px"></div>'
for x, ic, lab in zip(X, ['magnet', 'handshake', 'shopping-cart'], ['Atraer', 'Acercar', 'Convertir']):
    r2g += tile(ic, x - 80, 1020, 160, 0)
    r2g += f'<div class="node" style="left:{x - 28}px;top:{1260 - 28}px"></div>'
    r2g += f'<div class="lbl" style="left:{x - 150}px;top:1320px">{lab}</div>'
r2g += f'<div class="dot" style="left:{370 - 46}px;top:{1260 - 46}px">{icon("user-round")}</div>'
r2g += f'<div class="sale" style="left:{880 - 120}px;top:1420px">Venta ✓</div>'
r2 = cover('cover-r2', head('REEL', 'Atraer · Acercar · Convertir', 'Cada canal necesita <em>una función</em>') + f"""
{glow(540, 1250, 520, .7)}{r2g}""")

# R3 · they buy what it does for them
rows = [('5 GB', '1.000 canciones', 'Apple'), ('Zapatillas', 'Superación', 'Nike'), ('Coches', 'Seguridad', 'Volvo')]
r3g = ''.join(f'<div class="row" style="top:{1010 + i * 180}px"><span class="old">{o}</span><i class="arrow">{icon("arrow-right")}</i>'
              f'<span class="new">{n}</span><span class="brand">{b}</span></div>' for i, (o, n, b) in enumerate(rows))
r3 = cover('cover-r3', head('REEL', 'Apple · Nike · Volvo', 'Tu cliente<br>no compra<br><s>lo que vendes</s>') + f"""
<div class="sub2" style="top:858px">Compra <em>lo que hace por él.</em></div>
{glow(540, 1250, 520, .6)}{r3g}""")

# R4 · how to position yourself
pil = [('shield-check', 'Seguridad'), ('award', 'Reconocimiento'), ('trending-up', 'Crecimiento'), ('feather', 'Tranquilidad'), ('sparkles', 'Belleza')]
r4g = ''
for k, (ic, name) in enumerate(pil):
    cx = 540 + (k - 2) * 188
    cy = 1250 + abs(k - 2) ** 2 * 14
    r4g += (f'<div class="pcard" style="left:{cx - 100}px;top:{cy - 131}px;transform:rotate({(k - 2) * 7}deg);z-index:{10 + (2 - abs(k - 2))}">'
            f'<b>0{k + 1}</b><i>{icon(ic)}</i><span style="font-size:{21 if len(name) > 12 else 25}px">{name}</span></div>')
r4 = cover('cover-r4', head('REEL', '5 ideas para posicionarte', '¿Cómo quieres que <em>te recuerden?</em>') + f"""
{glow(540, 1260, 520, .7)}{ring(540, 1260, 330, thin=True)}{r4g}""")

open('capas_reels.html', 'w', encoding='utf-8').write(
    '<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Capas Reels</title><link rel="stylesheet" href="style.css">'
    + CSS + EXTRA + '</head><body>' + r1 + r2 + r3 + r4 + '</body></html>')
print('capas_reels.html')
