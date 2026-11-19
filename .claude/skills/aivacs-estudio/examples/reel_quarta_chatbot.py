"""Reel de quarta 3 · 23:14 (qué pasa detrás de un chatbot de WhatsApp). Usage: reel_quarta_chatbot.py PROJECT_DIR"""
import re
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
from vkit_explicativo import Kit, icon, phone, wa_header, endcard, E  # noqa: E402

P = sys.argv[1]
K = Kit(P)
JH = 'assets/img/jhony.png'   # the cutout already in the project (copy one from AIVACS_FOTOS for a new project)

def lock(pid, clock, notif_html):
    inner = f"""<div style="position:absolute;inset:0;background:radial-gradient(500px 700px at 50% 20%, #12304A, #05080B 70%)"></div>
<div style="position:absolute;left:0;right:0;top:120px;text-align:center">
  <div class="mono" style="font-size:22px;color:#9AA5B1">martes, 1 de diciembre</div>
  <div style="font:700 140px/1 'Jakarta';letter-spacing:-.03em;margin-top:10px">{clock}</div></div>
{notif_html}"""
    return phone(pid, '#05080B', inner, time=clock)


def notif(nid, app_icon, title, body, top=420):
    return (f'<div id="{nid}" style="position:absolute;left:18px;right:18px;top:{top}px;padding:18px 20px;border-radius:26px;background:rgba(30,40,50,.88);border:1px solid rgba(255,255,255,.12);display:flex;gap:16px;align-items:flex-start">'
            f'<div style="width:52px;height:52px;border-radius:14px;background:#25D366;display:grid;place-items:center;flex:none;color:#fff"><i class="ic" style="width:32px;height:32px">{app_icon}</i></div>'
            f'<div><div style="display:flex;justify-content:space-between;gap:20px;font-size:18px;color:#B9C4CE"><b style="color:#fff;font-size:20px">{title}</b><span>ahora</span></div>'
            f'<div style="font-size:22px;line-height:1.3;margin-top:4px">{body}</div></div></div>')


# ---------- scene 1 · 23:14 ----------
st, en = K.start('s1'), K.end('s1')
L = lambda t: round(t - st, 3)
t_cli = K.at('s1', 'cliente'); t_pide = K.at('s1', 'pide')
html = lock('n1-ph', '23:14', notif('n1-nt', icon('si:whatsapp'), 'Carlos', 'Hola, ¿me pasáis presupuesto para reformar el baño?'))
html += f'<div id="n1-moon" style="position:absolute;left:830px;top:240px;width:110px;height:110px;color:#BDEBFF;opacity:.9"><i class="ic" style="width:110px;height:110px;display:block">{icon("moon")}</i></div>'
js = f"""tl.fromTo("#n1-ph", {{ scale: 1 }}, {{ scale: 1.04, duration: {L(en) - 0.6}, ease: "none" }}, 0);
tl.fromTo("#n1-nt", {{ opacity: 0, y: -60 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "back.out(1.4)" }}, {L(t_cli) - 0.2});
tl.to("#n1-ph", {{ scale: 2.3, y: 380, opacity: 0, duration: 0.55, ease: "power3.in" }}, {L(en) - 0.55});
tl.to("#n1-moon", {{ opacity: 0, duration: 0.3 }}, {L(en) - 0.5});"""
K.add_scene('n1', st, en, '#n1-nt { opacity: 0; }', html, js, stage=(1.06, 690))
K.fx('notify', t_cli - 0.15)

