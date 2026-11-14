"""Cutout on a plain backdrop: rembg person mask united with every pixel that differs from the backdrop and is not connected to the frame edge through backdrop.
Usage: plaincut.py SRC.jpg OUT.png PREVIEW.jpg"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from rembg import remove, new_session

src, out, prev = sys.argv[1:4]
im = Image.open(src).convert('RGB')
if im.width > 1600:
    im = im.resize((1600, int(im.height * 1600 / im.width)), Image.LANCZOS)
w, h = im.size
person = np.array(remove(im, session=new_session('isnet-general-use'), post_process_mask=True).getchannel('A'))

a = np.array(im, dtype=np.float32)
edge = np.concatenate([a[:8].reshape(-1, 3), a[:, :8].reshape(-1, 3), a[:, -8:].reshape(-1, 3)])
bg = np.median(edge, axis=0)
# backdrop has a soft light falloff: compare chroma and allow brightness drift
dist = np.sqrt(((a - bg) ** 2).sum(axis=2))
lum = a.mean(axis=2)
backdrop = (dist < 38) | ((np.abs((a - a.mean(axis=2, keepdims=True)) - (bg - bg.mean())).sum(axis=2) < 14) & (lum > 120))
img = Image.fromarray((backdrop * 255).astype(np.uint8)).copy()
for x in range(0, w, 25):
    for y in (0,):
        if img.getpixel((x, y)) == 255:
            ImageDraw.floodfill(img, (x, y), 128)
for y in range(0, h, 25):
    for x in (0, w - 1):
        if img.getpixel((x, y)) == 255:
            ImageDraw.floodfill(img, (x, y), 128)
fg = np.array(img) != 128
comp = Image.fromarray((fg * 255).astype(np.uint8)).copy()
ImageDraw.floodfill(comp, (w // 2, int(h * 0.75)), 200)
fg = (np.array(comp) == 200) & ~backdrop
fgm = np.array(Image.fromarray((fg * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.GaussianBlur(1.0)))
alpha = np.maximum(fgm, person).astype(np.uint8)
res = im.copy()
res.putalpha(Image.fromarray(alpha))
bb = res.getchannel('A').point(lambda v: 255 if v > 10 else 0).getbbox()
res = res.crop(bb)
res.save(out)
t = Image.new('RGBA', res.size, (8, 12, 16, 255)); t.alpha_composite(res)
t.convert('RGB').resize((res.width // 3, res.height // 3)).save(prev, quality=88)
print(out, res.size, 'bg', bg.round())
