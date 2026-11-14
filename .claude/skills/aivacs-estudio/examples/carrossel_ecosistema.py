"""Post 1 · No hacemos solo webs (ecosistema digital)."""
import math
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
from lib import *  # noqa: F403

T = 7
BUST = 'img/jhony-bust-rim.png'
FACE = 'img/jhony-bust.png'


def avatar(size, x, y):
    # face centre in jhony-bust.png is about (310, 330) on a 753 px wide image
    scale = size * 2.8 / 753
    bw = 753 * scale
    fx, fy = 310 * scale, 330 * scale
    return (f'<div class="avatar abs" style="left:{x}px;top:{y}px;width:{size}px;height:{size}px;'
            f'background-image:url({FACE});background-size:{bw:.0f}px auto;'
            f'background-position:{size / 2 - fx:.0f}px {size / 2 - fy:.0f}px;z-index:12"></div>')


cover = slide('p1-01', f'''
{top(1, T)}
{glow(670, 760, 440)}{ring(670, 720, 330)}{ring(670, 720, 420, thin=True)}
<div class="abs" style="left:64px;top:150px;z-index:12"><span class="tape">Soluciones digitales</span></div>
<div class="abs" style="left:60px;top:232px;width:960px;z-index:5">
  <div class="hx wt" data-fit style="font-size:150px;white-space:nowrap">No hacemos</div>
  <div class="hx cy" data-fit style="font-size:196px;white-space:nowrap;margin-top:6px">solo webs.</div>
</div>
<p class="sub abs" style="left:64px;top:560px;width:410px;z-index:12">Construimos el <b>ecosistema digital</b> que hace crecer tu empresa.</p>
{person('img/o05.png', 282, 474, 815)}
<div class="fade-bottom" style="height:150px"></div>
{tile('globe', 56, 820, 124, -10)}{tile('clapperboard', 200, 930, 108, 8)}{tile('megaphone', 70, 1040, 116, 6)}
{tile('si:whatsapp', 894, 560, 116, 10)}{tile('layout-dashboard', 930, 770, 104, -9)}{tile('shopping-cart', 902, 975, 100, 7)}
{streak('M -60 1290 C 300 1360, 700 1190, 1140 1235', 'M -60 1320 C 330 1380, 720 1230, 1140 1280', 'c1')}
{chip('<b>+2.000</b> proyectos desde 2018', 'circle-check', 64, 1172)}
{bot()}''')

# 2 · el problema
off = [('globe', 96, 640, 'Web · agencia A'), ('si:instagram', 700, 610, 'Redes · freelance'),
       ('megaphone', 420, 810, 'Anuncios · agencia B'), ('si:whatsapp', 120, 975, 'WhatsApp · a mano'),
       ('layers', 720, 950, 'Hojas de cálculo')]
off_tiles = ''.join(tile(n, x, y, 128, r, lab, '') .replace('class="tile', 'class="tile off')
                    for (n, x, y, lab), r in zip(off, [-6, 7, -4, 5, -8]))
centers = [(x + 64, y + 64) for _, x, y, _ in off]
pairs = [(0, 2), (2, 1), (0, 3), (2, 4), (3, 4), (1, 4)]
lines = ''
for a, b in pairs:
    (x1, y1), (x2, y2) = centers[a], centers[b]
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    lines += (f'<line x1="{x1}" y1="{y1}" x2="{mx - (mx - x1) * .18:.0f}" y2="{my - (my - y1) * .18:.0f}"/>'
              f'<line x1="{mx + (x2 - mx) * .18:.0f}" y1="{my + (y2 - my) * .18:.0f}" x2="{x2}" y2="{y2}"/>'
              f'<text x="{mx}" y="{my + 12}" text-anchor="middle">×</text>')
s2 = slide('p1-02', f'''
{top(2, T)}
<div class="abs" style="left:64px;top:170px;width:950px">
  <div class="eyebrow">El problema</div>
  <h2 class="h2" style="margin-top:22px">Una web por aquí, anuncios por allá… <em>y nada habla con nada.</em></h2>
</div>
<svg class="abs" style="left:0;top:0;width:1080px;height:1350px;z-index:3" viewBox="0 0 1080 1350"
  stroke="#56616C" stroke-width="3" stroke-dasharray="10 12" fill="#8A949E" font-family="Mono" font-size="40">{lines}</svg>
{off_tiles}
<p class="body abs" style="left:64px;top:1180px;width:950px;font-size:34px">Cada proveedor hace su parte. <b>Nadie mira el conjunto.</b></p>
{bot()}''', 'calm')

