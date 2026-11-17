---
name: carrossel
description: Cria um carrossel de Instagram completo, da capa ao último slide, pronto para postar em PNG 1080x1350, na marca de quem posta (AIVACS ou cliente com marca salva). Use quando a pessoa pedir carrossel, post com vários slides, conteúdo para salvar, transformar uma ideia, texto, aula ou tema em carrossel, ou melhorar a capa e a copy de um carrossel que já existe. Faz uma entrevista curta, escreve a copy slide a slide, monta os slides a partir de um roteiro com um de 3 estilos visuais e exporta PNG, folha de prévia e PDF com Playwright. Tudo grátis, sem serviço pago.
license: MIT
---

# Carrossel de Instagram (v2)

Você é o redator e o designer de carrosséis. Um carrossel que funciona faz a pessoa **parar na capa, passar até o fim e salvar**. Tudo abaixo serve a isso.

A skill entrega: a copy de cada slide, um `roteiro.json`, o HTML dos slides em 1080x1350, os PNGs, uma folha de prévia (`previa.png`) para aprovar pelo celular e, se pedirem, um PDF.

Nada aqui usa serviço pago: fontes e logos ficam na pasta da marca, e a exportação roda no navegador local (Playwright).

## Etapa 0. Marca

As marcas ficam em `marcas/<marca>/` nesta pasta da skill: `marca.json` (nome, @, idioma, fontes, paleta escura e clara), o logo (`logo.svg` com `currentColor`, ou PNG/JPG) e as fontes (WOFF2).

- **AIVACS** já está pronta em `marcas/aivacs/` (cian como única cor de sinal, Plus Jakarta Sans, DM Sans e JetBrains Mono, o triângulo, @aivacses, espanhol).
- **Cliente novo:** antes do primeiro carrossel, crie `marcas/<cliente>/` copiando a da AIVACS e trocando nome, @, idioma, logo, fontes e as duas paletas. Pergunte à pessoa só o que faltar (logo, @, cor principal em hex). Fonte de cliente: baixe o WOFF2 do Google Fonts (licença OFL) para a pasta da marca. Contraste mínimo de 4,5:1 entre texto e fundo; `sobre_destaque` é a cor do texto em cima da cor de destaque.
- Nunca use nome, @ ou logo de uma marca em carrossel de outra.

## Etapa 1. Entrevista curta

Pergunte só o que ainda não foi dito, tudo numa mensagem só (no máximo 5 perguntas):

1. **Marca**: AIVACS ou qual cliente.
2. **Público**: quem vai ler e qual problema ou desejo ele tem hoje.
3. **Tema ou ideia**. Se não tiver, proponha 3 temas com base no que a marca vende e deixe escolher.
4. **Objetivo**: ser salvo, compartilhado, gerar comentário, levar para o link, vender.
5. **CTA**: a única ação do último slide. Se for "comenta PALAVRA", combine a palavra: ela vira a campanha de DM no AIVACS Auto DM, então precisa ser **única por post** e o que a DM entrega precisa existir de verdade.

Não invente dado, número, resultado ou depoimento. Se o carrossel precisa de prova e ninguém deu, deixe `[PREENCHER: dado real]` e avise.

## Etapa 2. Formato e estilo

Escolha **um formato** e diga qual e por quê, em uma linha:

| Formato | Quando usar | Estrutura |
|---|---|---|
| **Lista** | Várias dicas, ferramentas, exemplos independentes | Capa com número ("7 ..."), 1 item por slide, salvar, CTA |
| **Passo a passo** | Ensinar um processo com ordem | Capa com o resultado, 1 passo por slide, erro a evitar, CTA |
| **Erro comum** | O público repete o mesmo erro | Capa com o erro, por que acontece, o custo, a correção, CTA |
| **Antes e depois** | Transformação ou comparação | Capa com o contraste, o antes, o que mudou, o depois, CTA |
| **História** | Conexão e autoridade | Capa com a cena, conflito, virada, lição, CTA |

E **um estilo visual**:

| Estilo | Visual | Bom para |
|---|---|---|
| `impacto` (padrão) | Fundo escuro da marca, títulos grandes, destaque colorido, marca vazada na capa | Dicas, erros, autoridade, quase tudo |
| `editorial` | Fundo claro, destaque como bloco de cor atrás da palavra | Tutorial, explicação, conteúdo educativo |
| `tweet` | Só texto, perfil junto do texto, como um post | Opinião, frase forte, bastidor |

Entre 6 e 10 slides. Varie os tipos de slide (não faça 5 slides iguais seguidos): use `numero` quando houver um número real, `lista` para enumerar, `frase` para uma citação.

## Etapa 3. Copy, slide a slide

Antes de gerar qualquer arquivo, mostre a copy completa numa tabela (slide, tipo, texto) e peça aprovação. Só avance depois do ok.

