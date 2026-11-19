"""Reel de quarta 1 · El recorrido de Lucía (ecosistema digital). Usage: reel_quarta_ecosistema.py PROJECT_DIR
Scenes keep local times (seconds from each scene's start); the kit centres each one on a stage."""
import os
import re
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
from vkit_explicativo import Kit, icon, endcard, E  # noqa: E402

P = sys.argv[1]
K = Kit(P)
JH = 'assets/img/jhony.png'   # the cutout already in the project (copy one from AIVACS_FOTOS for a new project)
meta = K.meta
IDS = K.ids
VO_OFF = 0.15
starts = [K.start(s) for s in IDS]
durs = [K.ld[s] for s in IDS]
TOTAL = K.total


def words(sid):
    """script words with transcript timings (local to the scene, VO offset included)"""
    toks = meta[sid]['text'].split()
    tw = meta[sid].get('words') or []
    out = []
    if len(tw) == len(toks):
        for tok, w in zip(toks, tw):
            out.append((tok, VO_OFF + w['start'], VO_OFF + w['end']))
    else:  # proportional fallback
        total = sum(len(x) for x in toks); acc = 0; D = meta[sid]['duration_s']
        for tok in toks:
            s = VO_OFF + D * acc / total; acc += len(tok); out.append((tok, s, VO_OFF + D * acc / total))
    return out


def at(sid, word_prefix, which='start', nth=0):
    hits = [w for w in words(sid) if re.sub(r'[^\wáéíóúñ]', '', w[0].lower()).startswith(word_prefix.lower())]
    w = hits[nth]
    return round(w[1] if which == 'start' else w[2], 3)


V1CSS = """.grow { position: absolute; left: 294px; top: 184px; width: 492px; height: 1012px; transform-origin: 0 0; background: #4BBFEF; border-radius: 40px; z-index: 30; opacity: 0; }
.finger { position: absolute; width: 70px; height: 70px; border-radius: 50%; background: rgba(255,255,255,.85); box-shadow: 0 0 0 10px rgba(255,255,255,.25); z-index: 40; opacity: 0; }
.ripple { position: absolute; width: 70px; height: 70px; border-radius: 50%; border: 4px solid #4BBFEF; z-index: 39; opacity: 0; }
.btn { display: flex; align-items: center; justify-content: space-between; padding: 0 22px; font: 700 21px "DMSans"; }
"""


def phone(pid, screen_bg, inner, time='22:40', light=False):
    col = '#000' if light else '#fff'
    return (f'<div class="ph" id="{pid}"><div class="scr" style="background:{screen_bg}">'
            f'<div class="notch"></div><div class="sb" style="color:{col}"><span class="mono">{time}</span><span>●●● 5G</span></div>'
            f'{inner}</div></div>')


def tap_js(prefix, x, y, t_tap):
    """finger moves in, taps at t_tap (absolute coords inside #root)"""
    return f"""
tl.fromTo("#{prefix}-finger", {{ opacity: 0, x: {x + 120}, y: {y + 160} }}, {{ opacity: 1, x: {x}, y: {y}, duration: 0.35, ease: "power3.out" }}, {t_tap - 0.4});
tl.to("#{prefix}-finger", {{ scale: 0.82, duration: 0.08, ease: "power2.in" }}, {t_tap});
tl.to("#{prefix}-finger", {{ scale: 1, duration: 0.12, ease: "power2.out" }}, {t_tap + 0.08});
tl.fromTo("#{prefix}-ripple", {{ opacity: 0.9, scale: 0.4, x: {x}, y: {y} }}, {{ opacity: 0, scale: 2.2, duration: 0.45, ease: "power2.out", immediateRender: false }}, {t_tap});
tl.to("#{prefix}-finger", {{ opacity: 0, duration: 0.2 }}, {t_tap + 0.3});
"""


def grow_js(prefix, x, y, w, h, t0, dur):
    """the tapped button grows into the next screen (phone screen box 294,184 -> 492x1012), transforms only"""
    return f"""
tl.set("#{prefix}-grow", {{ opacity: 1, x: {x - 294}, y: {y - 184}, scaleX: {w / 492:.4f}, scaleY: {h / 1012:.4f} }}, {t0});
tl.to("#{prefix}-grow", {{ x: 0, y: 0, scaleX: 1, scaleY: 1, duration: {dur}, ease: "power3.inOut" }}, {t0});
"""


