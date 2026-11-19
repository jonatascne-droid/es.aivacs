---
name: grupo-site
description: Grupo "skills de site" da AIVACS - o site aivacs.es e sites de clientes - código, SEO, buscas com IA, dados estruturados, conversão e apps. Use quando o Jhony disser "use as skills de site", "grupo site", "grupo SEO", ou pedir mudança no site, página nova, auditoria de SEO, Google, velocidade, conversão ou um app/site para cliente.
---

# Grupo: Site e SEO

## Qual skill usar

| Pedido | Skill principal | Apoio |
|---|---|---|
| Página nova ou ajuste no aivacs.es | este repositório (HTML, `styles/`, `scripts/`) | `frontend-design`, `impeccable`, `modern-web-guidance` |
| Auditoria de SEO técnico e on-page | `seo-audit` | `marketing:seo-audit` |
| Aparecer em respostas de IA (ChatGPT, Gemini) | `ai-seo` | `llms.txt` do repositório |
| Dados estruturados (schema.org) | `schema` | |
| Estrutura de páginas e menus | `site-architecture` | |
| Páginas em escala (cidades, serviços) | `programmatic-seo` | |
| Texto do site | `copywriting`, `copy-editing` | `product-marketing` |
| Conversão (formulário, página de vendas) | `cro`, `signup`, `popups`, `onboarding` | `ab-testing` |
| Medição (GA4, eventos, UTM) | `analytics` | `attribution` |
| Negócio local: aparecer no mapa e no resumo de IA do Google, ficha do Google, avaliações, páginas por cidade | `seo-local` | `schema`, `ai-seo` |
| Copiar ou migrar o site antigo de um cliente | `clone-website` | Playwright (já instalado), `scripts/capturar.js` e `comparar.py` da skill |
| Diretórios e citações locais | `seo-local` (diretórios espanhóis) | `directory-submissions` (diretórios de SaaS e IA) |
| Ferramenta gratuita como isca | `free-tools` | |
| Site ou app para cliente sem código | conector Lovable | conector Supabase (banco e login) |
| Teste do site no navegador | `run` | Playwright (já instalado) |
| Código de cliente bagunçado (exportado do Lovable, herdado de outro dev) | `untangle-codebase` (só quando chamada) | `prune-tests` |

## Regras da casa

- Mudanças no site vão por branch e PR; confira desktop e celular antes de entregar.
- Textos do site em espanhol da Espanha; números e contatos atualizados (+2.000 projetos, +50 clientes, WhatsApp +34 603 82 96 57).
- Nada de dados pessoais no site.
