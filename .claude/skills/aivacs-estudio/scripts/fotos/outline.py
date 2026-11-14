"""Solid white sticker outline around a cutout (no glow).
Usage: outline.py OUT.png IN.png DISPLAY_WIDTH [TARGET_PX]
The outline is sized so it shows about TARGET_PX (default 13) wide at the width the slide displays the image."""
import sys
import numpy as np
from PIL import Image, ImageFilter

out, src, disp = sys.argv[1], sys.argv[2], float(sys.argv[3])
target = float(sys.argv[4]) if len(sys.argv) > 4 else 13.0
im = Image.open(src).convert('RGBA')
t = max(4, round(target * im.width / disp))
pad = t + 6
canvas = Image.new('RGBA', (im.width + 2 * pad, im.height + pad), (0, 0, 0, 0))   # no padding at the bottom
canvas.paste(im, (pad, pad))
a = np.array(canvas.getchannel('A'), dtype=np.float32) / 255.0
binary = Image.fromarray(((a > 0.5) * 255).astype(np.uint8))
sigma = t / 2.05
spread = np.array(binary.filter(ImageFilter.GaussianBlur(sigma)), dtype=np.float32) / 255.0
mask = (spread > 0.02).astype(np.uint8) * 255
mask = Image.fromarray(mask).filter(ImageFilter.GaussianBlur(1.0))
white = Image.new('RGBA', canvas.size, (255, 255, 255, 0))
white.putalpha(mask)
white.alpha_composite(canvas)
white.save(out)
print(out, white.size, 'outline', t, 'px source')