def tapper(prefix):
    return f'<div class="finger" id="{prefix}-finger" style="left:0;top:0" data-layout-allow-occlusion></div><div class="ripple" id="{prefix}-ripple" style="left:0;top:0"></div><div class="grow" id="{prefix}-grow" data-layout-allow-occlusion></div>'


def ent(sel, t0, y=40, d=0.5, extra=''):
    return f'tl.fromTo("{sel}", {{ opacity: 0, y: {y} {extra} }}, {{ opacity: 1, y: 0, duration: {d}, ease: "power3.out" }}, {t0});\n'


# ---------- 1 · anuncio ----------
s = 's1'; D = durs[0]
t_ad = at(s, 'anuncio'); t_tap = round(D - 0.85, 3)
ad = f"""
<div style="position:absolute;left:0;right:0;top:54px;height:64px;display:flex;align-items:center;justify-content:space-between;padding:0 26px;border-bottom:1px solid #222">
  <b style="font:700 30px 'Jakarta';letter-spacing:-.02em">Instagram</b><span style="display:flex;gap:18px"><i class="ic" style="width:30px;height:30px;color:#fff">{icon('heart-handshake')}</i></span></div>
<div id="s1-post" style="position:absolute;left:0;right:0;top:120px">
  <div style="display:flex;align-items:center;gap:14px;padding:16px 20px">
    <div style="width:52px;height:52px;border-radius:50%;background:linear-gradient(135deg,#4BBFEF,#2A8BBF);display:grid;place-items:center;font:800 18px 'Jakarta';color:#04121B">RM</div>
    <div><b style="font:700 21px 'DMSans'">reformasmartin</b><br><span style="font-size:17px;color:#aaa">Publicidad</span></div></div>
  <div id="s1-creative" style="position:relative;height:492px;background:linear-gradient(160deg,#16364A,#0B1A24 60%,#07121A);overflow:hidden">
    <div style="position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.06) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.06) 2px,transparent 2px);background-size:70px 70px"></div>
    <div style="position:absolute;left:34px;top:60px;right:30px">
      <div class="mono" style="font-size:18px;letter-spacing:.14em;color:#7FD3F5">REFORMAS EN MADRID</div>
      <div style="font:800 54px/1.02 'Jakarta';margin-top:16px">Tu baño nuevo,<br><span style="color:#4BBFEF">sin sorpresas.</span></div>
      <div style="font-size:22px;color:#C9D6DF;margin-top:18px">Presupuesto cerrado antes de empezar.</div></div>
    <i class="ic" style="position:absolute;right:30px;bottom:26px;width:110px;height:110px;color:#4BBFEF">{icon('sparkles')}</i></div>
  <div id="s1-cta" class="btn" style="height:62px;background:#4BBFEF;color:#04121B">Más información <i class="ic" style="width:26px;height:26px">{icon('arrow-right')}</i></div>
  <div style="display:flex;gap:20px;padding:16px 20px;color:#fff"><i class="ic" style="width:32px;height:32px">{icon('heart-handshake')}</i><i class="ic" style="width:32px;height:32px">{icon('message-circle')}</i></div>
  <div style="padding:0 20px;font-size:19px;color:#ddd"><b>reformasmartin</b> Reformas integrales con presupuesto cerrado y plazos claros.</div>
</div>"""
html = f"""{phone('s1-ph', '#000', ad)}
<div id="s1-ring" style="position:absolute;left:294px;top:384px;width:492px;height:620px;border:4px solid #4BBFEF;border-radius:10px;box-shadow:0 0 40px rgba(75,191,239,.6);opacity:0"></div>
<div id="s1-stamp" style="position:absolute;left:40px;top:250px;display:flex;align-items:center;gap:14px;padding:14px 22px;border-radius:20px;background:#0F1821;border:1.5px solid rgba(110,210,250,.5);box-shadow:0 20px 40px rgba(0,0,0,.5);z-index:20">
  <div style="width:46px;height:46px;border-radius:50%;background:#E8B7A0;display:grid;place-items:center;font:800 20px 'Jakarta';color:#3A2018">L</div>
  <div><b style="font:800 28px 'Jakarta'">Lucía</b><br><span class="mono" style="font-size:20px;color:#7FD3F5">22:40</span></div></div>
{tapper('s1')}"""
cx, cy = 280 + 14 + 246, 170 + 14 + 120 + 84 + 492 + 31  # CTA centre in root coords
js = f"""tl.fromTo("#s1-ph", {{ scale: 1 }}, {{ scale: 1.035, duration: {D}, ease: "none" }}, 0);
tl.fromTo("#s1-stamp", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.8)" }}, 0.3);
tl.fromTo("#s1-ring", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, {t_ad});
tl.to("#s1-ring", {{ opacity: 0, duration: 0.25 }}, {t_tap - 0.45});
{tap_js('s1', cx - 35, cy - 35, t_tap)}
{grow_js('s1', 294, cy - 31, 492, 62, t_tap + 0.25, D - t_tap - 0.25 - 0.02)}"""
K.add_scene(s, starts[0], starts[0] + D, V1CSS + '', html, js, stage=(1.06, 690))
SFX = [('pop', starts[0] + 0.3), ('click', starts[0] + t_tap)]

