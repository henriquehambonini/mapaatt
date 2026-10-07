# Tabela de Preço do Gás P13 – Disk Gás Indaiatuba

Ferramenta de consulta usada pelo call center para informar o preço do gás P13 conforme o bairro ou a rua do cliente em Indaiatuba/SP.

## Conteúdo

- `tabela-gas.html`: página de consulta, com busca por bairro ou por rua, preço, preço negociável e distância aproximada até a Loja 1.
- `dados/tabela.json`: base de dados com bairros, faixa de preço, preço negociável, distância e ruas de cada bairro.

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
- A versão em uso pelo atendimento é a página publicada no Claude. Este repositório guarda cópias de segurança da página e dos dados.
