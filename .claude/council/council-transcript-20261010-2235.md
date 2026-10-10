# Conselho: agência de agentes de IA para clientes de marketing digital

Sessão de 10/10/2026, 22:35 UTC. Skill `llm-council`: 5 conselheiros, revisão cruzada às cegas e veredito do presidente.

---

## Pergunta original (do dono)

> Preciso atender uns clientes aonde irei prestar o serviço de marketing digital: postagens no Instagram e tráfego pago (Meta Ads e Google Ads). Já tenho algumas skills de marketing, sei que conseguimos fazer as campanhas no Meta Ads e vi que agora tem o MCP para conectar no Google Ads. Conseguimos desenvolver um software ou uma agência de agentes de IA para eu conectar os meus clientes e automatizar os processos (campanhas no Meta e Google Ads, desenvolvimento e postagem de posts no Instagram), com um dashboard das campanhas e dados dos perfis, e talvez uma "área do cliente" onde ele vê esses dashboards mas não opera nem edita nada? Como faríamos? Uma "agência de IA" para cada cliente? Essa "agência" consumiria os seus créditos para operar? Ou criamos um sistema estilo os que já temos, usando GitHub, Supabase, hospedado na Hostinger?

## Pergunta enquadrada (enviada aos conselheiros)

**Contexto do negócio**
- AIVACS: agência de soluções digitais em Madrid (Espanha), desde 2018, atende toda a Espanha em espanhol e português, remotamente. Sem pacotes fixos: diagnóstico gratuito + proposta sob medida.
- Já vende sites, chatbots/automação de WhatsApp (n8n), software de gestão sob medida e gestão de Meta Ads e Google Ads (com criativos, vídeos e reels feitos com IA).
- Já tem SaaS próprios no ar (Obra Organize, Emite Fácil, WorkProspec, Brilla House), feitos com Next.js/Lovable + Supabase, código no GitHub e deploy automático para a Hostinger via GitHub Actions.
- O dono opera com Claude Code (assinatura) + skills de marketing e um conector MCP do Meta Ads que cria/edita campanhas, conjuntos e anúncios e lê métricas e mídia do Instagram. Existe também um MCP do Google Ads. As skills de conteúdo geram o material, mas não publicam.
- Está começando a atender poucos clientes novos (Instagram + Meta Ads + Google Ads).

**A ideia:** um software / "agência de agentes de IA" que automatize (1) campanhas Meta e Google Ads, (2) criação e publicação de posts no Instagram, (3) dashboard do dono com todos os clientes, (4) "área do cliente" somente leitura com login.

**As perguntas:** uma "agência de IA" por cliente? Ela consome os créditos do Claude? Ou um sistema próprio no estilo GitHub + Supabase + Hostinger? Como desenvolver na prática?

**Fatos técnicos:** a assinatura do Claude é para uso interativo do dono; um sistema rodando sozinho usaria a API da Anthropic (por token). Automatizar fora do Claude Code exige app Meta com verificação de empresa e App Review (ads_management, ads_read, instagram_content_publish, instagram_manage_insights), conta Business/Creator no Instagram com limite diário de posts via API, conta MCC e developer token aprovado na Google Ads API, tokens guardados com segurança e RGPD. Ferramentas prontas cobrem pedaços (Postiz, Meta Business Suite, Looker Studio, Supermetrics, Reportei). A verba é do cliente e um erro de automação queima o dinheiro dele.

**O que está em jogo:** tempo e dinheiro em plataforma vs. atender e reter os primeiros clientes; custo (assinatura vs. API); risco de IA operar verba; possibilidade de virar SaaS vendável.

---

## Respostas dos conselheiros

### O Contrário

A falha fatal: você quer construir a fábrica antes de ter a demanda. "Poucos clientes novos" não justificam plataforma. Com 3 clientes, o gargalo é vender e reter, não automatizar. E você já tem quatro SaaS no ar. Quanto eles faturam? Se a resposta for "pouco", o padrão é construir para não ter que vender.

Perguntas que você está evitando:

1. **Quem paga quando o agente erra?** Um orçamento diário com um zero a mais, uma campanha que não pausa no fim de semana, um anúncio reprovado que derruba a conta de anúncios do cliente. Seu contrato cobre isso? "A IA fez" não serve de defesa diante de um cliente que perdeu 2.000 €.
2. **Concentração de risco.** Um único app Meta guarda os tokens de todos os clientes. Se a Meta restringir o app ou o seu Business Manager (acontece sem aviso e sem suporte humano), todos os clientes caem juntos. O mesmo vale para operar clientes na sua assinatura do Claude: se a conta for bloqueada, você perde a ferramenta com que faz tudo.
3. **Contra quem você está otimizando?** Advantage+ e Performance Max já são IA ajustando lance, público e criativo. Um agente mexendo todo dia reinicia a fase de aprendizado e piora o resultado. "Otimizar automaticamente" pode ser justamente o que destrói a performance.
4. **Cliente faz login em dashboard?** Quase nunca. Ele quer um resumo no WhatsApp e uma reunião por mês. Área do cliente vira manutenção que ninguém usa.
5. **SaaS vendável contra quem?** Metricool, Reportei, Madgicx e a própria Meta, que já têm distribuição e IA nativa. Qual seria a sua vantagem real?

"Agência de IA por cliente" é metáfora, não arquitetura. É o mesmo prompt com outro contexto, que você teria de manter N vezes.

**Caminho:** opere na mão com Claude Code + MCP, com aprovação humana em toda alteração de verba. Use Looker Studio para os relatórios e Postiz para agendar posts. Anote o que você repete. Construa só quando 10 clientes pagantes tiverem a mesma dor.

### O Pensador de Primeiros Princípios

Você está fazendo a pergunta errada. A pergunta real não é "como construo uma agência de agentes". É "qual gargalo me impede de atender 10 clientes com margem e mantê-los?". Com poucos clientes, esse gargalo ainda não existe. Você está desenhando a solução antes de sentir o problema.

Desmonte os quatro itens. São quatro problemas diferentes, não um software só:

- **Área do cliente e dashboard:** é um problema de confiança e retenção, não de engenharia. O Looker Studio com conectores resolve isso numa tarde. O cliente quer ver que o dinheiro dele está rendendo. Um login bonito não é o que ele procura.
- **Publicação de posts:** é um problema já resolvido (Postiz, Meta Business Suite). Construir isso é reinventar algo que já existe e passar pelo App Review sem necessidade.
- **Criação e otimização de campanhas:** é o único item com valor de verdade, e também onde está o risco de queimar a verba do cliente. Aqui, ter um humano decidindo não é limitação: é justamente o que você vende. E você já tem isso: Claude Code com os MCPs do Meta e do Google.

"Uma agência por cliente" é uma metáfora errada. Agente não é funcionário. O que muda de um cliente para outro é o contexto, não a infraestrutura. Basta uma pasta por cliente com briefing, tom de voz, público, limites de orçamento, histórico de decisões e regras como "nunca subir o orçamento mais de X% sem aprovação". Isso é 90% da "agência de IA", não custa nada e roda na sua assinatura, porque quem opera é você.

Sobre créditos, a dúvida desaparece. Enquanto você opera, usa a assinatura. A API só entra no que precisa rodar sem você, como relatório semanal ou alerta de anomalia, e isso custa centavos.

Sobre virar SaaS: não dá para transformar em produto um processo que você nunca repetiu. Atenda de 5 a 10 clientes na mão e anote o que faz toda semana. Aí o software que vale construir fica óbvio, e provavelmente bem menor do que você imagina hoje.

### O Expansionista

