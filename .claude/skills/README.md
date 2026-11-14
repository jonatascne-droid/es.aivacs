# Skills do projeto

Carregadas automaticamente pelo Claude Code em toda sessão aberta neste repositório (o que está no `main`). As de terceiros foram revisadas antes de entrar; para atualizar uma, substitua a pasta pela versão nova do repositório de origem (revise antes).

## Grupos

Diga "use as skills do grupo X" e o Claude carrega o roteiro do grupo: o que usar em cada situação, o que precisa estar conectado e as regras da casa.

| Grupo | Skill | Reúne |
|---|---|---|
| Vídeos | `grupo-videos` | `aivacs-estudio`, `hyperframes` e família, `media-use`, `gsap`, `short-form-edit`, `cut-silences`, `cut-mistakes`, `edit-video`, `motion-showreel`, `reverse-any-video`, `style-sampling`, `watch`, `legenda`, `video` |
| Instagram e Facebook | `grupo-instagram` | `insta`, `watch`, `perfil`, `carrossel`, `legenda`, `comentarios`, `content-strategy`, `social`, conector Metricool |
| ADS | `grupo-ads` | `ads`, `ad-creative`, `ab-testing`, `analytics`, `attribution`, `cro`, `offers`, conectores Meta Ads e Google Ads |
| Documentos | `grupo-documentos` | `anthropic-skills:pdf`, `docx`, `pptx`, `xlsx`, `google-workspace`, Claude Docs, `canvas-design` |
| Design | `grupo-design` | `frontend-design`, `ui-ux-pro-max`, `impeccable`, `animate` e família, `image`, plugin `design` |
| Site e SEO | `grupo-site` | `seo-audit`, `ai-seo`, `schema`, `site-architecture`, `cro`, `analytics`, conectores Lovable e Supabase |
| Estratégia | `grupo-estrategia` | `marketing-plan`, `product-marketing`, `offers`, `pricing`, `emails`, `prospecting`, `llm-council` e as demais de marketing e vendas |

`python3 .claude/skills/aivacs-estudio/scripts/verificar.py <grupo>` confere o que a sessão tem (ffmpeg, Chromium, Gemini, HeyGen, Google Ads...) e diz como corrigir o que faltar.

## Kit da agência

| Skill | Origem | Como usar |
|---|---|---|
| `aivacs-estudio` | criada para nós | Reels em motion com narração em espanhol (Gemini TTS), montagem em HyperFrames, revisão automática com os critérios do motionmaxxing, capas, carrosséis, fotos recortadas com contorno branco, identidade e lições. Os quatro Reels de terça e quinta e as capas estão em `examples/`. |


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
| `hyperframes` · `hyperframes-cli` · `hyperframes-registry` · `media-use` · `slideshow` · `reverse-any-video` · `style-sampling` · `remotion-to-hyperframes` · `figma` | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) @ 0f6ed7d (Apache 2.0) | `hyperframes` é a porta de entrada para qualquer vídeo (lançamento, explicativo, vertical, música, 3D, legendas): as antigas `hyperframes-core/-animation/-audio/-creative/-keyframes/-studio`, `general-video`, `faceless-explainer`, `motion-graphics`, `product-launch-video`, `embedded-captions` e `talking-head-recut` viraram referências dentro dela. Novas: recriar um vídeo de referência, episódio num estilo pronto, portar Remotion/Lottie e trazer Figma. A telemetria fica desligada em `.claude/settings.json`. |
| `short-form-edit` · `cut-silences` · `cut-mistakes` · `edit-video` · `motion-showreel` · `gsap` | [nateherkai/herk-edit-kit](https://github.com/nateherkai/herk-edit-kit) @ 10511e5 (MIT; os materiais da marca AIS do repositório não vieram) | Editar gravações: Reel/Short com gancho e payoff, tirar pausas e erros (com revisão antes de cortar), vídeo longo, showreel de marca no ritmo da música e referência de GSAP. A transcrição usa `aivacs-estudio/scripts/transcribe.py` (Whisper local, sem chave) no lugar do ElevenLabs. `kie.mjs` e `sfx.mjs` do showreel só funcionam com chaves pagas da Kie.ai e ElevenLabs. |
| `watch` | [bradautomates/claude-video](https://github.com/bradautomates/claude-video) @ 03ceb42 (MIT; `gemini.py` com ajuste local para a chave injetada pelo proxy) | `/watch <link ou arquivo> [pergunta]`: assiste vídeos de Instagram, YouTube, TikTok etc. |
| `insta` | criada para nós | Mande o link de um reel/post do Instagram (ou `/insta <link>`): legenda, autor, métricas e conteúdo do vídeo, com leitura de marketing. |

## Produtividade

| Skill | Origem | Como usar |
|---|---|---|
| `handoff` | [mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/productivity/handoff) @ d81f3a1 (MIT) | `/handoff [foco da próxima sessão]`: resume a conversa para continuar numa sessão nova. |

## Avaliados e não incluídos

- [openfilm/openfilm](https://github.com/openfilm/openfilm) (MIT): outro motor de vídeo em HTML com um editor visual no navegador. Faz o mesmo que o HyperFrames; o editor roda no computador local, não na sessão na nuvem. Vale rever se quisermos ajustar vídeos à mão.
- [OpenMontageInc/OpenMontage](https://github.com/OpenMontageInc/OpenMontage) (AGPL-3.0): sistema enorme de produção com IA, focado em gerar cenas com modelos pagos (Veo, Kling, ElevenLabs). A licença AGPL obrigaria a abrir o que for derivado dele, e o nosso estilo (motion na identidade) já está coberto.
- Do Herk Edit Kit ficaram de fora: a biblioteca de 406 cartões (estilo de outra marca), `video-storytelling` (depende de scripts que não vêm no repositório), `make-a-video`, `short-form-video` e as cópias antigas do HyperFrames.

## Configuração (sessões na nuvem)

O hook `.claude/hooks/session-start.sh` instala `ffmpeg` e `yt-dlp` e configura o `/watch` em cada sessão. Nas configurações do ambiente:

- **Acesso à rede:** liberar `instagram.com`, `cdninstagram.com`, `fbcdn.net` e `generativelanguage.googleapis.com`.
- **Credencial de API "Gemini"** (site `generativelanguage.googleapis.com`, cabeçalho `x-goog-api-key`): o Gemini assiste ao vídeo inteiro, com áudio. Sem ela, o `/watch` usa quadros + legendas.
- **Segredo `INSTAGRAM_COOKIES_B64`** (opcional, quando o Instagram pedir login): `cookies.txt` de uma conta secundária, em base64.

Nunca cole chaves ou cookies no chat.
