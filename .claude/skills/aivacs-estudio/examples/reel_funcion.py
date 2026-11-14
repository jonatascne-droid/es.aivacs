"""Reel 2 · Cada canal necesita una función (atraer, acercar, convertir).
One world: a horizontal path with three stages; the camera travels along it and a customer dot rides it; the payoff pulls back."""
import random
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
FOTOS = os.environ.get('AIVACS_FOTOS') or sys.exit('Defina AIVACS_FOTOS com a pasta das fotos recortadas do Jhony (o06chair.png, o11.png, o14.png, o17.png...)')
from vkit import Kit, icon, endcard, E

P = sys.argv[1]
K = Kit(P)
JH = K.image(os.path.join(FOTOS, 'o17.png'), 'jhony.png')
R = lambda t: round(t, 3)


def wspans(pid, txt):
    return ''.join(f'<span id="{pid}x{n}" style="display:inline-block;margin:0 .12em;opacity:0">{w}</span>' for n, w in enumerate(txt.split()))

A, B, C, D = K.start('s2'), K.start('s3'), K.start('s4'), K.start('s5')
t_mark = K.at('s5', 'aivacs') - 0.25
st, en = 0.0, t_mark + 0.2
PATH_Y = 940
X = [540, 1620, 2700]

# ---------- hook layer (screen space) ----------
w1 = K.words('s1')
t_a2 = [w for w in w1 if w[0] == 'A'][0][1]
sent1 = [w for w in w1 if w[1] < t_a2]
sent2 = [w for w in w1 if w[1] >= t_a2]


def block(bid, lines, top, big_last=False, first_visible=False):
    h, j, n = f'<div id="{bid}" style="position:absolute;left:0;right:0;top:{top}px;text-align:center">', '', 0
    for li, ln in enumerate(lines):
        last = big_last and li == len(lines) - 1
        fs = 140 if last else 96
        h += f'<div class="hx" style="font-size:{fs}px;margin-top:{18 if li else 0}px">'
        for w in ln:
            h += f'<span id="{bid}w{n}" class="{"hx cy" if last else "hx"}" style="display:inline-block;margin:0 .13em;opacity:0">{w[0]}</span>'
            vis = first_visible and n == 0
            t0 = 0 if vis else R(w[1] - 0.04)
            j += f'tl.set("#{bid}w{n}", {{ y: 44, opacity: {1 if vis else 0} }}, 0);\n'
            j += f'tl.to("#{bid}w{n}", {{ opacity: 1, duration: 0.1, ease: "none" }}, {t0});\n'
            j += f'tl.to("#{bid}w{n}", {{ y: 0, duration: 0.42, ease: "{E["softLand"]}" }}, {t0});\n'
            n += 1
        h += '</div>'
    return h + '</div>', j


def split(ws, sizes):
    out, i = [], 0
    for s in sizes:
        out.append(ws[i:i + s]); i += s
    return out


ha, ja = block('ha', split(sent1, [3, 4, len(sent1) - 7]), 640, first_visible=True)
hb, jb = block('hb', split(sent2, [4, 2, len(sent2) - 6]), 470, big_last=True)
t_func = K.at('s1', 'función')
random.seed(7)
chaos_icons = ['si:instagram', 'si:tiktok', 'si:facebook', 'si:youtube', 'si:google', 'si:googlemaps', 'si:whatsapp', 'globe', 'megaphone', 'star', 'si:linkedin', 'mail']
spots = [(90, 230), (820, 200), (420, 200), (110, 1180), (860, 1120), (760, 1450), (180, 1500), (470, 1640), (900, 1700), (40, 1010), (950, 470), (640, 1300)]
chaos, cj = '', ''
for i, (ic, (x, y)) in enumerate(zip(chaos_icons, spots)):
    ic = ic if ic != 'mail' else 'send'
    rot = random.randint(-25, 25)
    chaos += f'<div id="k{i}" class="glass" style="position:absolute;left:{x}px;top:{y}px;width:118px;height:118px;border-radius:30%;display:grid;place-items:center;opacity:0"><i class="ic" style="width:58px;height:58px;color:#E9F8FF">{icon(ic)}</i></div>'
    t_in = R(0.05 + i * 0.06)
    dx, dy = random.randint(-80, 80), random.randint(-60, 60)
    cj += f'tl.set("#k{i}", {{ opacity: 1, scale: 1.5, rotation: {rot - 30} }}, {t_in});\n'
    cj += f'tl.to("#k{i}", {{ scale: 1, rotation: {rot}, duration: 0.5, ease: "{E["softLand"]}" }}, {t_in});\n'
    cj += f'tl.to("#k{i}", {{ x: {dx}, y: {dy}, rotation: {rot + random.randint(-40, 40)}, duration: {R(t_func - t_in - 0.52)}, ease: "none" }}, {R(t_in + 0.52)});\n'
    tx = 60 + i * (960 / 11) - x - 59
    cj += f'tl.to("#k{i}", {{ x: {tx:.0f}, y: {PATH_Y - y - 59}, rotation: 0, scale: .32, duration: 0.5, ease: "{E["whip"] if "whip" in E else "power2.inOut"}" }}, {R(t_func + 0.02 * i)});\n'
    cj += f'tl.set("#k{i}", {{ opacity: 0 }}, {R(t_func + 0.52 + 0.02 * i)});\n'
