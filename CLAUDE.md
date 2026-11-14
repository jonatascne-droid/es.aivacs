# AIVACS

Repositório do site aivacs.es e da caixa de ferramentas do Claude para a agência (em `.claude/`). Fale com o Jhony em português; tudo o que vai para o público é em espanhol da Espanha.

## Grupos de skills

Quando o Jhony pedir para usar um grupo ("use as skills de vídeos", "grupo ADS"...), carregue a skill do grupo e siga o roteiro dela.

| Grupo | Skill | Para |
|---|---|---|
| Vídeos | `grupo-videos` | Reels em motion, edição de gravações, narração, música, capas, showreel |
| Instagram e Facebook | `grupo-instagram` | Analisar Reels e perfis, carrosséis, legendas, comentários, calendário, agendar no Metricool |
| ADS | `grupo-ads` | Meta Ads e Google Ads: plano, públicos, palavras-chave, criativos, relatórios |
| Documentos | `grupo-documentos` | PDF, Word, PowerPoint, Excel, Google Docs, propostas, relatórios |
| Design | `grupo-design` | Peças, identidade, interfaces, revisão visual, animação de interface |
| Site e SEO | `grupo-site` | aivacs.es e sites de clientes, SEO, buscas com IA, conversão |
| Estratégia | `grupo-estrategia` | Plano de marketing, oferta, preço, funil, e-mail, prospecção, decisões |

O kit próprio da agência (Reels, capas, carrosséis, fotos recortadas, identidade e lições) é a skill `aivacs-estudio`. As fotos do Jhony ficam no repositório privado `jonatascne-droid/Mi-auto-trading`, pasta `aivacs/fotos/` (este repositório é público). A lista completa das skills e de onde cada uma veio está em `.claude/skills/README.md`.

## Para funcionar igual em toda sessão

- Tudo o que for reutilizável (script, modelo, lição, ajuste de skill) vai para `.claude/skills/` neste repositório e entra no `main` por PR. O scratchpad e `~/.claude` somem quando a sessão acaba.
- Antes de um trabalho de vídeo ou imagem, rode `python3 .claude/skills/aivacs-estudio/scripts/verificar.py <grupo>`.
- Conectores (Metricool, Meta Ads, Google Ads, Claude Docs) vêm da conta: se as ferramentas não aparecerem, avise o Jhony para reconectar em claude.ai → Configurações → Conectores.
- Skill ou repositório de terceiros: leia antes, copie para `.claude/skills/` com a origem e o commit no README; não rode código externo direto do clone.

## Site

HTML estático (`index.html`, `servicios/`, `portafolio/`, `privacidad/`), estilos em `styles/`, scripts em `scripts/`. Mudanças por branch e PR, conferidas no desktop e no celular.
