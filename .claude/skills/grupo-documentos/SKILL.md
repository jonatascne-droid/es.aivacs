---
name: grupo-documentos
description: Grupo "skills de documentos" da AIVACS - PDF, Word, PowerPoint, Excel, Google Docs/Sheets, propostas, relatórios e apresentações. Use quando o Jhony disser "use as skills de documentos", "grupo PDF", "grupo documentos", ou pedir para ler, criar, editar, juntar ou preencher PDF, proposta comercial, contrato, orçamento, planilha, relatório ou apresentação.
---

# Grupo: Documentos

## Ao ser chamado

Escolha pela tabela e leia a skill antes de começar. As skills `anthropic-skills:*` vêm da conta do Jhony e estão em toda sessão; as demais estão neste repositório.

## Qual skill usar

| Pedido | Skill principal | Apoio |
|---|---|---|
| Ler, extrair, juntar, dividir, preencher ou criar PDF | `anthropic-skills:pdf` | |
| Documento Word (.docx): proposta, contrato | `anthropic-skills:docx` | `copywriting`, `sales-enablement` |
| Apresentação PowerPoint (.pptx) | `anthropic-skills:pptx` | `slideshow` (apresentação ao vivo em HTML) |
| Planilha Excel (.xlsx): orçamento, controle | `anthropic-skills:xlsx` | `data:analyze` |
| Google Docs, Sheets, Drive, Gmail, Agenda | `anthropic-skills:google-workspace` | |
| Documento vivo para editar e compartilhar | conector Claude Docs (`anthropic-skills:docs`) | |
| Página para mostrar ou compartilhar (relatório visual, proposta navegável) | ferramenta Artifact | `artifact-design`, `dataviz` |
| Pôster ou peça visual em PDF/PNG | `canvas-design` | identidade em `aivacs-estudio/references/identidade.md` |
| Gráficos e análise de dados | `dataviz`, `data:create-viz`, `data:analyze` | |
| Pesquisa aprofundada com fontes | `anthropic-skills:deep-research` | |

## Regras da casa

- Documentos da AIVACS seguem a identidade (cores, Plus Jakarta Sans, logo); para cliente, a marca dele.
- Dados pessoais (documento de identidade, endereço) só quando o Jhony pedir, e nunca em página pública.
- Entregue o arquivo na pasta de trabalho e mostre o resultado (página de revisão ou o arquivo) antes de enviar a alguém.
