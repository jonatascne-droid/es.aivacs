---
name: auditoria-site
description: Auditoria completa de um site (SEO técnico, conteúdo, velocidade, dados estruturados, SEO local e palavras-chave) com relatório pronto para o cliente. Use quando pedirem "analisa o site", "auditoria do site", "por que o site não aparece no Google", "relatório de SEO", "análisis web", "auditoría SEO" ou mandarem só a URL de um cliente pedindo diagnóstico. Substitui Screaming Frog, PageSpeed, Rich Results, AnswerThePublic e Ubersuggest com ferramentas grátis; usa Search Console, Google Ads (planejador de palavras-chave) e Perfil de Empresa quando houver acesso.
---

# /auditoria-site

Coleta os dados sozinha, interpreta com o conhecimento das skills `seo-audit`, `schema`, `ai-seo`, `site-architecture`, `cro` e entrega um relatório HTML com notas, prioridades e passo a passo. `SKILL_DIR` é a pasta deste arquivo.

## 0. Entrada (pergunte só o que faltar, numa mensagem)
- **URL** do site (obrigatório) e **nome do cliente**.
- **Idioma do relatório**: `es` (clientes na Espanha, padrão) ou `pt`.
- **Cidade/região** que atende (ex.: Madrid) e **3–5 serviços/produtos principais** (viram as sementes de palavras-chave). Se o usuário não souber, tire da home.
- **Concorrentes** (opcional). Sem eles, descubra pesquisando os serviços + cidade.

Trabalhe em `<scratchpad>/auditoria-<dominio>/` (a pasta `W` abaixo). Nunca imprima os JSON completos no chat; leia só os `*-summary.json` e o necessário (economia de tokens).

## 1. Rastreamento (Screaming Frog)
```bash
python3 SKILL_DIR/scripts/crawl.py https://site --max 300 --out W
```
Lê robots.txt e sitemaps, rastreia até 300 páginas e aponta: erros 4xx/5xx, redirecionamentos, title/description ausente, duplicado ou fora do tamanho, H1, canonical, noindex, conteúdo fino, imagens sem alt, lang/viewport, conteúdo misto, schema da home, páginas fora do sitemap e órfãs, telefones encontrados (consistência NAP). Leia `W/crawl-summary.json`.

## 2. Velocidade (PageSpeed / Lighthouse)
Escolha a home + até 3 páginas-modelo (produto/serviço, categoria, contato ou blog) a partir do crawl:
```bash
python3 SKILL_DIR/scripts/lighthouse.py --out W --desktop https://site/ https://site/servico https://site/contato
```
Roda o mesmo motor do PageSpeed, localmente (sem cota). Requer Node (npx) e Chromium/Chrome; o script acha o Chromium do Playwright sozinho. Leia `W/lighthouse-summary.json`.

## 3. Palavras-chave e perguntas (AnswerThePublic / Ubersuggest)
```bash
python3 SKILL_DIR/scripts/keywords.py --seeds "serviço 1" "serviço 2" --hl es --gl es --city madrid --crawl W/crawl.json --out W
```
Usa o autocompletar do Google (perguntas, buscas comerciais e locais) e marca as **lacunas**: buscas sem nenhuma página com aqueles termos no title/H1. Leia só as chaves `perguntas`, `comerciais`, `locais` e as 30 primeiras `lacunas` de `W/keywords.json`.

## 4. Concorrência e SERP
Com a ferramenta de busca na web, pesquise 3–5 buscas comerciais principais (+ cidade) e anote quem aparece e o que essas páginas têm que o cliente não tem (preço visível, avaliações, FAQ, schema, conteúdo local). Sem raspar o Google.

## 5. Dados que dependem de acesso (use se houver; senão vira item em "o que precisamos")
- **Search Console**: cliques, impressões, posição por busca e páginas não indexadas. O cliente adiciona o e-mail da agência como usuário em *Configurações → Usuários e permissões*.
- **Planejador de palavras-chave**: pelo conector do Google Ads (conta MCC da agência), volumes de busca das sementes e das lacunas.
- **Google Trends**: sazonalidade do nicho (ex.: caldeiras sobem em outubro–janeiro).
- **Perfil de Empresa no Google**: categoria principal, horário, fotos, avaliações e se nome/endereço/telefone batem com o site. Sem API: peça um print ou acesso de gerente.
- **WordPress**: se o crawl mostrar `wp-` nas URLs, recomende Yoast ou Rank Math para títulos, descrições, sitemap e schema.

## 6. Análise
Leia `../seo-audit/SKILL.md` (prioridades e checklist) e, quando relevante, `../schema/SKILL.md` e `../ai-seo/SKILL.md`. Cruze os dados e escreva `W/findings.json`:
```json
{
  "site": "https://…", "cliente": "…", "fecha": "AAAA-MM-DD", "idioma": "es",
  "nota_global": 0-100,
  "notas": {"tecnico": 0-100, "contenido": 0-100, "rendimiento": 0-100, "local": 0-100, "datos_estructurados": 0-100, "conversion": 0-100},
  "resumen": "3–5 frases em linguagem de dono de empresa: como está, o que mais prejudica, o que ganha corrigindo.",
  "prioridades": [{"titulo": "…", "area": "tecnico|contenido|rendimiento|local|datos_estructurados|conversion",
                   "impacto": "alto|medio|bajo", "esfuerzo": "bajo|medio|alto",
                   "evidencia": "número concreto do crawl/Lighthouse", "recomendacion": "ação específica", "urls": ["…"]}],
  "palabras_clave": [{"termino": "…", "intencion": "informacional|comercial|local", "pagina_sugerida": "nova página ou URL existente"}],
  "accesos_pendientes": ["…"], "proximos_pasos": ["…"]
}
```
Regras: 8–15 prioridades, ordenadas por impacto alto + esforço baixo primeiro; toda prioridade cita uma evidência medida (nunca invente números ou volumes); nota de rendimiento = média de performance mobile do Lighthouse; se faltar acesso a um dado, diga isso em vez de estimar. Use `impacto`/`esfuerzo` com esses valores mesmo em relatório pt.

## 7. Relatório
```bash
python3 SKILL_DIR/scripts/report.py --dir W
```
Gera `W/relatorio.html` (um arquivo, imprime em PDF pelo navegador). Envie o arquivo ao usuário e, se ele quiser compartilhar com o cliente, ofereça publicar como página privada (Artifact). No chat, responda curto: nota geral, as 3 prioridades principais e o que precisa do cliente.

## Dependências
Python 3 com `requests`, `beautifulsoup4`, `lxml` (`pip install requests beautifulsoup4 lxml`); Node 18+ (npx baixa o Lighthouse 12 na primeira vez); Chromium/Chrome. Funciona na nuvem do Claude e no Mac.
