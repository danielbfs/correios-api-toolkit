# API Correios — STER (Padrões Técnicos de Comunicação)

> **API de nicho.** Voltada a **empresas contratadas/parceiras** que prestam serviços
> terceirizados dentro da rede dos Correios — **não** é de uso geral para o
> desenvolvedor comum.

- **Fonte:** https://www.correios.com.br/atendimento/developers/padroes-tecnicos-de-comunicacao-ster
- **Serviço:** STER Rest — **serviceId 288**
- **Nome:** STER = Sistema de Serviços de Terceiros
- **Tipo:** padrão técnico de comunicação **+** API REST que o implementa.

## O que é / para que serve

O STER define o padrão de integração entre os sistemas de **contratados/parceiros** e a
infraestrutura dos Correios, para **registrar atendimentos e serviços** prestados nos
pontos de atendimento (e gerar protocolo). Usado por:

- Empresas que prestam serviços de terceiros na rede dos Correios;
- Desenvolvedores integrando sistemas externos aos pontos de atendimento.

## Modelos de integração

1. **Formulário dinâmico interno** — interface hospedada pelos Correios que submete à API
   do contratado.
2. **Sistema externo do contratado** — o usuário é redirecionado ao site do parceiro e,
   ao concluir, o sistema do contratado chama o STER para registrar a finalização.

## Endpoint conhecido

| Método | Path | Função |
|--------|------|--------|
| POST | `/v1/atendimentos/registra` | Registra a realização de um atendimento/serviço |

## Auth e hosts

- Autenticação via Bearer token (ver [token](./api-correios-token.md)).
- A documentação oficial referencia os hosts do **portal** (`cws`/`cwshom`); as chamadas
  REST seguem o padrão do **gateway** (`api`/`apihom`).

## Observação

> O `api-docs` (OpenAPI) deste serviço **não respondeu** no caminho padrão
> `…/ster/v3/api-docs` (HTTP 404) no momento da extração. Os detalhes acima vêm da
> página oficial de padrões técnicos, não do spec OpenAPI. Schemas de request/response
> devem ser confirmados no manual do STER no portal do desenvolvedor. Considere este
> documento um **ponteiro**, não uma referência completa.