# ---------- scene 2 · la IA entiende ----------
st, en = K.start('s2'), K.end('s2')
L = lambda t: round(t - st, 3)
t_ia = K.at('s2', 'inteligencia'); t_ent = K.at('s2', 'entiende'); t_nec = K.at('s2', 'necesita')
chips = [('Intención', 'Pedir presupuesto', 360), ('Servicio', 'Reforma de baño', 590), ('Le falta saber', 'Metros y ciudad', 820)]
chip_html = ''.join(f'<div class="ch" id="n2-c{i}" style="top:{y + 300}px"><span>{k}</span><b>{v}</b></div>' for i, (k, v, y) in enumerate(chips))
html = f"""<div class="card" id="n2-msg" style="left:110px;top:230px;width:860px;padding:34px 38px;overflow:hidden"><div id="n2-scan" style="position:absolute;top:0;bottom:0;left:0;width:180px;background:linear-gradient(90deg,transparent,rgba(75,191,239,.32),transparent)"></div>
  <div style="display:flex;align-items:center;gap:14px;font:700 24px 'Jakarta';color:#9AA5B1"><i class="ic" style="width:34px;height:34px;color:#25D366">{icon('si:whatsapp')}</i>Carlos · 23:14</div>
  <div style="font:600 40px/1.35 'DMSans';margin-top:16px">Hola, ¿me pasáis <span class="hl" id="n2-h1">presupuesto</span> para reformar el <span class="hl" id="n2-h2">baño</span>?</div></div>
<div id="n2-ai" style="position:absolute;left:110px;top:560px;display:flex;align-items:center;gap:14px;padding:14px 22px;border-radius:999px;background:#0F1821;border:1.5px solid rgba(110,210,250,.55);font:800 28px 'Jakarta'">
  <i class="ic" style="width:34px;height:34px;color:#4BBFEF">{icon('sparkles')}</i>Inteligencia artificial</div>
<svg style="position:absolute;left:0;top:0" width="1080" height="1300" viewBox="0 0 1080 1300">
  {''.join(f'<path id="n2-w{i}" d="M150 640 C 150 {y + 340}, 150 {y + 340}, 200 {y + 340}" stroke="#4BBFEF" stroke-width="4" fill="none" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/>' for i, (_, _, y) in enumerate(chips))}</svg>
{chip_html}"""
css = """.hl { padding: 0 6px; border-radius: 8px; background: rgba(75,191,239,0); }
.ch { position: absolute; left: 210px; width: 760px; padding: 22px 28px; border-radius: 22px; background: #0E161E; border: 1.5px solid rgba(110,210,250,.4); display: flex; flex-direction: column; gap: 4px; opacity: 0; }
.ch span { font-size: 22px; color: #9AA5B1; } .ch b { font: 800 38px "Jakarta"; color: #F0F4F8; }
#n2-ai { opacity: 0; }"""
js = f"""tl.set("#n2-msg", {{ opacity: 1, scale: 0.85, y: 120 }}, 0);
tl.to("#n2-msg", {{ scale: 1, y: 0, duration: 0.5, ease: "expo.out" }}, 0);
tl.fromTo("#n2-ai", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.4, ease: "power3.out" }}, {L(t_ia) - 0.2});
tl.to("#n2-h1", {{ backgroundColor: "rgba(75,191,239,.35)", duration: 0.25 }}, {L(t_ent) - 0.1});
tl.to("#n2-h2", {{ backgroundColor: "rgba(75,191,239,.35)", duration: 0.25 }}, {L(t_ent) + 0.15});
{''.join(f'tl.to("#n2-w{i}", {{ strokeDashoffset: 0, duration: 0.3, ease: "power2.out" }}, {L(t_ent) + 0.1 + i * 0.3:.3f});' + chr(10) + f'tl.fromTo("#n2-c{i}", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }}, {L(t_ent) + 0.25 + i * 0.3:.3f});' + chr(10) for i in range(3))}"""
js = f'tl.set("#n2-scan", {{ x: -220 }}, 0);\ntl.to("#n2-scan", {{ x: 900, duration: {round(max(0.6, (t_ent - t_ia - 0.3) / 2), 3)}, ease: "power1.inOut", repeat: 1 }}, {L(t_ia) + 0.1:.3f});\n' + f'tl.to("#n2-ai", {{ boxShadow: "0 0 40px rgba(75,191,239,.6)", duration: 0.35, ease: "power2.inOut", yoyo: true, repeat: 3 }}, {L(t_ia) + 0.3:.3f});\n' + js
js += f'tl.set("#n2-stg", {{ y: 455 }}, 0);\ntl.to("#n2-stg", {{ y: 150, duration: 0.8, ease: "power2.inOut" }}, {L(t_ent) - 0.3:.3f});\n'
K.add_scene('n2', st, en, css, html, js, stage=(1.06, 730))
K.fx('pop', t_ent + 0.25); K.fx('pop', t_ent + 0.85)

