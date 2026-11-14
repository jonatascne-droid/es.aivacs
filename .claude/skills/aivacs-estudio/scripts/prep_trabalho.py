"""Prepare a work folder for AIVACS slides (carousels, Reel covers): style.css, the three brand fonts and an img/ folder.
Usage: prep_trabalho.py DIR   then put the photos in DIR/img, write the HTML there and render with render_slides.js."""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
d = sys.argv[1]
os.makedirs(os.path.join(d, 'fonts'), exist_ok=True)
os.makedirs(os.path.join(d, 'img'), exist_ok=True)
shutil.copy(os.path.join(HERE, 'style.css'), os.path.join(d, 'style.css'))
for f in ('plus-jakarta-sans.woff2', 'dm-sans.woff2', 'jetbrains-mono.woff2'):
    shutil.copy(os.path.join(REPO, 'assets', 'fonts', f), os.path.join(d, 'fonts', f))
print('ok', os.path.abspath(d))