Vocês estão vendo isso como "automatizar meus primeiros clientes", e isso é pensar pequeno. A AIVACS já faz sites, chatbot de WhatsApp (n8n), tráfego pago e software sob medida, mas ninguém está juntando essas peças. Reportei e Supermetrics não ligam o clique no anúncio à conversa no WhatsApp e depois à venda. A AIVACS consegue ligar. Então a área do cliente não deveria mostrar CPM e alcance. Deveria mostrar o custo por cliente fechado, cruzando os dados da Meta e do Google com as conversas do bot e o CRM. Esse é o produto. Painel de anúncios qualquer ferramenta tem. Mostrar o caminho inteiro, do anúncio à venda, para negócio local que vende pelo WhatsApp é raro na Espanha.

Segundo: não é "uma agência de IA por cliente". É uma plataforma única, onde todos os clientes usam o mesmo sistema, com roteiros prontos por nicho: reformas, clínicas, limpeza. Obra Organize e Brilla House já apontam para esses nichos. Cada cliente novo alimenta comparativos que só vocês terão, como o custo médio por contato de reformas em Madrid ou o criativo que converte para clínica estética. Com 20 clientes, vocês têm dados que nenhuma agência local tem, e isso vira argumento de venda.

Terceiro: quem já usa os SaaS de vocês é um canal de venda pronto. Quem usa o Obra Organize é construtor e precisa de clientes. Dá para oferecer o serviço de marketing de dentro do próprio produto.

Quarto: a burocracia (aprovação do app pela Meta, developer token do Google, RGPD) parece obstáculo, mas protege vocês. Depois de aprovada, segura concorrentes e permite vender a plataforma com a marca de outras agências pequenas na Espanha, em Portugal e no Brasil. Ferramentas americanas atendem mal quem trabalha em espanhol e português.

O caminho maior: hoje o serviço é o laboratório, amanhã vira plataforma, um "sistema operacional de crescimento" para negócio local que vende pelo WhatsApp. Construam cada peça para os clientes atuais já preparada para atender muitos clientes e para ser revendida por outras agências com a marca delas.

### O Outsider

Olhando de fora, a pergunta inteira está escrita na língua de quem constrói, não na de quem paga. "Agente", "MCP", "token", "conjunto de anúncios", "ROAS": o dono de uma padaria em Valência não sabe o que é nada disso, e não quer saber. Ele quer três respostas. Quanto eu gastei? Quantos clientes chegaram? Vale a pena continuar?

O que me parece ponto cego:

1. **O painel "somente leitura" é o contrário do que o cliente quer.** O que ele de fato faria nessa área é aprovar ou recusar o post antes de ir ao ar, e avisar "esse contato não prestou". A área do cliente foi desenhada sem a única coisa que ele usaria nela.
2. **Os números vão brigar com a realidade dele.** A Meta diz 40 leads, o Google diz 25, e o telefone tocou 8 vezes. Um painel bonito, com métricas que contradizem o que ele vê no balcão, destrói a confiança mais rápido do que não ter painel nenhum. E o dado que importa (virou venda?) nenhuma API entrega. Só perguntando a ele.
3. **"IA" assusta quem paga a verba.** Se o cliente souber que um robô mexe no dinheiro dele, a primeira campanha ruim vira "a máquina queimou meu dinheiro". Venda resultado, com um humano responsável. A IA é ferramenta interna, não argumento de venda.
4. **Painel é coisa que se abre duas vezes e se esquece.** Um resumo mensal em espanhol simples, pelo WhatsApp, com quatro números e uma frase de "o que vamos mudar", provavelmente retém mais cliente do que qualquer dashboard.

Teste antes de construir: faça esse relatório à mão, até num PDF, para os primeiros clientes durante dois meses. Veja se eles leem, o que perguntam e o que pedem. É isso que vai desenhar o produto. Se ninguém pedir login, não construa login.

### O Executor

Não construa plataforma agora. Você tem poucos clientes e já tem 80% do "sistema" funcionando: Claude Code, skills e MCP do Meta Ads. Falta só publicar e mostrar dados. Isso se resolve em uma semana, sem escrever código.

"Agência de IA por cliente" na prática significa uma pasta por cliente, e não um software. Na segunda-feira de manhã:

1. **Criar `clientes/<nome>/CLAUDE.md`** com briefing, tom de voz, IDs das contas, metas, verba máxima e o que é proibido mexer. Você abre o Claude Code na pasta e ele já sabe quem é o cliente. Continua sendo a sua assinatura, uso interativo, sem custo de API.
2. **Instalar o Postiz** (cloud ou VPS) e conectar o Instagram dos clientes. As skills geram o post, o Postiz agenda e publica. O problema de "não publica sozinho" acaba na terça.
3. **Montar a "área do cliente" no Looker Studio.** O Google Ads tem conector nativo; o Meta entra por um conector pago (Supermetrics ou similar). Um template duplicado por cliente, link só de leitura. Fica pronto em uma tarde. O seu dashboard geral é outro relatório com todas as contas.
4. **Ritual semanal de 1h por cliente:** o Claude lê as métricas pelo MCP, propõe mudanças, você aprova e ele executa. Nenhuma alteração de verba sem o seu "ok". Isso resolve o risco de queimar dinheiro do cliente.
5. **Abrir hoje** a verificação de empresa na Meta e o pedido do developer token do Google. Isso leva semanas e é o gargalo de qualquer sistema próprio. Começa a correr enquanto você atende.

Só construa o sistema Supabase quando tiver uns 5 clientes pagando e a rotina manual tiver mostrado o que se repete toda semana. Aí a especificação já existe, porque é o registro do que você fez na mão. Antes disso, é chute.

O SaaS vendável vem depois de 3 meses dessa operação, nunca antes.

---

## Revisão cruzada

**Mapeamento do anonimato:** A = Outsider · B = Executor · C = Contrário · D = Expansionista · E = Primeiros Princípios

**Resultado:** os 5 revisores escolheram **B (Executor)** como a resposta mais forte e **D (Expansionista)** como a de maior ponto cego. Três deles citaram **E (Primeiros Princípios)** logo atrás de B.

### Revisor 1

1. **A mais forte é a B.** É a única que responde às quatro perguntas com um plano que dá para executar: uma pasta por cliente rodando na assinatura, Postiz para publicar, Looker Studio para os relatórios e uma rotina semanal com aprovação do dono. Também é a única que manda abrir hoje a verificação de empresa na Meta e o pedido do developer token do Google. Esse é o gargalo de semanas e ele corre enquanto o dono atende. A E vem logo atrás e explica melhor a dúvida dos créditos: assinatura enquanto o dono opera, API só para o que roda sozinho.
2. **O maior ponto cego é da D.** Ela propõe uma plataforma para muitos clientes, revendida com a marca de outras agências, quando existem poucos clientes. Não fala do risco de a IA mexer na verba nem da fase de aprendizado que a C aponta. E trata como vantagem o "comparativo com dados de todos os clientes", que na verdade é um problema de RGPD e de contrato.
3. **O que todas deixaram passar:**
   - **Trava de verdade na plataforma.** A B e a E confiam em regras escritas no CLAUDE.md, mas o MCP tem permissão de escrita. Uma regra no prompt não é trava. É preciso configurar o limite de gasto da conta na Meta e um teto de orçamento no Google.
   - **Propriedade e contrato.** A conta de anúncios e o Business Manager devem ficar no nome do cliente, com a AIVACS só como parceira. Falta também o contrato de tratamento de dados (art. 28 do RGPD), que precisa cobrir Postiz, Supermetrics e Anthropic.
   - **Criativos feitos com IA.** É preciso cumprir a transparência exigida pelo AI Act (art. 50, em vigor desde agosto de 2026) e usar o rótulo de IA da Meta.

### Revisor 2