# ---------- scene 3 · preguntas + sistema ----------
st, en = K.start('s3'), K.end('s3')
L = lambda t: round(t - st, 3)
t_preg = K.at('s3', 'preguntas'); t_cons = K.at('s3', 'consulta'); t_obras = K.at('s3', 'obras')
html = f"""<div class="card" id="n3-chat" style="left:110px;top:220px;width:860px;padding:28px 30px;display:flex;flex-direction:column;gap:16px;background:#0B141A">
  <div id="n3-q" class="bub-in" style="font-size:30px;max-width:90%">¿Cuántos m² tiene el baño y en qué ciudad está?<div class="ts">23:14</div></div>
  <div id="n3-a" class="bub-out" style="font-size:30px">Unos 6 m², en Madrid.<div class="ts" style="color:#9FC9BD">23:15 ✓✓</div></div></div>
<svg style="position:absolute;left:0;top:0" width="1080" height="1300" viewBox="0 0 1080 1300">
  <path id="n3-line" d="M540 600 L540 700" stroke="#4BBFEF" stroke-width="5" stroke-linecap="round" fill="none" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/></svg>
<div class="card" id="n3-db" style="left:110px;top:710px;width:860px;padding:34px 38px">
  <div style="display:flex;align-items:center;gap:14px"><i class="ic" style="width:40px;height:40px;color:#4BBFEF">{icon('database')}</i><b style="font:800 32px 'Jakarta'">Obra Organize · tarifas</b></div>
  <div style="display:flex;justify-content:space-between;margin-top:24px;font-size:28px;color:#C9D4DD"><span>Reforma de baño completa</span><span class="mono">6 m²</span></div>
  <div style="display:flex;justify-content:space-between;margin-top:12px;font-size:28px;color:#C9D4DD"><span>Zona</span><span class="mono">Madrid</span></div>
  <div id="n3-est" style="display:flex;justify-content:space-between;align-items:center;margin-top:24px;padding-top:20px;border-top:1.5px solid rgba(110,210,250,.18);font:800 40px 'Jakarta'"><span>Estimación</span><span style="color:#4BBFEF">€ 4.850</span></div></div>"""
css = '#n3-q, #n3-a, #n3-db, #n3-est { opacity: 0; }'
js = f"""tl.set("#n3-chat", {{ opacity: 1, y: 160 }}, 0);
tl.to("#n3-chat", {{ y: 0, duration: 0.5, ease: "expo.out" }}, 0);
tl.fromTo("#n3-q", {{ opacity: 0, y: 24, scale: 0.92 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(1.6)" }}, {max(0.2, L(t_preg) - 0.5)});
tl.fromTo("#n3-a", {{ opacity: 0, y: 24, scale: 0.92 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(1.6)" }}, {L(t_preg) + 0.5});
tl.to("#n3-line", {{ strokeDashoffset: 0, duration: 0.3, ease: "power2.out" }}, {L(t_cons) - 0.2});
tl.fromTo("#n3-db", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }}, {L(t_cons)});
tl.fromTo("#n3-est", {{ opacity: 0, x: 30 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }}, {L(t_obras) + 0.1});"""
K.add_scene('n3', st, en, css, html, js, stage=(1.08, 650))
K.fx('pop', t_preg + 0.5); K.fx('pop', t_obras + 0.1)