# 3 · qué es un ecosistema
hub = (540, 820)
nodes = [('globe', 'Web y tienda'), ('clapperboard', 'Contenido y vídeo'), ('megaphone', 'Tráfico pago'),
         ('si:whatsapp', 'WhatsApp y\nautomatización'), ('layout-dashboard', 'Sistemas de\ngestión')]
R = 290
pos = []
for i in range(5):
    ang = math.radians(-90 + i * 72)
    pos.append((hub[0] + R * math.cos(ang), hub[1] + R * math.sin(ang)))
spokes = ''.join(f'<line x1="{hub[0]}" y1="{hub[1]}" x2="{x:.0f}" y2="{y:.0f}"/>' for x, y in pos)
ring_path = ''.join(f'<line x1="{pos[i][0]:.0f}" y1="{pos[i][1]:.0f}" x2="{pos[(i + 1) % 5][0]:.0f}" y2="{pos[(i + 1) % 5][1]:.0f}"/>' for i in range(5))
node_html = ''
for (n, lab), (x, y) in zip(nodes, pos):
    node_html += tile(n, x - 66, y - 66, 132, 0)
    if y < hub[1] - 200:
        lx, ly, al = x + 84, y - 18, 'left'
    else:
        lx, ly, al = x - 160, y + 82, 'center'
    node_html += (f'<div class="abs" style="left:{lx:.0f}px;top:{ly:.0f}px;width:320px;text-align:{al};z-index:10;'
                  f'font-family:Jakarta;font-weight:800;font-size:28px;line-height:1.15;white-space:pre-line">{lab}</div>')
s3 = slide('p1-03', f'''
{top(3, T)}
<div class="abs" style="left:64px;top:170px;width:950px">
  <div class="eyebrow">La solución</div>
  <h2 class="h2" style="margin-top:22px">Un ecosistema digital <em>es esto:</em></h2>
  <p class="body" style="margin-top:18px;font-size:32px"><b>Cinco piezas, un solo equipo.</b> Todo conectado.</p>
</div>
{glow(hub[0], hub[1], 300, .8)}
<svg class="abs" style="left:0;top:0;width:1080px;height:1350px;z-index:4" viewBox="0 0 1080 1350" fill="none">
  <defs><filter id="lg"><feGaussianBlur stdDeviation="6"/></filter></defs>
  <g stroke="#4BBFEF" stroke-width="10" opacity=".35" filter="url(#lg)">{spokes}</g>
  <g stroke="#7FD3F5" stroke-width="3">{spokes}</g>
  <g stroke="#4BBFEF" stroke-width="2" stroke-dasharray="4 10" opacity=".55">{ring_path}</g>
</svg>
<div class="abs glass" style="left:{hub[0] - 110}px;top:{hub[1] - 110}px;width:220px;height:220px;border-radius:50%;display:grid;place-items:center;z-index:9;border:3px solid rgba(110,210,250,.8);box-shadow:0 0 80px rgba(75,191,239,.6),inset 0 0 50px rgba(75,191,239,.3)">
  <div style="width:110px;filter:drop-shadow(0 0 16px rgba(75,191,239,.9))">{LOGO}</div></div>
{node_html}
{bot()}''', 'calm')

# 4 · cada pieza empuja a la siguiente
steps = [('megaphone', 'Anuncios', 'Atraen a quien ya te está buscando.'),
         ('globe', 'Web o tienda online', 'Convence y convierte la visita en contacto.'),
         ('si:whatsapp', 'WhatsApp automático', 'Responde en segundos, también a las 23:00.'),
         ('layout-dashboard', 'Sistema de gestión', 'Presupuestos, pedidos y facturas en orden.'),
         ('clapperboard', 'Contenido y vídeo', 'Te mantiene presente para que vuelvan.')]
rows = ''.join(f'''<div class="glass row" style="height:142px">{tile(n, 0, 0, 98, 0).replace('class="tile', 'class="tile static')}
  <div><span class="n">PASO {i + 1:02d}</span><h4>{t}</h4><p>{d}</p></div></div>''' for i, (n, t, d) in enumerate(steps))
s4 = slide('p1-04', f'''
{top(4, T)}
<div class="abs" style="left:64px;top:170px;width:950px">
  <div class="eyebrow">Cómo funciona</div>
  <h2 class="h2" style="margin-top:22px">Cada pieza <em>empuja a la siguiente.</em></h2>
</div>
<div class="abs" style="left:113px;top:470px;width:4px;height:640px;background:linear-gradient(#4BBFEF,#2A8BBF);box-shadow:0 0 18px #4BBFEF;z-index:1"></div>
<div class="abs" style="left:64px;top:400px;width:952px;display:flex;flex-direction:column;gap:16px;z-index:5">{rows}</div>
{bot()}''', 'calm')