1. **A mais forte é a B.** É a única que vira passos para esta semana: uma pasta por cliente com CLAUDE.md, o Postiz para publicar, o Looker Studio como área do cliente e um ritual semanal em que a IA só mexe na verba com a aprovação do dono. Também é a única que manda abrir hoje a verificação da Meta e o pedido do developer token do Google. Esses pedidos levam semanas e travam qualquer sistema próprio no futuro. A E vem logo atrás, porque separa melhor os quatro itens.
2. **O maior ponto cego é o da D.** Ela propõe uma plataforma revendida com a marca de outras agências tendo poucos clientes. Não fala do risco de a automação queimar a verba do cliente, nem do custo de construir, nem do prazo de aprovação, nem de quem opera no dia a dia. Ligar o anúncio à conversa no WhatsApp e depois à venda exige CRM e registro das vendas, coisa que esses clientes não têm.
3. **O que todas deixaram passar:**
   - **RGPD do próprio Claude.** Os dados dos clientes passariam por uma assinatura de uso pessoal. Falta o contrato de encarregado de tratamento e checar se esses dados podem ser usados para treino. Talvez seja preciso o plano Team ou a API, com um contrato de proteção de dados.
   - **Como a agência acessa as contas.** O cliente seria dono do próprio Business Manager e das contas, e daria acesso de parceiro à AIVACS. Se a agência só operar contas compartilhadas assim, talvez o acesso padrão da Meta reduza ou adie o App Review. Isso muda a decisão entre construir ou não.
   - **Preço e contrato.** Margem por cliente, teto de verba por escrito e cláusula de responsabilidade.

### Revisor 3

1. **Mais forte: B.** É a única que responde às quatro perguntas com passos que dá para executar já. "Agência por cliente" vira uma pasta com CLAUDE.md. O dono continua na assinatura porque o uso é interativo. O Postiz publica, o Looker Studio serve de área do cliente, nenhuma mudança de verba sai sem aprovação humana e a verificação na Meta e no Google começa agora, em paralelo. Uma ressalva: o Postiz instalado em VPS exige um app Meta próprio, com App Review. No começo, use a versão cloud. E chega perto, mas é menos prática.
2. **Maior ponto cego: D.** Ignora que a agência está só começando, com poucos clientes, e já propõe white-label e comparativos a partir de 20 clientes. Trata o App Review como barreira contra concorrentes, mas qualquer agência consegue a aprovação. Não fala do risco de a IA mexer na verba nem do custo da API. Também esquece que usar dados de clientes em comparativos exige consentimento e contrato pelo RGPD. E ligar anúncio, WhatsApp e venda depende de um CRM que o negócio local raramente mantém atualizado.
3. **O que todas deixaram passar:**
   - Uma trava na própria plataforma: limite de gasto da conta na Meta e orçamento máximo no Google. Ela segura mesmo quando a IA ou o humano erra. "Verba máxima" escrita no CLAUDE.md é só uma instrução.
   - O contrato: entrar como parceiro no Business Manager do cliente, já que a conta é dele, assinar o acordo de encarregado de tratamento exigido pelo RGPD e ter uma cláusula de responsabilidade sobre a verba.
   - O momento de construir: medir horas e margem por cliente, em vez de esperar por um número arbitrário como "5" ou "10 clientes".

### Revisor 4

1. **A mais forte é a B.** Todas concordam em não construir agora, mas só a B transforma isso num plano para a semana. Ela propõe uma pasta por cliente com CLAUDE.md, Postiz para publicar, Looker Studio para os relatórios e aprovação humana em toda mudança de verba. Também manda pedir hoje a verificação da Meta e o developer token do Google, que são o gargalo de prazo. E responde direto à dúvida dos créditos. A E chega perto, mas é menos concreta.
2. **O maior ponto cego é o da D.** Ela propõe plataforma para muitos clientes, marca de terceiros e comparativos entre clientes, tendo poucos clientes. Também ignora o risco de operar a verba de outra pessoa. Cruzar anúncios, conversas de WhatsApp e CRM de vários clientes exige consentimento, contrato e anonimização pelo RGPD. A D trata a burocracia como proteção contra concorrentes, sem ver que ela pode travar o produto.
3. **Todas deixaram passar quem é dono das contas e quem responde pelos erros.** O cliente deve ser dono da conta de anúncios, da página e do Instagram, e dar acesso de parceiro ao Business Manager da AIVACS. Assim, o MCP que o dono já usa provavelmente alcança essas contas sem um App Review próprio, e a saída do cliente fica limpa. Faltam ainda um contrato de RGPD como "encargado del tratamiento", um limite de responsabilidade sobre a verba e um registro de cada alteração feita pela IA. Ninguém falou de preço e margem por cliente.