# ---------- scene 4 · PDF ----------
st, en = K.start('s4'), K.end('s4')
L = lambda t: round(t - st, 3)
t_gen = K.at('s4', 'genera'); t_pdf = K.at('s4', 'pdf'); t_env = K.at('s4', 'envía')
lines = [('Demolición y retirada', '€ 950'), ('Fontanería y desagües', '€ 1.200'), ('Alicatado y suelo', '€ 1.650'), ('Sanitarios y mampara', '€ 1.050')]
lrow = ''.join(f'<div class="lr" id="n4-l{i}"><span>{a}</span><span class="mono">{b}</span></div>' for i, (a, b) in enumerate(lines))
html = f"""<div class="card" id="n4-doc" style="left:150px;top:230px;width:780px;padding:40px 44px;background:#F4F7F9;color:#0C141B;border-color:rgba(255,255,255,.6)">
  <div style="display:flex;justify-content:space-between;align-items:center"><b style="font:800 40px 'Jakarta'">Presupuesto</b><span style="padding:8px 14px;border-radius:8px;background:#E5484D;color:#fff;font:700 20px 'JetBrains Mono'">PDF</span></div>
  <div style="font-size:24px;color:#51606C;margin-top:8px">Carlos · Baño 6 m² · Madrid</div>
  <div style="margin-top:24px">{lrow}</div>
  <div id="n4-tot" style="display:flex;justify-content:space-between;margin-top:22px;font:800 40px 'Jakarta'"><span>Total</span><span style="color:#0B76A6">€ 4.850</span></div></div>
<div id="n4-sent" style="position:absolute;left:0;right:0;top:930px;display:flex;justify-content:center">
  <span style="display:inline-flex;align-items:center;gap:14px;padding:18px 30px;border-radius:999px;background:#0F1821;border:1.5px solid rgba(110,210,250,.55);font:800 32px 'Jakarta'">
    <i class="ic" style="width:38px;height:38px;color:#25D366">{icon('si:whatsapp')}</i>Enviado a Carlos</span></div>"""
css = """.lr { display: flex; justify-content: space-between; padding: 14px 0; border-bottom: 1.5px solid #DCE3E8; font-size: 27px; opacity: 0; }
#n4-tot, #n4-sent { opacity: 0; }"""
js = f"""tl.fromTo("#n4-doc", {{ opacity: 0, y: 60, rotation: -2 }}, {{ opacity: 1, y: 0, rotation: 0, duration: 0.5, ease: "power3.out" }}, {max(0.05, L(t_gen) - 0.3)});
{''.join(f'tl.fromTo("#n4-l{i}", {{ opacity: 0, x: -20 }}, {{ opacity: 1, x: 0, duration: 0.25, ease: "power2.out" }}, {L(t_gen) + 0.25 + i * 0.18:.3f});' + chr(10) for i in range(4))}
tl.fromTo("#n4-tot", {{ opacity: 0, scale: 0.9 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {L(t_pdf)});
tl.to("#n4-doc", {{ scale: 0.75, y: 30, duration: 0.5, ease: "power3.inOut" }}, {L(t_env) - 0.45});
tl.fromTo("#n4-sent", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "back.out(1.6)" }}, {L(t_env) - 0.05});"""
K.add_scene('n4', st, en, css, html, js, stage=(1.1, 685))
K.fx('typing', t_gen + 0.2); K.fx('whoosh', t_env - 0.1)

# ---------- scene 5 · 23:16 ----------
st, en = K.start('s5'), K.end('s5')
L = lambda t: round(t - st, 3)
t_ya = K.at('s5', 'tiene'); t_sin = K.at('s5', 'sin'); t_con = K.at('s5', 'conectado')
html = lock('n5-ph', '23:16', notif('n5-nt', icon('si:whatsapp'), 'Tu asistente', 'Presupuesto enviado a Carlos. Respondió en 2 minutos.'))
html += f"""<div id="n5-team" style="position:absolute;left:0;right:0;top:1060px;display:flex;justify-content:center">
  <span style="display:inline-flex;align-items:center;gap:14px;padding:18px 30px;border-radius:999px;background:#0F1821;border:1.5px solid rgba(110,210,250,.35);font:800 30px 'Jakarta';color:#C9D4DD">
    <i class="ic" style="width:36px;height:36px;color:#BDEBFF">{icon('moon')}</i>Tu equipo: 0 conectados</span></div>"""
