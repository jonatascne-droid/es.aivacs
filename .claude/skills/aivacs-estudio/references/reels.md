# Reel em motion, do roteiro ao agendamento

`KIT=.claude/skills/aivacs-estudio` (a partir da raiz do repositório). Trabalhe em uma pasta fora do repositório (o scratchpad da sessão), por exemplo `$W/videos/r1-tema`. Antes de entregar ou agendar, tudo o que for reutilizável volta para o `$KIT` (scripts, exemplos, lições).

## 1. Roteiro e página de aprovação

Escreva as falas em espanhol (6 a 8 frases, 30 a 40 s) e o que aparece na tela em cada uma. Mostre ao Jhony numa página (Artifact) com «Aprovado / Mudar algo» antes de produzir.

## 2. Projeto

```bash
npx hyperframes init $W/videos/r1-tema --skip-skills --skill=hyperframes
```

Crie `audio_request.json` no projeto:

```json
{
 "provider": "gemini", "voice": "Charon", "lang": "es",
 "style": "Español de España, voz masculina cercana y segura, ritmo ágil de Reels, pausa clara entre frases.",
 "lines": [ { "id": "s1", "text": "..." }, { "id": "s2", "text": "...", "say": "texto alternativo só para a pronúncia" } ],
 "bgm": { "mode": "retrieve", "query": "elegant confident corporate, deep pulse, premium and calm, 105 bpm" }
}
```

## 3. Narração

```bash
TEMPO=1.08 TTS_MODEL=gemini-2.5-flash-preview-tts python3 $KIT/scripts/tts_align.py $W/videos/r1-tema
```

Um único pedido ao Gemini (limite de uns 10 por dia por modelo), cortado nas pausas e conferido com a transcrição. Gera `assets/voice/s*.wav` e `voice_meta.json`. Para recortar de novo sem gastar outro pedido: `--reuse`. Ouça o "AIVACS" do final; se sair errado, veja `licoes.md`.

## 4. Música

```bash
cd $W/videos/r1-tema && node <raiz-do-repo>/.claude/skills/media-use/audio/scripts/audio.mjs --request ./audio_request.json --hyperframes . --out ./bgm_meta.json --only bgm
```

Usa o catálogo da HeyGen e precisa do login da HeyGen na sessão. Rode `npx hyperframes auth login --device`: ele mostra um link e um código; mande ao Jhony, ele aprova no celular em meio minuto e a música sai pela cota gratuita do HyperFrames. Não use chave de API da HeyGen: ela cobra do saldo pré-pago da API. Confira a duração: a faixa tem de cobrir o vídeo inteiro. Sem login, use música própria do Jhony ou gere uma localmente (`media-use`).

## 5. Montagem

Copie o exemplo mais parecido de `$KIT/examples/reel_*.py` e adapte. A base é `vkit.Kit(projeto)`:

- `K.start(sid)`, `K.words(sid)`, `K.at(sid, 'palavra')`: tempos absolutos de cada fala e palavra.
- `K.add_scene(id, início, fim, css, html, js)`: uma cena (tempos do `js` relativos ao início da cena).
- `K.fx('pop' | 'click' | 'whoosh' | 'impact' | 'notify' | 'chime', t)`: efeitos sonoros.
- `endcard(K, 'e', início, t_logo, foto, left, top, largura, 'Título', '+34 603 82 96 57')`: tela final.
- `K.captions(palavras_azuis, skip=..., until=...)` e `K.write_index(bgm_volume=0.2)`.

```bash
AIVACS_FOTOS=<pasta das fotos> python3 build.py $W/videos/r1-tema
cd $W/videos/r1-tema && npx hyperframes check --json
npx hyperframes snapshot . --at 1.5,5,9.5,14,20,26 --no-end
```

`check` tem de dar `ok: true`. Olhe a folha de contato do snapshot antes de renderizar: posição, alinhamento, sobreposição, texto pequeno demais (mínimo uns 28 px), um destaque por quadro.

## 6. Render e revisão

```bash
npx hyperframes render -o renders/r1-tema.mp4 -q looks
python3 $KIT/scripts/mogcheck.py renders/r1-tema.mp4 $W/check/r1 --expect <duração>
```

Passa quando: G0, G2 e G3 em PASS, tela final ≤ 25% e "EVENTS" (maior trecho sem nada novo) ≤ 2 s. A média de movimento fica abaixo da faixa de referência por causa do fundo escuro; isso é esperado. Abra `sheet.jpg` e confira cena por cena.

## 7. Capas (só design ou com foto)

```bash
python3 $KIT/scripts/prep_trabalho.py $W/capas
cd $W/capas && python3 <script de capas baseado em $KIT/examples/capas_reels.py>
node $KIT/scripts/render_slides.js capas_reels.html .
```

Tema escrito grande, marca AIVACS e um gráfico do próprio vídeo, com o conteúdo entre y 285 e 1635 (recorte do feed).

## 8. Página de revisão

Comprima para a página: `ffmpeg -i in.mp4 -c:v libx264 -preset slow -crf 22 -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 128k out.mp4` (cada arquivo do Artifact até 15 MB). Vídeo com a capa como pôster, roteiro, legenda e «Aprovado / Mudar algo».

## 9. Agendar no Metricool

- Marca AIVACS: `blogId 7845357`, fuso `Europe/Madrid`. Antes, liste o que já está agendado nos mesmos dias (`getScheduledPosts`).
- Um post por rede, como os Reels já agendados:
  - Instagram: `providers [{"network":"instagram"}]`, `instagramData {"type":"REEL","showReelOnFeed":true,"isAiGenerated":true}` (a narração é gerada por IA).
  - Facebook: `providers [{"network":"facebook"}]`, `facebookData {"type":"REEL"}`.
  - Os dois com `media` (o MP4 em qualidade máxima, não o comprimido) e `videoThumbnailUrl` (a capa em JPG).
- O Metricool só aceita links públicos. Coloque os arquivos numa pasta temporária no branch de trabalho, faça commit e push, use `https://raw.githubusercontent.com/<dono>/<repo>/<SHA do commit>/<pasta>/<arquivo>`, crie os posts, confira que a resposta traz links `static.metricool.com` e então remova a pasta num novo commit (sem force push).
