#!/usr/bin/env node
// Exporta cada slide de um carrossel HTML como PNG 1080x1350 (formato de feed do Instagram).
//
// Uso:
//   node exportar.mjs carrossel.html [pasta-de-saida] [--seletor ".slide"] [--escala 1] [--previa] [--pdf]
//
// Cada elemento que casar com o seletor (padrão: .slide) vira um arquivo slide-01.png, slide-02.png...
// --previa  gera também previa.png, todos os slides numa folha só (bom para aprovar pelo celular).
// --pdf     gera também carrossel.pdf, uma página por slide (LinkedIn aceita carrossel em PDF).
// Antes de exportar, avisa quando algum texto passa da área segura do slide.
// Requer o pacote "playwright" instalado na pasta de trabalho (npm i playwright).
// Usa o Chromium do Playwright; se ele não estiver baixado, tenta o Google Chrome instalado no computador.

import { resolve, join } from 'node:path';
import { pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';
import { mkdirSync, existsSync, writeFileSync, unlinkSync } from 'node:fs';

const LARGURA = 1080;
const ALTURA = 1350;

function lerArgumentos(argv) {
  const posicionais = [];
  const opcoes = { seletor: '.slide', escala: 1, previa: false, pdf: false };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--seletor') opcoes.seletor = argv[++i];
    else if (argv[i] === '--escala') opcoes.escala = Number(argv[++i]) || 1;
    else if (argv[i] === '--previa') opcoes.previa = true;
    else if (argv[i] === '--pdf') opcoes.pdf = true;
    else posicionais.push(argv[i]);
  }
  return { arquivo: posicionais[0], saida: posicionais[1] || 'out', ...opcoes };
}

const { arquivo, saida, seletor, escala, previa, pdf } = lerArgumentos(process.argv.slice(2));

if (!arquivo) {
  console.error('Uso: node exportar.mjs carrossel.html [pasta-de-saida] [--seletor ".slide"] [--escala 1]');
  process.exit(1);
}
if (!existsSync(arquivo)) {
  console.error(`Arquivo não encontrado: ${arquivo}`);
  process.exit(1);
}

// O Playwright é procurado primeiro na pasta de onde você roda o comando (onde você fez npm i playwright),
// e só depois ao lado deste script.
let chromium;
try {
  let alvo = 'playwright';
  try {
    alvo = pathToFileURL(createRequire(join(process.cwd(), 'x.js')).resolve('playwright')).href;
  } catch { /* cai no import padrão */ }
  const modulo = await import(alvo);
  chromium = modulo.chromium ?? modulo.default.chromium;
} catch {
  console.error('O pacote "playwright" não está instalado aqui.');
  console.error('Rode na pasta de trabalho:  npm i playwright && npx playwright install chromium');
  process.exit(1);
}

async function abrirNavegador() {
  try {
    return await chromium.launch();
  } catch {
    // Chromium do Playwright não baixado: tenta o Chrome do sistema.
    try {
      return await chromium.launch({ channel: 'chrome' });
    } catch (erro) {
      console.error('Não consegui abrir um navegador.');
      console.error(String(erro.message).split('\n')[0]);
      console.error('Rode:  npx playwright install chromium   (ou instale o Google Chrome)');
      process.exit(1);
    }
  }
}

const navegador = await abrirNavegador();
const pagina = await navegador.newPage({
  viewport: { width: LARGURA, height: ALTURA },
  deviceScaleFactor: escala,
});

await pagina.goto(pathToFileURL(resolve(arquivo)).href, { waitUntil: 'networkidle' });
await pagina.evaluate(() => document.fonts.ready);

const slides = await pagina.locator(seletor).all();
if (slides.length === 0) {
  console.error(`Nenhum elemento encontrado com o seletor "${seletor}".`);
  await navegador.close();
  process.exit(1);
}