js = f"""tl.set("#n5-ph", {{ opacity: 1, scale: 0.9, y: 160 }}, 0);
tl.to("#n5-ph", {{ scale: 1, y: 0, duration: 0.5, ease: "expo.out" }}, 0);
tl.fromTo("#n5-nt", {{ opacity: 0, y: -60 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "back.out(1.4)" }}, {L(t_ya) - 0.3});
tl.fromTo("#n5-team", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }}, {L(t_sin) - 0.1});
tl.to(["#n5-ph", "#n5-team"], {{ y: -1300, duration: 0.32, ease: "power3.in" }}, {L(en) - 0.3});"""
K.add_scene('n5', st, en, '#n5-nt, #n5-team { opacity: 0; }', html, js, stage=(1.06, 690))
K.fx('notify', t_ya - 0.25)

# ---------- scene 6 · end ----------
st, en = K.start('s6'), K.end('s6')
t_bot = K.at('s6', 'bot'); t_mark = K.at('s6', 'aivacs'); t_demo = K.at('s6', 'demo')
kw = f"""<div id="e-kw" style="position:absolute;left:0;right:0;top:330px;text-align:center">
  <div style="font:700 40px 'Jakarta';color:#C9D4DD;display:flex;justify-content:center;align-items:center;gap:14px"><i class="ic" style="width:46px;height:46px;color:#25D366">{icon('si:whatsapp')}</i>Escríbenos por WhatsApp</div>
  <div id="e-key" style="position:relative;overflow:hidden;display:inline-block;margin-top:18px;padding:18px 54px;border-radius:26px;background:#4BBFEF;color:#04121B;font:800 120px 'Jakarta';box-shadow:0 0 70px rgba(75,191,239,.6)">BOT<span id="e-ksw" style="position:absolute;top:-20px;bottom:-20px;left:0;width:90px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.6),transparent)"></span></div>
  <div style="font:700 34px 'Jakarta';color:#C9D4DD;margin-top:22px">y te enseño la demo</div></div>"""
kw_js = f"""tl.fromTo("#e-kw", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)" }}, {round(max(0.05, t_bot - st - 0.2), 3)});
tl.to("#e-kw", {{ scale: 1.04, duration: {round(max(0.5, t_mark - t_bot - 1.0), 3)}, ease: "none" }}, {round(max(0.05, t_bot - st - 0.2) + 0.45, 3)});
tl.set("#e-ksw", {{ x: -160, skewX: -18 }}, 0);
tl.to("#e-ksw", {{ x: 420, duration: 0.7, ease: "power2.inOut" }}, {round(max(0.05, t_bot - st - 0.2) + 0.75, 3)});
tl.set("#e-ksw", {{ x: -160 }}, {round(max(0.05, t_bot - st - 0.2) + 1.5, 3)});
tl.to("#e-ksw", {{ x: 420, duration: 0.7, ease: "power2.inOut" }}, {round(max(0.05, t_bot - st - 0.2) + 1.5, 3)});
tl.to("#e-key", {{ scale: 0.92, duration: 0.1, ease: "power2.in", yoyo: true, repeat: 1 }}, {round(t_demo - st - 0.05, 3)});
tl.to("#e-key", {{ boxShadow: "0 0 110px rgba(75,191,239,.95)", duration: 0.3, ease: "power2.out", yoyo: true, repeat: 1 }}, {round(t_demo - st, 3)});
tl.to("#e-kw", {{ opacity: 0, y: -40, duration: 0.35, ease: "power2.in" }}, {round(t_mark - st - 0.75, 3)});"""
css, html, js = endcard(K, 'e', st, t_mark, JH, 250, 930, 580, 'Escríbenos «BOT» por WhatsApp', '+34 603 82 96 57', extra_html=kw, extra_js=kw_js,
                        css_extra='#e-kw { opacity: 0; }', jh_at=st)
K.add_scene('e', st, en, css, html, js)
K.fx('pop', t_bot)

groups = K.captions({'whatsapp', 'inteligencia', 'artificial', 'entiende', 'preguntas', 'sistema', 'pdf', 'envía', 'tiene', 'bot', 'demo', 'aivacs', 'presupuesto'}, until=st)
K.write_index(bgm_volume=0.26)
print('total', K.total)
for g in groups:
    print(g)
