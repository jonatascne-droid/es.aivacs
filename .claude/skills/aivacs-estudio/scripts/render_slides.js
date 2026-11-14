// node render.js file.html outdir [prefix]
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [file, outdir, only] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1180, height: 1400 }, deviceScaleFactor: 1 });
  const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  p.on('requestfailed', r => errs.push('failed ' + r.url()));
  await p.goto('file://' + path.resolve(file), { waitUntil: 'networkidle' });
  await p.evaluate(async () => {
    await document.fonts.ready;
    document.querySelectorAll('[data-fit]').forEach(el => {
      let fs = parseFloat(getComputedStyle(el).fontSize);
      while (el.scrollWidth > el.clientWidth + 1 && fs > 20) { fs -= 2; el.style.fontSize = fs + 'px'; }
    });
  });
  const slides = await p.$$('section.slide');
  for (const s of slides) {
    const name = await s.getAttribute('data-out');
    if (only && !name.startsWith(only)) continue;
    await s.screenshot({ path: path.join(outdir, name + '.jpg'), type: 'jpeg', quality: 92 });
    console.log('ok', name);
  }
  if (errs.length) console.log('ERRORS', errs);
  await b.close();
})();