t_b = sent2[0][1]
hook_js = ja + jb + cj + f"""
tl.to("#ha", {{ y: -560, duration: 0.38, ease: "{E['accelExit']}" }}, {R(t_b - 0.36)});
tl.set("#ha", {{ visibility: "hidden" }}, {R(t_b + 0.02)});
tl.to("#hb", {{ y: -620, duration: 0.42, ease: "{E['accelExit']}" }}, {R(A - 0.3)});
tl.set("#hb", {{ visibility: "hidden" }}, {R(A + 0.12)});
"""

# ---------- the world: path, three stages, customer dot ----------
stages = [
    ('s2', 'magnet', 'Atraer', 'Llegar a las personas correctas', 'Donde tu cliente te descubre',
     [('clapperboard', 'Un reel', 'reel'), ('megaphone', 'Un anuncio', 'anuncio'), ('si:googlemaps', 'Google Maps', 'google')], 'atraer', 'llegar'),
    ('s3', 'handshake', 'Acercar', 'Construir confianza e interés', 'Donde decide si se fía de ti',
     [('globe', 'Tu web', 'web'), ('star', 'Reseñas ★★★★★', 'reseñas'), ('badge-check', 'Casos reales', 'casos')], 'acercar', 'construir'),
    ('s4', 'shopping-cart', 'Convertir', 'Transformar ese interés en una venta', 'Donde compra',
     [('si:whatsapp', 'WhatsApp', 'whatsapp'), ('file-text', 'Presupuesto', 'presupuesto'), ('store', 'Tienda online', 'tienda')], 'convertir', 'transformar'),
]
world = f'<div id="path" style="position:absolute;left:0;top:{PATH_Y - 2}px;width:3240px;height:4px;border-radius:2px;background:linear-gradient(90deg,rgba(75,191,239,.15),#4BBFEF 12%,#4BBFEF 88%,rgba(75,191,239,.15));box-shadow:0 0 18px rgba(75,191,239,.8)"></div>\n'
wj = f'tl.set("#path", {{ scaleX: 0, transformOrigin: "540px 50%" }}, 0);\ntl.to("#path", {{ scaleX: 1, duration: 0.7, ease: "{E["softLand"]}" }}, {R(t_func + 0.3)});\n'
for k in range(3):
    wj += f'tl.to("#n{k}", {{ opacity: 1, duration: 0.15, ease: "none" }}, {R(t_func + 0.45 + 0.1 * k)});\n'