### Revisor 5

1. **Mais forte: B.** Transforma o "não construa agora" num plano que dá para executar: uma pasta por cliente com CLAUDE.md e teto de verba, o Postiz publicando, o Looker Studio como área do cliente e aprovação humana antes de qualquer mudança de verba. E traz o passo decisivo: abrir hoje a verificação da Meta e o pedido do developer token do Google, que levam semanas, enquanto atende os clientes. E chega perto no diagnóstico, mas não tem esse cronograma.
2. **Maior ponto cego: D.** Propõe plataforma única para todos os clientes, revenda com a marca de outras agências e uma base de dados exclusiva para quem tem poucos clientes. Não fala de custo, de prazo nem do risco de a automação queimar a verba do cliente. Usar dados de um cliente para comparar com outros exige base legal e anonimização pelo RGPD, e D trata essa burocracia como vantagem. Também supõe que os SaaS atuais já têm usuários suficientes para servir de canal de venda, sem nenhum dado.
3. **O que todas deixaram passar: contrato e acesso.** As contas de anúncio e o Instagram devem ficar no nome do cliente, com a AIVACS como parceira no Business Manager, para que a saída seja limpa. Faltam três coisas: o contrato de encarregado de tratamento exigido pelo RGPD, uma cláusula de responsabilidade por erro de verba e um registro de cada alteração feita pelo Claude. E ninguém definiu o preço do serviço nem calculou quantos clientes o dono aguenta sozinho, que é o gatilho real para automatizar.

---

## Veredito do presidente

### Onde o conselho concorda

- **Não construa a plataforma agora.** O Contrário, o Pensador de Primeiros Princípios, o Outsider e o Executor chegaram a isso cada um por um caminho. Com poucos clientes, o gargalo é vender, entregar e reter, não automatizar.
- **"Uma agência por cliente" é só uma imagem.** O que muda de um cliente para outro é o contexto: briefing, tom, contas, metas, verba máxima e histórico. A infraestrutura é a mesma. Basta uma pasta por cliente, cada uma com seu CLAUDE.md.
- **Créditos:** enquanto o dono opera, usa a assinatura. O que roda sozinho vai para a API, cobrado por token.
- **Humano aprova toda mudança de verba.** O resto já existe pronto: o Postiz publica, o Looker Studio mostra os números.
- **O cliente quer três respostas:** quanto gastou, quantos contatos chegaram e se vale continuar. Um resumo pelo WhatsApp provavelmente segura mais o cliente do que um painel.
- Os cinco revisores escolheram o Executor como a resposta mais forte e o Expansionista como a de maior ponto cego.

### Onde o conselho diverge

- **Expansionista contra os demais.** Ele viu algo que os outros não viram. A AIVACS já tem o bot de WhatsApp no n8n e pode ligar anúncio → conversa → venda, coisa que Reportei e Supermetrics não fazem. Os outros respondem que isso exige registro de vendas, e negócio local quase nunca tem. E white-label com três clientes não se sustenta. Os dois lados têm razão: é o produto certo na hora errada.
- **Painel ou mensagem.** O Executor quer a área do cliente no Looker Studio desde já. O Outsider e o Contrário dizem que ninguém abre painel e que o cliente quer é aprovar o post antes de ir ao ar. A diferença vem de clientes diferentes. Um teste barato resolve.
- **Quando começar a construir.** O Contrário fala em 10 clientes e o Executor em uns 5. Os revisores preferem medir horas e margem por cliente. Número de clientes é fácil de ver, mas o que aperta de verdade são as horas.

### Pontos cegos que o conselho pegou

