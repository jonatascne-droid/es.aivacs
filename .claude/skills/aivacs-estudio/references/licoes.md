# Lições aprendidas

## Narração (Gemini TTS)

- Use `gemini-2.5-flash-preview-tts` com a voz Charon: pronuncia "AIVACS" certo. O modelo 3.x soletrou "A-I-V-A-C-S"; escrever "Aibacs" virou "iBox". O Jhony corrigiu os dois casos.
- Um pedido com o roteiro inteiro soa mais natural do que uma fala por pedido, e gasta menos da cota (uns 10 pedidos por dia por modelo; em 429 o script espera e tenta de novo).
- A chave do Gemini é injetada pelo proxy do ambiente (cabeçalho `x-goog-api-key`); o script manda `dummy` de propósito.
- O corte entre falas usa as pausas guiadas pela transcrição; dois-pontos dentro da frase criam pausas falsas, por isso não basta pegar as N maiores pausas.

## HyperFrames

- O id da cena (div que hospeda a composição) **não pode** ser igual ao id de um elemento de dentro: o seletor pega os dois e as transformações acontecem duas vezes (o R2 ficou com 18 s de tela vazia por isso).
- Posição inicial sempre com `tl.set(..., 0)`, nunca `transform` no CSS (aviso `gsap_css_transform_conflict`).
- Calcule tudo em Python antes de escrever o JS; expressão Python dentro do JS quebra (`opacity: 1 if ...`).
- Dois tweens na mesma propriedade ao mesmo tempo geram aviso; encurte um ou comece o outro depois.
- O primeiro quadro não pode ser vazio: deixe a primeira palavra visível em t = 0.
- Efeitos sonoros revezam as faixas 21, 22 e 24; voz na 20, música na 23 (faixas repetidas sobrepostas dão erro).
- Avisos esperados: `composition_file_too_large` e `container_overflow` de elementos saindo da tela.
- Ao atualizar as skills do HyperFrames, rode `npx hyperframes check` num projeto antigo antes de produzir.

## Revisão

- O motionmaxxing (github.com/Tejashmakwana/motionmaxxing) é a referência de ofício; os scripts dele não rodam aqui (bloqueados por serem código externo). `mogcheck.py` é a nossa implementação dos mesmos critérios.
- No fundo escuro, palavras entrando mexem pouco na média de luminância; por isso o `mogcheck` mede "EVENTS" contra o próprio ruído do vídeo. Mire em ≤ 2 s sem evento.
- Cena parada de 3 s ou mais: faça a definição entrar palavra por palavra, ponha um cometa de luz no caminho, um ícone de fundo com parallax, ou um leve empurrão de câmera.

## Capas e carrosséis

- A capa precisa funcionar no recorte do feed: conteúdo entre y 285 e 1635.
- Riscado que quebra de linha fica feio: force a quebra (`<br>`) antes do trecho riscado.
- Texto longo dentro de cartão: reduza a fonte só daquele item em vez do layout inteiro.

## Metricool

- Não há ferramenta para apagar post: para "remover", vire rascunho (`draft: true`) com `updateScheduledPost`.
- Instagram com link do Instagram pede login: não insista.
- Facebook e Instagram em posts separados, como os demais.

## Sessões

- Nada que precise sobreviver fica no scratchpad ou em `~/.claude`: vai para `.claude/skills/` no repositório e entra no `main` por PR.
- Login da HeyGen (`npx hyperframes auth login --device`) vale só para a sessão: faça no começo de cada trabalho com música (o Jhony aprova pelo link). Chave de API da HeyGen não compensa: as chamadas com chave saem do saldo pré-pago da API, enquanto o login usa a cota gratuita do HyperFrames.
- Fotos do Jhony: repositório privado `Mi-auto-trading`, pasta `aivacs/fotos/`.
