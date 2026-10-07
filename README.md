# Tabela de Preço do Gás P13 – Disk Gás Indaiatuba

Ferramenta de consulta usada pelo call center para informar o preço do gás P13 conforme o bairro ou a rua do cliente em Indaiatuba/SP.

## Arquivos

| Arquivo | Para que serve |
|---|---|
| `versao-claude.html` | Código da página publicada no Claude (versão em uso pelo atendimento). Lê e salva os dados no banco do artifact. |
| `dados/tabela.json` | Cópia dos dados: bairros, preço, preço negociável, distância até a Loja 1, loja que entrega e ruas de cada bairro. |
| `index.html` | Versão para a Vercel, só leitura, com os dados embutidos. **Gerada automaticamente**, não editar à mão. |
| `scripts/montar.py` | Gera o `index.html` a partir dos dois arquivos acima e valida os dados. |
| `vercel.json` | URLs limpas e `noindex` (a página não aparece no Google). |
| `CLAUDE.md` | Passo a passo para o Claude manter tudo sincronizado. |

## Como atualizar

1. Altere a tabela pela página no Claude (botão **Editar tabela**) ou peça ao Claude.
2. Atualize `dados/tabela.json` com os dados novos.
3. Rode `python3 scripts/montar.py` para regenerar o `index.html`.
4. Faça commit. A Vercel publica sozinha.

## Lojas

| Loja | Endereço |
|---|---|
| Loja 1 | Av. Francisco de Paula Leite, 3243 – Jd. Parque das Nações |
| Loja 2 | Rua Walter Gutt, 395 – Jd. Morada do Sol |
| Loja 3 | Av. Manoel Ruz Perez, 3884 – Jd. Monte Carlo |

## Faixas de preço

R$ 130,00 · R$ 132,00 · R$ 135,00 · R$ 138,00 · R$ 140,00 · R$ 142,99 · R$ 144,99

## Observações

- As distâncias são aproximadas e servem só de referência de localização. O preço vem sempre da tabela.
- Bairros com `"ok": false` ainda não tiveram preço conferido.
- As ruas vieram da base pública de CEPs do CEP Brasil (cepbrasil.org) e podem não incluir loteamentos muito recentes.
