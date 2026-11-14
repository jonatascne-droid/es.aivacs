---
name: aivacs-estudio
description: Estúdio próprio da AIVACS para Reels em motion (narração em espanhol, montagem em HyperFrames, revisão automática, capas), carrosséis e fotos recortadas do Jhony, sempre na identidade da AIVACS. Use para qualquer Reel, vídeo curto, capa de Reel, carrossel ou foto recortada da AIVACS ou de um cliente da agência, e quando pedirem "o mesmo estilo dos Reels da AIVACS".
---

# Estúdio AIVACS

Kit que produziu os Reels de terça e quinta (canais, funções, produto, posicionamento), as capas só de design e os carrosséis. Tudo aqui roda a partir do repositório; nada depende de pastas temporárias da sessão.

Leia antes de começar:
- `references/identidade.md`: cores, fontes, logo, fotos, CTA e regras de texto. Para cliente, troque pela marca dele.
- `references/reels.md`: o passo a passo de um Reel, do roteiro ao agendamento, com os comandos.
- `references/licoes.md`: problemas que já aconteceram e como evitar.

## O que tem aqui

| Arquivo | Para quê |
|---|---|
| `scripts/tts_align.py` | Narração: um pedido ao Gemini TTS com o roteiro inteiro, cortado em uma faixa por fala, com o tempo de cada palavra (`voice_meta.json`). |
| `scripts/vkit.py` | Base dos Reels: cenas, legendas palavra por palavra, fundo vivo, efeitos sonoros, música e tela final (logo, foto, WhatsApp). |
| `scripts/mogcheck.py` | Revisão do vídeo pronto: quadro vazio, final parado, tela final longa, trechos sem nada novo e uma folha de contato. |
| `scripts/transcribe.py` | Transcrição palavra por palavra com Whisper local (sem chave). Também alimenta `cut-silences` e `cut-mistakes`. |
| `scripts/capas.py` + `scripts/lib.py` + `scripts/style.css` | Capas 1080×1920 e carrosséis 1080×1350 em HTML, com ícones Lucide e Simple Icons em `scripts/icons/`. |
| `scripts/prep_trabalho.py` | Prepara a pasta de trabalho das capas e carrosséis (CSS, fontes, `img/`). |
| `scripts/render_slides.js` | Renderiza cada `<section class="slide" data-out="nome">` em JPG com o Playwright. |
| `scripts/fotos/` | Recorte de pessoa (`photocut.py`, `plaincut.py`, `cutbatch.py`, com rembg) e contorno branco sólido (`outline.py`). |
| `scripts/gem_imagem.py` | Gerar ou editar imagem com o Gemini (a chave vem do ambiente). |
| `examples/reel_*.py` | Os quatro Reels prontos como modelo: estações com câmera (canales), mundo com caminho (funcion), ensaio tipográfico com risco (producto), cartas que viram (posicion). |
| `examples/capas_reels.py` | As quatro capas só de design. |
| `examples/carrossel_ecosistema.py` | Um carrossel completo de 7 slides. |

## Fotos do Jhony

As fotos recortadas não ficam no repositório (ele é público). Peça a pasta ao Jhony ou recorte das fotos que ele enviar com `scripts/fotos/` e aplique o contorno branco com `outline.py`. Os exemplos leem a pasta em `AIVACS_FOTOS`.

## Como usar com outras skills

- Base técnica de vídeo: `hyperframes` (contrato, `check`, `render`), `hyperframes-cli`, `hyperframes-registry` (blocos prontos), `media-use` (música, efeitos, imagens), `gsap`.
- Vídeo gravado pelo Jhony (talking head): `short-form-edit` para Reels, `cut-silences` e `cut-mistakes` para limpar a gravação, `edit-video` para vídeo longo.
- Recriar um vídeo de referência: `reverse-any-video`. Ver um Reel do Instagram: `insta` ou `watch`.
- Agendar: conector Metricool (veja `references/reels.md`, passo 9).
