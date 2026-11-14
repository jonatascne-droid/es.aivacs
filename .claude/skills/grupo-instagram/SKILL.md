---
name: grupo-instagram
description: Grupo "skills de Instagram e Facebook" da AIVACS - conteúdo orgânico do início ao fim - analisar Reels e perfis (inclusive por link), carrosséis, legendas, respostas a comentários, calendário e agendamento no Metricool. Use quando o Jhony disser "use as skills de Instagram", "grupo Instagram", "grupo redes sociais", "grupo social", ou pedir posts, carrosséis, calendário, análise de um Reel ou do perfil, ou agendamento.
---

# Grupo: Instagram e Facebook (orgânico)

## Ao ser chamado

1. Rode `python3 .claude/skills/aivacs-estudio/scripts/verificar.py instagram`.
2. Confira se as ferramentas do conector Metricool aparecem (`getBrandSettings`, `getScheduledPosts`, `createScheduledPost`). Sem elas, avise o Jhony para reconectar.
3. Escolha pela tabela e leia a skill antes de produzir.

## Qual skill usar

| Pedido | Skill principal | Apoio |
|---|---|---|
| Analisar um Reel ou post por link | `insta` | `watch` (assiste o vídeo com áudio) |
| Auditar um perfil (nosso ou de concorrente) | `perfil` | `competitor-profiling` |
| Carrossel | `aivacs-estudio` (`examples/carrossel_ecosistema.py`, identidade AIVACS) | `carrossel` (roteiro e copy slide a slide) |
| Reel ou vídeo | grupo `grupo-videos` | |
| Legenda | `legenda` | `copywriting`, `marketing-psychology` |
| Responder comentários e montar DMs | `comentarios` | |
| Calendário, pilares, ideias da semana | `content-strategy`, `social` | `marketing-ideas`, `marketing:content-creation` |
| Fotos do Jhony recortadas com contorno branco | repositório privado `Mi-auto-trading`, pasta `aivacs/fotos/` | `aivacs-estudio/scripts/fotos/` para recortes novos |
| Influenciadores e parcerias | `influencer-marketing`, `co-marketing` | |
| Comunidade e engajamento | `community-marketing` | |
| Números do perfil (alcance, melhores horários) | conector Metricool (`getAnalyticsDataByMetrics`, `getBestTimeToPostByNetwork`) | `marketing:performance-report` |
| Posts do Instagram e métricas pela Meta | conector Meta Ads (`ads_get_ig_accounts`, `ads_get_ig_media`) | |

## Agendamento no Metricool

Marcas: AIVACS `7845357`, GASTRON `7897102`, Cambia Caldera - Hidrotec `7919016`; fuso `Europe/Madrid`. Um post por rede (Instagram e Facebook separados). Mídia por link público (passo a passo em `aivacs-estudio/references/reels.md`, item 9). Antes de agendar, liste o que já existe nos mesmos dias; depois, confira que a mídia virou link `static.metricool.com`. Não há como apagar post pelo conector: para tirar, vire rascunho.

## Regras da casa

- CTA só para o WhatsApp +34 603 82 96 57; nunca "comenta X" (não há automação de direct ainda; quando houver, será no n8n).
- Textos para o público em espanhol da Espanha; com o Jhony, português.
- A foto da capa de um Reel não repete a foto do post ao lado no feed.
- Mostre tudo numa página de revisão e só agende depois do ok do Jhony.
