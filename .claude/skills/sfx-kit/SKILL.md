---
name: sfx-kit
description: "Biblioteca de 320 efeitos sonoros CC0 (whooshes, pops, impactos, cliques, notificações, risers, logo stings, dinheiro, dados...) com os dados para escolher, sincronizar e mixar cada um. Use quando um Reel, motion, animação ou interface precisar de efeitos sonoros: 'coloca efeito sonoro', 'som de transição', 'whoosh', 'pop quando o texto aparece', 'sound design do vídeo'."
---

# SFX Kit

320 efeitos originais de [wyzowl/sfx-kit](https://github.com/wyzowl/sfx-kit) (CC0: uso comercial livre, sem crédito). Cada som traz o que é, quando usar e quando não usar, a duração que ele cobre, o **ponto de sincronia** e quanto baixar sob narração.

`SKILL_DIR` é a pasta deste arquivo. O áudio não fica no repositório: `scripts/sfx.py` baixa só os sons usados (cache em `~/.cache/sfx-kit`).

## Como usar

1. **Escolha pelo que acontece na tela.** Leia a tabela "On screen → Sounds" de [GUIDE.md](GUIDE.md) e, se precisar, o [catalogue.md](catalogue.md) (uma linha por som). Ou procure:
   ```bash
   python3 "$SKILL_DIR/scripts/sfx.py" buscar "card appears pop"
   ```
2. **Baixe** só os escolhidos para a pasta do projeto:
   ```bash
   python3 "$SKILL_DIR/scripts/sfx.py" baixar pop-small-in whoosh-fast-soft --para assets/sfx
   ```
3. **Posicione pelo ponto de sincronia**, não pelo início do arquivo: o som começa em `momento − sync.at`.
   ```bash
   python3 "$SKILL_DIR/scripts/sfx.py" colocar whoosh-fast-soft 2.40
   ```
4. **Volume:** os sons já vêm nivelados entre si. Sob narração, aplique o `under_voiceover_db` de cada um. Para encaixar um movimento um pouco mais curto ou longo, ajuste a velocidade dentro de `adapt.rate`; fora disso, use a variante de outra velocidade.

## Quando o SFX Kit não tem o som

Ambiências, sons reais específicos ou trilhas: procure no Openverse (Freesound, Jamendo, Wikimedia; sem chave, só licenças que permitem uso comercial):
```bash
python3 "$SKILL_DIR/scripts/openverse.py" buscar "rain on window" --n 8
python3 "$SKILL_DIR/scripts/openverse.py" baixar <url do arquivo> assets/sfx/chuva.mp3
```
CC0 dispensa crédito. CC BY exige crédito: o script imprime a linha pronta, que vai na descrição do post.

## Regras da casa

- Menos é mais: um efeito por acontecimento importante, nunca em cada palavra. A narração manda.
- Nos Reels da AIVACS, siga as regras de som do `aivacs-estudio` e confira a mixagem com a skill `earshot` (`earshot critique video.mp4`) antes de entregar.
- CC0 libera qualquer uso, inclusive comercial e em vídeos de clientes, sem crédito.
