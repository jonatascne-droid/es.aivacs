"""Reel de quarta 4 · Un «adelante», cinco herramientas (n8n). Usage: reel_quarta_n8n.py PROJECT_DIR"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
from vkit_explicativo import Kit, icon, phone, wa_header, endcard, E  # noqa: E402

P = sys.argv[1]
K = Kit(P)
JH = 'assets/img/jhony.png'   # the cutout already in the project (copy one from AIVACS_FOTOS for a new project)

# ---------- scene 1 · ¡Adelante! ----------
st, en = K.start('s1'), K.end('s1')
L = lambda t: round(t - st, 3)
t_resp = K.at('s1', 'responde'); t_ad = K.at('s1', 'adelante')
chat = f"""{wa_header('Carlos', 'en línea', 'C')}
<div style="position:absolute;left:0;right:0;top:138px;bottom:0;background:#0B141A;padding:26px 18px;display:flex;flex-direction:column;justify-content:flex-end;gap:14px;padding-bottom:80px">
  <div class="bub-out" style="opacity:.7">Te envío el presupuesto del baño en PDF.<div class="ts" style="color:#9FC9BD">10:02 ✓✓</div></div>
  <div id="f1-yes" class="bub-in" style="font:800 46px 'Jakarta';padding:20px 28px">¡Adelante!<div class="ts" style="font-weight:400">10:04</div></div></div>"""
html = phone('f1-ph', '#0B141A', chat, time='10:04') + '<div id="f1-dot" style="position:absolute;left:510px;top:860px;width:60px;height:60px;border-radius:50%;background:#4BBFEF;box-shadow:0 0 40px #4BBFEF;opacity:0;z-index:20"></div>'
js = f"""tl.fromTo("#f1-ph", {{ scale: 1 }}, {{ scale: 1.04, duration: {L(en) - 0.7}, ease: "none" }}, 0);
tl.fromTo("#f1-yes", {{ opacity: 0, y: 40, scale: 0.85 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(1.8)" }}, {max(0.15, L(t_ad) - 0.25)});
tl.to("#f1-ph", {{ opacity: 0, scale: 0.9, duration: 0.4, ease: "power2.in" }}, {L(en) - 0.65});
tl.fromTo("#f1-dot", {{ opacity: 0, scale: 0.3 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }}, {L(en) - 0.55});
tl.to("#f1-dot", {{ y: -560, duration: 0.4, ease: "power2.in" }}, {L(en) - 0.35});"""
K.add_scene('f1', st, en, '#f1-yes { opacity: 0; }', html, js, stage=(1.06, 690))
K.fx('pop', t_ad - 0.2)

# ---------- scene 2 · the flow (s2..s5) ----------
st, en = K.start('s2'), K.end('s5')
L = lambda t: round(t - st, 3)
t_n8n = K.words('s2')[1][1]; t_entra = K.at('s2', 'entra'); t_flujo = K.at('s2', 'flujo')
t_crea = K.at('s3', 'crea'); t_obra = K.at('s3', 'obra')
t_emite = K.at('s4', 'emite'); t_fact = K.at('s4', 'factura'); t_veri = K.at('s4', 'verifactu')
t_agenda = K.at('s5', 'agenda'); t_avisa = K.at('s5', 'avisa')
nodes = [
    ('n0', 'si:whatsapp', '#25D366', 'WhatsApp', 'Mensaje recibido', '«¡Adelante!» de Carlos', 240, 270, 600),
    ('n1', 'layout-dashboard', '#4BBFEF', 'Obra Organize', 'Crear obra', 'Obra · Baño Carlos creada', 240, 480, 600),
    ('n2', 'receipt', '#4BBFEF', 'Emite Fácil', 'Emitir factura', 'F-2026-0148 · Verifactu', 240, 690, 600),
    ('n3', 'calendar-check', '#4BBFEF', 'Agenda', 'Agendar visita', 'Jueves · 10:00', 60, 900, 450),
    ('n4', 'users', '#4BBFEF', 'Equipo', 'Avisar al equipo', 'Aviso enviado', 570, 900, 450),
]
nh = 150
nhtml = ''
for nid, ic, col, app, title, done, x, y, w in nodes:
    nhtml += (f'<div class="nd" id="f-{nid}" style="left:{x}px;top:{y}px;width:{w}px">'
              f'<div class="nic" style="color:{col}"><i class="ic" style="width:56px;height:56px">{icon(ic)}</i></div>'
              f'<div style="min-width:0"><div class="napp">{app}</div><div class="ntit">{title}</div><div class="ndone" id="f-{nid}-d"><i class="ic" style="width:24px;height:24px">{icon("circle-check")}</i>{done}</div></div></div>')
# wires: (from node, to node) as bezier from bottom centre to top centre
def ctr(n, side):
    _, _, _, _, _, _, x, y, w = [m for m in nodes if m[0] == n][0]
    return (x + w / 2, y + (nh if side == 'b' else 0))
wires = [('n0', 'n1'), ('n1', 'n2'), ('n2', 'n3'), ('n2', 'n4')]
whtml = ''
for i, (a, b) in enumerate(wires):
    (x1, y1), (x2, y2) = ctr(a, 'b'), ctr(b, 't')
    my = (y1 + y2) / 2
    d = f'M{x1:.0f} {y1:.0f} C {x1:.0f} {my:.0f}, {x2:.0f} {my:.0f}, {x2:.0f} {y2:.0f}'
    whtml += f'<path d="{d}" stroke="#26333F" stroke-width="6" fill="none"/><path id="f-w{i}" d="{d}" stroke="#4BBFEF" stroke-width="6" fill="none" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/>'
html = f"""<div id="f-head" style="position:absolute;left:0;right:0;top:196px;display:flex;justify-content:center">
  <span style="display:inline-flex;align-items:center;gap:14px;padding:12px 24px;border-radius:999px;background:#0F1821;border:1.5px solid rgba(234,75,113,.6);font:800 28px 'Jakarta'">
    <i class="ic" style="width:34px;height:34px;color:#EA4B71">{icon('workflow')}</i>n8n · flujo de automatización</span></div>
<svg style="position:absolute;left:0;top:0" width="1080" height="1300" viewBox="0 0 1080 1300">{whtml}</svg>
{nhtml}
<div id="f-dot" style="position:absolute;left:510px;top:240px;width:60px;height:60px;border-radius:50%;background:#4BBFEF;box-shadow:0 0 40px #4BBFEF;z-index:20"></div>"""
css = f""".nd {{ position: absolute; height: {nh}px; display: flex; align-items: center; gap: 22px; padding: 0 26px; border-radius: 26px;
  background: linear-gradient(170deg, #121B24, #0B1117); border: 2px solid #26333F; box-shadow: 0 30px 60px rgba(0,0,0,.5); opacity: 0; }}
.nic {{ width: 92px; height: 92px; border-radius: 22px; background: #0E161E; border: 1.5px solid rgba(110,210,250,.25); display: grid; place-items: center; flex: none; }}
.napp {{ font: 500 22px "JetBrains Mono"; color: #9AA5B1; }}
.ntit {{ font: 800 34px "Jakarta"; line-height: 1.1; margin-top: 2px; }}
.ndone {{ display: flex; align-items: center; gap: 8px; font: 700 22px "DMSans"; color: #7BE3A6; margin-top: 6px; opacity: 0; white-space: nowrap; }}
#f-head {{ opacity: 0; }}"""
def light(nid, t):
    return (f'tl.to("#f-{nid}", {{ borderColor: "#4BBFEF", boxShadow: "0 0 50px rgba(75,191,239,.45), 0 30px 60px rgba(0,0,0,.5)", duration: 0.3 }}, {L(t):.3f});\n'
            f'tl.fromTo("#f-{nid}-d", {{ opacity: 0, x: -14 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "power3.out" }}, {L(t) + 0.15:.3f});\n')
def travel(i, a, b, t):
    (x1, y1), (x2, y2) = ctr(a, 'b'), ctr(b, 't')
    return (f'tl.to("#f-w{i}", {{ strokeDashoffset: 0, duration: 0.5, ease: "power1.inOut" }}, {L(t) - 0.5:.3f});\n'
            f'tl.to("#f-dot", {{ x: {x2 - 540:.0f}, y: {y2 - 270:.0f}, duration: 0.5, ease: "power1.inOut" }}, {L(t) - 0.5:.3f});\n')
js = f"""tl.fromTo("#f-dot", {{ x: 0, y: 0, opacity: 1 }}, {{ x: 0, y: 30, opacity: 1, duration: 0.3, ease: "power2.out" }}, 0);
tl.fromTo("#f-head", {{ opacity: 0, y: -20 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }}, {max(0.1, L(t_n8n) - 0.2)});
tl.fromTo("#f-n0", {{ opacity: 0, scale: 0.9 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.6)" }}, {max(0.2, L(t_entra) - 0.3)});
{light('n0', t_entra)}
{''.join(f'tl.fromTo("#f-{n}", {{ opacity: 0, y: 30 }}, {{ opacity: 0.55, y: 0, duration: 0.35, ease: "power3.out" }}, {L(t_flujo) + i * 0.12:.3f});' + chr(10) for i, n in enumerate(['n1', 'n2', 'n3', 'n4']))}
{travel(0, 'n0', 'n1', t_crea + 0.15)}tl.to("#f-n1", {{ opacity: 1, duration: 0.2 }}, {L(t_crea) - 0.1:.3f});
{light('n1', t_obra)}
{travel(1, 'n1', 'n2', t_emite + 0.15)}tl.to("#f-n2", {{ opacity: 1, duration: 0.2 }}, {L(t_emite) - 0.1:.3f});
{light('n2', t_fact)}
{travel(2, 'n2', 'n3', t_agenda + 0.15)}tl.to("#f-n3", {{ opacity: 1, duration: 0.2 }}, {L(t_agenda) - 0.1:.3f});
{light('n3', t_agenda + 0.2)}
tl.to("#f-w3", {{ strokeDashoffset: 0, duration: 0.5, ease: "power1.inOut" }}, {L(t_avisa) - 0.35:.3f});
tl.to("#f-n4", {{ opacity: 1, duration: 0.2 }}, {L(t_avisa) - 0.1:.3f});
{light('n4', t_avisa + 0.15)}
tl.to("#f-dot", {{ opacity: 0, duration: 0.2 }}, {L(t_avisa) + 0.2:.3f});
{''.join(f'tl.to("#f-{n}", {{ borderColor: "rgba(110,210,250,.75)", duration: 0.16, ease: "power2.out", yoyo: true, repeat: 1 }}, {L(t_flujo) + 0.9 + i * 0.14:.3f});' + chr(10) for i, n in enumerate(['n1', 'n2', 'n3', 'n4']))}{''.join(f'tl.to("#f-dot", {{ scale: 1.35, duration: 0.35, ease: "power2.inOut", yoyo: true, repeat: 1 }}, {t:.3f});' + chr(10) for t in [L(t_entra) + 0.5 + 0.9 * j for j in range(40)] if t < L(t_crea) - 0.45)}
tl.to(["#f-n0", "#f-n1", "#f-n2", "#f-n3", "#f-n4", "#f-head"], {{ y: "-=1300", duration: 0.32, ease: "power3.in" }}, {L(en) - 0.3:.3f});"""
K.add_scene('flow', st, en, css, html, js, stage=(1.0, 623))
for t in (t_obra, t_fact, t_agenda + 0.2, t_avisa + 0.15):
    K.fx('pop', t)

# ---------- scene 3 · end ----------
st, en = K.start('s6'), K.end('s6')
w6 = K.words('s6')
t_msg, t_cinco, t_nadie, t_mark = w6[1][1], K.at('s6', 'cinco'), K.at('s6', 'nadie'), K.at('s6', 'aivacs')
tools = [('si:whatsapp', '#25D366'), ('layout-dashboard', '#4BBFEF'), ('receipt', '#4BBFEF'), ('calendar-check', '#4BBFEF'), ('users', '#4BBFEF')]
tiles = ''.join(f'<div class="tile" id="e-t{i}" style="left:{90 + i * 190}px;top:470px;width:140px;height:140px;color:{c}"><i class="ic" style="width:64px;height:64px">{icon(ic)}</i></div>' for i, (ic, c) in enumerate(tools))
stats = f"""<div id="e-stats" style="position:absolute;inset:0">{tiles}
<div id="e-s1" class="st" style="top:250px"><b>1</b> mensaje</div>
<div id="e-s2" class="st" style="top:660px"><b>5</b> herramientas</div>
<div id="e-s3" class="st" style="top:760px"><b>0</b> datos copiados a mano</div></div>"""
stats_js = f"""tl.set("#e-stats", {{ scale: 1.12, y: 340, transformOrigin: "540px 540px" }}, 0);
tl.to("#e-stats", {{ scale: 1.16, duration: {round(t_mark - st, 3)}, ease: "none" }}, 0);
tl.fromTo("#e-s1", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }}, 0);
{''.join(f'tl.fromTo("#e-t{i}", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {round(t_cinco - st - 0.1 + i * 0.08, 3)});' + chr(10) for i in range(5))}
tl.fromTo("#e-s2", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }}, {round(t_cinco - st + 0.2, 3)});
tl.fromTo("#e-s3", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }}, {round(t_nadie - st, 3)});
tl.to(["#e-s1", "#e-s2", "#e-s3", "#e-t0", "#e-t1", "#e-t2", "#e-t3", "#e-t4"], {{ opacity: 0, y: -30, duration: 0.35, ease: "power2.in" }}, {round(t_mark - st - 0.75, 3)});"""
st_css = """.st { position: absolute; left: 0; right: 0; text-align: center; font: 700 44px "Jakarta"; color: #C9D4DD; opacity: 0; }
.st b { font: 800 72px "Jakarta"; color: #4BBFEF; margin-right: 10px; }
#e-t0, #e-t1, #e-t2, #e-t3, #e-t4 { opacity: 0; }"""
css, html, js = endcard(K, 'e', st, t_mark, JH, 250, 930, 580, 'Lo montamos para tu negocio', '+34 603 82 96 57', extra_html=stats, extra_js=stats_js,
                        css_extra=st_css, jh_at=t_mark + 0.3)
K.add_scene('e', st, en, css, html, js)

groups = K.captions({'adelante', 'n8n', 'automatización', 'obra', 'sistema', 'factura', 'verifactu', 'visita', 'equipo', 'cinco', 'herramientas', 'aivacs'}, until=t_mark - 0.3)
K.write_index(bgm_volume=0.16, bgm_media_start=5)
print('total', K.total)
for g in groups:
    print(g)
