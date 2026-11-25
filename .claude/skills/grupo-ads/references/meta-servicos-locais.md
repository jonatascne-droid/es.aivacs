# Meta Ads para serviços locais (instaladores, reformas, clínicas, oficinas)

Roteiro da AIVACS para a **primeira campanha** de um cliente de serviço local na Espanha. Complementa a skill `ads` (feita para B2B/SaaS): aqui o "lead" é alguém que quer uma obra ou um serviço em casa, na zona do cliente.

## 1. Conferir a conta antes de planejar (conector Meta Ads)
- `ads_get_ad_accounts`: qual conta tem `has_payment_method: true` e `account_status: ACTIVE`. É comum o cliente ter duas contas e só uma com cartão.
- `ads_get_pages_for_business` + `ads_get_ig_accounts`: a página e o Instagram ligados (o IG aparece com `page_id`).
- `ads_get_datasets` (conta e portfólio): existe pixel? Conta nova costuma não ter.
- `ads_get_ad_entities` com `date_preset: maximum`: já rodou campanha? Se nunca rodou, é **conta fria**: nada de benchmarks de conta madura nem previsões confiantes. Use faixas e diga que vão ser recalibradas após 30 dias.

## 2. Escolher o destino (sem pixel não é bloqueio)
| Destino | Quando | Cuidado |
|---|---|---|
| Formulário instantâneo, tipo **Mayor intención** | O cliente liga de volta rápido; quer telefone + 2–3 dados | Aceitar os termos de leadgen na página (facebook.com/legal/leadgen/tos). No máximo 3 perguntas próprias (a 4.ª derruba o preenchimento). Política de privacidade com URL. |
| **WhatsApp** (apps de mensagens) | O cliente já vive no WhatsApp (quase todos na Espanha) | Número do WhatsApp Business conectado à página. Mensagem de boas-vindas que já pede os dados. Mensagem de ausência. |
| Site | Só com pixel/GTM e página que converte ≥ 5 % | Sem medição, não dá para otimizar. |

Na dúvida, rode **formulário × WhatsApp na mesma campanha**, com os **mesmos anúncios** nos dois conjuntos e o orçamento na campanha. É o teste de destino do `ads/references/meta-decision-system.md`. Decida no dia 14 pelo custo por contato **qualificado**.

## 3. Público
- Localização por **raio** a partir do endereço do cliente (+ um segundo raio onde houver clientes). Cruze com as cidades dos seguidores (Metricool, IGDC).
- Idade como sugestão do Advantage+, sem interesses. Quem segmenta é o criativo (municípios no texto, "chalet o adosado", obra real).
- Serviço para casa (instalação, reforma) **não** é categoria especial de "vivienda". Imobiliária e crédito são.

## 4. Criativo
- **Obra real do cliente** antes de foto de banco. É a prova que o setor usa nos anúncios que ficam meses no ar (ver na Biblioteca de Anúncios: data de início antiga + várias versões).
- 3 peças para começar: (1) headline + foto da obra principal, (2) grade com 4 obras/serviços (formato "grid static"), (3) a peça que mais rendeu no orgânico. Cada uma em 4:5 e 9:16.
- Próxima peça: vídeo do dono ou do técnico na obra, 20–25 s ("founder content", o S-tier da `ad-creative`).
- Textos longos, com os municípios citados. Até 5 textos e 5 títulos por anúncio.
- Nunca: preço, percentagem de economia, garantia, ajudas ou IRPF, prazos, certificações ou números que o cliente não confirmou (ver PRODUCT.md / ficha do cliente).

## 5. Orçamento e metas (conta fria)
- Mínimo útil: **~10 €/dia** para dois conjuntos (≈ 3× TCPL de gasto por conjunto em 14 dias). Com menos, um destino só.
- Evitar estrear na Black Friday e na Cyber Monday (CPM +30–70 %). Natal: pausar ou meia verba, conforme o cliente atende.
- TCPL (custo por contato qualificado) inicial: o teto da faixa da pesquisa do setor (ex.: reformas na Espanha 8–25 €). Metas de apoio: CTR ≥ 1 %, frequência < 2,5, ≥ 60 % qualificados.
- "Qualificado" quem decide é o cliente, numa planilha: serviço que ele faz + zona + casa/projeto real. Sem planilha não existe custo por cliente.

## 6. Calendário
Criar **em pausa** (só com o ok do Jhony) → ativar → dia 3 entrega → dia 7 checagem de entrega por anúncio → dia 14 decisão de destino e criativos novos → relatório toda segunda. Não editar anúncio rodando; subir verba no máximo 20 % a cada 5 dias.

## 7. Fase 2 (após 30 dias)
Remarketing sem pixel (quem viu vídeos ou interagiu com a página/IG) com **outra oferta**; público semelhante a partir de 100+ qualificados; devolver ao Meta quem virou cliente (conversões offline). Para auditar a conta com histórico: avaliar `claude-ads` (abaixo).

## Fontes e skills avaliadas (25/11/2026)
- [AgriciDaniel/claude-ads](https://github.com/AgriciDaniel/claude-ads) (MIT): auditoria só de leitura de 12 plataformas. A ideia do "contrato de conta fria" (conta, pixel e conversões avaliados separadamente) entrou no passo 1. Instalar quando houver conta com 30+ dias de dados.
- BlitzMetrics, "The Meta Ad Agent" (artigo, sem código público): medir pelo custo por contato qualificado e devolver ao Meta quem virou cliente. Entrou nos passos 5 e 7.