# ---------- 2 · web ----------
s = 's2'; D = durs[1]
t_obras = at(s, 'obras'); t_tap = round(D - 0.75, 3)
tiles = ''.join(f'<div style="height:200px;border-radius:16px;background:linear-gradient(150deg,{c},#0B141B);position:relative"><span style="position:absolute;left:14px;bottom:12px;font:700 19px \'Jakarta\'">{n}</span></div>'
                for n, c in [('Baño · Chamberí', '#1E4A61'), ('Cocina · Retiro', '#2B4F63'), ('Salón · Tetuán', '#1B3B4D'), ('Baño · Usera', '#24506A')])
web = f"""
<div style="position:absolute;left:0;right:0;top:54px;height:62px;display:flex;align-items:center;gap:12px;padding:0 20px;background:#151D26;z-index:4">
  <span class="mono" style="flex:1;padding:8px 14px;border-radius:10px;background:#0B1117;font-size:17px;color:#9AA5B1">reformasmartin.es</span></div>
<div id="s2-page" style="position:absolute;left:0;right:0;top:116px;padding:30px 26px">
  <div style="display:flex;justify-content:space-between;align-items:center;font:800 24px 'Jakarta'">Reformas Martín <span style="font:500 18px 'DMSans';color:#9AA5B1">Menú</span></div>
  <div style="margin-top:34px;height:300px;border-radius:22px;background:linear-gradient(160deg,#1E4A61,#0B1A24);padding:30px 26px">
    <div style="font:800 46px/1.04 'Jakarta'">Reformas integrales en <span style="color:#4BBFEF">Madrid.</span></div>
    <div style="font-size:20px;color:#C9D6DF;margin-top:14px">Presupuesto en 1 minuto, sin compromiso.</div></div>
  <div style="margin-top:30px;font:800 30px 'Jakarta'">Nuestras obras</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:16px">{tiles}</div>
  <div style="margin-top:26px;font-size:19px;color:#9AA5B1">Más de 15 años reformando casas en Madrid.</div>
</div>
<div id="s2-cta" class="btn" style="position:absolute;left:22px;right:22px;bottom:34px;height:70px;border-radius:18px;background:#4BBFEF;color:#04121B;z-index:6">
  <span style="display:flex;align-items:center;gap:12px"><i class="ic" style="width:30px;height:30px">{icon('si:whatsapp')}</i>Pedir presupuesto</span><i class="ic" style="width:26px;height:26px">{icon('arrow-right')}</i></div>"""
html = f"""{phone('s2-ph', '#0B1117', web)}
<div id="s2-cover" data-layout-allow-occlusion style="position:absolute;left:294px;top:184px;width:492px;height:1012px;border-radius:52px;background:#4BBFEF;z-index:30"></div>
{tapper('s2')}"""
cx, cy = 540, 170 + 14 + 1012 - 34 - 35
js = f"""tl.fromTo("#s2-cover", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.35, ease: "power2.out" }}, 0.02);
tl.fromTo("#s2-page", {{ y: 30 }}, {{ y: 0, duration: 0.5, ease: "power3.out" }}, 0.05);
tl.to("#s2-page", {{ y: -470, duration: 0.8, ease: "power2.inOut" }}, {t_obras - 0.25});
{tap_js('s2', cx - 35, cy - 35, t_tap)}
{grow_js('s2', 316, cy - 35, 448, 70, t_tap + 0.22, D - t_tap - 0.22 - 0.02)}"""
K.add_scene(s, starts[1], starts[1] + D, V1CSS + '', html, js, stage=(1.06, 690))
SFX += [('whoosh', starts[1]), ('click', starts[1] + t_tap)]

