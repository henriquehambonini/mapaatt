#!/usr/bin/env python3
"""Monta o index.html (versão Vercel) a partir de versao-claude.html + dados/tabela.json.

Uso:
    python3 scripts/montar.py            # normaliza dados/tabela.json e gera index.html
    python3 scripts/montar.py --checar   # só confere se index.html está em dia (sai com erro se não)

Regras:
- versao-claude.html é a página-fonte (idêntica ao artifact publicado no Claude).
- dados/tabela.json é a fonte dos dados (cópia do banco "tabela/atual" do artifact).
- index.html é GERADO: nunca editar à mão.
"""
import json, re, sys, pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FONTE = RAIZ / "versao-claude.html"
DADOS = RAIZ / "dados" / "tabela.json"
SAIDA = RAIZ / "index.html"

CAMPOS = ["bairros", "lojas", "precos"]


def carregar_dados():
    d = json.loads(DADOS.read_text(encoding="utf-8"))
    d = {k: d[k] for k in CAMPOS}
    erros = []
    precos = set(d["precos"])
    lojas = {l["id"] for l in d["lojas"]}
    nomes = set()
    for b in d["bairros"]:
        n = b.get("n", "").strip()
        if not n:
            erros.append("bairro sem nome")
        if n in nomes:
            erros.append(f"bairro repetido: {n}")
        nomes.add(n)
        if b.get("p") not in precos:
            erros.append(f"{n}: preço {b.get('p')} fora das faixas {sorted(precos)}")
        if b.get("pn") is not None and b["pn"] > b["p"]:
            erros.append(f"{n}: preço negociável maior que o preço")
        if b.get("l") not in lojas:
            erros.append(f"{n}: loja {b.get('l')} inexistente")
    if erros:
        sys.exit("Erros em dados/tabela.json:\n- " + "\n- ".join(erros))
    return d


def json_legivel(d):
    """Um bairro por linha: diffs do git mostram exatamente o bairro que mudou."""
    linhas = ['{"bairros":[']
    linhas += [
        json.dumps(b, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + ("," if i < len(d["bairros"]) - 1 else "")
        for i, b in enumerate(d["bairros"])
    ]
    linhas.append('],"lojas":' + json.dumps(d["lojas"], ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    linhas.append(',"precos":' + json.dumps(d["precos"]) + "}")
    return "\n".join(linhas) + "\n"


def gerar_index(d):
    corpo = FONTE.read_text(encoding="utf-8").strip()
    titulo = re.search(r"<title>.*?</title>", corpo, re.S)
    corpo = corpo.replace(titulo.group(0), "", 1).lstrip() if titulo else corpo
    embutido = json.dumps(d, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    # Fora do Claude, usa os dados embutidos antes de tentar buscar o JSON
    gancho = "  if(!window.claude){\n"
    if gancho not in corpo:
        sys.exit("Não achei o trecho de carregamento em versao-claude.html; ajuste scripts/montar.py.")
    corpo = corpo.replace(
        gancho,
        "  if(!window.claude&&window.__TABELA__){data=window.__TABELA__;streetIdx=null;renderAll();return}\n" + gancho,
        1,
    )
    return (
        "<!doctype html>\n<html lang=\"pt-BR\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">\n"
        "<meta name=\"robots\" content=\"noindex,nofollow\">\n"
        + (titulo.group(0) + "\n" if titulo else "")
        + "<!-- ARQUIVO GERADO por scripts/montar.py. Não edite: altere versao-claude.html ou dados/tabela.json. -->\n"
        "</head>\n<body>\n"
        f"<script>window.__TABELA__={embutido};</script>\n"
        + corpo
        + "\n</body>\n</html>\n"
    )


def main():
    d = carregar_dados()
    novo_json, novo_index = json_legivel(d), gerar_index(d)
    if "--checar" in sys.argv:
        ok = DADOS.read_text(encoding="utf-8") == novo_json and SAIDA.exists() and SAIDA.read_text(encoding="utf-8") == novo_index
        print("index.html em dia." if ok else "index.html desatualizado: rode python3 scripts/montar.py")
        sys.exit(0 if ok else 1)
    DADOS.write_text(novo_json, encoding="utf-8")
    SAIDA.write_text(novo_index, encoding="utf-8")
    sem = sum(1 for b in d["bairros"] if not b.get("ok"))
    print(f"OK: {len(d['bairros'])} bairros ({sem} a conferir), {sum(len(b.get('r', [])) for b in d['bairros'])} ruas -> index.html")


if __name__ == "__main__":
    main()