for k, (sid, ic, title, defi, donde, chips, kw_t, kw_d) in enumerate(stages):
    x = X[k]
    world += (f'<div id="n{k}" style="position:absolute;left:{x - 24}px;top:{PATH_Y - 24}px;width:48px;height:48px;border-radius:50%;background:#0B1117;border:4px solid #4BBFEF;box-shadow:0 0 24px rgba(75,191,239,.8);opacity:0"></div>\n'
              f'<div id="g{k}" style="position:absolute;left:{x - 540}px;top:0;width:1080px;height:1920px">'
              f'<div id="g{k}tile" class="glass" style="position:absolute;left:460px;top:290px;width:160px;height:160px;border-radius:32%;display:grid;place-items:center;opacity:0">'
              f'<i class="ic" style="width:78px;height:78px;color:#E9F8FF;filter:drop-shadow(0 0 12px rgba(75,191,239,.9))">{icon(ic)}</i></div>'
              f'<div id="g{k}t" class="hx" style="position:absolute;left:40px;right:40px;top:480px;text-align:center;font-size:132px;opacity:0">{title}</div>'
              f'<div id="g{k}d" style="position:absolute;left:80px;right:80px;top:640px;text-align:center;font:700 56px/1.18 \'Jakarta\';text-wrap:balance">{wspans(f"g{k}d", defi)}</div>'
              f'<div id="g{k}w" class="cy" style="position:absolute;left:60px;right:60px;top:{PATH_Y - 128}px;text-align:center;font:700 54px \'Jakarta\'">{wspans(f"g{k}w", donde)}</div>')
    for i, (cic, lab, _) in enumerate(chips):
        world += (f'<div style="position:absolute;left:0;right:0;top:{PATH_Y + 100 + i * 160}px;display:flex;justify-content:center">'
                  f'<div id="g{k}c{i}" class="glass chip" style="position:relative;opacity:0;height:140px;font-size:48px;padding:0 36px"><i class="ic" style="width:66px;height:66px">{icon(cic)}</i>{lab}</div></div>')
    world += '</div>\n'
    world += f'<div id="bg{k}" class="ic" style="position:absolute;left:{x - 410}px;top:560px;width:820px;height:820px;color:#4BBFEF;opacity:.055">{icon(ic)}</div>\n'
    wj += f'tl.fromTo("#bg{k}", {{ scale: 1.2, rotation: -8 }}, {{ scale: .95, rotation: 8, duration: {R(en)}, ease: "none" }}, 0);\n'
    t_title = K.at(sid, kw_t)
    wj += f'tl.set("#g{k}tile", {{ opacity: 1, scale: 1.6 }}, {R(t_title - 0.2)});\ntl.to("#g{k}tile", {{ scale: 1, duration: 0.5, ease: "{E["snapSettle"]}" }}, {R(t_title - 0.2)});\n'
    wj += f'tl.set("#g{k}t", {{ y: 50 }}, 0);\ntl.to("#g{k}t", {{ opacity: 1, duration: 0.1, ease: "none" }}, {R(t_title - 0.05)});\ntl.to("#g{k}t", {{ y: 0, duration: 0.45, ease: "{E["softLand"]}" }}, {R(t_title - 0.05)});\n'
    ws = K.words(sid)
    for el, txt, kw in ((f'g{k}d', defi, kw_d), (f'g{k}w', donde, 'donde')):
        i0 = next(i for i, w in enumerate(ws) if w[0].lower().startswith(kw))
        for n, _ in enumerate(txt.split()):
            t = ws[min(i0 + n, len(ws) - 1)][1]
            wj += f'tl.set("#{el}x{n}", {{ y: 36 }}, 0);\ntl.to("#{el}x{n}", {{ opacity: 1, duration: 0.08, ease: "none" }}, {R(t - 0.04)});\ntl.to("#{el}x{n}", {{ y: 0, duration: 0.4, ease: "{E["softLand"]}" }}, {R(t - 0.04)});\n'
    for i, (_, _, kw) in enumerate(chips):
        t = K.at(sid, kw)
        wj += f'tl.set("#g{k}c{i}", {{ y: 70, scale: .92 }}, 0);\ntl.to("#g{k}c{i}", {{ opacity: 1, duration: 0.1, ease: "none" }}, {R(t - 0.05)});\ntl.to("#g{k}c{i}", {{ y: 0, scale: 1, duration: 0.42, ease: "{E["softLand"]}" }}, {R(t - 0.05)});\n'
        K.fx('click', t - 0.05)
        wj += f'tl.to("#g{k}c{i}", {{ y: -10, duration: {R(min(2.0, D + 0.03 - (t + 0.4)))}, ease: "none" }}, {R(t + 0.4)});\n'
    t_dn = K.at(sid, 'donde')
    world += f'<div id="cm{k}" style="position:absolute;left:{x - 130}px;top:{PATH_Y - 6}px;width:260px;height:12px;border-radius:6px;background:linear-gradient(90deg,transparent,#E9F8FF 60%,transparent);box-shadow:0 0 24px rgba(75,191,239,.9);opacity:0"></div>\n'
    wj += f'tl.set("#cm{k}", {{ opacity: 1, x: 0 }}, {R(t_dn - 0.1)});\ntl.to("#cm{k}", {{ x: 760, duration: 0.85, ease: "{E["gentleIn"]}" }}, {R(t_dn - 0.1)});\ntl.set("#cm{k}", {{ opacity: 0 }}, {R(t_dn + 0.76)});\n'
    wj += f'tl.to("#n{k}", {{ scale: 1.5, duration: 0.18, ease: "{E["softLand"]}", yoyo: true, repeat: 1 }}, {R(t_title - 0.1)});\n'

# customer dot
world += (f'<div id="dot" style="position:absolute;left:{X[0] - 44}px;top:{PATH_Y - 44}px;width:88px;height:88px;border-radius:50%;background:radial-gradient(circle,#E9F8FF,#4BBFEF 60%);'
          f'box-shadow:0 0 40px rgba(75,191,239,.95);display:grid;place-items:center;color:#04121B;opacity:0"><i class="ic" style="width:46px;height:46px">{icon("user-round")}</i></div>\n'
          f'<div id="sale" style="position:absolute;left:{X[2] - 170}px;top:{PATH_Y - 190}px;width:340px;text-align:center;opacity:0"><span style="display:inline-flex;align-items:center;gap:12px;padding:16px 30px;border-radius:999px;background:#25D366;color:#04121B;font:800 50px \'Jakarta\';box-shadow:0 0 40px rgba(37,211,102,.45)">Venta ✓</span></div>\n')