# ---------- 3 · whatsapp ----------
s = 's3'; D = durs[2]
t_resp = at(s, 'whatsapp'); t_env = at(s, 'envía')
wa = f"""
<div style="position:absolute;left:0;right:0;top:54px;height:84px;display:flex;align-items:center;gap:14px;padding:0 20px;background:#1F2C34;z-index:4">
  <div style="width:56px;height:56px;border-radius:50%;background:linear-gradient(135deg,#4BBFEF,#2A8BBF);display:grid;place-items:center;font:800 19px 'Jakarta';color:#04121B">RM</div>
  <div><b style="font:700 22px 'Jakarta'">Reformas Martín</b><br><span style="font-size:17px;color:#8696A0">en línea</span></div></div>
<div style="position:absolute;left:0;right:0;top:138px;bottom:0;background:#0B141A;padding:26px 18px;display:flex;flex-direction:column;gap:14px">
  <div id="s3-m1" style="align-self:flex-end;max-width:80%;background:#005C4B;border-radius:18px 4px 18px 18px;padding:14px 18px;font-size:22px;line-height:1.32">Hola, quiero presupuesto para reformar mi baño.<div class="mono" style="text-align:right;font-size:14px;color:#9FC9BD;margin-top:4px">22:42 ✓✓</div></div>
  <div style="position:relative;align-self:flex-start;max-width:82%">
    <div id="s3-m2" style="background:#202C33;border-radius:4px 18px 18px 18px;padding:14px 18px;font-size:22px;line-height:1.32">¡Hola, Lucía! Te lo preparo ahora mismo.<div class="mono" style="text-align:right;font-size:14px;color:#8696A0;margin-top:4px">22:42</div></div>
    <div id="s3-typing" style="position:absolute;left:0;top:0;background:#202C33;border-radius:4px 18px 18px 18px;padding:18px 22px;display:flex;gap:8px">
      <i id="s3-d1" style="width:12px;height:12px;border-radius:50%;background:#8696A0;display:block"></i><i id="s3-d2" style="width:12px;height:12px;border-radius:50%;background:#8696A0;display:block"></i><i id="s3-d3" style="width:12px;height:12px;border-radius:50%;background:#8696A0;display:block"></i></div></div>
  <div id="s3-pdf" style="align-self:flex-start;width:82%;background:#202C33;border-radius:18px;padding:12px">
    <div style="display:flex;align-items:center;gap:14px;background:rgba(0,0,0,.25);border-radius:12px;padding:14px">
      <div style="width:50px;height:62px;border-radius:7px;background:#E5484D;display:grid;place-items:center;font:700 15px 'JetBrains Mono';color:#fff">PDF</div>
      <div><b style="font-size:21px">Presupuesto_Lucia.pdf</b><br><span style="font-size:17px;color:#9FB3BD">2 páginas · 180 kB</span></div></div>
    <div class="mono" style="text-align:right;font-size:14px;color:#8696A0;margin-top:6px">22:43</div></div>
</div>"""
html = f"""{phone('s3-ph', '#0B141A', wa)}
<div id="s3-cover" data-layout-allow-occlusion style="position:absolute;left:294px;top:184px;width:492px;height:1012px;border-radius:52px;background:#4BBFEF;z-index:30"></div>"""
js = f"""tl.fromTo("#s3-cover", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.35, ease: "power2.out" }}, 0.02);
tl.fromTo("#s3-m1", {{ opacity: 0, y: 30, scale: 0.92 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(1.6)" }}, 0.2);
tl.fromTo("#s3-typing", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, {t_resp - 0.5});
tl.fromTo(["#s3-d1", "#s3-d2", "#s3-d3"], {{ y: 0 }}, {{ y: -8, duration: 0.18, ease: "power1.inOut", yoyo: true, repeat: 3, stagger: 0.1 }}, {t_resp - 0.45});
tl.to("#s3-typing", {{ opacity: 0, duration: 0.12 }}, {t_resp + 0.38});
tl.fromTo("#s3-m2", {{ opacity: 0, y: 30, scale: 0.92 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(1.6)" }}, {t_resp + 0.4});
tl.fromTo("#s3-pdf", {{ opacity: 0, y: 30, scale: 0.9 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(1.8)" }}, {t_env - 0.15});"""
K.add_scene(s, starts[2], starts[2] + D, V1CSS + '#s3-m2, #s3-pdf, #s3-typing { opacity: 0; }', html, js, stage=(1.06, 690))
SFX += [('pop', starts[2] + t_env - 0.12)]

