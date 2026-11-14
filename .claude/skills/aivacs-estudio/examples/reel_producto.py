"""Reel 3 · El cliente no compra lo que vendes: compra lo que hace por él.
A typographic essay: each brand's product is struck through by a cyan stroke and the benefit lands in its place.
Brands appear as plain text only (no logos); facts are the narrated ones."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
FOTOS = os.environ.get('AIVACS_FOTOS') or sys.exit('Defina AIVACS_FOTOS com a pasta das fotos recortadas do Jhony (o06chair.png, o11.png, o14.png, o17.png...)')
from vkit import Kit, icon, endcard, E

P = sys.argv[1]
K = Kit(P)
JH = K.image(os.path.join(FOTOS, 'o14.png'), 'jhony.png')
R = lambda t: round(t, 3)
GREY = '#9FB0BE'

CSS = """
.lab { position: absolute; left: 0; right: 0; text-align: center; font: 600 50px 'DMSans'; color: #9FB0BE; }
.mono { font-family: 'JBMono'; font-weight: 700; letter-spacing: -.02em; }
.card { position: absolute; left: 0; right: 0; display: flex; justify-content: center; }
.card .glass { position: relative; display: inline-flex; align-items: center; gap: 30px; height: 190px; padding: 0 56px; font: 800 84px 'Jakarta'; letter-spacing: -.03em; color: #fff; white-space: nowrap; }
.card .ic { width: 96px; height: 96px; color: #BDEBFF; filter: drop-shadow(0 0 14px rgba(75,191,239,.7)); }
.strike { position: absolute; left: 34px; right: 34px; top: 50%; height: 14px; margin-top: -7px; border-radius: 7px; background: #4BBFEF; box-shadow: 0 0 26px rgba(75,191,239,.9); }
.ln { position: absolute; left: 40px; right: 40px; text-align: center; }
.w { display: inline-block; margin: 0 .12em; opacity: 0; }
.bgi { position: absolute; left: 130px; top: 560px; width: 820px; height: 820px; color: #4BBFEF; opacity: 0; }
"""


class Scene:
    """Collects html/js for one scene; every time passed in is absolute."""

    def __init__(self, sid, st):
        self.sid, self.st, self.h, self.j, self.n = sid, st, '', '', 0

    def L(self, t):
        return R(max(0, t - self.st))

    def land(self, el, t, dy=44, dur=0.42, ease=None, scale=None):
        b = f'y: {dy}' + (f', scale: {scale}' if scale else '')
        self.j += f'tl.set("#{el}", {{ {b} }}, 0);\n'
        self.j += f'tl.to("#{el}", {{ opacity: 1, duration: 0.08, ease: "none" }}, {self.L(t - 0.04)});\n'
        self.j += f'tl.to("#{el}", {{ y: 0{", scale: 1" if scale else ""}, duration: {dur}, ease: "{ease or E["softLand"]}" }}, {self.L(t - 0.04)});\n'

    def line(self, words, top, fs, cls='hx', color='#F0F4F8', lid=None, extra=''):
        """words: [(text, t, cyan?)] -> one centred line, each word lands at its spoken time."""
        lid = lid or f'{self.sid}-l{self.n}'
        self.n += 1
        h = f'<div id="{lid}" class="ln {cls}" style="top:{top}px;font-size:{fs}px;color:{color};{extra}">'
        for i, (w, t, cy) in enumerate(words):
            h += f'<span id="{lid}w{i}" class="w{" cy" if cy else ""}">{w}</span>'
            self.land(f'{lid}w{i}', t, dy=int(fs * 0.4))
        self.h += h + '</div>\n'
        return lid


def spoken(sid, prefix, n, nth=0):
    ws = K.words(sid)
    hits = [i for i, w in enumerate(ws) if w[0].lower().strip('¿?¡!.,:').startswith(prefix)]
    i0 = hits[nth]
    return [ws[min(i0 + k, len(ws) - 1)][1] for k in range(n)]


def W(text, sid, prefix, cyan=(), nth=0):
    ts = spoken(sid, prefix, len(text.split()), nth)
    return [(w, t, w in cyan) for w, t in zip(text.split(), ts)]


def exit_all(sc, ids, t, dy=-620):
    for k, el in enumerate(ids):
        sc.j += f'tl.to("#{el}", {{ y: "+={dy}", duration: 0.32, ease: "{E["accelExit"]}" }}, {sc.L(t + 0.025 * k)});\n'
    K.fx('whoosh', t + 0.05)


# ---------- hook ----------
T2 = K.start('s2')
h = Scene('hk', 0)
h.line(W('Tu cliente', 's1', 'tu'), 560, 112, lid='hk-a')
h.line(W('no compra', 's1', 'no'), 690, 112, lid='hk-b')
# the struck line
tsv = spoken('s1', 'lo', 3)
h.h += ('<div id="hk-c" class="ln hx" style="top:820px;font-size:132px"><span id="hk-cs" style="position:relative;display:inline-block;padding:0 .1em">'
        + ''.join(f'<span id="hk-cw{i}" class="w">{w}</span>' for i, w in enumerate(['lo', 'que', 'vendes.']))
        + '<span id="hk-x" class="strike" style="left:-6px;right:-6px;height:16px;margin-top:-4px"></span></span></div>\n')
for i, t in enumerate(tsv):
    h.land(f'hk-cw{i}', t, dy=52)
t_cmp = K.at('s1', 'compra', nth=1)
h.j += f'tl.set("#hk-x", {{ scaleX: 0, rotation: -3, transformOrigin: "0% 50%" }}, 0);\n'
h.j += f'tl.to("#hk-x", {{ scaleX: 1, duration: 0.28, ease: "{E["softLand"]}" }}, {h.L(t_cmp - 0.16)});\n'
h.j += f'tl.to("#hk-cs", {{ opacity: .4, scale: .94, duration: 0.3, ease: "{E["softLand"]}" }}, {h.L(t_cmp + 0.1)});\n'
K.fx('whoosh', t_cmp - 0.2)
h.line(W('Compra lo que', 's1', 'compra', nth=1), 1060, 112, lid='hk-d')
h.line(W('hace por él.', 's1', 'hace', cyan=('hace', 'por', 'él.')), 1190, 156, lid='hk-e')
K.fx('pop', K.at('s1', 'hace') - 0.04)
# first word on screen from frame 0
h.j = h.j.replace('tl.set("#hk-aw0", { y: 44 }, 0);', 'tl.set("#hk-aw0", { opacity: 1 }, 0);', 1)
exit_all(h, ['hk-a', 'hk-b', 'hk-c', 'hk-d', 'hk-e'], T2 - 0.25)
K.add_scene('hk', 0, T2 + 0.15, CSS, h.h, h.j)


# ---------- brand sections ----------
def section(code, sid, st, en, brand, t_brand, neg, card_ic, card_txt, t_card, strike_kw, pos, ben, ben_fs, bg_ic,
            label=None, brand_cy=False, card_fs=84, reflow_at=None):
    sc = Scene(code, st)
    ids = []
    if label:
        sc.h += f'<div id="{code}-lb" class="ln" style="top:392px;opacity:0"><span class="glass mono cy" style="display:inline-block;padding:10px 30px;border-radius:999px;font-size:52px">{label[0]}</span></div>\n'
        sc.land(f'{code}-lb', label[1], dy=30)
        ids.append(f'{code}-lb')
    ids.append(sc.line(brand, 500 if label else 470, 128, color='#4BBFEF' if brand_cy else '#F0F4F8', lid=f'{code}-br'))
    ids.append(sc.line(neg, 690, 50, cls='', color=GREY, lid=f'{code}-ng', extra="font-family:'DMSans';font-weight:600"))
    sc.h += (f'<div id="{code}-cd" class="card" style="top:765px;opacity:0"><div id="{code}-cg" class="glass" style="font-size:{card_fs}px"><i class="ic">{icon(card_ic)}</i>{card_txt}'
             f'<span id="{code}-x" class="strike"></span></div></div>\n')
    sc.land(f'{code}-cd', t_card, dy=60, scale=.92)
    K.fx('click', t_card - 0.04)
    t_x = strike_kw - 0.14
    sc.j += f'tl.set("#{code}-x", {{ scaleX: 0, rotation: -3, transformOrigin: "0% 50%" }}, 0);\n'
    sc.j += f'tl.to("#{code}-x", {{ scaleX: 1, duration: 0.28, ease: "{E["softLand"]}" }}, {sc.L(t_x)});\n'
    sc.j += f'tl.to("#{code}-cg", {{ opacity: .4, scale: .94, duration: 0.3, ease: "{E["softLand"]}" }}, {sc.L(t_x + 0.26)});\n'
    K.fx('whoosh', t_x - 0.05)
    ids.append(f'{code}-cd')
    ids.append(sc.line(pos, 1012, 50, cls='', color=GREY, lid=f'{code}-ps', extra="font-family:'DMSans';font-weight:600"))
    bl = []
    for k, ln in enumerate(ben):
        bl.append(sc.line(ln, 1090 + k * int(ben_fs * 1.06), ben_fs, lid=f'{code}-b{k}', color='#4BBFEF', extra='text-shadow:0 0 40px rgba(75,191,239,.45)'))
    K.fx('pop', ben[0][0][1] - 0.04)
    sc.h = f'<div id="{code}-bg" class="bgi ic">{icon(bg_ic)}</div>\n' + sc.h
    t_bg = ben[0][0][1]
    sc.j += f'tl.set("#{code}-bg", {{ scale: 1.25, rotation: -10 }}, 0);\ntl.to("#{code}-bg", {{ opacity: .06, duration: 0.3, ease: "none" }}, {sc.L(t_bg)});\n'
    sc.j += f'tl.to("#{code}-bg", {{ scale: 1, rotation: 6, duration: {R(en - t_bg)}, ease: "none" }}, {sc.L(t_bg)});\n'
    if reflow_at:
        for k, el in enumerate(ids):
            sc.j += f'tl.to("#{el}", {{ y: -300, opacity: 0, duration: 0.3, ease: "{E["accelExit"]}" }}, {sc.L(reflow_at + 0.02 * k)});\n'
        dy = 400 - 1090
        for k, el in enumerate(bl):
            sc.j += f'tl.to("#{el}", {{ y: {dy - k * int(ben_fs * 1.06) * 0.28:.0f}, scale: .72, duration: 0.6, ease: "{E["softInOut"]}" }}, {sc.L(reflow_at + 0.08)});\n'
        exits = bl
    else:
        exits = ids + bl
    return sc, exits


# Apple, 2001
TA, TN, TV, TY, T6 = K.start('s2'), K.start('s3'), K.start('s4'), K.start('s5'), K.start('s6')
t_mark = K.at('s6', 'aivacs') - 0.25
est = t_mark - 0.35
ta_mil = K.at('s2', 'mil')
ap, ap_ex = section('ap', 's2', TA - 0.1, TN + 0.15, W('Apple', 's2', 'apple'), 0, W('no anunció', 's2', 'no'),
                    'music', 'Reproductor de 5 GB', K.at('s2', 'reproductor'), K.at('s2', 'anunció', nth=1), W('anunció', 's2', 'anunció', nth=1),
                    [[('<span id="ap-num">0</span>', ta_mil, True), ('canciones', K.at('s2', 'canciones'), True)], W('en tu bolsillo', 's2', 'en', nth=1)],
                    112, 'music-2', label=('2001', K.at('s2', '2001')), card_fs=68)
ap.j += (f'const apN = {{ v: 0 }};\n'
         f'tl.to(apN, {{ v: 1000, duration: 0.6, ease: "{E["softLand"]}", onUpdate: () => {{ const v = Math.round(apN.v); document.querySelector("#ap-num").textContent = v >= 1000 ? "1.000" : String(v); }} }}, {ap.L(ta_mil - 0.04)});\n')
exit_all(ap, ap_ex, TN - 0.25)
K.add_scene('ap', TA - 0.1, TN + 0.15, CSS, ap.h, ap.j)

# Nike
t_nf = K.at('s3', 'y') - 0.06
nk, nk_ex = section('nk', 's3', TN - 0.1, TV + 0.15, W('Nike', 's3', 'nike'), 0, W('no vende', 's3', 'no'),
                    'footprints', 'Zapatillas', K.at('s3', 'zapatillas'), K.at('s3', 'vende', nth=1), W('vende', 's3', 'vende', nth=1),
                    [W('Superación', 's3', 'superación')], 150, 'trending-up', reflow_at=t_nf)
nk.line(W('Hoy es la marca deportiva', 's3', 'hoy'), 690, 64, lid='nk-f1')
nk.line(W('que más vende del mundo', 's3', 'que', cyan=('más', 'vende')), 775, 64, lid='nk-f2')
t_mas = K.at('s3', 'más')
nk.h += (f'<div id="nk-n1" class="ln hx cy" style="top:900px;font-size:300px;opacity:0;text-shadow:0 0 60px rgba(75,191,239,.55)">N.º 1</div>\n'
         f'<div id="nk-md" class="ln" style="top:1250px;opacity:0"><span class="glass" style="display:inline-flex;align-items:center;gap:20px;padding:20px 40px;border-radius:999px;font:800 54px \'Jakarta\';color:#fff">'
         f'<i class="ic" style="width:64px;height:64px;color:#BDEBFF">{icon("medal")}</i>en el mundo</span></div>\n')
nk.land('nk-n1', t_mas, dy=0, dur=0.55, ease=E['snapSettle'], scale=1.5)
nk.land('nk-md', t_mas + 0.15, dy=50)
K.fx('pop', t_mas - 0.04)
exit_all(nk, nk_ex + ['nk-f1', 'nk-f2', 'nk-n1', 'nk-md'], TV - 0.25)
K.add_scene('nk', TN - 0.1, TV + 0.15, CSS, nk.h, nk.j)

# Volvo
t_vf = K.at('s4', 'creó') - 0.08
vo, vo_ex = section('vo', 's4', TV - 0.1, TY + 0.15, W('Volvo', 's4', 'volvo'), 0, W('no vende', 's4', 'no'),
                    'car', 'Coches', K.at('s4', 'coches'), K.at('s4', 'vende', nth=1), W('vende', 's4', 'vende', nth=1),
                    [W('Seguridad', 's4', 'seguridad')], 150, 'shield-check', reflow_at=t_vf)
vo.line(W('Creó el cinturón', 's4', 'creó'), 680, 66, lid='vo-f1')
vo.line(W('de tres puntos', 's4', 'de'), 762, 66, lid='vo-f2')
t59 = K.at('s4', '1959')
vo.h += f'<div id="vo-yr" class="ln mono cy" style="top:860px;font-size:220px;line-height:1;opacity:0;text-shadow:0 0 60px rgba(75,191,239,.55)">1959</div>\n'
vo.land('vo-yr', t59, dy=0, dur=0.55, ease=E['snapSettle'], scale=1.45)
K.fx('pop', t59 - 0.04)
vo.line(W('y dejó que todas', 's4', 'y'), 1112, 60, lid='vo-f3')
vo.line(W('las marcas lo usaran', 's4', 'las', cyan=('usaran.',)), 1190, 60, lid='vo-f4')
t_tod, t_us = K.at('s4', 'todas'), K.at('s4', 'usaran')
cars = '<div id="vo-cars" style="position:absolute;left:0;right:0;top:1300px;display:flex;justify-content:center;gap:24px">'
for i in range(5):
    cars += (f'<div id="vo-c{i}" class="glass" style="width:150px;height:150px;border-radius:32%;display:grid;place-items:center;opacity:0">'
             f'<i id="vo-ci{i}" class="ic" style="width:78px;height:78px;color:#6E7F8D">{icon("car")}</i></div>')
    vo.land(f'vo-c{i}', t_tod + 0.13 * i, dy=60, scale=.8)
    vo.j += f'tl.to("#vo-ci{i}", {{ color: "#4BBFEF", duration: 0.2, ease: "none" }}, {vo.L(t_us + 0.06 * i)});\n'
    vo.j += f'tl.to("#vo-c{i}", {{ borderColor: "#4BBFEF", boxShadow: "0 0 40px rgba(75,191,239,.55)", duration: 0.2, ease: "none" }}, {vo.L(t_us + 0.06 * i)});\n'
vo.h += cars + '</div>\n'
K.fx('click', t_tod - 0.04); K.fx('chime', t_us - 0.05)
exit_all(vo, vo_ex + ['vo-f1', 'vo-f2', 'vo-yr', 'vo-f3', 'vo-f4', 'vo-cars'], TY - 0.25)
K.add_scene('vo', TV - 0.1, TY + 0.15, CSS, vo.h, vo.j)

# ¿Y tú?
yo, yo_ex = section('yo', 's5', TY - 0.1, est + 0.4, W('¿Y tú?', 's5', 'y'), 0, W('No vendes', 's5', 'no'),
                    'hammer', 'Reformas', K.at('s5', 'reformas'), K.at('s5', 'vendes', nth=1), W('vendes', 's5', 'vendes', nth=1),
                    [W('Una casa en la que', 's5', 'una'), W('da gusto vivir', 's5', 'da')], 104, 'house', brand_cy=True)
exit_all(yo, yo_ex, est + 0.05)
K.add_scene('yo', TY - 0.1, est + 0.4, CSS, yo.h, yo.j)

# ---------- end card ----------
css, html, js = endcard(K, 'e', est, t_mark, JH, 225, 1000, 630, 'Te ayudamos a contarlo así', '+34 603 82 96 57')
K.add_scene('e', est, K.total, css, html, js)

K.captions(set(), skip=set(K.ids))
K.write_index(bgm_volume=0.2, bgm_media_start=0)
print('total', K.total, 'mark', t_mark)
