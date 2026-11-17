#!/usr/bin/env python3
"""Monta o HTML de um carrossel a partir de um roteiro.json e de uma marca.

Uso:
  python3 montar.py roteiro.json [carrossel.html]

O roteiro diz a marca (pasta em ../marcas/<marca>/ ou caminho de um marca.json),
o estilo (impacto, editorial ou tweet) e os slides. Cada slide vira um
<section class="slide"> de 1080x1350, pronto para o exportar.mjs.

Texto entre **asteriscos** sai na cor de destaque. Quebra de linha: \\n.
"""

import base64
import html
import json
import re
import sys
from pathlib import Path

PASTA_SKILL = Path(__file__).resolve().parent.parent
ESTILOS = ("impacto", "editorial", "tweet")
TIPOS = ("capa", "texto", "numero", "lista", "frase", "salvar", "cta")

FRASES = {
    "es": {"desliza": "Desliza", "guardar": "Guárdalo"},
    "pt": {"desliza": "Arrasta", "guardar": "Salva"},
    "en": {"desliza": "Swipe", "guardar": "Save it"},
}

SETA = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
MARCADOR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M6 3.5h12v17l-6-4.2-6 4.2z"/></svg>'


def falhar(mensagem):
    print(f"Erro: {mensagem}", file=sys.stderr)
    sys.exit(1)


def texto_rico(valor):
    """Escapa o HTML e transforma **x** em destaque e \\n em quebra de linha."""
    seguro = html.escape(str(valor or ""), quote=False)
    seguro = re.sub(r"\*\*(.+?)\*\*", r"<mark>\1</mark>", seguro)
    return seguro.replace("\n", "<br>")


def carregar_marca(nome, base_roteiro):
    candidatos = [
        PASTA_SKILL / "marcas" / nome / "marca.json",
        (base_roteiro / nome) if nome.endswith(".json") else None,
    ]
    for caminho in candidatos:
        if caminho and caminho.exists():
            marca = json.loads(caminho.read_text(encoding="utf-8"))
            marca["_pasta"] = caminho.parent
            return marca
    falhar(f'marca "{nome}" não encontrada. Crie {PASTA_SKILL / "marcas" / nome / "marca.json"}')


def fonte_css(papel, fonte, pasta):
    familia = fonte["familia"]
    css = ""
    if fonte.get("arquivo"):
        arquivo = pasta / fonte["arquivo"]
        if not arquivo.exists():
            falhar(f"fonte não encontrada: {arquivo}")
        dados = base64.b64encode(arquivo.read_bytes()).decode()
        css += (f"@font-face{{font-family:'{familia}';src:url(data:font/woff2;base64,{dados}) format('woff2');"
                f"font-weight:100 900;font-display:block}}\n")
    return css, f"--f-{papel}:'{familia}',system-ui,sans-serif;"


def logo_html(marca):
    pasta = marca["_pasta"]
    logo = marca.get("logo")
    if logo:
        arquivo = pasta / logo
        if arquivo.suffix.lower() == ".svg":
            return arquivo.read_text(encoding="utf-8")
        tipo = {"png": "png", "jpg": "jpeg", "jpeg": "jpeg", "webp": "webp"}.get(arquivo.suffix.lower().lstrip("."))
        if tipo:
            dados = base64.b64encode(arquivo.read_bytes()).decode()
            return f'<img src="data:image/{tipo};base64,{dados}" alt="">'
    iniciais = "".join(p[0] for p in marca.get("nome", "?").split()[:2]).upper()
    return f"<span class=\"iniciais\">{html.escape(iniciais)}</span>"


def topo(marca, logo, indice, total):
    return (f'<header class="topo"><span class="marca">{logo}</span>'
            f'<span class="quem"><b>{html.escape(marca.get("nome", ""))}</b>'
            f'<span>{html.escape(marca.get("perfil", ""))}</span></span>'
            f'<span class="contador">{indice:02d}/{total:02d}</span></header>')


def base(indice, total, ultimo):
    largura = round(indice / total * 100, 2)
    seta = "" if ultimo else f'<span class="seta">{SETA}</span>'
    return f'<footer class="base"><span class="progresso"><i style="width:{largura}%"></i></span>{seta}</footer>'


