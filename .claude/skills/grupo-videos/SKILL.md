---
name: grupo-videos
description: Grupo "skills de vídeos" da AIVACS - reúne motion, edição, narração, música, legendas, revisão e agendamento de vídeo. Use quando o Jhony disser "use as skills de vídeos", "grupo de vídeos", "grupo vídeo", ou pedir um Reel, Short, vídeo de anúncio, motion, edição de gravação, narração ou capa de vídeo.
---

# Grupo: Vídeos

## Ao ser chamado

1. Rode `python3 .claude/skills/aivacs-estudio/scripts/verificar.py videos` e resolva ou avise o que faltar.
2. Escolha o caminho pela tabela abaixo e leia a skill indicada antes de produzir.
3. Siga as regras da casa (no fim) e entregue numa página de revisão antes de publicar ou agendar.

## Qual skill usar

| Pedido | Skill principal | Apoio |
|---|---|---|
| Reel em motion da AIVACS (sem gravação, com narração) | `aivacs-estudio` (`references/reels.md`) | `hyperframes`, `hyperframes-registry`, `gsap`, `media-use` |
| Reel/Short a partir de uma gravação do Jhony ou de cliente | `short-form-edit` | `cut-silences` → `cut-mistakes`, depois `hyperframes` |
| Só tirar pausas ou erros de uma gravação | `cut-silences`, `cut-mistakes` | `aivacs-estudio/scripts/transcribe.py` (transcrição sem chave) |
| Vídeo longo (YouTube) a partir de gravação | `edit-video` | `short-form-edit/references/editing-playbook.md` |
| Showreel ou vídeo de marca de 10 a 30 s com música | `motion-showreel` | `hyperframes-registry` |
| Recriar um vídeo de referência | `reverse-any-video` | `watch` para entender o vídeo antes |
| Episódio num estilo pronto (explicativo, finanças, 3D...) | `style-sampling` | `hyperframes` |
| Trazer algo do Figma ou portar Remotion/Lottie | `figma`, `remotion-to-hyperframes` | |
| Apresentação para mostrar ao vivo | `slideshow` | |
| Música, efeitos, voz, imagens, recorte, correção de cor | `media-use` | `aivacs-estudio/scripts/fotos/`, `gem_imagem.py` |
| Capa de Reel | `aivacs-estudio` (`examples/capas_reels.py`) | |
| Assistir a um vídeo de referência (Instagram, YouTube, TikTok) | `watch`, `insta` | |
| Estratégia de vídeo, roteiro, gancho | `video`, `social` | `marketing-psychology`, `copywriting` |
| Legenda do post | `legenda` | |
| Reel com Remotion | `reel` | só se pedirem: Remotion exige licença paga para empresas com mais de 3 pessoas |

## Ferramentas e conexões

| O quê | Para quê | Se faltar |
|---|---|---|
| HyperFrames CLI (`npx hyperframes`) | montar, conferir, renderizar, transcrever | baixa sozinho pelo npx |
| ffmpeg, Playwright/Chromium | cortes, compressão, capas | o hook de início instala o ffmpeg; o Chromium já vem na nuvem |
| Credencial "Gemini" do ambiente | narração (`tts_align.py`), imagens, `/watch` | configurar em Ambiente → Credenciais (site `generativelanguage.googleapis.com`, cabeçalho `x-goog-api-key`) |
| Login ou chave da HeyGen | música do catálogo | `npx hyperframes auth login --device` (vale só na sessão) ou chave `HEYGEN_API_KEY` nas credenciais |
| Conector Metricool | agendar Instagram e Facebook | reconectar em claude.ai → Configurações → Conectores |

## Regras da casa

- Identidade da AIVACS em `aivacs-estudio/references/identidade.md`; para cliente, a marca dele.
- Narração e textos em espanhol da Espanha; CTA só para o WhatsApp +34 603 82 96 57.
- Antes de entregar: `npx hyperframes check` sem erro, folha de contato revisada, `mogcheck.py` em PASS.
- Script, exemplo ou lição nova que sirva de novo vai para `.claude/skills/aivacs-estudio/` (nunca só no scratchpad) e entra no `main` por PR.