# ---------- 4 · sistema ----------
s = 's4'; D = durs[3]
t_ap = at(s, 'aprueba'); t_sola = at(s, 'sola')
chat = f"""
<div style="position:absolute;left:0;right:0;top:54px;height:84px;display:flex;align-items:center;gap:14px;padding:0 20px;background:#1F2C34">
  <div style="width:56px;height:56px;border-radius:50%;background:linear-gradient(135deg,#4BBFEF,#2A8BBF);display:grid;place-items:center;font:800 19px 'Jakarta';color:#04121B">RM</div>
  <div><b style="font:700 22px 'Jakarta'">Reformas Martín</b><br><span style="font-size:17px;color:#8696A0">en línea</span></div></div>
<div style="position:absolute;left:0;right:0;top:138px;bottom:0;background:#0B141A;padding:26px 18px;display:flex;flex-direction:column;justify-content:flex-end;gap:14px;padding-bottom:60px">
  <div style="align-self:flex-start;width:82%;background:#202C33;border-radius:18px;padding:12px;opacity:.75">
    <div style="display:flex;align-items:center;gap:14px;background:rgba(0,0,0,.25);border-radius:12px;padding:14px">
      <div style="width:50px;height:62px;border-radius:7px;background:#E5484D;display:grid;place-items:center;font:700 15px 'JetBrains Mono';color:#fff">PDF</div>
      <div><b style="font-size:21px">Presupuesto_Lucia.pdf</b><br><span style="font-size:17px;color:#9FB3BD">2 páginas · 180 kB</span></div></div></div>
  <div id="s4-yes" style="align-self:flex-end;background:#005C4B;border-radius:18px 4px 18px 18px;padding:16px 24px;font:700 34px 'Jakarta'">¡Adelante!<div class="mono" style="text-align:right;font-size:14px;font-weight:400;color:#9FC9BD;margin-top:4px">22:45 ✓✓</div></div>
</div>"""
fields = ''.join(f'<div style="background:#0E161E;border:1px solid rgba(110,210,250,.18);border-radius:18px;padding:18px 20px"><div style="font-size:19px;color:#9AA5B1">{k}</div><div style="font:800 32px \'Jakarta\';margin-top:6px">{v}</div></div>'
                 for k, v in [('Presupuesto', '€ 4.850'), ('Inicio', '24 nov'), ('Equipo', '2 personas'), ('Plazo', '3 semanas')])
dash = f"""<div class="card" id="s4-dash" style="left:70px;top:330px;width:940px;padding:40px 44px">
  <div style="display:flex;align-items:center;gap:14px"><svg viewBox="0 0 100 100" width="44" height="44" fill="none"><path d="M50 7 L93 79 Q95 85 89 85 L11 85 Q5 85 7 79 Z" stroke="#4BBFEF" stroke-width="8" stroke-linejoin="round"/></svg>
    <b style="font:800 30px 'Jakarta'">Obra Organize</b><span class="mono" style="margin-left:auto;font-size:18px;color:#9AA5B1">OBRAS · NUEVA</span></div>
  <div style="font:800 54px 'Jakarta';margin-top:34px">Baño · Lucía Romero</div>
  <div style="position:relative;height:56px;margin-top:22px">
    <span id="s4-st1" class="pill" style="position:absolute;left:0;top:0;color:#F2C46B;background:rgba(242,196,107,.14);border:1px solid rgba(242,196,107,.45)">Presupuesto enviado</span>
    <span id="s4-st2" class="pill" style="position:absolute;left:0;top:0;color:#7BE3A6;background:rgba(46,204,113,.14);border:1px solid rgba(46,204,113,.45)"><i class="ic" style="width:24px;height:24px">{icon('circle-check')}</i> Aprobada · obra creada</span></div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:30px">{fields}</div>
  <div style="margin-top:28px;font-size:19px;color:#9AA5B1">Progreso</div>
  <div style="height:16px;border-radius:8px;background:#16202A;margin-top:10px;overflow:hidden"><div id="s4-bar" style="width:0;height:100%;background:#4BBFEF"></div></div>
  <div class="mono" style="margin-top:22px;font-size:17px;color:#6B7682">Reformas Martín es una empresa de ejemplo · datos ficticios</div></div>"""
