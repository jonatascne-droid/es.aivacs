---
name: grupo-ads
description: Grupo "skills de ADS" da AIVACS - campanhas pagas no Meta Ads (Facebook e Instagram) e Google Ads - planejamento, públicos, palavras-chave, criativos, landing page, medição e otimização. Use quando o Jhony disser "use as skills de ADS", "grupo ADS", "grupo anúncios", "grupo tráfego pago", ou pedir campanha, anúncio, criativo, palavras-chave, orçamento ou relatório de campanha para a AIVACS ou um cliente.
---

# Grupo: ADS (tráfego pago)

## Ao ser chamado

1. Confira as conexões: ferramentas `ads_*` do conector Meta Ads e `google_ads_*` do conector Google Ads. Rode `python3 .claude/skills/aivacs-estudio/scripts/verificar.py ads` para as variáveis do Google Ads.
2. Descubra a conta certa antes de qualquer coisa: Meta `ads_get_ad_accounts`; Google `google_ads_list_accounts`. Contas conhecidas no Metricool: AIVACS `act_1118147360783828`, GASTRON `act_28807603225570842`, Hidrotec `act_1910121607037910`.
3. Escolha pela tabela e leia a skill antes de propor.

## Qual skill usar

| Etapa | Skill principal | Apoio |
|---|---|---|
| Estratégia, objetivo, estrutura, orçamento, lances | `ads` | `marketing:campaign-plan` |
| Palavras-chave e previsão (Google) | conector Google Ads (`google_ads_generate_keyword_ideas`, `..._historical_metrics`, `..._forecast_metrics`) | `ads` |
| Textos e variações de anúncio (RSA, Meta) | `ad-creative` | `copywriting`, `marketing-psychology` |
| Criativo em vídeo ou imagem | grupo `grupo-videos`, `aivacs-estudio` | `image`, `canvas-design` |
| Referências de concorrentes | conector Meta Ads (`ads_library_search`) | `competitor-profiling`, `competitors` |
| Oferta e proposta | `offers`, `pricing` | `lead-magnets` |
| Landing page que converte | `cro`, `signup`, `popups` | grupo `grupo-site` |
| Teste A/B | `ab-testing` | |
| Pixel, eventos, conversões, UTM | `analytics`, `attribution` | conector Meta Ads (`ads_get_datasets`, `ads_get_dataset_quality`) |
| Relatório e otimização | conector Meta Ads (`ads_get_ad_entities`, `ads_insights_*`); Google (`google_ads_get_campaigns`, `google_ads_run_gaql`) | `marketing:performance-report` |

## O que cada conector faz

- **Meta Ads:** lê contas, campanhas, públicos, criativos e métricas, e também cria e altera (campanha, conjunto, anúncio, criativo, público, impulsionar post). Criar e alterar gasta dinheiro: sempre mostre o plano e espere o ok do Jhony antes de cada ação que mude algo.
- **Google Ads:** somente leitura (palavras-chave, previsões, campanhas, relatórios em GAQL). Configurado em `.mcp.json` com as variáveis `GOOGLE_ADS_*` do ambiente. A campanha é criada pelo Jhony na interface do Google com o plano que montarmos.

## Regras da casa

- Nunca ative, pause, mude orçamento ou crie nada sem confirmação explícita naquela conversa.
- Anúncio da AIVACS: identidade da casa e CTA para o WhatsApp +34 603 82 96 57. Cliente: marca e regras dele.
- Entregue o plano numa página (Artifact) com públicos, orçamento, criativos e métricas de sucesso.