- **Regra no CLAUDE.md não é trava.** O MCP tem permissão de escrita. O limite precisa estar na própria plataforma: limite de gasto da conta na Meta e orçamento máximo no Google.
- **De quem são as contas.** Conta de anúncios, página e Instagram ficam no nome do cliente, e a AIVACS entra como parceira no Business Manager dele. Isso garante uma saída limpa. Segundo dois revisores, talvez também diminua ou adie a necessidade de App Review próprio. Vale confirmar na documentação da Meta antes de contar com isso.
- **Postiz.** A versão self-hosted provavelmente exige um app Meta próprio. A versão cloud evita isso no começo.
- **RGPD.** É preciso um contrato de encarregado do tratamento com cada cliente, e checar se Postiz, Supermetrics e Anthropic estão cobertos como subprocessadores. Dados de clientes passando por uma assinatura individual talvez não sejam adequados. Vale verificar os termos e considerar o plano Team ou a API com DPA. A obrigação de transparência do AI Act e o rótulo de IA da Meta para criativos também precisam ser checados, sem tratar como certos.
- **Contrato.** Precisa de cláusula de responsabilidade por erro de verba e de um registro de cada alteração feita pela IA.
- **Preço e capacidade.** Ninguém definiu preço, margem, nem quantos clientes o dono aguenta sozinho.

### A recomendação

Opere manualmente por três meses com o que já tem, protegido por travas reais e por contrato. Use esse tempo para escrever, na prática, a especificação do sistema que vai construir depois.

**(a) Uma agência de IA por cliente?** Não. Um sistema só, com um contexto por cliente.

**(b) Consome os créditos do Claude?** Hoje sim, porque quem opera é você (com a ressalva de RGPD acima). Tudo o que rodar sem você vai para a API. Resumos e alertas devem custar pouco por mês. Não deixe a assinatura operando clientes sozinha.

**(c) Sistema próprio (GitHub + Supabase + Hostinger)?** Sim, mas não agora. Quando chegar a hora, construa na stack que você já domina.

**(d) Como desenvolver, em fases:**

**Fase 0 (primeira semana):**
- Travas de gasto nas plataformas.
- Contas no nome do cliente.
- Contrato com cláusula de responsabilidade e termos de RGPD.
- Uma pasta por cliente.
- Postiz cloud para publicar.
- Resumo mensal pelo WhatsApp. Looker Studio só para quem pedir.
- Abrir já a verificação de empresa na Meta e o pedido de developer token do Google, que levam semanas.

**Fase 1 (meses 1 a 3):**
- Ritual semanal: o Claude lê as métricas pelo MCP, propõe, você aprova e ele executa.
- Um `change_log.md` por cliente, com cada alteração e o tempo gasto. Esse registro vira a especificação do sistema.

**Fase 2 (sistema próprio):** Next.js + Supabase, código no GitHub, front na Hostinger.
- Tabelas de clientes, contas, métricas diárias, posts, aprovações e log.
- RLS (regras de acesso por linha) separando o que o dono vê do que o cliente vê.
- Tokens guardados no Supabase Vault.
- Edge Functions com pg_cron puxando métricas da Meta e do Google, primeiro só leitura.
- API do Claude gerando o resumo semanal e alertas de anomalia, enviados pelo n8n que você já usa.
- Área do cliente com Supabase Auth: ver os números e aprovar posts.
- Escrita em campanhas por último, passando por fila de aprovação e com limites no código (variação máxima de orçamento, nunca acima do teto).

**Gatilho para começar a Fase 2:** três condições juntas.
- 5 clientes pagando.
- Aprovações da Meta e do Google concedidas.
- O log mostrando mais de 2 horas por semana, por cliente, em tarefas repetidas.

Antes disso, construir é fugir de vender.

**Fase 3:** só depois que o sistema rodar internamente, avaliar o produto do Expansionista: anúncio → WhatsApp → venda, para negócio local.

### A primeira coisa a fazer

Hoje, em cada conta de anúncios de cliente, configure o limite de gasto da conta na Meta e o orçamento máximo no Google. Assim nenhum erro, seu ou da IA, passa de um valor que o cliente aceitou por escrito.
