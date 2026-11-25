# Skills do projeto

Carregadas automaticamente pelo Claude Code em toda sessão aberta neste repositório (o que está no `main`). As de terceiros foram revisadas antes de entrar; para atualizar uma, substitua a pasta pela versão nova do repositório de origem (revise antes).

**Descrições curtas:** a lista de skills (nome + descrição) vai no contexto de toda sessão e, se passar do limite, as últimas aparecem sem descrição. Em 25/11/2026 as descrições de 79 skills foram reescritas para até ~380 caracteres (de ~60 mil para ~31 mil no total), mantendo as frases que acionam cada uma; o corpo das skills não mudou. Ao atualizar uma skill de terceiros, encurte a descrição de novo. Os plugins da conta que repetem ou não usamos (`marketing-skills`, que duplica as 50 de marketing daqui, `engineering`, `product-management`, `cowork-plugin-management`, `auth0`, `postiz`) estão desligados só neste repositório em `.claude/settings.json` (`enabledPlugins`); para religar um, troque `false` por `true`.

## Grupos

Diga "use as skills do grupo X" e o Claude carrega o roteiro do grupo: o que usar em cada situação, o que precisa estar conectado e as regras da casa.

| Grupo | Skill | Reúne |
|---|---|---|
| Vídeos | `grupo-videos` | `aivacs-estudio`, `hyperframes` e família, `media-use`, `gsap`, `short-form-edit`, `cut-silences`, `cut-mistakes`, `edit-video`, `motion-showreel`, `reverse-any-video`, `style-sampling`, `watch`, `legenda`, `video`, as 11 de animação (`graph`, `map-route`...), `sfx-kit`, `earshot`, `roteiro`, `radar-de-nicho` |
| Instagram e Facebook | `grupo-instagram` | `insta`, `watch`, `perfil`, `carrossel`, `legenda`, `comentarios`, `content-strategy`, `social`, `radar-de-nicho`, `roteiro`, conector Metricool |
| ADS | `grupo-ads` | `ads`, `ad-creative`, `ab-testing`, `analytics`, `attribution`, `cro`, `offers`, conectores Meta Ads e Google Ads (com o roteiro "Espiar concorrentes" na Biblioteca de Anúncios) |
| Documentos | `grupo-documentos` | `anthropic-skills:pdf`, `docx`, `pptx`, `xlsx`, `google-workspace`, Claude Docs, `canvas-design` |
| Design | `grupo-design` | `frontend-design`, `ui-ux-pro-max`, `impeccable`, `animate` e família, `image`, plugin `design` |
| Site e SEO | `grupo-site` | `seo-audit`, `ai-seo`, `seo-local`, `schema`, `site-architecture`, `cro`, `analytics`, `clone-website`, `untangle-codebase`, conectores Lovable e Supabase |
| Estratégia | `grupo-estrategia` | `marketing-plan`, `product-marketing`, `offers`, `pricing`, `emails`, `prospecting`, `llm-council`, `radar-de-nicho` e as demais de marketing e vendas |

`python3 .claude/skills/aivacs-estudio/scripts/verificar.py <grupo>` confere o que a sessão tem (ffmpeg, Chromium, Gemini, HeyGen, Google Ads...) e diz como corrigir o que faltar.

## Kit da agência

| Skill | Origem | Como usar |
|---|---|---|
| `roteiro` | criada para nós (ideia das skills "hooks", "roteiro" e "voz" de @guilhermemorais.ia, que só saem por DM) | Ganchos que seguram o scroll, auditoria Gancho → Problema → Solução → Prova → CTA e perfil de voz da pessoa. A voz da AIVACS está em `roteiro/vozes/aivacs.md` (rascunho para completar com textos do Jhony); a voz de cliente fica no repositório privado, em `aivacs/vozes/`. |
| `radar-de-nicho` | criada para nós (ideia do "Viral Brand Analyst" de @gabrieltomaz.ia, que só sai por DM) | Acha os vídeos do YouTube e do TikTok que passaram muito da média do próprio canal (`scripts/radar.py`, yt-dlp, sem chave), assiste os campeões e devolve padrões e ideias de vídeo. Instagram só reel a reel, com `insta`. |
| `aivacs-estudio` | criada para nós | Reels em motion com narração em espanhol (Gemini TTS), montagem em HyperFrames, revisão automática com os critérios do motionmaxxing, capas, carrosséis, fotos recortadas com contorno branco, identidade e lições. Os quatro Reels de terça e quinta e as capas estão em `examples/`. |


