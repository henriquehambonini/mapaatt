# Instruções para o Claude: Tabela de Preço do Gás P13

Ferramenta do call center da Disk Gás Indaiatuba (Zambonini Gás) para informar o preço do P13 por bairro ou rua.

## Onde as coisas vivem

| O quê | Onde | Papel |
|---|---|---|
| Página em uso pelo atendimento | Artifact Claude "Preço do Gás por Bairro": https://claude.ai/artifact/2ARLwawTxrCGLogVHSCfS9 | Versão oficial |
| Dados oficiais | Banco do artifact, coleção `tabela`, documento `atual` (campos `bairros`, `lojas`, `precos`) | Fonte da verdade dos preços |
| Código da página | `versao-claude.html` | Idêntico ao HTML publicado no artifact |
| Cópia dos dados | `dados/tabela.json` (um bairro por linha) | Backup e fonte da versão Vercel |
| Versão Vercel | `index.html` | **Gerado** por `scripts/montar.py`. Nunca editar à mão |

Capabilities do artifact: `{"db":{"rules":[{"path":"tabela","read":"view","write":"admin"}]},"user":{}}`.
Ao republicar a página, manter essas capabilities (omitir o campo no redeploy preserva).

## Formato de cada bairro

`{"n": nome, "p": preço, "pn": preço negociável ou null, "km": distância até a Loja 1 ou null, "l": "L1"|"L2"|"L3", "ok": conferido (bool), "r": [ruas]}`

- `p` precisa ser uma das faixas em `precos`.
- `pn` nunca maior que `p`.
- `ok: false` = preço ainda não conferido pelo Henrique.

## Fluxos de atualização

### 1. Mudar preço, bairro ou rua
1. Ler o documento ao vivo: `ArtifactData get` (url do artifact, collection `tabela`, doc_id `atual`) e guardar a `version`.
2. Aplicar a mudança e gravar com `ArtifactData update/set` usando `if_version`.
3. Copiar o resultado para `dados/tabela.json`, rodar `python3 scripts/montar.py` e fazer commit.

### 2. Mudar o layout ou a lógica da página
1. Editar `versao-claude.html`.
2. Republicar o artifact (`Artifact publish` com `url` do artifact, lendo-o antes).
3. Rodar `python3 scripts/montar.py` e fazer commit.

### 3. Conferir sincronia (sempre antes de começar)
- Comparar o documento ao vivo com `dados/tabela.json`. Se o ao vivo for diferente, alguém editou pela página: o ao vivo vence, atualize o repositório primeiro.
- `python3 scripts/montar.py --checar` confere se `index.html` está em dia.

## Regras
- O preço vem sempre da tabela; distância é só referência.
- Não inventar preço para bairro novo: perguntar ao Henrique ou marcar `ok: false`.
- Mensagens de commit em português, dizendo o que mudou (ex.: "Jd. Morada do Sol: R$ 135 → R$ 138").
