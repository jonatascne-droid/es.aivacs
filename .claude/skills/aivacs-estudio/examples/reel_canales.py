"""Reel 1 · ¿Dónde te descubren? (canales de adquisición)."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
FOTOS = os.environ.get('AIVACS_FOTOS') or sys.exit('Defina AIVACS_FOTOS com a pasta das fotos recortadas do Jhony (o06chair.png, o11.png, o14.png, o17.png...)')
from vkit import Kit, icon, endcard, E

P = sys.argv[1]
K = Kit(P)
JH = K.image(os.path.join(FOTOS, 'o11.png'), 'jhony.png')
R = lambda t, st: round(t - st, 3)

# ---------- s1 · hook: whole words at speech rhythm, "canal" opens six paths ----------
st, en = 0.0, K.start('s2') + 0.35
w1 = K.words('s1')
sent1 = [w for w in w1 if w[1] < K.at('s1', 'te', nth=1)]
sent2 = [w for w in w1 if w[1] >= K.at('s1', 'te', nth=1)]
lines1 = [sent1[:2], sent1[2:5], sent1[5:]]
lines2 = [sent2[:2], sent2[2:6], sent2[6:]]


def block(bid, lines, top, big_last=False):
    h, j = f'<div id="{bid}" style="position:absolute;left:0;right:0;top:{top}px;text-align:center">', ''
    n = 0
    for li, ln in enumerate(lines):
        last = big_last and li == len(lines) - 1
        fs = 150 if last else (96 if (big_last and li == 0) else 104)
        h += f'<div class="hx" style="font-size:{fs}px;margin-top:{18 if li else 0}px">'
        for w in ln:
            cls = 'hx cy' if last else 'hx'
            h += f'<span id="{bid}w{n}" class="{cls}" style="display:inline-block;margin:0 .13em;opacity:0">{w[0]}</span>'
            j += f'tl.set("#{bid}w{n}", {{ y: 46, opacity: {1 if (bid == 'a' and n == 0) else 0} }}, 0);\n'
            t0 = 0 if (bid == 'a' and n == 0) else R(w[1] - 0.04, st)
            j += f'tl.to("#{bid}w{n}", {{ opacity: 1, duration: 0.1, ease: "none" }}, {t0});\n'
            j += f'tl.to("#{bid}w{n}", {{ y: 0, duration: 0.42, ease: "{E["softLand"]}" }}, {t0});\n'
            n += 1
        h += '</div>'
    return h + '</div>', j


h1, j1 = block('a', lines1, 640)
h2, j2 = block('b', lines2, 560, big_last=True)
cats = ['search', 'share-2', 'megaphone', 'users-round', 'map-pin', 'radio']
t_canal = K.at('s1', 'canal')
T2 = K.start('s2') - 0.05          # pan to the first station is centred here
en = T2 + 0.3
ring, rj = '', ''
for i, c in enumerate(cats):
    x, y = 105 + i * 150, 1060
    ring += f'<div id="t{i}" class="glass" style="position:absolute;left:{x}px;top:{y}px;width:120px;height:120px;border-radius:32%;display:grid;place-items:center;opacity:0"><i class="ic" style="width:56px;height:56px;color:#E9F8FF;filter:drop-shadow(0 0 10px rgba(75,191,239,.9))">{icon(c)}</i></div>'
    dx, dy = 540 - (x + 60), 870 - (y + 60)
    t0 = R(t_canal + 0.1 * i / 1.5 * 0.5, st)
    rj += f'tl.set("#t{i}", {{ opacity: 1, x: {dx}, y: {dy}, scale: .5 }}, {t0});\n'
    rj += f'tl.to("#t{i}", {{ x: 0, y: 0, scale: 1, duration: 0.55, ease: "{E["softLand"]}" }}, {t0});\n'
html = f'<div id="cam" style="position:absolute;inset:0">{h1}{h2}<div id="ringw" style="position:absolute;inset:0">{ring}</div></div>'
t_te = K.at('s1', 'te', nth=1)
js = j1 + j2 + rj + f"""
tl.to("#a", {{ y: -520, duration: 0.38, ease: "{E['accelExit']}" }}, {R(t_te - 0.36, st)});
tl.set("#a", {{ visibility: "hidden" }}, {R(t_te + 0.02, st)});
tl.fromTo("#ringw", {{ y: 0 }}, {{ y: -14, duration: {R(en - 0.6, t_canal + 0.6)}, ease: "none" }}, {R(t_canal + 0.6, st)});
tl.fromTo("#cam", {{ scale: 1 }}, {{ scale: 1.05, duration: {R(en - 0.6, st)}, ease: "none", transformOrigin: "540px 860px" }}, 0);
tl.to("#cam", {{ y: -1920, duration: 0.6, ease: "power3.inOut" }}, {R(en - 0.6, st)});
"""
K.add_scene('hook', st, en, '', html, js)
K.fx('whoosh', t_canal - 0.05)

# ---------- s2-s7 · six stations, one continuous downward camera ----------
stations = [
    ('s2', 'Búsqueda', 'search', [('si:google', 'Google', ('google', 0)), ('si:googlemaps', 'Google Maps', ('google', 1)), ('scan-search', 'SEO', None),
                                  ('si:youtube', 'YouTube', ('youtube', 0)), ('tag', 'Wallapop', ('wallapop', 0))]),
    ('s3', 'Redes sociales', 'share-2', [('si:instagram', 'Instagram', ('instagram', 0)), ('si:tiktok', 'TikTok', ('tiktok', 0)), ('si:linkedin', 'LinkedIn', ('linkedin', 0)), ('si:facebook', 'Facebook', ('facebook', 0))]),
    ('s4', 'Publicidad', 'megaphone', [('si:googleads', 'Google Ads', ('google', 0)), ('si:meta', 'Meta Ads', ('meta', 0)), ('si:linkedin', 'LinkedIn Ads', ('linkedin', 0)), ('si:tiktok', 'TikTok Ads', ('tiktok', 0))]),
    ('s5', 'Audiencias de terceros', 'users-round', [('star', 'Influencers', ('influencers', 0)), ('mic', 'Podcasts', ('podcasts', 0)), ('newspaper', 'Prensa', ('prensa', 0)), ('handshake', 'Collabs', ('colaboraciones', 0))]),
    ('s6', 'Presencia física', 'map-pin', [('presentation', 'Charlas', ('charlas', 0)), ('calendar-days', 'Eventos', ('eventos', 0)), ('tent', 'Ferias', ('ferias', 0)), ('store', 'Puntos de venta', ('puntos', 0))]),
    ('s7', 'Medios tradicionales', 'radio', [('radio', 'Radio', ('radio', 0)), ('tv', 'Televisión', ('televisión', 0)), ('signpost', 'Publicidad exterior', ('publicidad', 0))]),
]
order = [s[0] for s in stations] + ['s8']
for k, (sid, title, cic, chips) in enumerate(stations):
    Tin = K.start(sid) - 0.05
    Tout = K.start(order[k + 1]) - 0.05
    st, en = Tin - 0.3, Tout + 0.3
    times = []
    for c in chips:
        times.append(K.at(sid, c[2][0], nth=c[2][1]) if c[2] else None)
    for i, t in enumerate(times):        # unspoken chip (SEO): between its neighbours
        if t is None:
            times[i] = round((times[i - 1] + times[i + 1]) / 2, 3)
    single = any(len(c[1]) > 13 for c in chips)
    rows = [[i] for i in range(len(chips))] if single else [list(range(i, min(i + 2, len(chips)))) for i in range(0, len(chips), 2)]
    two = len(title) > 16
    top_chips = 1040 if two else 930
    rh = ''
    for r, idx in enumerate(rows):
        rh += f'<div style="position:absolute;left:0;right:0;top:{top_chips + r * 162}px;display:flex;justify-content:center;gap:28px">'
        for i in idx:
            ic, lab, _ = chips[i]
            rh += f'<div id="{sid}c{i}" class="glass chip" style="position:relative;opacity:0;height:140px;font-size:48px;padding:0 36px"><i class="ic" style="width:66px;height:66px">{icon(ic)}</i>{lab}</div>'
        rh += '</div>'
    html = f"""<div id="{sid}bgi" class="ic" style="position:absolute;left:130px;top:640px;width:820px;height:820px;color:#4BBFEF;opacity:.06">{icon(cic)}</div>