// Área segura: 72 px de margem em cada borda. Texto fora dela fica colado na borda
// ou é cortado pela grade do perfil.
const problemas = await pagina.evaluate(([sel, largura, altura]) => {
  const margem = 72;
  const avisos = [];
  document.querySelectorAll(sel).forEach((slide, i) => {
    const caixa = slide.getBoundingClientRect();
    if (Math.round(caixa.width) !== largura || Math.round(caixa.height) !== altura) {
      avisos.push(`slide ${i + 1}: tem ${Math.round(caixa.width)}x${Math.round(caixa.height)} px, deveria ter ${largura}x${altura}`);
    }
    slide.querySelectorAll('h1, h2, p, li, blockquote').forEach((el) => {
      const r = el.getBoundingClientRect();
      const fora = r.left < caixa.left + margem - 1 || r.right > caixa.right - margem + 1 ||
        r.top < caixa.top + margem - 1 || r.bottom > caixa.bottom - margem + 1;
      const transborda = el.scrollWidth > el.clientWidth + 1;
      if (fora || transborda) avisos.push(`slide ${i + 1}: "${el.textContent.trim().slice(0, 50)}" passa da área segura`);
    });
    const conteudo = slide.querySelector('.conteudo');
    const base = slide.querySelector('.base');
    const topo = slide.querySelector('.topo');
    if (conteudo && topo && getComputedStyle(topo).position === 'absolute' &&
        conteudo.getBoundingClientRect().top < topo.getBoundingClientRect().bottom + 40) {
      avisos.push(`slide ${i + 1}: o texto sobe até o cabeçalho; corte palavras`);
    }
    if (conteudo && base && conteudo.getBoundingClientRect().bottom > base.getBoundingClientRect().top - 24) {
      avisos.push(`slide ${i + 1}: o texto encosta na barra de progresso; corte palavras`);
    }
  });
  return avisos;
}, [seletor, LARGURA, ALTURA]);
for (const aviso of problemas) console.warn(`AVISO  ${aviso}`);

const pastaSaida = resolve(saida);
mkdirSync(pastaSaida, { recursive: true });

for (let i = 0; i < slides.length; i++) {
  const nome = `slide-${String(i + 1).padStart(2, '0')}.png`;
  await slides[i].screenshot({ path: join(pastaSaida, nome) });
  console.log(`ok  ${nome}`);
}

if (pdf) {
  await pagina.addStyleTag({ content: `@page { size: ${LARGURA}px ${ALTURA}px; margin: 0 }
    body { background: none !important; padding: 0 !important; gap: 0 !important; display: block !important; }
    ${seletor} { break-after: page; }` });
  await pagina.pdf({ path: join(pastaSaida, 'carrossel.pdf'), width: `${LARGURA}px`, height: `${ALTURA}px`, printBackground: true });
  console.log('ok  carrossel.pdf');
}

if (previa) {
  // Folha de prévia: os slides lado a lado, em miniatura, na ordem.
  const colunas = slides.length <= 4 ? slides.length : Math.ceil(slides.length / 2);
  const largura = 360, altura = 450, vao = 24;
  const imagens = slides.map((_, i) => `<img src="slide-${String(i + 1).padStart(2, '0')}.png">`).join('');
  const folha = join(pastaSaida, '.previa.html');
  writeFileSync(folha, `<!doctype html><style>body{margin:0;background:#1a1d21;padding:${vao}px;display:grid;
    grid-template-columns:repeat(${colunas},${largura}px);gap:${vao}px;width:max-content}
    img{width:${largura}px;height:${altura}px;border-radius:14px;display:block}</style>${imagens}`);
  const paginaPrevia = await navegador.newPage({ viewport: { width: 400, height: 400 }, deviceScaleFactor: 1 });
  await paginaPrevia.goto(pathToFileURL(folha).href, { waitUntil: 'load' });
  await paginaPrevia.screenshot({ path: join(pastaSaida, 'previa.png'), fullPage: true });
  unlinkSync(folha);
  console.log('ok  previa.png');
}

await navegador.close();
console.log(`\n${slides.length} slide(s) exportado(s) em ${pastaSaida}`);
if (problemas.length) console.log(`${problemas.length} aviso(s) de texto fora da área segura: confira os slides acima.`);
