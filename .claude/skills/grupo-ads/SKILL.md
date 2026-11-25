---
name: grupo-ads
description: "Grupo 'skills de ADS' da AIVACS: Meta Ads e Google Ads, plano, públicos, palavras-chave, criativos, concorrentes na Biblioteca de Anúncios, landing page e relatórios. Use quando o Jhony disser 'use as skills de ADS', 'grupo ADS', 'tráfego pago', ou pedir campanha, anúncio ou relatório."
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
| Referências de concorrentes | conector Meta Ads (`ads_library_search`), roteiro "Espiar concorrentes" abaixo | `competitor-profiling`, `competitors`, `seo-local` |
| Oferta e proposta | `offers`, `pricing` | `lead-magnets` |
| Landing page que converte | `cro`, `signup`, `popups` | grupo `grupo-site` |
| Teste A/B | `ab-testing` | |
| Pixel, eventos, conversões, UTM | `analytics`, `attribution` | conector Meta Ads (`ads_get_datasets`, `ads_get_dataset_quality`) |
| Relatório e otimização | conector Meta Ads (`ads_get_ad_entities`, `ads_insights_*`); Google (`google_ads_get_campaigns`, `google_ads_run_gaql`) | `marketing:performance-report` |

## Espiar concorrentes (Biblioteca de Anúncios)

Para "o que os concorrentes do cliente estão anunciando" ou "que oferta está funcionando no nicho":

1. **Liste os concorrentes:** pergunte ao cliente ou descubra pelo mapa do Google (skill `seo-local`, frente "concorrentes do mapa") e pela busca do nicho na cidade.
2. **Busque no conector Meta Ads:** `ads_library_search` com `search_terms` (serviço + cidade, em espanhol) ou `page_ids` dos concorrentes, `countries: ["ES"]`, `ad_active_status: "ACTIVE"`, `limit: 50`. Na União Europeia a Biblioteca traz todos os anúncios (teste de 19/11/2026: "clínica dental" na Espanha, 6.680 ativos). Fora da UE só vêm anúncios políticos: para clientes no Brasil ou nos EUA, avise e combine outra fonte.
3. **Separe teste de oferta validada:** no ar há 30 dias ou mais (`ad_delivery_start_time`) e com várias versões do mesmo título = oferta validada; menos de 7 dias = teste. Anúncio que dá prejuízo não fica ligado por meses.
4. **Olhe os campeões:** abra o `ad_snapshot_url` dos 5 a 10 mais antigos (print com o Playwright) e anote promessa, oferta, preço, prova, formato (vídeo, imagem, carrossel) e botão.
5. **Entregue** a tabela "ofertas campeãs" (anunciante, há quantos dias, promessa, oferta, formato, link) e 3 ângulos para o cliente, com os textos feitos na skill `ad-creative` e os criativos no `aivacs-estudio` ou nas skills de animação. Sugestão de mudar verba só com os dados da conta do cliente (`ads_get_ad_entities`, `ads_insights_*`).

Modele a oferta, nunca copie o anúncio: textos, imagens e marca dos concorrentes são deles.

## O que cada conector faz

- **Meta Ads:** lê contas, campanhas, públicos, criativos e métricas, e também cria e altera (campanha, conjunto, anúncio, criativo, público, impulsionar post). Criar e alterar gasta dinheiro: sempre mostre o plano e espere o ok do Jhony antes de cada ação que mude algo.
- **Google Ads:** somente leitura (palavras-chave, previsões, campanhas, relatórios em GAQL). Configurado em `.mcp.json` com as variáveis `GOOGLE_ADS_*` do ambiente. A campanha é criada pelo Jhony na interface do Google com o plano que montarmos.

## Regras da casa

- Nunca ative, pause, mude orçamento ou crie nada sem confirmação explícita naquela conversa.
- Anúncio da AIVACS: identidade da casa e CTA para o WhatsApp +34 603 82 96 57. Cliente: marca e regras dele.
- Entregue o plano numa página (Artifact) com públicos, orçamento, criativos e métricas de sucesso.
