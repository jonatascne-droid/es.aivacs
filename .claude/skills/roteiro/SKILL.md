---
name: roteiro
description: "Roteiro de Reel que não soa como robô, em três frentes: ganchos (detecta abertura genérica e devolve ganchos que seguram o scroll), estrutura (audita Gancho → Problema → Solução → Prova → CTA) e voz (aprende o jeito de falar da pessoa pelos textos dela e escreve assim). Use para 'escreve o roteiro', 'melhora esse gancho', 'esse hook está fraco?', 'revisa a estrutura do reel', 'escreve com a minha voz', 'o roteiro está com cara de IA'."
argument-hint: "ganchos <tema> | estrutura <roteiro> | voz <cliente> | <tema>"
---

# Roteiro

Versão da AIVACS das três skills "hooks", "roteiro" e "voz" (do @guilhermemorais.ia, que só saem por DM). Sem argumento, faz as três em ordem: **voz → ganchos → estrutura**. A voz vem primeiro porque, sem ela, o resto sai com cara de robô.

Público e idioma padrão: Espanha, espanhol da Espanha (tú, não usted, salvo se a voz do cliente disser outra coisa). Para um Reel da AIVACS, siga também `aivacs-estudio/references/identidade.md` e `reels.md`.

## 1. Voz

Antes de escrever uma palavra, carregue o perfil de voz:

- **AIVACS:** `vozes/aivacs.md` (nesta pasta).
- **Cliente:** `aivacs/vozes/<cliente>.md` no repositório privado `jonatascne-droid/Mi-auto-trading` (este repositório é público: perfil de cliente não fica aqui).
- **Sem perfil:** crie um. Peça 5 a 10 textos reais da pessoa (legendas que ela mesma escreveu, mensagens, transcrição de vídeos falados; os vídeos podem ser transcritos com o `/watch` ou com `aivacs-estudio/scripts/transcribe.py`) e preencha o modelo de `vozes/modelo.md`: palavras e expressões que ela usa, as que nunca usaria, tamanho das frases, ritmo, como abre e fecha, humor, tú/usted, regionalismos e 3 trechos dela como exemplo.

Regra de ouro: na dúvida entre a frase "bonita" e a frase que a pessoa diria, fique com a dela.

## 2. Ganchos

Entrada: o tema (e, se houver, o cliente ideal). Saída: 10 ganchos de no máximo 12 palavras, de tipos diferentes, e os 3 melhores marcados.

Tipos: resultado com número ("De 0 a 40 citas al mes sin anuncios"), erro comum ("El error que hace que tu clínica no salga en Google"), contrário ("Publicar todos los días te está quitando clientes"), dor com cena ("Otro lunes contestando WhatsApps a las 11 de la noche"), pergunta que filtra ("¿Tienes un negocio local y nadie te encuentra en Google?"), prova ("Le hicimos esto a una peluquería de Valencia"), segredo ou bastidor, comparação antes e depois.

Para cada gancho (o do usuário ou os seus), passe o checklist e marque ✓ / ⚠ / ✗:

- **Genérico?** ✗ se for abertura de enrolação: "Hola, soy…", "Hoy te traigo 5 consejos", "En este vídeo te voy a contar", "¿Sabías que…?" sem dado, "Muchos me preguntan…", "Atención emprendedores".
- **Tensão nos 3 primeiros segundos?** Há algo em aberto (pergunta, número, conflito) que só se resolve assistindo?
- **Filtra o cliente ideal?** Quem é o público fica claro (dono de clínica, restaurante, autônomo), não "todo mundo".
- **Promete algo grande e concreto?** Resultado, prazo, número ou cena; não "dicas", "truques", "cosas".
- **Funciona sem som?** O texto na tela sozinho segura (a maioria assiste mudo).

Reescreva os fracos e diga quantos estavam fracos ("3 ganchos fracos, reescritos").

## 3. Estrutura

Audite o roteiro nesta ordem e devolva cada parte com ✓ / ⚠ / ✗ e a correção:

1. **Gancho** (0–3 s): para o scroll? (checklist acima)
2. **Problema:** toca numa dor real e específica do cliente ideal, com cena ou número?
3. **Solução:** um caminho claro, uma ideia só (não três dicas soltas)?
4. **Prova:** caso concreto, número, print, antes e depois ou demonstração? Sem prova, o Reel vira opinião.
5. **CTA:** uma ação só, coerente com o vídeo. **AIVACS e clientes da agência: chamada para o WhatsApp** (para a AIVACS, +34 603 82 96 57). Nunca "comenta X que te mando" (não há automação de direct).

Limites: 30 a 40 s, 6 a 8 frases, uns 2,5 palavras por segundo (75 a 100 palavras). Corte toda frase que não empurra para a próxima. Escreva também o que aparece na tela em cada frase.

Termine com "pronto para gravar" só quando as 5 partes estiverem ✓. Para um Reel da AIVACS, o roteiro aprovado segue para a página de aprovação do `aivacs-estudio` (passo 1 de `reels.md`).