t_dot = K.at('s2', 'cliente')
wj += ''.join(f'tl.to("#dot", {{ scale: 1.14, duration: 0.45, ease: "{E["softInOut"]}", yoyo: true, repeat: 1 }}, {R(t)});\n' for t in [t_dot + 0.6 + 1.6 * j for j in range(30)] if t < D - 0.2 and not any(abs(t - u) < 1.1 for u in (B - 0.4, C - 0.4)))
wj += f'tl.set("#dot", {{ opacity: 1, x: -640 }}, {R(t_dot - 0.4)});\ntl.to("#dot", {{ x: 0, duration: 0.6, ease: "{E["softLand"]}" }}, {R(t_dot - 0.4)});\n'
wj += f'tl.to("#dot", {{ x: 1080, duration: 0.95, ease: "power2.inOut" }}, {R(B - 0.4)});\n'
wj += f'tl.to("#dot", {{ x: 2160, duration: 0.95, ease: "power2.inOut" }}, {R(C - 0.4)});\n'

# camera: pans along the path, then pulls back to the whole map
S3, TY = 0.37, 512
wj += f'tl.set("#wld", {{ x: 0, y: 0, scale: 1, transformOrigin: "0px 0px" }}, 0);\n'
wj += f'tl.to("#wld", {{ x: -1080, duration: 0.7, ease: "power3.inOut" }}, {R(B - 0.4)});\n'
wj += f'tl.to("#wld", {{ x: -2160, duration: 0.7, ease: "power3.inOut" }}, {R(C - 0.4)});\n'
K.fx('whoosh', B - 0.45); K.fx('whoosh', C - 0.45)
t_pb = D + 0.05
wj += f'tl.to("#wld", {{ x: {540 - 1620 * S3:.0f}, y: {TY}, scale: {S3:.4f}, duration: 1.0, ease: "power3.inOut" }}, {R(t_pb)});\n'
for k in range(3):
    for i in range(3):
        wj += f'tl.to("#g{k}c{i}", {{ opacity: 0, y: 40, duration: 0.3, ease: "{E["accelExit"]}" }}, {R(t_pb + 0.02 * i)});\n'
    wj += f'tl.to("#g{k}w", {{ opacity: 0, duration: 0.25, ease: "none" }}, {R(t_pb)});\n'
    wj += f'tl.to("#g{k}d", {{ opacity: 0, duration: 0.25, ease: "none" }}, {R(t_pb)});\n'
# the customer runs the whole path on its own
t_cl = K.at('s5', 'cliente')
t_sig = K.at('s5', 'siguiente')
wj += f'tl.set("#dot", {{ x: 0, scale: 2 }}, {R(t_pb + 1.0)});\n'
wj += f'tl.to("#dot", {{ x: 2160, duration: {R(max(1.2, t_sig - t_cl))}, ease: "{E["softInOut"]}" }}, {R(t_cl)});\n'
for k in range(3):
    tk = t_cl + (t_sig - t_cl) * k / 2
    wj += f'tl.to("#n{k}", {{ scale: 1.8, backgroundColor: "#4BBFEF", duration: 0.2, ease: "{E["softLand"]}" }}, {R(tk)});\n'
wj += f'tl.set("#sale", {{ opacity: 1, scale: 2.2, y: 30 }}, {R(t_sig)});\ntl.to("#sale", {{ scale: 2.7, y: 0, duration: 0.5, ease: "{E["popOver"]}" }}, {R(t_sig)});\n'
K.fx('chime', t_sig)
wj += f'tl.to("#wld", {{ y: {TY - 360}, opacity: 0, duration: 0.34, ease: "{E["accelExit"]}" }}, {R(t_mark - 0.05)});\n'

html = f'<div id="hk" style="position:absolute;inset:0">{chaos}{ha}{hb}</div>\n<div id="wld" style="position:absolute;left:0;top:0;width:3240px;height:1920px">{world}</div>'
K.add_scene('world', st, en, '', html, hook_js + wj)
K.fx('whoosh', t_func + 0.05)

# ---------- end card ----------
est = t_mark - 0.35
css, html, js = endcard(K, 'e', est, t_mark, JH, 250, 1010, 600, 'Lo montamos contigo', '+34 603 82 96 57')
K.add_scene('e', est, K.total, css, html, js)

groups = K.captions({'función', 'siguiente'}, skip={'s1', 's2', 's3', 's4'}, until=t_mark - 0.3)
K.write_index(bgm_volume=0.2, bgm_media_start=0)
print('total', K.total)
for g in groups:
    print(g)
