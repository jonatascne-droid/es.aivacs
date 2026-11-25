---
name: seo-local
description: "SEO local para negócios com endereço ou área de atendimento: por que não aparece no mapa do Google, no resumo de IA ou no ChatGPT, e como corrigir (ficha do Google, avaliações, páginas de serviço e de cidade, schema, diretórios, concorrentes do mapa). Use para 'auditoria de SEO local', 'Google Maps', 'ficha de Google', '/search'."
---

# SEO local

Roteiro da casa para SEO local. As referências em `references/` vêm de [garrettjsmith/localseoskills](https://github.com/garrettjsmith/localseoskills) (MIT), escritas para os EUA. Leia só a que o pedido pede e aplique a adaptação para a Espanha abaixo.

| Pedido | Leia |
|---|---|
| Diagnóstico completo, "por que não aparece" | `references/local-seo-audit.md` |
| Aparecer no resumo de IA do Google, AI Mode, ChatGPT, Gemini, Perplexity | `references/ai-local-search.md` |
| Perfil da Empresa no Google (categorias, fotos, serviços, atributos) | `references/gbp-optimization.md` |
| Publicações no Perfil da Empresa | `references/gbp-posts.md` |
| Perfil suspenso ou em análise | `references/gbp-suspension-recovery.md` |
| Mais avaliações, responder avaliações, reputação | `references/review-management.md` |
| Schema LocalBusiness / JSON-LD | `references/local-schema.md` (e a skill `schema`) |
| Páginas por cidade ou por serviço | `references/local-landing-pages.md` |
| Negócio sem loja, que atende na casa do cliente | `references/service-area-seo.md` |
| Diretórios e consistência de nome, endereço e telefone (NAP) | `references/local-citations.md` |
| Por que o concorrente aparece na frente | `references/local-competitor-analysis.md` |
| Como o ranking local funciona (base) | `references/how-local-search-works.md` |

## Auditoria rápida em paralelo

Para "por que o meu cliente não aparece", rode as frentes abaixo em paralelo (um subagente por frente quando o cliente tiver site e ficha) e junte tudo num plano priorizado. Cada frente responde: o que está faltando, a prova (print, URL, trecho) e a correção.

1. **Ficha do Google:** categoria principal e secundárias, serviços, horário, fotos recentes, perguntas e respostas, publicações.
2. **Avaliações:** quantidade, nota, ritmo dos últimos 90 dias, respostas do dono, palavras de serviço e cidade nas avaliações.
3. **Páginas de serviço:** uma página por serviço principal, com cidade, preço ou faixa, prova e chamada para ação.
4. **Perguntas dos clientes:** FAQ real (o que perguntam no WhatsApp e nos comentários) respondido no site, com schema FAQPage quando fizer sentido.
5. **Schema e dados técnicos:** LocalBusiness com NAP idêntico à ficha, `sameAs`, `areaServed`, horário; site rápido no celular.
6. **Citações:** NAP igual no site, na ficha e nos diretórios espanhóis (abaixo).
7. **Concorrentes do mapa:** os 3 primeiros para a busca principal; compare categorias, avaliações e páginas.
8. **Busca com IA:** pergunte ao Google (AI Mode), ChatGPT e Perplexity "mejor <serviço> en <cidade>" e veja quem citam e de quais fontes.

Termine sempre com "o que corrigir primeiro e por quê", em espanhol se for para o cliente.

## Adaptação para a Espanha

- **Idioma e buscas:** as buscas são em espanhol ("dentista en Valencia", "cerca de mí"); em Catalunha, Galiza, País Basco e Valência, considere também a língua cooficial.
- **Diretórios** (troque os americanos Yelp/BBB/Angi por estes, confirmando antes que continuam ativos): Páginas Amarillas, QDQ, Cylex, Infobel, Hotfrog, Yelp España, Apple Maps (Apple Business Connect), Bing Places. Por setor: Doctoralia e Top Doctors (saúde), TheFork e Tripadvisor (restaurantes), Idealista, Fotocasa e Habitaclia (imóveis), Booking (hospedagem).
- **Avaliações:** as regras do Google proíbem dar desconto ou brinde em troca de avaliação e pedir só aos clientes satisfeitos, e na UE avaliação falsa ou comprada é prática comercial ilegal. Peça a todos os clientes, com link direto.
- **Dados de pesquisa:** as referências recomendam LocalSEOData, Local Falcon, BrightLocal, DataForSEO e Semrush, todos pagos. Sem eles, use a busca manual no navegador (Playwright, modo anônimo, localização da cidade), o Google Search Console do cliente e o conector Google Ads (`google_ads_generate_keyword_ideas`, com segmentação geográfica) para volumes.
- **Ligações com outras skills:** `schema` para o JSON-LD, `ai-seo` para conteúdo citável por IA, `seo-audit` para o técnico do site, `cro` para converter a visita em contato, `comentarios` para responder avaliações no mesmo tom.
- Algumas referências citam skills do repositório original que não trouxemos (`localseodata-tool`, `brief`, `geogrid-analysis`...). Ignore essas menções.