<div id="{sid}g" style="position:absolute;inset:0">
  <div id="{sid}tile" class="glass" style="position:absolute;left:460px;top:510px;width:160px;height:160px;border-radius:32%;display:grid;place-items:center">
    <i class="ic" style="width:76px;height:76px;color:#E9F8FF;filter:drop-shadow(0 0 12px rgba(75,191,239,.9))">{icon(cic)}</i></div>
  <div class="hx" style="position:absolute;left:60px;right:60px;top:710px;text-align:center;font-size:124px;text-wrap:balance">{title}</div>
  {rh}
</div>"""
    D = R(en, st)
    js = f"""tl.fromTo("#{sid}g", {{ y: 1920 }}, {{ y: 0, duration: 0.6, ease: "power3.inOut" }}, 0);
tl.fromTo("#{sid}bgi", {{ y: 1150 }}, {{ y: 0, duration: 0.6, ease: "power3.inOut" }}, 0);
tl.fromTo("#{sid}bgi", {{ scale: 1.25, rotation: -8 }}, {{ scale: 1, rotation: 6, duration: {D}, ease: "{E['glide']}" }}, 0);
tl.to("#{sid}g", {{ y: -1920, duration: 0.6, ease: "power3.inOut" }}, {R(en - 0.6, st)});
tl.to("#{sid}bgi", {{ y: -1150, duration: 0.6, ease: "power3.inOut" }}, {R(en - 0.6, st)});
"""
    for i, t in enumerate(times):
        js += f'tl.set("#{sid}c{i}", {{ y: 70, scale: .92 }}, 0);\n'
        js += f'tl.to("#{sid}c{i}", {{ opacity: 1, duration: 0.1, ease: "none" }}, {R(t - 0.05, st)});\n'
        js += f'tl.to("#{sid}c{i}", {{ y: 0, scale: 1, duration: 0.42, ease: "{E["softLand"]}" }}, {R(t - 0.05, st)});\n'
        js += f'tl.to("#{sid}c{i}", {{ y: -8, duration: {R(en - 0.65, t + 0.4)}, ease: "none" }}, {R(t + 0.4, st)});\n'
    K.add_scene(sid, st, en, '', html, js)
    K.fx('whoosh', Tin - 0.25)

# ---------- s8 · pull back to the whole map, two stay lit ----------
st = K.start('s8') + 0.1
t_mark = K.at('s8', 'aivacs') - 0.25
en = t_mark + 0.2
t_todos = K.at('s8', 'todos', 'end')
t_busca = K.at('s8', 'busca')
mini = ''
for i, (sid, title, cic, chips) in enumerate(stations):
    x, y = 70 + (i % 2) * 490, 330 + (i // 2) * 250
    lit = i in (0, 1)
    short = {'Audiencias de terceros': 'Audiencias de otros', 'Medios tradicionales': 'Medios de siempre'}.get(title, title)
    mini += (f'<div id="m{i}" class="glass" style="position:absolute;left:{x}px;top:{y}px;width:450px;height:210px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;opacity:0">'
             f'<i class="ic" style="width:64px;height:64px;color:#E9F8FF;filter:drop-shadow(0 0 10px rgba(75,191,239,.9))">{icon(cic)}</i>'
             f'<div style="font:800 38px \'Jakarta\';letter-spacing:-.02em">{short}</div></div>')
js = ''
for i in range(6):
    t0 = round(0.06 + [0, 3, 5, 7, 9, 11][i] / 30, 3)
    js += f'tl.set("#m{i}", {{ opacity: 1, scale: 1.55, y: {(i // 2 - 1) * 160} }}, {t0});\n'
    js += f'tl.to("#m{i}", {{ scale: 1, y: 0, duration: 0.55, ease: "{E["softLand"]}" }}, {t0});\n'
    js += f'tl.to("#m{i}", {{ scale: 1.04, duration: 0.16, ease: "{E["softLand"]}", yoyo: true, repeat: 1 }}, {R(t_todos - 0.1 + i * 0.03, st)});\n'
    if i in (0, 1):
        js += f'tl.to("#m{i}", {{ scale: 1.08, borderColor: "rgba(75,191,239,1)", boxShadow: "0 30px 60px rgba(0,0,0,.5), 0 0 70px rgba(75,191,239,.6), inset 0 1px 0 rgba(255,255,255,.08)", duration: 0.45, ease: "{E["snapSettle"]}" }}, {R(t_busca, st)});\n'
    else:
        js += f'tl.to("#m{i}", {{ opacity: .22, scale: .93, duration: 0.4, ease: "{E["glide"]}" }}, {R(t_busca + 0.03 * i, st)});\n'
    js += f'tl.to("#m{i}", {{ y: {-260 - i * 20}, opacity: 0, duration: 0.35, ease: "{E["accelExit"]}" }}, {R(en - 0.36 + i * 0.012, st)});\n'
js += f'tl.fromTo("#mapw", {{ scale: 1 }}, {{ scale: .96, duration: {R(en, st)}, ease: "none", transformOrigin: "540px 700px" }}, 0);\n'
K.add_scene('map', st, en, '', f'<div id="mapw" style="position:absolute;inset:0">{mini}</div>', js)
K.fx('pop', t_busca)

# ---------- end card ----------
st = t_mark - 0.35
css, html, js = endcard(K, 'e', st, t_mark, JH, 270, 1010, 540, 'Te ayudamos a elegir tus canales', '+34 603 82 96 57')
K.add_scene('e', st, K.total, css, html, js)

groups = K.captions({'todos', 'cliente'}, skip={'s1', 's2', 's3', 's4', 's5', 's6', 's7'}, until=t_mark - 0.3)
K.write_index(bgm_volume=0.2, bgm_media_start=0)
print('total', K.total)
for g in groups:
    print(g)