html = f"""{phone('s4-ph', '#0B141A', chat, time='22:45')}
{dash}"""
js = f"""tl.fromTo("#s4-yes", {{ opacity: 0, y: 30, scale: 0.85 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(1.8)" }}, {max(0.2, t_ap - 0.3)});
tl.to("#s4-ph", {{ y: -1400, duration: 0.55, ease: "power3.in" }}, {t_ap + 0.75});
tl.set("#s4-dash", {{ opacity: 1, y: 1000 }}, {t_ap + 0.95});
tl.to("#s4-dash", {{ y: 0, duration: 0.6, ease: "expo.out" }}, {t_ap + 0.95});
tl.fromTo("#s4-st2", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }}, {t_sola});
tl.to("#s4-st1", {{ opacity: 0, duration: 0.15 }}, {t_sola});
tl.fromTo("#s4-bar", {{ width: "0%" }}, {{ width: "6%", duration: 0.5, ease: "power2.out" }}, {t_sola + 0.2});"""
K.add_scene(s, starts[3], starts[3] + D, V1CSS + '#s4-yes, #s4-dash, #s4-st2 { opacity: 0; }', html, js, stage=(1.06, 690))
SFX += [('pop', starts[3] + max(0.2, t_ap - 0.3)), ('pop', starts[3] + t_sola)]

# ---------- 5 · factura + contenido ----------
s = 's5'; D = durs[4]
t_fac = at(s, 'factura'); t_cont = at(s, 'contenido'); t_vuel = at(s, 'vuelva'); t_rec = at(s, 'recomiende')
inv = f"""<div class="card" id="s5-inv" style="left:150px;top:360px;width:780px;padding:44px 48px">
  <div style="display:flex;justify-content:space-between;align-items:flex-start">
    <div><div class="mono" style="font-size:20px;color:#9AA5B1;letter-spacing:.1em">FACTURA</div><b style="font:800 46px 'Jakarta'">F-2026-0148</b></div>
    <span class="pill" style="color:#7BE3A6;background:rgba(46,204,113,.14);border:1px solid rgba(46,204,113,.45)"><i class="ic" style="width:22px;height:22px">{icon('circle-check')}</i> Verifactu</span></div>
  <div style="margin-top:30px;font-size:22px;color:#9AA5B1">Cliente</div><div style="font-size:30px;font-weight:600">Lucía Romero</div>
  <div style="margin-top:28px;border-top:1px solid rgba(110,210,250,.15)">
    <div style="display:flex;justify-content:space-between;padding:16px 0;border-bottom:1px solid rgba(110,210,250,.1);font-size:25px"><span>Reforma de baño · 1ª parte</span><span>€ 2.004,13</span></div>
    <div style="display:flex;justify-content:space-between;padding:16px 0;border-bottom:1px solid rgba(110,210,250,.1);font-size:25px"><span>IVA 21 %</span><span>€ 420,87</span></div>
    <div style="display:flex;justify-content:space-between;padding:20px 0 0;font:800 40px 'Jakarta'"><span>Total</span><span style="color:#4BBFEF">€ 2.425,00</span></div></div>
  <div id="s5-sent" style="margin-top:26px;display:flex;align-items:center;gap:12px;font:700 26px 'Jakarta';color:#7BE3A6"><i class="ic" style="width:30px;height:30px;color:#25D366">{icon('si:whatsapp')}</i> Enviada a Lucía por WhatsApp</div></div>"""
