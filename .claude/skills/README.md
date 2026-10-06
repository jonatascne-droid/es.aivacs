# Skills do projeto

Carregadas automaticamente pelo Claude Code em toda sessão aberta neste repositório. As de terceiros foram revisadas antes de entrar; para atualizar uma, substitua a pasta pela versão nova do repositório de origem (revise antes).

Este repositório também tem as skills de marketing que já estavam aqui (`copywriting`, `seo-audit`, `ads`, `ad-creative`, `social`, `launch` e as demais), além de `frontend-design`, `ui-ux-pro-max` e `canvas-design`. Elas não foram alteradas e não estão listadas abaixo.

## Design de interface

| Skill | Origem | Como usar |
|---|---|---|
| `impeccable` | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) @ cf3d2fa (Apache 2.0) | `/impeccable [comando] [alvo]`: 23 comandos de design (`polish`, `typeset`, `layout`, `bolder`, `quieter`, `audit`, `critique`…). O hook de detecção automática dele **não** vem ativado (`/impeccable hooks on` liga). |
| `animate` · `improve-animations` · `review-animations` · `emil-design-eng` · `find-animation-opportunities` · `mobile-native` · `break-ui` | [emilkowalski/skills](https://github.com/emilkowalski/skills) @ e8a175d (MIT) | Animações com movimento e tempo certos, auditoria de animações, polimento de UI, app web com cara de nativo no celular e teste de UI com dados extremos. `review-animations` só roda quando chamada. |

## Decisões e opinião sincera

| Skill | Origem | Como usar |
|---|---|---|
| `llm-council` | [tenfoldmarc/llm-council-skill](https://github.com/tenfoldmarc/llm-council-skill) @ 0dc0327 (MIT, segundo o README) | "council this", "pressure-test this", "coloca isso no conselho": 5 conselheiros (Contrário, Primeiros Princípios, Expansionista, Outsider, Executor) avaliam a ideia, revisam uns aos outros às cegas e um presidente dá o veredito. |

## Conteúdo para Instagram

| Skill | Origem | Como usar |
|---|---|---|
| `reel` · `carrossel` · `legenda` · `perfil` · `comentarios` | [andreoliveiras/skills-de-conteudo](https://github.com/andreoliveiras/skills-de-conteudo) @ 95b05ae (MIT) | Reel renderizado (Remotion; narração opcional com `ELEVENLABS_API_KEY`), carrossel 1080×1350 em PNG, legenda, auditoria de perfil e respostas a comentários. Não postam sozinhas. O Remotion exige licença paga para empresas com mais de 3 pessoas. |

## Vídeo

| Skill | Origem | Como usar |
|---|---|---|
| `hyperframes` + `hyperframes-*` + `media-use` | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) @ 34552a2 (Apache 2.0) | Porta de entrada para qualquer vídeo: "faz um vídeo de…". Vídeos em HTML/GSAP renderizados em MP4, sem licença paga. |
| `product-launch-video` · `motion-graphics` · `faceless-explainer` · `embedded-captions` · `talking-head-recut` · `general-video` · `slideshow` | idem | Vídeo de lançamento a partir do projeto, motion graphics, explicativo sem rosto, legendas embutidas, recorte de vídeo falado e slideshow. A telemetria do HyperFrames fica desligada em `.claude/settings.json`. |
| `watch` | [bradautomates/claude-video](https://github.com/bradautomates/claude-video) @ 03ceb42 (MIT; `gemini.py` com ajuste local para a chave injetada pelo proxy) | `/watch <link ou arquivo> [pergunta]`: assiste vídeos de Instagram, YouTube, TikTok etc. |
| `insta` | criada para nós | Mande o link de um reel/post do Instagram (ou `/insta <link>`): legenda, autor, métricas e conteúdo do vídeo, com leitura de marketing. |

## Produtividade

| Skill | Origem | Como usar |
|---|---|---|
| `handoff` | [mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/productivity/handoff) @ d81f3a1 (MIT) | `/handoff [foco da próxima sessão]`: resume a conversa para continuar numa sessão nova. |

## Configuração (sessões na nuvem)

O hook `.claude/hooks/session-start.sh` instala `ffmpeg` e `yt-dlp` e configura o `/watch` em cada sessão. Nas configurações do ambiente:

- **Acesso à rede:** liberar `instagram.com`, `cdninstagram.com`, `fbcdn.net` e `generativelanguage.googleapis.com`.
- **Credencial de API "Gemini"** (site `generativelanguage.googleapis.com`, cabeçalho `x-goog-api-key`): o Gemini assiste ao vídeo inteiro, com áudio. Sem ela, o `/watch` usa quadros + legendas.
- **Segredo `INSTAGRAM_COOKIES_B64`** (opcional, quando o Instagram pedir login): `cookies.txt` de uma conta secundária, em base64.

Nunca cole chaves ou cookies no chat.