# 5 · qué consigues
outs = [('trending-up', 'Ventas', 'Más contactos que se convierten en clientes.'),
        ('users', 'Alcance', 'Que te encuentre la gente que te busca.'),
        ('heart-handshake', 'Engagement', 'Una comunidad que interactúa y confía.'),
        ('star', 'Posicionamiento', 'Una marca profesional que se recuerda.'),
        ('rocket', 'Crecimiento', 'Procesos que aguantan cuando creces.')]
orows = ''.join(f'''<div style="display:flex;align-items:center;gap:34px;padding:22px 0;border-bottom:1.5px solid rgba(75,191,239,.16)">
  {tile(n, 0, 0, 104, 0).replace('class="tile', 'class="tile static')}
  <div><div class="hx cy" style="font-size:60px;letter-spacing:-.03em">{t}</div><p class="body" style="font-size:30px;margin-top:8px">{d}</p></div></div>''' for n, t, d in outs)
s5 = slide('p1-05', f'''
{top(5, T)}
<div class="abs" style="left:64px;top:170px;width:950px">
  <div class="eyebrow">El resultado</div>
  <h2 class="h2" style="margin-top:22px">¿Qué consigue <em>tu empresa?</em></h2>
</div>
<div class="abs" style="left:64px;top:390px;width:952px;z-index:5">{orows}</div>
{bot()}''')

# 6 · prueba + Jhony
s6 = slide('p1-06', f'''
{top(6, T)}
{glow(780, 820, 400)}{ring(760, 800, 300)}
<div class="abs" style="left:64px;top:170px;width:700px;z-index:12">
  <div class="eyebrow">Quién lo construye</div>
  <h2 class="h2" style="margin-top:22px;font-size:68px">Detrás de cada ecosistema, <em>una persona.</em></h2>
</div>
{person('img/o16.png', 434, 454, 673)}
<div class="fade-bottom"></div>
<div class="abs" style="left:64px;top:520px;display:flex;flex-direction:column;gap:44px;z-index:12">
  <div class="stat"><b class="cy">+2.000</b><span>proyectos realizados</span></div>
  <div class="stat"><b class="cy">+50</b><span>clientes atendidos</span></div>
  <div class="stat"><b class="cy">2018</b><span>en el digital desde</span></div>
</div>
{streak('M -60 1215 C 300 1300, 700 1060, 1140 1100', 'M -60 1250 C 330 1330, 720 1100, 1140 1150', 'c6')}
{chip('Y hablas siempre con <b>quien lo construye.</b>', 'message-circle', 64, 1150)}
{bot()}''')

# 7 · CTA
s7 = slide('p1-07', f'''
{top(7, T)}
{glow(540, 760, 460, .9)}
<div class="abs" style="left:64px;top:190px;width:952px;text-align:center;z-index:5">
  <div class="eyebrow">Diagnóstico gratis</div>
  <h2 class="h2" style="margin-top:24px;font-size:84px">¿Tu negocio tiene <em>piezas sueltas?</em></h2>
  <p class="body" style="margin:30px auto 0;max-width:820px">Te reviso tu web, tus redes, tus anuncios y tu WhatsApp, y te digo <b>por dónde empezar.</b></p>
</div>
<div class="abs glass" style="left:110px;top:720px;width:860px;padding:54px 40px 50px;text-align:center;z-index:6">
  <p class="sub" style="font-size:40px">Escríbenos</p>
  <div style="margin:22px 0 26px"><span class="kw">ECOSISTEMA</span></div>
  <p class="sub" style="font-size:36px;color:var(--tx2)">por WhatsApp y te hago el diagnóstico.</p>
</div>
<div class="abs" style="left:0;right:0;top:1130px;display:flex;justify-content:center;z-index:6">
  <div style="display:inline-flex;align-items:center;gap:18px;padding:20px 40px;border-radius:999px;background:#25D366;color:#04121B;font-family:Jakarta;font-weight:800;font-size:40px;box-shadow:0 0 50px rgba(37,211,102,.35)">
  <span style="width:46px;height:46px">{icon('si:whatsapp')}</span>+34 603 82 96 57</div></div>
{bot(last=True)}''')

open('p1.html', 'w', encoding='utf-8').write(page('Post 1', [cover, s2, s3, s4, s5, s6, s7]))
print('p1.html')
