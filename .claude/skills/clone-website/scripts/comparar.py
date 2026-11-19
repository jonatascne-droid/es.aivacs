"""Junta o print do site original e o do clone lado a lado, cortado em faixas, para achar diferenças.
Uso: python3 comparar.py ORIGINAL.png CLONE.png SAIDA_PREFIXO [--faixa 1400]
Saída: SAIDA_PREFIXO-01.png, -02.png... (original à esquerda, clone à direita, mesma largura)
e uma linha com a diferença de altura total, que já denuncia seção faltando ou espaçamento errado."""
import argparse
from PIL import Image, ImageDraw, ImageChops

a = argparse.ArgumentParser()
a.add_argument('original'); a.add_argument('clone'); a.add_argument('saida')
a.add_argument('--faixa', type=int, default=1400, help='altura de cada faixa, em pixels do original')
args = a.parse_args()

o = Image.open(args.original).convert('RGB')
c = Image.open(args.clone).convert('RGB')
if c.width != o.width:
    c = c.resize((o.width, round(c.height * o.width / c.width)))
print(f'altura: original {o.height}px · clone {c.height}px · diferença {c.height - o.height:+d}px')

n = 0
for y in range(0, max(o.height, c.height), args.faixa):
    n += 1
    po = o.crop((0, y, o.width, min(y + args.faixa, o.height))) if y < o.height else Image.new('RGB', (o.width, 10), 'white')
    pc = c.crop((0, y, c.width, min(y + args.faixa, c.height))) if y < c.height else Image.new('RGB', (c.width, 10), 'white')
    h = max(po.height, pc.height)
    sheet = Image.new('RGB', (o.width * 2 + 24, h + 36), (235, 235, 235))
    sheet.paste(po, (0, 36)); sheet.paste(pc, (o.width + 24, 36))
    d = ImageDraw.Draw(sheet)
    d.text((8, 10), f'ORIGINAL  y={y}', fill=(200, 0, 0)); d.text((o.width + 32, 10), f'CLONE  y={y}', fill=(0, 120, 0))
    if po.size == pc.size:
        diff = ImageChops.difference(po, pc).convert('L').point(lambda v: 255 if v > 40 else 0)
        pct = 100 * sum(diff.histogram()[255:]) / (po.width * po.height)
        d.text((o.width - 160, 10), f'pixels diferentes: {pct:.1f}%', fill=(0, 0, 0))
    out = f'{args.saida}-{n:02d}.png'
    sheet.save(out)
    print(out)