post = f"""<div class="card" id="s5-post" style="left:170px;top:250px;width:740px;padding:0;overflow:hidden;background:#000;border-color:rgba(255,255,255,.18)">
  <div style="display:flex;align-items:center;gap:14px;padding:18px 22px">
    <div style="width:56px;height:56px;border-radius:50%;background:#E8B7A0;display:grid;place-items:center;font:800 22px 'Jakarta';color:#3A2018">L</div>
    <div><b style="font:700 23px 'DMSans'">lucia.romero</b><br><span style="font-size:18px;color:#aaa">Madrid</span></div></div>
  <div style="position:relative;height:600px;overflow:hidden;display:flex">
    <div style="flex:1;position:relative;background:repeating-linear-gradient(0deg,#6B5A48 0 58px,#564737 58px 61px),repeating-linear-gradient(90deg,transparent 0 58px,#564737 58px 61px);background-blend-mode:multiply">
      <div style="position:absolute;left:40px;right:40px;bottom:0;height:170px;background:#8A7B6A;border-radius:8px 8px 0 0"></div>
      <span style="position:absolute;left:20px;top:20px;padding:8px 16px;border-radius:999px;background:rgba(0,0,0,.6);font:800 22px 'Jakarta'">ANTES</span></div>
    <div style="width:6px;background:#fff"></div>
    <div style="flex:1;position:relative;background:repeating-linear-gradient(0deg,#EEF3F6 0 78px,#D6E0E6 78px 80px),repeating-linear-gradient(90deg,transparent 0 118px,#D6E0E6 118px 120px);background-blend-mode:multiply">
      <div style="position:absolute;left:70px;top:110px;width:220px;height:220px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#E8F7FF,#9FD8F0);border:8px solid #DDE6EB;box-shadow:0 0 40px rgba(159,216,240,.8)"></div>
      <div style="position:absolute;left:30px;right:30px;bottom:0;height:170px;background:#FFFFFF;border-radius:10px 10px 0 0;box-shadow:0 -4px 16px rgba(0,0,0,.12)"></div>
      <span style="position:absolute;right:20px;top:20px;padding:8px 16px;border-radius:999px;background:#4BBFEF;color:#04121B;font:800 22px 'Jakarta'">DESPUÉS</span></div>
    <i id="s5-heart" class="ic" style="position:absolute;left:50%;top:50%;width:230px;height:230px;margin:-115px 0 0 -115px;color:#fff;filter:drop-shadow(0 10px 30px rgba(0,0,0,.4))"><svg viewBox="0 0 24 24" fill="#fff"><path d="M12 21s-7.5-4.6-10-9.3C.3 8.3 2.4 4 6.4 4c2.2 0 3.6 1.2 4.6 2.6C12 5.2 13.4 4 15.6 4c4 0 6.1 4.3 4.4 7.7C19.5 16.4 12 21 12 21z"/></svg></i></div>
  <div style="display:flex;gap:22px;padding:18px 22px;color:#fff"><i class="ic" style="width:36px;height:36px">{icon('heart-handshake')}</i><i class="ic" style="width:36px;height:36px">{icon('message-circle')}</i></div>
  <div style="padding:0 22px 26px;font-size:23px;color:#ddd"><b>lucia.romero</b> ¡Por fin mi baño nuevo! Gracias, <span style="color:#4BBFEF">@reformasmartin</span></div></div>
<div id="s5-share" style="position:absolute;left:250px;top:1090px;display:flex;align-items:center;gap:14px;padding:16px 26px;border-radius:999px;background:#0F1821;border:1.5px solid rgba(110,210,250,.5);font:700 28px 'Jakarta';z-index:5">
  <i class="ic" style="width:32px;height:32px;color:#4BBFEF">{icon('arrow-right')}</i> Compartido con 3 amigos</div>"""
html = inv + post
js = f"""tl.set("#s5-inv", {{ opacity: 1, y: 420, rotation: -3 }}, 0);
tl.to("#s5-inv", {{ y: 0, rotation: 0, duration: 0.55, ease: "expo.out" }}, 0);
tl.fromTo("#s5-sent", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }}, {t_fac + 0.6});
tl.to("#s5-inv", {{ x: 900, y: -500, rotation: 18, opacity: 0, duration: 0.55, ease: "power2.in" }}, {t_cont - 0.55});
tl.fromTo("#s5-post", {{ opacity: 0, scale: 0.86, y: 60 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.55, ease: "power3.out" }}, {t_cont - 0.15});
tl.fromTo("#s5-heart", {{ opacity: 0, scale: 0.3 }}, {{ opacity: 1, scale: 1.1, duration: 0.3, ease: "back.out(2.4)" }}, {t_vuel - 0.05});
tl.to("#s5-heart", {{ opacity: 0, scale: 1.3, duration: 0.3, ease: "power2.in" }}, {t_vuel + 0.55});
tl.fromTo("#s5-share", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "back.out(1.6)" }}, {t_rec - 0.1});
tl.to(["#s5-post", "#s5-share"], {{ y: "-=1150", duration: 0.36, ease: "power3.in" }}, {D - 0.38:.3f});"""
K.add_scene(s, starts[4], starts[4] + D, V1CSS + '#s5-post, #s5-heart, #s5-share, #s5-sent { opacity: 0; }', html, js, stage=(1.15, 705))
SFX += [('whoosh', starts[4] + t_cont - 0.55), ('pop', starts[4] + t_vuel), ('whoosh', starts[4] + D - 0.4)]

