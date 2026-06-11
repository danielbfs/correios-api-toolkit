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

## Onde obter os dados de conexão

Este documento é um **ponteiro**: o STER não expôs `api-docs` OpenAPI no caminho padrão
(`…/ster/v3/api-docs` retornou **HTTP 404**). Para obter os dados completos de conexão
(schemas de request/response, parâmetros, credenciais e fluxo de integração), use as
fontes oficiais:

1. **Página de padrões técnicos (STER):**
   https://www.correios.com.br/atendimento/developers/padroes-tecnicos-de-comunicacao-ster
   — descrição, modelos de integração e manual para download.
2. **Portal do desenvolvedor (CWS):** https://cws.correios.com.br (produção) /
   https://cwshom.correios.com.br (homologação) — exige login Meu Correios. É onde ficam
   o manual do STER, o `serviceId 288` e a liberação de acesso à API.
3. **Hub de developers dos Correios:**
   https://www.correios.com.br/atendimento/developers — índice geral das APIs e manuais.
4. **Suporte/credenciamento:** como o STER é destinado a **contratados/parceiros**, o
   acesso costuma depender de credenciamento — trate via canais de atendimento a
   empresas dos Correios / gestor do contrato.

> Os detalhes deste arquivo vêm da página oficial de padrões técnicos, **não** de um
> spec OpenAPI. Confirme os schemas no manual do STER antes de implementar.