Este repositório também tem as skills de marketing que já estavam aqui (`copywriting`, `seo-audit`, `ads`, `ad-creative`, `social`, `launch` e as demais), além de `frontend-design`, `ui-ux-pro-max` e `canvas-design`. Elas não foram alteradas e não estão listadas abaixo.

## Design de interface

| Skill | Origem | Como usar |
|---|---|---|
| `impeccable` | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) @ cf3d2fa (Apache 2.0) | `/impeccable [comando] [alvo]`: 23 comandos de design (`polish`, `typeset`, `layout`, `bolder`, `quieter`, `audit`, `critique`…). O hook de detecção automática dele **não** vem ativado (`/impeccable hooks on` liga). |
| `animate` · `improve-animations` · `review-animations` · `emil-design-eng` · `find-animation-opportunities` · `mobile-native` · `break-ui` | [emilkowalski/skills](https://github.com/emilkowalski/skills) @ e8a175d (MIT) | Animações com movimento e tempo certos, auditoria de animações, polimento de UI, app web com cara de nativo no celular e teste de UI com dados extremos. `review-animations` só roda quando chamada. |

## Site e SEO

| Skill | Origem | Como usar |
|---|---|---|
| `clone-website` | [JCodesMore/ai-website-cloner-template](https://github.com/JCodesMore/ai-website-cloner-template) @ 5426e0e (MIT) | `/clone-website <url>`: mapeia, inspeciona no desktop e no celular, reconstrói e compara até bater. Ajuste local: escolher o destino (HTML estático, Next.js com o template original ou Lovable) e dois scripts nossos, `capturar.js` (prints da página inteira + inventário de fontes, imagens e seções) e `comparar.py` (original e clone lado a lado). Só para sites que o cliente tem direito de copiar. |
| `seo-local` | criada para nós, com 11 skills de [garrettjsmith/localseoskills](https://github.com/garrettjsmith/localseoskills) @ c3b7a25 (MIT) como `references/` | Por que o negócio não aparece no mapa e no resumo de IA do Google: auditoria em 8 frentes (ficha, avaliações, páginas de serviço, perguntas, schema, citações, concorrentes, busca com IA) e adaptação para a Espanha (diretórios espanhóis, regras de avaliações). Ficaram de fora as skills que dependem de ferramentas pagas (LocalSEOData, Local Falcon, BrightLocal, DataForSEO, Semrush...). |
| `untangle-codebase` · `prune-tests` | [caldoai/skills](https://github.com/caldoai/skills) @ d5b68da (MIT) | Só quando chamadas: refatoração completa de um código bagunçado (lista os acoplamentos escondidos, registra as decisões e arruma) e limpeza de testes que não protegem nada. `prune-tests` ganhou `disable-model-invocation` aqui. |

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
| `graph` · `map-route` · `breakdown` · `minimalistic-graphics` · `dan-koe` · `kurzgesagt` · `low-poly` · `minecraft` · `stick-figure` · `zach-d-films` · `zach-3d-films` | [artemnovitckii/claude-animation-skills](https://github.com/artemnovitckii/claude-animation-skills) @ 86f7010 (MIT) | Animações para Reels sem gravação, em HyperFrames + GSAP + three.js: gráfico que se desenha, rota em mapa 3D, aparelho desmontado, linhas minimalistas, explicativos com bonecos de palito ou 3D cartoon. O kit compartilhado está em `.claude/kit/` (`bash .claude/kit/setup.sh`). Ajustes locais: usa o Playwright da sessão e o HyperFrames atual (o 0.8.34 fixado não instala mais), números e cartões em espanhol (`graph` e `map-route`), e `kit/palavras_es.py` para marcar as palavras de uma narração em espanhol (o original só entende inglês). Testados aqui: `graph` (45 s) e `map-route` (1 min 50 s). `stick-figure` só foi testada pelo autor, em inglês. |
| `sfx-kit` | [wyzowl/sfx-kit](https://github.com/wyzowl/sfx-kit) @ 92780e7 (CC0) | 320 efeitos sonoros com ponto de sincronia e volume sob narração. Só o catálogo fica aqui; `scripts/sfx.py` baixa os .wav usados. `scripts/openverse.py` (nosso) busca sons reais de licença aberta no Openverse. |
| `earshot` | [Leonxlnx/earshot](https://github.com/Leonxlnx/earshot) @ 4ac3d2a (MIT) | Dá ouvidos ao Claude: descreve um som, escolhe entre candidatos, acha o melhor trecho e critica a mixagem de um vídeo (`earshot critique`). Instalação de uma linha, fixada no commit, em `earshot/SKILL.md` (~1 min + 1,1 GB de modelos, só CPU). O comando `llm` (manda áudio para o Gemini) não é usado. |
| `watch` | [bradautomates/claude-video](https://github.com/bradautomates/claude-video) @ 03ceb42 (MIT; ajustes locais: `gemini.py` usa a chave injetada pelo proxy; `watch.py` tenta outros modelos do Gemini quando um está sobrecarregado (`WATCH_GEMINI_FALLBACK_MODELS`), cai sozinho para os quadros locais se todos falharem e monta uma folha de quadros para ler numa imagem só) | `/watch <link ou arquivo> [pergunta]`: assiste vídeos de Instagram, YouTube, TikTok etc. |
| `insta` | criada para nós | Mande o link de um reel/post do Instagram (ou `/insta <link>`): legenda, autor, métricas e conteúdo do vídeo, com leitura de marketing. |

## Produtividade

| Skill | Origem | Como usar |
|---|---|---|
| `handoff` | [mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/productivity/handoff) @ d81f3a1 (MIT) | `/handoff [foco da próxima sessão]`: resume a conversa para continuar numa sessão nova. |

## Avaliados e não incluídos

- [AgriciDaniel/claude-ads](https://github.com/AgriciDaniel/claude-ads) (MIT): auditoria de contas de anúncios em 12 plataformas, só leitura, com saída em JSON. Serve para contas com histórico; para campanha nova virou o roteiro `grupo-ads/references/meta-servicos-locais.md`. Instalar quando um cliente tiver 30+ dias de dados.
- BlitzMetrics "Meta Ad Agent": artigo sem código público; a ideia (custo por contato qualificado e devolver vendas ao Meta) entrou no mesmo roteiro.
- [openfilm/openfilm](https://github.com/openfilm/openfilm) (MIT): outro motor de vídeo em HTML com um editor visual no navegador. Faz o mesmo que o HyperFrames; o editor roda no computador local, não na sessão na nuvem. Vale rever se quisermos ajustar vídeos à mão.
- [OpenMontageInc/OpenMontage](https://github.com/OpenMontageInc/OpenMontage) (AGPL-3.0): sistema enorme de produção com IA, focado em gerar cenas com modelos pagos (Veo, Kling, ElevenLabs). A licença AGPL obrigaria a abrir o que for derivado dele, e o nosso estilo (motion na identidade) já está coberto.
- Do Herk Edit Kit ficaram de fora: a biblioteca de 406 cartões (estilo de outra marca), `video-storytelling` (depende de scripts que não vêm no repositório), `make-a-video`, `short-form-video` e as cópias antigas do HyperFrames.

### Lote de 19/11/2026 (Reels enviados pelo Jhony)

- [shinyobjectz/raea](https://github.com/shinyobjectz/raea) (FSL-1.1): motor de render de vídeo, 3D e jogos em React, com 8 dias de vida e que precisa de placa de vídeo. Repete o HyperFrames; rever em alguns meses.
- [elder-plinius/G0DM0D3](https://github.com/elder-plinius/G0DM0D3) (AGPL): interface de *jailbreak* com vários modelos pela OpenRouter. Viola os termos das empresas de IA; a comparação entre modelos o `llm-council` já faz.
- [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) (MIT): agente completo e separado (servidor 24 h, IA paga por uso). Não serve de base para o que temos; só se um dia quisermos um assistente no WhatsApp ou Telegram, como projeto à parte.
- [facebook/astryx](https://github.com/facebook/astryx) (MIT, beta): sistema de design da Meta; exige React 19 + StyleX e não encaixa no HTML estático nem no Lovable.
- [hieunc229/mailflare](https://github.com/hieunc229/mailflare) (AGPL): e-mail com domínio próprio, agenda e drive na Cloudflare. Funciona, mas entrega, backup e segurança do e-mail ficariam por nossa conta; se for testar, com um domínio secundário.
- [kalil0321/reverse-api-engineer](https://github.com/kalil0321/reverse-api-engineer) (MIT): grava o tráfego de um site e gera o cliente da API. Instalar quando surgir o caso (só em sistemas com autorização).
- [RamsesAguirre777/facebook-ads-library-mcp](https://github.com/RamsesAguirre777/facebook-ads-library-mcp) (MIT): lê a Biblioteca de Anúncios pelo navegador, sem conta. Na Espanha o conector Meta Ads já traz os anúncios; útil só para clientes fora da UE.
- [bradautomates/head-of-content](https://github.com/bradautomates/head-of-content) (MIT): pesquisa de conteúdo com Apify e TubeLab (pagos) e Mac; fizemos o `radar-de-nicho` no lugar.
- [ReceitaFederal/calculadora-rtc-regime-regular](https://github.com/ReceitaFederal/calculadora-rtc-regime-regular) (MIT): calculadora oficial da reforma tributária; guardada para um projeto futuro, não é skill.
- Os 9 apps open source do vídeo "9 apps pagos" (Open Higgsfield, Chatterbox, OpenSEO, AppFlowy, Handy, Plane, Cal.com, Chatwoot, Cap) são aplicativos, não skills. Chatwoot e Cal.com podem virar serviço para clientes.
- Só por DM, sem código público: `/search` (@felipetambara.ia), `/ads` (@raphaelmassagardi), `maquina-de-vsl` (@lucasgarciapit), "Viral Brand Analyst" (@gabrieltomaz.ia) e "hooks/roteiro/voz" (@guilhermemorais.ia). `/search` está coberta pelo `seo-local`; `/ads`, pelo conector Meta Ads e pelo roteiro "Espiar concorrentes" do `grupo-ads`; as duas últimas viraram `radar-de-nicho` e `roteiro`. A `maquina-de-vsl` (vídeo com rosto e voz clonados) não tem equivalente: depende de serviço pago de avatar e voz, de autorização por escrito do cliente e, na UE, do aviso de conteúdo gerado por IA.

### Lote de 25/11/2026

- `/search` (@matheusfonseca.ia): a mesma skill do lote anterior, só por DM; coberta pela `seo-local`.
- [meituan-longcat/LongCat-Video](https://github.com/meituan-longcat/LongCat-Video) (MIT), LongCat-Video-Avatar 1.6: foto + áudio viram a pessoa falando, por mais de 10 minutos. Precisa de placa NVIDIA grande (~40 GB); não roda na nuvem nem no Mac. A testar por um serviço hospedado (WaveSpeedAI, Magiclight) antes de virar skill. Com cliente: autorização por escrito e aviso de IA (AI Act).
- [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) (Apache 2.0): mapa do código em grafo. O ganho de "71x" foi medido num conjunto de 52 arquivos e cai em projeto pequeno; instala ganchos que interceptam leitura e busca de arquivos. Só para código grande de cliente, instalado no projeto dele.
- Economia de tokens: [caveman](https://github.com/JuliusBrussee/caveman) (respostas telegráficas; o próprio autor mede ~3% além de "seja conciso"), [RTK](https://github.com/rtk-ai/rtk) (encolhe só saídas de terminal), [context-mode](https://github.com/mksglu/context-mode) (licença Elastic; intercepta todas as ferramentas e pode travar a sessão) e [ccusage](https://github.com/ryoppippi/ccusage) (só mede). No lugar deles: descrições curtas, plugins duplicados desligados e as regras de economia do `CLAUDE.md`.

## Configuração (sessões na nuvem)

O hook `.claude/hooks/session-start.sh` instala `ffmpeg` e `yt-dlp` e configura o `/watch` em cada sessão. Nas configurações do ambiente:

- **Acesso à rede:** liberar `instagram.com`, `cdninstagram.com`, `fbcdn.net` e `generativelanguage.googleapis.com`.
- **Credencial de API "Gemini"** (site `generativelanguage.googleapis.com`, cabeçalho `x-goog-api-key`): o Gemini assiste ao vídeo inteiro, com áudio. Sem ela, o `/watch` usa quadros + legendas.
- **Segredo `INSTAGRAM_COOKIES_B64`** (opcional, quando o Instagram pedir login): `cookies.txt` de uma conta secundária, em base64.

Nunca cole chaves ou cookies no chat.
