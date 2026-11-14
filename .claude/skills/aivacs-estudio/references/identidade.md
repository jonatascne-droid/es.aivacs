# Identidade visual AIVACS

Agência digital em Madri. Instagram @aivacses. Site aivacs.es. Fale com o Jhony em português; tudo o que vai para o público é em espanhol da Espanha.

## Cores

| Uso | Cor |
|---|---|
| Fundo | `#080C10` (degradê para `#0A1016` em cima e `#06090C` embaixo) |
| Azul da marca (destaque, palavras-chave, logo) | `#4BBFEF` |
| Azul escuro (brilhos) | `#2A8BBF` |
| Azul claro (ícones, chips) | `#BDEBFF` / `#E9F8FF` |
| Texto | `#F0F4F8`; secundário `#9AA5B1` / `#C9D4DD` |
| Verde do WhatsApp (só no botão de contato) | `#25D366` |

Nada de outras cores de destaque. Fundo sempre escuro, com grade azul de 60 px bem sutil e brilhos radiais azuis.

## Fontes (em `assets/fonts/` do repositório)

- **Plus Jakarta Sans** 800: títulos e palavras grandes (letter-spacing −0.035em).
- **DM Sans**: textos corridos e rótulos.
- **JetBrains Mono**: números, rótulos pequenos em maiúsculas, anos, "01 / 05".

## Logo

Triângulo de contorno azul com cantos arredondados e uma linha embaixo, mais a palavra AIVACS em Jakarta 800 com espaçamento largo. SVG em `scripts/lib.py` (`LOGO`) e, animado (desenhando-se), em `scripts/vkit.py` (`LOGO_SVG`).

## Elementos

- Cartões de vidro: degradê azul translúcido para quase preto, borda `rgba(110,210,250,.45)`, sombra e brilho azul leve (`.glass` em `vkit.py`, `.tile` e `.chip` em `style.css`).
- Ícones: Lucide (traço) e Simple Icons (marcas) em `scripts/icons/`. Para baixar um novo: `https://cdn.jsdelivr.net/npm/lucide-static@0.460.0/icons/<nome>.svg`.
- Marcas de terceiros (Apple, Nike...) só em texto, nunca logo.

## Fotos do Jhony

- Recorte com **contorno branco sólido** (sem brilho), uns 13 px na largura em que aparece (`scripts/fotos/outline.py`).
- A foto da capa de um Reel não pode ser a mesma do post ao lado no feed. Capas só de design (tema escrito + gráfico) também valem.

## Texto e chamada

- CTA sempre para o **WhatsApp +34 603 82 96 57**. Nunca "comenta X para receber" (não existe automação de direct).
- Narração e legendas em espanhol da Espanha. "AIVACS" se pronuncia "ái-vacs" (veja `licoes.md`).
- Legendas de post: gancho, 2 a 4 linhas de valor, CTA do WhatsApp com o número, 4 a 7 hashtags.

## Movimento (método motionmaxxing)

Sem HUD ou moldura de interface no vídeo; nada de layout de slide; texto entra palavra por palavra no ritmo da fala; entradas freiam no fim (power3.out / expo.out), saídas aceleram (power3.in); quase nada some com fade; um destaque por quadro; nenhum quadro morto; final parado no máximo 1,4 s; tela final no máximo 25% do vídeo.