# ---------- 6 · the ecosystem ring, then the end card ----------
s = 's6'; D = durs[5]
t_eco = at(s, 'ecosistema'); t_aiv = at(s, 'aivacs')
ring_icons = [('megaphone', 'Anuncios'), ('globe', 'Web'), ('si:whatsapp', 'WhatsApp'), ('layout-dashboard', 'Sistema'), ('receipt', 'Factura'), ('clapperboard', 'Contenido')]
import math
CX, CY, R = 540, 640, 300
pts = [(CX + R * math.cos(math.radians(-90 + i * 60)), CY + R * math.sin(math.radians(-90 + i * 60))) for i in range(6)]
nodes = ''
for i, ((ic, lab), (x, y)) in enumerate(zip(ring_icons, pts)):
    nodes += (f'<div class="nd" id="s6-n{i}" style="left:{x - 70:.0f}px;top:{y - 70:.0f}px"><i class="ic" style="width:66px;height:66px;color:#E9F8FF">{icon(ic)}</i></div>'
              f'<div class="lb" id="s6-l{i}" style="left:{x - 110:.0f}px;top:{y + 78:.0f}px">{lab}</div>')
segs = ''.join(f'<line id="s6-e{i}" x1="{pts[i][0]:.0f}" y1="{pts[i][1]:.0f}" x2="{pts[(i + 1) % 6][0]:.0f}" y2="{pts[(i + 1) % 6][1]:.0f}" stroke="#4BBFEF" stroke-width="5" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/>' for i in range(6))
css = """.nd { position: absolute; width: 140px; height: 140px; border-radius: 30%; display: grid; place-items: center;
  background: linear-gradient(145deg, rgba(110,210,250,.30), rgba(16,26,36,.92) 55%); border: 2px solid rgba(110,210,250,.6); box-shadow: 0 20px 40px rgba(0,0,0,.5); }
.lb { position: absolute; width: 220px; text-align: center; font: 800 26px "Jakarta"; }
.nd, .lb { opacity: 0; }"""
html = f"""<div id="s6-ring" style="position:absolute;inset:0">
<svg style="position:absolute;left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920">{segs}</svg>{nodes}</div>"""
t_out = t_aiv - 0.75
# the six pieces arrive one by one (no dead hold before "ecosistema"), the ring closes on the word, then the pieces flash in a chase
js = ''.join(f'tl.set("#s6-n{i}", {{ opacity: 1, scale: 0.4 }}, {i * 0.2:.3f});\ntl.to("#s6-n{i}", {{ scale: 1, duration: 0.4, ease: "{E['popOver']}" }}, {i * 0.2:.3f});\n'
             f'tl.fromTo("#s6-l{i}", {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "{E['softLand']}" }}, {0.14 + i * 0.2:.3f});\n' for i in range(6))
js += ''.join(f'tl.to("#s6-e{i}", {{ strokeDashoffset: 0, duration: 0.22, ease: "power1.inOut" }}, {t_eco - 0.4 + i * 0.16:.3f});\n' for i in range(6))
js += ''.join(f'tl.to("#s6-n{i}", {{ boxShadow: "0 0 40px rgba(75,191,239,.85), 0 20px 40px rgba(0,0,0,.5)", scale: 1.1, duration: 0.16, ease: "power2.out", yoyo: true, repeat: 1 }}, {t_eco + 0.6 + i * 0.11:.3f});\n' for i in range(6))
js += f'tl.to("#s6-ring", {{ opacity: 0, scale: 0.4, duration: 0.45, ease: "{E['accelExit']}" }}, {t_out:.3f});\n'
K.add_scene('s6', starts[5], starts[5] + t_out + 0.5, V1CSS + css, html, js, stage=(1.22, 659))
SFX += [('whoosh', starts[5] + t_eco - 0.45)]
T_MARK = starts[5] + t_aiv
est = T_MARK - 0.6
css, html, js = endcard(K, 'e', est, T_MARK, JH, 250, 930, 620, 'Diagnóstico gratis por WhatsApp', '+34 603 82 96 57')
K.add_scene('e', est, K.total, css, html, js)

KEY = {'anuncio', 'instagram', 'web', 'obras', 'whatsapp', 'presupuesto', 'sistema', 'factura', 'contenido', 'recomiende', 'ecosistema', 'aivacs', 'sola'}
for n, t in SFX:
    K.fx(n, t)
groups = K.captions(KEY, until=T_MARK - 0.3)
K.write_index(bgm_volume=0.26, bgm_media_start=0)
print('total', K.total)
for g in groups:
    print(g)