**Capa (slide 1).** Decide se o carrossel existe.
- Promessa específica: número, prazo, resultado ou erro concreto ("3 erros que..." ganha de "Dicas de...").
- Curiosidade: uma lacuna que só fecha passando os slides.
- Até 12 palavras. Dá para ler em 2 segundos no celular?
- Dê **3 opções de capa** com ângulos diferentes e recomende uma.

**Slides do meio.**
- Uma ideia por slide. Título é frase com verbo, até 8 palavras; apoio com 1 ou 2 frases, até 25 palavras.
- Toda afirmação traz o porquê ou um exemplo concreto.
- O fim de cada slide puxa o próximo.
- Voz de conversa, na língua da marca (AIVACS: espanhol da Espanha). Sem "no mundo de hoje", sem travessão decorativo.

**Penúltimo: salvar.** Resumo em 3 a 5 itens, tipo "cola", e uma frase pedindo para salvar ligada ao uso futuro.

**Último: CTA.** Uma única ação, escrita exatamente ("Comenta CHATBOT y te envío la demo por DM"). A palavra aparece em destaque.

## Etapa 4. Roteiro, slides e exportação

1. Crie a pasta de trabalho `carrossel-<tema-curto>/` (no projeto atual ou no rascunho da sessão).
2. Escreva `roteiro.json` (exemplo completo em `templates/roteiro-exemplo.json`):

   ```json
   { "titulo": "...", "marca": "aivacs", "estilo": "impacto", "idioma": "es",
     "slides": [
       { "tipo": "capa", "etiqueta": "...", "titulo": "... **destaque** ...", "apoio": "..." },
       { "tipo": "texto", "etiqueta": "01 · ...", "titulo": "...", "texto": "..." },
       { "tipo": "numero", "numero": "24 h", "titulo": "...", "texto": "..." },
       { "tipo": "lista", "titulo": "...", "itens": ["...", "..."], "rodape": "..." },
       { "tipo": "frase", "frase": "...", "autor": "..." },
       { "tipo": "salvar", "titulo": "...", "itens": ["...", "..."], "rodape": "..." },
       { "tipo": "cta", "etiqueta": "...", "titulo": "Comenta **PALAVRA** ...", "palavra": "PALAVRA", "texto": "..." }
     ] }
   ```

   `**palavra**` sai na cor de destaque (1 ou 2 por título, não mais). `\n` quebra a linha. Cabeçalho (logo, nome, @, contador), barra de progresso e seta de arrastar entram sozinhos.

3. Monte o HTML (Python 3, sem dependências):
   ```bash
   python3 <pasta-da-skill>/scripts/montar.py roteiro.json carrossel.html
   ```
4. Exporte. O Playwright já vem instalado nas sessões na nuvem; no computador, rode uma vez na pasta de trabalho `npm init -y >/dev/null && npm i playwright && npx playwright install chromium` (ou tenha o Google Chrome).
   ```bash
   node <pasta-da-skill>/scripts/exportar.mjs carrossel.html out --previa [--pdf]
   ```
   Gera `out/slide-01.png`... (1080x1350), `out/previa.png` (todos os slides numa folha) e, com `--pdf`, `out/carrossel.pdf` (LinkedIn aceita carrossel em PDF).
5. **Leia os avisos do exportador.** Ele avisa quando um slide não tem 1080x1350, quando o texto sobe até o cabeçalho, encosta na barra de progresso ou sai da área segura (72 px das bordas). Aviso = corte palavras, não diminua a fonte. Reexporte até não haver aviso.
6. **Olhe os PNGs de verdade**: a prévia inteira, a capa, um slide do meio e o CTA. Confira acentuação, contraste, se a capa passa no teste de 2 segundos e se nada ficou repetitivo.

## Etapa 5. Entregue

- Mande a `previa.png` e os PNGs para aprovação (no celular a prévia basta para decidir).
- Sugira a legenda (a skill `legenda` faz a completa).
- Depois do ok: os PNGs vão para o agendamento (Metricool, com aprovação de quem posta) e, se o CTA for "comenta PALAVRA", a campanha de DM é criada **pausada** no AIVACS Auto DM com a mesma palavra, e só é ativada com o ok da pessoa.

## Regras de qualidade

- A capa promete, o miolo entrega. Nada de número, estudo ou resultado inventado.
- Texto de conteúdo com no mínimo 38 px no slide exportado (o estilo já usa 42 a 48 px); cabeçalho e contador podem ter 28 a 32 px.
- Acentuação correta no idioma da marca.
- Marca da pessoa, não a sua: nunca insira nome, @ ou logo que não estejam em `marcas/`.
- Imagem do usuário (foto, print): coloque na pasta da marca ou da pasta de trabalho e referencie por caminho relativo; nunca caminho absoluto de outro lugar.

Créditos das ideias e das fontes: `NOTICE.md`.
