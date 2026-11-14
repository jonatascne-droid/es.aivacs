"""Batch cutout. Each job: name src x0 y0 x1 y1 (fractions). Saves trimmed RGBA PNG (max width 1400) + dark preview sheet."""
import sys
from PIL import Image
from rembg import remove, new_session

photos, outdir, sheet = sys.argv[1], sys.argv[2], sys.argv[3]
jobs = [j.split(':') for j in sys.argv[4:]]
sess = new_session('isnet-general-use')
prev = []
for name, src, box in jobs:
    x0, y0, x1, y1 = [float(v) for v in box.split(',')]
    im = Image.open(f'{photos}/{src}.jpg').convert('RGB')
    W, H = im.size
    im = im.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)))
    if im.width > 1600:
        im = im.resize((1600, int(im.height * 1600 / im.width)), Image.LANCZOS)
    res = remove(im, session=sess, post_process_mask=True)
    bb = res.getchannel('A').point(lambda v: 255 if v > 10 else 0).getbbox()
    res = res.crop(bb)
    res.save(f'{outdir}/{name}.png')
    t = Image.new('RGBA', res.size, (8, 12, 16, 255)); t.alpha_composite(res)
    t = t.convert('RGB'); t.thumbnail((300, 380))
    prev.append((name, t))
    print(name, res.size)
s = Image.new('RGB', (len(prev) * 310, 390), (60, 120, 160))
for k, (n, t) in enumerate(prev):
    s.paste(t, (k * 310 + 5, 5))
s.save(sheet, quality=85)
