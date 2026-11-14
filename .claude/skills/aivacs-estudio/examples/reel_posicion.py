"""Reel 4 · Cómo posicionarte: cinco ideas que una marca puede adueñarse.
A deck of five face-down cards; each pillar is dealt to the centre and turned over as it is named.
At "Elige la tuya" the five come back as tiles, one is picked, and it stamps every post."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
FOTOS = os.environ.get('AIVACS_FOTOS') or sys.exit('Defina AIVACS_FOTOS com a pasta das fotos recortadas do Jhony (o06chair.png, o11.png, o14.png, o17.png...)')
from vkit import Kit, icon, endcard, E

P = sys.argv[1]
K = Kit(P)
JH = K.image(os.path.join(FOTOS, 'o06chair.png'), 'jhony.png')
R = lambda t: round(t, 3)

CSS = """
.mono { font-family: 'JBMono'; font-weight: 700; letter-spacing: -.02em; }
.ln { position: absolute; left: 40px; right: 40px; text-align: center; }
.w { display: inline-block; margin: 0 .12em; opacity: 0; }
.back { position: absolute; width: 300px; height: 266px; border-radius: 30px; }
.front { position: absolute; left: 100px; top: 500px; width: 880px; height: 780px; border-radius: 52px; opacity: 0; }
.tile { position: absolute; width: 170px; height: 170px; border-radius: 34%; display: grid; place-items: center; opacity: 0; }
.ic svg { width: 100%; height: 100%; display: block; }
"""


class Scene:
    def __init__(self, sid, st):
        self.sid, self.st, self.h, self.j, self.n = sid, st, '', '', 0

    def L(self, t):
        return R(max(0, t - self.st))

    def land(self, el, t, dy=44, dur=0.42, ease=None, scale=None):
        b = f'y: {dy}' + (f', scale: {scale}' if scale else '')
        self.j += f'tl.set("#{el}", {{ {b} }}, 0);\n'
        self.j += f'tl.to("#{el}", {{ opacity: 1, duration: 0.08, ease: "none" }}, {self.L(t - 0.04)});\n'
        self.j += f'tl.to("#{el}", {{ y: 0{", scale: 1" if scale else ""}, duration: {dur}, ease: "{ease or E["softLand"]}" }}, {self.L(t - 0.04)});\n'

    def line(self, words, top, fs, cls='hx', color='#F0F4F8', lid=None, extra='', box='ln'):
        lid = lid or f'{self.sid}-l{self.n}'
        self.n += 1
        h = f'<div id="{lid}" class="{box} {cls}" style="top:{top}px;font-size:{fs}px;color:{color};{extra}">'
        for i, (w, t, cy) in enumerate(words):
            h += f'<span id="{lid}w{i}" class="w{" cy" if cy else ""}">{w}</span>'
            self.land(f'{lid}w{i}', t, dy=int(fs * 0.4))
        return lid, h + '</div>\n'


def spoken(sid, prefix, n, nth=0):
    ws = K.words(sid)
    hits = [i for i, w in enumerate(ws) if w[0].lower().strip('¿?¡!.,:').startswith(prefix)]
    i0 = hits[nth]
    return [ws[min(i0 + k, len(ws) - 1)][1] for k in range(n)]


def W(text, sid, prefix, cyan=(), nth=0):
    ts = spoken(sid, prefix, len(text.split()), nth)
    return [(w, t, w.strip('.,:') in cyan) for w, t in zip(text.split(), ts)]


def exit_up(sc, ids, t, dy=-1050):
    for k, el in enumerate(ids):
        sc.j += f'tl.to("#{el}", {{ y: "+={dy}", duration: 0.32, ease: "{E["accelExit"]}" }}, {sc.L(t + 0.025 * k)});\n'


PIL = [('shield-check', 'Seguridad', 'Transmitir confianza y constancia.', 'transmitir', ('confianza', 'constancia')),
       ('award', 'Reconocimiento', 'Ser la autoridad en un tema.', 'ser', ('autoridad',)),
       ('trending-up', 'Crecimiento', 'Que te asocien a evolución y resultados.', 'que', ('evolución', 'resultados')),
       ('feather', 'Tranquilidad', 'Ser quien simplifica las decisiones.', 'ser', ('simplifica',)),
       ('sparkles', 'Belleza y autoestima', 'Que te reconozcan por la transformación que provocas.', 'que', ('transformación',))]
PS = [K.start(f's{k + 2}') for k in range(5)]
T7 = K.start('s7')
t_mark = K.at('s7', 'aivacs') - 0.25
est = t_mark - 0.35

# ---------- hook: the question, then "own one idea" with the deck fanning in ----------
h = Scene('hk', 0)
q = [h.line(W('¿Cómo quieres', 's1', 'cómo'), 600, 112, lid='hk-a'),
     h.line(W('que te recuerden', 's1', 'que', cyan=('recuerden',)), 730, 112, lid='hk-b'),
     h.line(W('en tu sector?', 's1', 'en'), 860, 112, lid='hk-c')]
for _, x in q:
    h.h += x
h.j = h.j.replace('tl.set("#hk-aw0", { y: 44 }, 0);', 'tl.set("#hk-aw0", { opacity: 1 }, 0);', 1)
t_las = K.at('s1', 'las')
for k, (el, _) in enumerate(q):
    h.j += f'tl.to("#{el}", {{ y: -1000, duration: 0.3, ease: "{E["crashOut"]}" }}, {h.L(t_las - 0.2 + 0.02 * k)});\n'
a = [h.line([(w, max(t, t_las + 0.12), c) for w, t, c in W('Las marcas fuertes', 's1', 'las')], 430, 100, lid='hk-d'),
     h.line(W('se adueñan de', 's1', 'se'), 545, 100, lid='hk-e'),
     h.line(W('una idea.', 's1', 'una', cyan=('una', 'idea')), 660, 156, lid='hk-f')]
for _, x in a:
    h.h += x
K.fx('whoosh', t_las - 0.2)
exit_up(h, [i for i, _ in a], PS[0] - 0.5)
K.add_scene('hk', 0, PS[0] + 0.1, CSS, h.h, h.j)

# ---------- the deck ----------
d = Scene('dk', K.at('s1', 'adueñan') - 0.3)
FX = [-300, -150, 0, 150, 300]
FR = [-16, -8, 0, 8, 16]
FY = [44, 11, 0, 11, 44]
BASE_TOP, BASE_LEFT = 1330 - 133, 540 - 150
CARD_CY = 500 + 390
t_fan = K.at('s1', 'adueñan')
for k in range(5):
    d.h += (f'<div id="b{k}" class="back glass" style="left:{BASE_LEFT}px;top:{BASE_TOP}px;z-index:{k + 1};opacity:0">'
            f'<div class="mono cy" style="position:absolute;left:26px;top:18px;font-size:58px">0{k + 1}</div>'
            f'<div style="position:absolute;left:26px;bottom:24px;width:44px;height:6px;border-radius:3px;background:rgba(75,191,239,.6)"></div></div>\n')
    d.j += f'tl.set("#b{k}", {{ x: 0, y: 420, rotation: 0, scale: .9 }}, 0);\n'
    d.j += f'tl.to("#b{k}", {{ opacity: 1, duration: 0.08, ease: "none" }}, {d.L(t_fan + 0.07 * k)});\n'
    d.j += f'tl.to("#b{k}", {{ x: {FX[k]}, y: {FY[k]}, rotation: {FR[k]}, scale: 1, duration: 0.55, ease: "{E["softLand"]}" }}, {d.L(t_fan + 0.07 * k)});\n'
K.fx('whoosh', t_fan - 0.05)
prev = None
for k, (ic, title, desc, kw, cy) in enumerate(PIL):
    t_go = PS[k] - 0.3
    sid = f's{k + 2}'
    if k == 0:   # the rest of the deck drops to peek at the bottom
        for m in range(1, 5):
            d.j += f'tl.to("#b{m}", {{ y: {FY[m] + 330}, opacity: .55, duration: 0.45, ease: "{E["softInOut"]}" }}, {d.L(t_go)});\n'
    if prev is not None:
        d.j += f'tl.to("#{prev}", {{ x: -1150, rotation: -12, duration: 0.36, ease: "{E["accelExit"]}" }}, {d.L(t_go)});\n'
    d.j += f'tl.set("#b{k}", {{ zIndex: 20 }}, {d.L(t_go)});\n'
    d.j += f'tl.to("#b{k}", {{ x: 0, y: {CARD_CY - 1330}, rotation: 0, scale: 2.93, opacity: 1, duration: 0.34, ease: "power3.inOut" }}, {d.L(t_go)});\n'
    d.j += f'tl.to("#b{k}", {{ scaleX: 0, duration: 0.1, ease: "{E["gentleIn"]}" }}, {d.L(t_go + 0.34)});\n'
    d.j += f'tl.set("#b{k}", {{ visibility: "hidden" }}, {d.L(t_go + 0.45)});\n'
    K.fx('whoosh', t_go - 0.03)
    fid = f'f{k}'
    two = False
    t_title = K.at(sid, title.split()[0].lower())
    # front face
    _, dline = d.line(W(desc, sid, kw, cyan=cy, nth=0 if k != 2 else 0), 0, 56, cls='', color='#C9D4DD', lid=f'{fid}d',
                      extra=f"font-family:'Jakarta';font-weight:700;line-height:1.22;text-wrap:balance;top:{560 if two else 520}px;left:70px;right:70px", box='ln')
    d.h += (f'<div id="{fid}" class="front glass" style="z-index:30">'
            f'<div class="mono" style="position:absolute;left:58px;top:50px;font-size:44px;color:#4BBFEF">0{k + 1}<span style="color:#8796A3"> / 05</span></div>'
            f'<div style="position:absolute;left:340px;top:120px;width:200px;height:200px;border-radius:34%;display:grid;place-items:center;background:radial-gradient(circle at 50% 40%,rgba(75,191,239,.28),rgba(75,191,239,.04) 70%);border:2px solid rgba(110,210,250,.5)">'
            f'<i class="ic" style="width:116px;height:116px;color:#E9F8FF;filter:drop-shadow(0 0 16px rgba(75,191,239,.95))">{icon(ic)}</i></div>'
            f'<div class="hx" style="position:absolute;left:40px;right:40px;top:370px;text-align:center;font-size:{78 if len(title) > 15 else 88}px;line-height:1.02;text-wrap:balance">{title}</div>'
            f'<div style="position:absolute;left:380px;top:{(560 if two else 520) - 38}px;width:120px;height:8px;border-radius:4px;background:#4BBFEF;box-shadow:0 0 18px rgba(75,191,239,.8)"></div>'
            f'{dline}</div>\n')
    t_flip = t_go + 0.44
    d.j += f'tl.set("#{fid}", {{ scaleX: 0, scaleY: 1, x: 0, rotation: 0 }}, 0);\n'
    d.j += f'tl.set("#{fid}", {{ opacity: 1 }}, {d.L(t_flip)});\n'
    d.j += f'tl.to("#{fid}", {{ scaleX: 1, duration: 0.24, ease: "{E["softLand"]}" }}, {d.L(t_flip)});\n'
    K.fx('pop', t_flip)
    nxt = PS[k + 1] - 0.3 if k < 4 else T7 - 0.3
    d.j += f'tl.to("#{fid}", {{ rotation: {1.2 if k % 2 else -1.2}, y: -14, duration: {R(nxt - t_flip - 0.3)}, ease: "none" }}, {d.L(t_flip + 0.28)});\n'
    prev = fid
d.j += f'tl.to("#{prev}", {{ x: -1150, rotation: -12, duration: 0.36, ease: "{E["accelExit"]}" }}, {d.L(T7 - 0.3)});\n'
K.add_scene('dk', d.st, T7 + 0.2, CSS, d.h, d.j)

# ---------- pick one, then it stamps every post ----------
pk = Scene('pk', T7 - 0.35)
PICK = 2
lid, x = pk.line(W('Elige la tuya', 's7', 'elige', cyan=('tuya',)), 470, 120, lid='pk-h')
pk.h += x
for k, (ic, *_rest) in enumerate(PIL):
    left = 79 + k * 188
    pk.h += (f'<div id="pt{k}" class="tile glass" style="left:{left}px;top:700px;z-index:{10 if k == PICK else 2}">'
             f'<i class="ic" style="width:90px;height:90px;color:#E9F8FF;filter:drop-shadow(0 0 12px rgba(75,191,239,.8))">{icon(ic)}</i></div>\n')
    pk.land(f'pt{k}', T7 + 0.05 * k, dy=70, scale=.85)
t_tuya = K.at('s7', 'tuya')
pk.h += f'<div id="pk-cur" class="ic" style="position:absolute;left:560px;top:780px;width:120px;height:120px;color:#fff;filter:drop-shadow(0 6px 14px rgba(0,0,0,.6));opacity:0;z-index:40">{icon("mouse-pointer-click")}</div>\n'
pk.j += f'tl.set("#pk-cur", {{ x: 300, y: 520 }}, 0);\n'
pk.j += f'tl.to("#pk-cur", {{ opacity: 1, duration: 0.1, ease: "none" }}, {pk.L(t_tuya - 0.55)});\n'
pk.j += f'tl.to("#pk-cur", {{ x: 0, y: 0, duration: 0.5, ease: "{E["softInOut"]}" }}, {pk.L(t_tuya - 0.55)});\n'
pk.j += f'tl.to("#pk-cur", {{ scale: .82, duration: 0.09, ease: "power2.out", yoyo: true, repeat: 1 }}, {pk.L(t_tuya - 0.05)});\n'
pk.j += f'tl.to("#pt{PICK}", {{ scale: 1.22, borderColor: "#4BBFEF", boxShadow: "0 0 60px rgba(75,191,239,.65)", duration: 0.35, ease: "{E["popOver"]}" }}, {pk.L(t_tuya)});\n'
for k in range(5):
    if k != PICK:
        pk.j += f'tl.to("#pt{k}", {{ opacity: .3, duration: 0.25, ease: "none" }}, {pk.L(t_tuya + 0.05)});\n'
K.fx('click', t_tuya - 0.05)
t_todo = K.at('s7', 'todo')
t_out = t_todo - 0.22
pk.j += f'tl.to("#pk-cur", {{ x: 260, y: 600, opacity: 0, duration: 0.3, ease: "{E["accelExit"]}" }}, {pk.L(t_out)});\n'
exit_up(pk, ['pk-h'], t_out)
for k in range(5):
    if k != PICK:
        pk.j += f'tl.to("#pt{k}", {{ y: 260, opacity: 0, duration: 0.3, ease: "{E["accelExit"]}" }}, {pk.L(t_out + 0.02 * k)});\n'
pk.j += f'tl.to("#pt{PICK}", {{ y: -250, scale: 1.1, duration: 0.45, ease: "{E["softInOut"]}" }}, {pk.L(t_out)});\n'
# three posts, each stamped with the chosen idea
pic = PIL[PICK][0]
pts = spoken('s7', 'todo', 4)
post_t = [pts[0], pts[2], pts[3]]
for i in range(3):
    left = 105 + i * 300
    pk.h += (f'<div id="po{i}" class="glass" style="position:absolute;left:{left}px;top:800px;width:270px;height:338px;border-radius:26px;opacity:0">'
             f'<div id="po{i}i" class="ic" style="position:absolute;left:80px;top:62px;width:110px;height:110px;color:#4BBFEF;filter:drop-shadow(0 0 16px rgba(75,191,239,.9));opacity:0">{icon(pic)}</div>'
             f'<div style="position:absolute;left:34px;right:34px;top:222px;height:16px;border-radius:8px;background:rgba(201,212,221,.35)"></div>'
             f'<div style="position:absolute;left:34px;right:96px;top:256px;height:16px;border-radius:8px;background:rgba(201,212,221,.2)"></div></div>\n')
    pk.land(f'po{i}', post_t[i], dy=80, scale=.9)
    pk.j += f'tl.set("#po{i}i", {{ scale: 1.8 }}, 0);\n'
    pk.j += f'tl.to("#po{i}i", {{ opacity: 1, duration: 0.06, ease: "none" }}, {pk.L(post_t[i] + 0.18)});\n'
    pk.j += f'tl.to("#po{i}i", {{ scale: 1, duration: 0.35, ease: "{E["snapSettle"]}" }}, {pk.L(post_t[i] + 0.18)});\n'
    K.fx('click', post_t[i] + 0.15)
l1, x1 = pk.line(W('Que todo lo que publiques', 's7', 'que'), 1210, 64, lid='pk-l1')
l2, x2 = pk.line(W('la repita.', 's7', 'la', cyan=('repita',), nth=1), 1292, 64, lid='pk-l2')
pk.h += x1 + x2
exit_up(pk, ['pt2', 'po0', 'po1', 'po2', 'pk-l1', 'pk-l2'], est + 0.05)
K.add_scene('pk', T7 - 0.35, est + 0.42, CSS, pk.h, pk.j)

# ---------- end card ----------
css, html, js = endcard(K, 'e', est, t_mark, JH, 215, 1000, 650, 'Te ayudamos a construirla', '+34 603 82 96 57')
K.add_scene('e', est, K.total, css, html, js)

K.captions(set(), skip=set(K.ids))
K.write_index(bgm_volume=0.2, bgm_media_start=0)
print('total', K.total, 'mark', t_mark)
