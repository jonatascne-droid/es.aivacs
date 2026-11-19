"""Reel de quarta 2 · Así trabajamos (del primer mensaje a la entrega). Usage: reel_quarta_proceso.py PROJECT_DIR"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
from vkit_explicativo import Kit, icon, phone, wa_header, endcard, E  # noqa: E402

P = sys.argv[1]
K = Kit(P)
JH = 'assets/img/jhony.png'   # the cutout already in the project (copy one from AIVACS_FOTOS for a new project)

# ---------- scene 1 · first message ----------
st, en = K.start('s1'), K.end('s1')
L = lambda t: round(t - st, 3)
t_hola, t_asi = K.at('s1', 'hola'), K.at('s1', 'así')
chat = f"""{wa_header('AIVACS · Jhony', 'en línea', 'AI')}
<div style="position:absolute;left:0;right:0;top:138px;bottom:0;background:#0B141A;padding:26px 18px;display:flex;flex-direction:column;justify-content:flex-end;gap:14px;padding-bottom:70px">
  <div class="mono" style="align-self:center;font-size:16px;color:#8696A0;background:#1F2C34;padding:6px 14px;border-radius:10px">HOY</div>
  <div id="c1-msg" class="bub-out" style="font-size:28px">Hola, necesito ayuda con lo digital de mi empresa.<div class="ts" style="color:#9FC9BD">09:12 ✓✓</div></div>
  <div id="c1-typing" class="bub-in" style="display:flex;gap:8px;padding:18px 22px">
    <i style="width:12px;height:12px;border-radius:50%;background:#8696A0;display:block"></i><i style="width:12px;height:12px;border-radius:50%;background:#8696A0;display:block"></i><i style="width:12px;height:12px;border-radius:50%;background:#8696A0;display:block"></i></div>
