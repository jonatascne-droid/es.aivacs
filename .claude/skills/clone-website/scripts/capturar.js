// Captura uma página no Chromium já instalado (Playwright): print da página inteira em cada largura,
// depois de rolar até o fim para carregar imagens preguiçosas, e um inventário do que ela carrega.
// Uso: node capturar.js <url> <pasta-de-saida> [--larguras 1440,390] [--nome original]
// Saída: <pasta>/<nome>-<largura>.png e <pasta>/<nome>-inventario.json
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');

(async () => {

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const [url, saida] = args;
if (!url || !saida) { console.error('uso: node capturar.js <url> <pasta> [--larguras 1440,390] [--nome original]'); process.exit(2); }
const larguras = opt('--larguras', '1440,390').split(',').map(Number);
const nome = opt('--nome', 'pagina');
fs.mkdirSync(saida, { recursive: true });

const browser = await chromium.launch();
let inventario = null;
for (const w of larguras) {
  const mobile = w < 768;
  const ctx = await browser.newContext({ viewport: { width: w, height: mobile ? 844 : 900 }, deviceScaleFactor: 1,
    isMobile: mobile, hasTouch: mobile });
  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: 'networkidle', timeout: 90000 }).catch(() => page.waitForLoadState('load'));
  // rola com a roda do mouse (scripts de scroll suave reagem a ela) até o fim, devagar
  for (let i = 0; i < 80; i++) {
    const fim = await page.evaluate(() => window.scrollY + innerHeight >= document.documentElement.scrollHeight - 2);
    if (fim) break;
    await page.mouse.wheel(0, 700); await page.waitForTimeout(250);
  }
  await page.waitForTimeout(1200);
  await page.evaluate(() => window.scrollTo(0, 0)); await page.waitForTimeout(800);
  const arquivo = path.join(saida, `${nome}-${w}.png`);
  await page.screenshot({ path: arquivo, fullPage: true });
  console.log('print:', arquivo);
  if (!inventario) {
    inventario = await page.evaluate(() => {
      const cs = (el) => { const s = getComputedStyle(el); return { fonte: s.fontFamily, peso: s.fontWeight, tamanho: s.fontSize,
        altura_linha: s.lineHeight, espacamento: s.letterSpacing, cor: s.color, fundo: s.backgroundColor }; };
      const pick = (sel) => { const el = document.querySelector(sel); return el ? { texto: el.textContent.trim().slice(0, 80), ...cs(el) } : null; };
      const fontes = document.fonts ? [...document.fonts].filter(f => f.status === 'loaded').map(f => `${f.family} ${f.weight} ${f.style}`) : [];
      return {
        url: location.href, titulo: document.title,
        descricao: document.querySelector('meta[name="description"]')?.content || null,
        idioma: document.documentElement.lang || null,
        largura_util: Math.max(...[...document.querySelectorAll('main, section, header, footer, .container, [class*="container"]')]
          .map(e => e.getBoundingClientRect().width).filter(x => x < innerWidth), 0) || null,
        fontes_carregadas: [...new Set(fontes)],
        arquivos_de_fonte: performance.getEntriesByType('resource').map(r => r.name).filter(n => /\.(woff2?|ttf|otf)(\?|$)/i.test(n)),
        tipografia: { body: pick('body'), h1: pick('h1'), h2: pick('h2'), p: pick('p'), a: pick('a'), botao: pick('button, .btn, [class*="button"]') },
        imagens: [...document.images].map(i => ({ src: i.currentSrc || i.src, alt: i.alt, natural: `${i.naturalWidth}x${i.naturalHeight}`,
          mostrada: `${Math.round(i.getBoundingClientRect().width)}x${Math.round(i.getBoundingClientRect().height)}`, fit: getComputedStyle(i).objectFit })),
        fundos: [...document.querySelectorAll('*')].map(e => getComputedStyle(e).backgroundImage).filter(b => b && b !== 'none' && b.includes('url(')).slice(0, 60),
        videos: [...document.querySelectorAll('video')].map(v => ({ src: v.currentSrc, poster: v.poster, autoplay: v.autoplay, loop: v.loop, muted: v.muted })),
        svgs_inline: document.querySelectorAll('svg').length,
        links: [...document.querySelectorAll('a[href]')].map(a => ({ texto: a.textContent.trim().slice(0, 50), href: a.href })).slice(0, 150),
        secoes: [...document.querySelectorAll('header, nav, main > *, section, footer')].slice(0, 60).map(e => ({ tag: e.tagName.toLowerCase(),
          id: e.id || null, classe: (e.className && typeof e.className === 'string') ? e.className.slice(0, 60) : null,
          altura: Math.round(e.getBoundingClientRect().height), titulo: e.querySelector('h1,h2,h3')?.textContent.trim().slice(0, 60) || null })),
        scripts: [...document.scripts].map(s => s.src).filter(Boolean),
      };
    });
  }
  await ctx.close();
}
await browser.close();
const inv = path.join(saida, `${nome}-inventario.json`);
fs.writeFileSync(inv, JSON.stringify(inventario, null, 1));
console.log('inventário:', inv);
})();