def corpo(slide, frases, logo):
    tipo = slide["tipo"]
    etiqueta = f'<p class="etiqueta">{texto_rico(slide["etiqueta"])}</p>' if slide.get("etiqueta") else ""
    titulo = texto_rico(slide.get("titulo"))
    texto = f'<p class="texto">{texto_rico(slide["texto"])}</p>' if slide.get("texto") else ""

    if tipo == "capa":
        apoio = f'<p class="apoio">{texto_rico(slide["apoio"])}</p>' if slide.get("apoio") else ""
        return (f'<div class="fundo-marca">{logo}</div><div class="conteudo">{etiqueta}<h1>{titulo}</h1>{apoio}'
                f'<span class="pilula">{frases["desliza"]} {SETA}</span></div>')
    if tipo == "texto":
        return f'<div class="conteudo">{etiqueta}<h2>{titulo}</h2>{texto}</div>'
    if tipo == "numero":
        return (f'<div class="conteudo">{etiqueta}<p class="numero">{texto_rico(slide["numero"])}</p>'
                f'<h2>{titulo}</h2>{texto}</div>')
    if tipo in ("lista", "salvar"):
        itens = "".join(f'<li><span class="check">{CHECK}</span><span>{texto_rico(item)}</span></li>' for item in slide.get("itens", []))
        icone = f'<p class="etiqueta">{MARCADOR} {frases["guardar"]}</p>' if tipo == "salvar" and not slide.get("etiqueta") else etiqueta
        rodape = f'<p class="rodape">{texto_rico(slide["rodape"])}</p>' if slide.get("rodape") else ""
        return f'<div class="conteudo">{icone}<h2>{titulo}</h2><ul class="itens">{itens}</ul>{rodape}</div>'
    if tipo == "frase":
        autor = f'<p class="autor">{texto_rico(slide["autor"])}</p>' if slide.get("autor") else ""
        return f'<div class="conteudo">{etiqueta}<blockquote>{texto_rico(slide["frase"])}</blockquote>{autor}</div>'
    if tipo == "cta":
        palavra = f'<p class="palavra">{html.escape(slide["palavra"])}</p>' if slide.get("palavra") else ""
        return f'<div class="conteudo">{etiqueta}<h2>{titulo}</h2>{palavra}{texto}</div>'
    falhar(f'tipo de slide desconhecido: "{tipo}" (use {", ".join(TIPOS)})')


def montar(roteiro, base_roteiro):
    marca = carregar_marca(roteiro.get("marca", "aivacs"), base_roteiro)
    estilo = roteiro.get("estilo", "impacto")
    if estilo not in ESTILOS:
        falhar(f'estilo "{estilo}" não existe (use {", ".join(ESTILOS)})')
    paleta = marca["claro" if estilo == "editorial" else "escuro"]
    idioma = roteiro.get("idioma", marca.get("idioma", "es"))
    frases = FRASES.get(idioma, FRASES["es"])
    slides = roteiro.get("slides") or falhar("o roteiro não tem slides")
    if not 2 <= len(slides) <= 10:
        falhar("o Instagram aceita de 2 a 10 slides por carrossel (o ideal aqui é de 6 a 10)")

    fontes_css, variaveis = "", ""
    for papel in ("titulo", "texto", "dados"):
        css, var = fonte_css(papel, marca["fontes"][papel], marca["_pasta"])
        fontes_css += css
        variaveis += var
    cores = "".join(f"--{nome.replace('_', '-')}:{valor};" for nome, valor in paleta.items())
    logo = logo_html(marca)

    total = len(slides)
    secoes = []
    for i, slide in enumerate(slides, start=1):
        tipo = slide.get("tipo")
        alternado = " alt" if tipo not in ("capa", "cta") and i % 2 == 0 else ""
        secoes.append(
            f'<section class="slide tipo-{tipo}{alternado}">{topo(marca, logo, i, total)}'
            f'{corpo(slide, frases, logo)}{base(i, total, i == total)}</section>'
        )

    css = (PASTA_SKILL / "templates" / "estilos.css").read_text(encoding="utf-8")
    titulo_doc = html.escape(roteiro.get("titulo", "Carrossel"))
    return (f'<!doctype html><html lang="{idioma}"><head><meta charset="utf-8"><title>{titulo_doc}</title>'
            f'<style>{fontes_css}:root{{{variaveis}{cores}}}\n{css}</style></head>'
            f'<body data-estilo="{estilo}">{"".join(secoes)}</body></html>')


def main():
    if len(sys.argv) < 2:
        falhar("uso: python3 montar.py roteiro.json [carrossel.html]")
    entrada = Path(sys.argv[1])
    saida = Path(sys.argv[2]) if len(sys.argv) > 2 else entrada.with_name("carrossel.html")
    roteiro = json.loads(entrada.read_text(encoding="utf-8"))
    saida.write_text(montar(roteiro, entrada.parent), encoding="utf-8")
    print(f"ok  {saida} ({len(roteiro['slides'])} slides, estilo {roteiro.get('estilo', 'impacto')})")


if __name__ == "__main__":
    main()