</div>"""
html = phone('c1-ph', '#0B141A', chat, time='09:12')
js = f"""tl.fromTo("#c1-ph", {{ scale: 1 }}, {{ scale: 1.04, duration: {L(en) - 0.6}, ease: "none" }}, 0);
tl.fromTo("#c1-msg", {{ opacity: 0, y: 40, scale: 0.9 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(1.6)" }}, {max(0.1, L(t_hola) - 0.05)});
tl.fromTo("#c1-typing", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, {L(t_asi) - 0.4});
tl.to("#c1-ph", {{ y: -260, scale: 0.6, opacity: 0, duration: 0.55, ease: "power3.in" }}, {L(en) - 0.6});"""
K.add_scene('c1', st, en, '#c1-msg, #c1-typing { opacity: 0; }', html, js, stage=(1.06, 690))
K.fx('pop', t_hola)

# ---------- scene 2 · the route (s2..s5) ----------
st, en = K.start('s2'), K.end('s5')
L = lambda t: round(t - st, 3)
stages = [('search', 'Diagnóstico'), ('receipt', 'Propuesta'), ('layout-dashboard', 'Construcción'), ('rocket', 'Entrega')]
xs = [150, 410, 670, 930]
step = ''.join(f'<div class="nd" id="r-n{i}" style="left:{x - 46}px"><i class="ic" style="width:42px;height:42px">{icon(ic)}</i></div>'
               f'<div class="nl" id="r-l{i}" style="left:{x - 110}px">{lab}</div>' for i, ((ic, lab), x) in enumerate(zip(stages, xs)))
t_diag = K.at('s2', 'diagnóstico'); t_ent = K.at('s2', 'entendemos'); t_nada = K.at('s2', 'nada', 'end')
t_prop = K.at('s3', 'propuesta'); t_alc = K.at('s3', 'alcance'); t_plazo = K.at('s3', 'plazo'); t_inv = K.at('s3', 'inversión'); t_esc = K.at('s3', 'escrito')
t_cons = K.at('s4', 'construimos'); t_ens = K.at('s4', 'enseñamos'); t_av = K.at('s4', 'avance')
t_entr = K.at('s5', 'entregamos'); t_form = K.at('s5', 'formamos'); t_seg = K.at('s5', 'seguimos')

checks = ['Tu web', 'Tus redes', 'Tus anuncios', 'Tu WhatsApp', 'Tus procesos']
crow = ''.join(f'<div class="cr" id="r-c{i}"><i class="ic" style="width:40px;height:40px;color:#4BBFEF">{icon("circle-check")}</i>{c}</div>' for i, c in enumerate(checks))
card1 = f"""<div class="card stage" id="r-k1">
  <div class="kh"><span class="mono">ETAPA 01</span><span class="pill ok" id="r-free">GRATIS</span></div>
  <div class="kt">Diagnóstico</div>
  <div style="display:flex;flex-direction:column;gap:14px;margin-top:26px">{crow}</div></div>"""
rows = [('Alcance', 'Web + WhatsApp automático + anuncios', t_alc), ('Plazo', '4 semanas, por etapas', t_plazo), ('Inversión', 'Cerrada antes de empezar', t_inv)]
prow = ''.join(f'<div class="pr" id="r-p{i}"><span>{k}</span><b>{v}</b></div>' for i, (k, v, _) in enumerate(rows))
card2 = f"""<div class="card stage" id="r-k2">
  <div class="kh"><span class="mono">ETAPA 02</span><span class="mono" style="color:#9AA5B1">PROPUESTA.PDF</span></div>
  <div class="kt">Propuesta a medida</div>
  <div style="margin-top:22px">{prow}</div>
  <div id="r-sign" style="margin-top:30px;display:flex;align-items:center;gap:14px;font:800 32px 'Jakarta';color:#7BE3A6"><i class="ic" style="width:40px;height:40px">{icon('circle-check')}</i>Por escrito, sin letra pequeña</div></div>"""
tasks = [('Página web', 100), ('WhatsApp automático', 70), ('Campaña de anuncios', 40)]
trow = ''.join(f'<div style="margin-top:26px"><div style="display:flex;justify-content:space-between;font:700 30px \'Jakarta\'"><span>{n}</span><span class="mono" id="r-tp{i}" style="color:#4BBFEF">{v}%</span></div>'
               f'<div style="height:18px;border-radius:9px;background:#16202A;margin-top:12px;overflow:hidden"><div id="r-tb{i}" style="width:0;height:100%;background:#4BBFEF"></div></div></div>'
               for i, (n, v) in enumerate(tasks))
card3 = f"""<div class="card stage" id="r-k3">
  <div class="kh"><span class="mono">ETAPA 03</span><span class="mono" style="color:#9AA5B1">EN CURSO</span></div>
  <div class="kt">Construcción</div>{trow}
  <div id="r-toast" style="margin-top:34px;display:flex;align-items:center;gap:16px;padding:20px 24px;border-radius:20px;background:#0E161E;border:1.5px solid rgba(110,210,250,.45)">
    <i class="ic" style="width:44px;height:44px;color:#25D366">{icon('si:whatsapp')}</i><div><b style="font:800 28px 'Jakarta'">Avance enviado</b><br><span style="font-size:24px;color:#9AA5B1">Ya puedes probar tu nueva web</span></div></div></div>"""
card4 = f"""<div class="card stage" id="r-k4">
  <div class="kh"><span class="mono">ETAPA 04</span><span class="pill ok">EN LÍNEA</span></div>
  <div class="kt">Entrega y crecimiento</div>
  <div style="margin-top:26px;border-radius:20px;overflow:hidden;border:1.5px solid rgba(110,210,250,.3)">
    <div style="display:flex;align-items:center;gap:10px;padding:14px 18px;background:#151D26"><i style="width:12px;height:12px;border-radius:50%;background:#3A4652;display:block"></i><i style="width:12px;height:12px;border-radius:50%;background:#3A4652;display:block"></i><span class="mono" style="margin-left:12px;font-size:20px;color:#9AA5B1">tuempresa.es</span></div>
    <div style="height:200px;background:linear-gradient(160deg,#1E4A61,#0B1A24);padding:30px"><div style="font:800 46px 'Jakarta'">Tu empresa,<br><span style="color:#4BBFEF">en línea.</span></div></div></div>
  <div style="display:flex;flex-direction:column;gap:16px;margin-top:28px">
    <div class="cr" id="r-f1"><i class="ic" style="width:40px;height:40px;color:#4BBFEF">{icon('users')}</i>Te formamos para usarlo</div>
    <div class="cr" id="r-f2"><i class="ic" style="width:40px;height:40px;color:#4BBFEF">{icon('heart-handshake')}</i>Y seguimos contigo</div></div></div>"""
css = """.nd { position: absolute; top: 200px; width: 92px; height: 92px; border-radius: 50%; display: grid; place-items: center; color: #6B7682;
  background: #0E161E; border: 3px solid #26333F; z-index: 3; }
.nl { position: absolute; top: 304px; width: 220px; text-align: center; font: 700 24px "Jakarta"; color: #6B7682; }
.stage { left: 90px; top: 400px; width: 900px; padding: 46px 50px 50px; }
.kh { display: flex; justify-content: space-between; align-items: center; font-size: 22px; color: #4BBFEF; letter-spacing: .1em; }
.kt { font: 800 66px "Jakarta"; letter-spacing: -.02em; margin-top: 18px; }
.cr { display: flex; align-items: center; gap: 18px; font: 700 34px "Jakarta"; }
.pr { display: flex; flex-direction: column; gap: 6px; padding: 20px 0; border-bottom: 1.5px solid rgba(110,210,250,.15); }
.pr span { font-size: 24px; color: #9AA5B1; } .pr b { font: 800 34px "Jakarta"; }
#r-k1, #r-k2, #r-k3, #r-k4 { opacity: 0; }
"""
for i in range(5):
    css += f'#r-c{i} {{ opacity: 0; }}\n'
css += '#r-p0, #r-p1, #r-p2, #r-sign, #r-toast, #r-f1, #r-f2, #r-free { opacity: 0; }\n'
html = f"""<svg style="position:absolute;left:0;top:0" width="1080" height="400" viewBox="0 0 1080 400">
  <line x1="150" y1="246" x2="930" y2="246" stroke="#26333F" stroke-width="6" stroke-linecap="round"/>
  <line id="r-prog" x1="150" y1="246" x2="930" y2="246" stroke="#4BBFEF" stroke-width="6" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/></svg>
{step}{card1}{card2}{card3}{card4}"""

def node_on(i, t):
    return (f'tl.to("#r-n{i}", {{ backgroundColor: "#4BBFEF", borderColor: "#4BBFEF", color: "#04121B", scale: 1.12, duration: 0.3, ease: "back.out(2)" }}, {L(t)});\n'
            f'tl.to("#r-n{i}", {{ scale: 1, duration: 0.2 }}, {L(t) + 0.3});\n'
            f'tl.to("#r-l{i}", {{ color: "#F0F4F8", duration: 0.25 }}, {L(t)});\n')

def card_in(k, t):
    return f'tl.fromTo("#r-k{k}", {{ opacity: 0, x: 220 }}, {{ opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }}, {L(t)});\n'

def card_out(k, t):
    return f'tl.to("#r-k{k}", {{ opacity: 0, x: -220, duration: 0.35, ease: "power2.in" }}, {L(t)});\n'

js = f'tl.fromTo("#r-prog", {{ strokeDashoffset: 1.1 }}, {{ strokeDashoffset: 1.1, duration: 0.01 }}, 0);\n'
js += node_on(0, t_diag) + card_in(1, t_diag - 0.25) + f'tl.fromTo("#r-free", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }}, {L(t_diag) + 0.4});\n'
span = (t_nada - t_ent) / 5
for i in range(5):
    js += f'tl.fromTo("#r-c{i}", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "power3.out" }}, {L(t_ent + i * span):.3f});\n'
js += card_out(1, t_prop - 0.55) + f'tl.to("#r-prog", {{ strokeDashoffset: 0.77, duration: 0.5, ease: "power2.inOut" }}, {L(t_prop) - 0.4});\n'
js += node_on(1, t_prop) + card_in(2, t_prop - 0.2)
for i, (_, _, t) in enumerate(rows):
    js += f'tl.fromTo("#r-p{i}", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }}, {L(t) - 0.05});\n'
js += f'tl.fromTo("#r-sign", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }}, {L(t_esc) - 0.1});\n'
js += card_out(2, t_cons - 0.55) + f'tl.to("#r-prog", {{ strokeDashoffset: 0.43, duration: 0.5, ease: "power2.inOut" }}, {L(t_cons) - 0.4});\n'
js += node_on(2, t_cons) + card_in(3, t_cons - 0.2)
for i, (_, v) in enumerate(tasks):
    js += f'tl.fromTo("#r-tb{i}", {{ width: "0%" }}, {{ width: "{v}%", duration: 0.9, ease: "power2.out" }}, {L(t_cons) + 0.2 + i * 0.15:.3f});\n'
js += f'tl.fromTo("#r-toast", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "back.out(1.6)" }}, {L(t_av) - 0.3});\n'
js += card_out(3, t_entr - 0.5) + f'tl.to("#r-prog", {{ strokeDashoffset: 0, duration: 0.5, ease: "power2.inOut" }}, {L(t_entr) - 0.4});\n'
js += node_on(3, t_entr) + card_in(4, t_entr - 0.2)
js += f'tl.fromTo("#r-f1", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "power3.out" }}, {L(t_form) - 0.05});\n'
js += f'tl.fromTo("#r-f2", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "power3.out" }}, {L(t_seg) - 0.05});\n'
for i in range(4):
    js += f'tl.to("#r-n{i}", {{ scale: 1.18, boxShadow: "0 0 30px rgba(75,191,239,.8)", duration: 0.18, ease: "power2.out", yoyo: true, repeat: 1 }}, {L(t_seg) + 0.6 + i * 0.16:.3f});\n'
js += f'tl.to("#r-k4", {{ boxShadow: "0 0 70px rgba(75,191,239,.35), 0 40px 80px rgba(0,0,0,.55)", duration: 0.4, ease: "power2.inOut", yoyo: true, repeat: 1 }}, {L(t_seg) + 0.9:.3f});\n'
js += f'tl.to(["#r-k4", "#r-n0", "#r-n1", "#r-n2", "#r-n3", "#r-l0", "#r-l1", "#r-l2", "#r-l3", "#r-prog"], {{ y: -1300, duration: 0.32, ease: "power3.in" }}, {L(en) - 0.3});\n'
K.add_scene('route', st, en, css, html, js, stage=(1.0, 625))
for t in (t_diag, t_prop, t_cons, t_entr):
    K.fx('whoosh', t - 0.3)
K.fx('pop', t_esc); K.fx('pop', t_av - 0.25)

# ---------- scene 3 · end ----------
st, en = K.start('s6'), K.end('s6')
t_mark = K.at('s6', 'aivacs')
css, html, js = endcard(K, 'e', st, t_mark, JH, 240, 900, 600, 'Diagnóstico gratis por WhatsApp', '+34 603 82 96 57', jh_at=st + 0.1)
import re as _re
js = '\n'.join(l for l in js.split('\n') if '"#e-jh"' not in l)
sc = 760 / 600
js += (f'\ntl.fromTo("#e-jh", {{ opacity: 0, x: -45, y: -265, scale: {sc:.4f}, transformOrigin: "0 0" }}, {{ opacity: 1, x: -45, y: -365, scale: {sc:.4f}, duration: 0.5, ease: "power3.out" }}, 0);\n'
       f'tl.to("#e-jh", {{ x: 0, y: 0, scale: 1, duration: 0.6, ease: "power3.inOut" }}, {round(t_mark - st - 0.55, 3)});\n')
K.add_scene('e', st, en, css, html, js)

groups = K.captions({'diagnóstico', 'gratis', 'propuesta', 'medida', 'escrito', 'avance', 'contigo', 'construye', 'aivacs', 'digital'}, until=t_mark - 0.3)
K.write_index(bgm_volume=0.16, bgm_media_start=15)
print('total', K.total)
for g in groups:
    print(g)
