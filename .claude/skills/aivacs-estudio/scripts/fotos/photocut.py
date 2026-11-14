"""Person cutout from a crop of a photo, keeping only the component that holds the given face point.
Usage: photocut.py SRC OUT.png x0 y0 x1 y1 fx fy   (crop and face point as fractions of the photo)"""
import sys
import numpy as np
from PIL import Image
from rembg import remove, new_session
from scipy import ndimage

src, out = sys.argv[1], sys.argv[2]
x0, y0, x1, y1, fx, fy = map(float, sys.argv[3:9])
im = Image.open(src).convert('RGB')
W, H = im.size
box = (int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H))
cr = im.crop(box)
if cr.width > 1800:
    cr = cr.resize((1800, int(cr.height * 1800 / cr.width)), Image.LANCZOS)
rgba = remove(cr, session=new_session('isnet-general-use'), post_process_mask=True)
a = np.array(rgba.getchannel('A'))
lab, n = ndimage.label(a > 40)
px = int((fx * W - box[0]) / (box[2] - box[0]) * cr.width); py = int((fy * H - box[1]) / (box[3] - box[1]) * cr.height)
keep = lab[min(py, cr.height - 1), min(px, cr.width - 1)]
if keep:
    a = np.where(lab == keep, a, 0).astype(np.uint8)
rgba.putalpha(Image.fromarray(a))
bb = rgba.getchannel('A').getbbox()
rgba = rgba.crop((bb[0], bb[1], bb[2], rgba.height))   # keep the bottom cut flat
rgba.save(out)
print(out, rgba.size, 'components', n)
