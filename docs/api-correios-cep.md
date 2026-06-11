# API Correios — CEP / Endereços (v3)

Busca de endereços, localidades, bairros e faixas de CEP (base DNEC).

- **Fonte:** https://apihom.correios.com.br/cep/v3/api-docs
- **Serviço:** CEP (`cep`) — versão 3.13.16 (OpenAPI 3.1.0)
- **Base URL:** `https://apihom.correios.com.br/cep` (hom) / `https://api.correios.com.br/cep` (prod)
- **Auth:** `Authorization: Bearer <token>` (ver [token](./api-correios-token.md))

> É a API mais útil para uso geral (consulta de endereço por CEP). Ainda assim exige
> o Bearer token — não é um endpoint anônimo.

---

## Endpoints principais

### `GET /v2/enderecos/{cep}` — endereço por CEP
Path: `cep` (string, padrão `[0-9]{8}`). Resposta: `EnderecoResponse`.

```bash
curl "https://apihom.correios.com.br/cep/v2/enderecos/70150900" \
  -H "Authorization: Bearer <token>"
```

### `GET /v2/enderecos` — busca paginada de endereços
Query: `cep` (array, até 20), `uf` (enum UF), `localidade`, `bairro`, `logradouro`,
`tipoCEP` (int), `page`, `size` (até 2000). Resposta: `PagedModelEnderecoResponse`.

### Localidades
- `GET /v1/localidades` — todas (filtros: `uf`, `tipo` `M`/`D`/`P`, `localidade`, `page`, `size`)
- `GET /v1/localidades/{uf}` — por UF
- `GET /v1/localidades/lockers` — localidades com locker
- `GET /v1/localidades/cliques` — com click & collect
- `GET /v1/localidades/caixas-postais` — com caixa postal
- `GET /v1/localidades/agencias-modulares` — com agência modular

### UFs e bairros
- `GET /v1/ufs` e `GET /v1/ufs/{uf}` — estados (`UfResponse`: `uf`, `nome`, `faixas[]`)
- `GET /v1/bairros/{uf}/localidades/{localidade}` — bairros (`bairro` opcional na query)

### Metadados
- `GET /v1/atualizacao` — data da última publicação DNEC (`AtualizacaoResponse`)

---

## Schemas

**EnderecoResponse**: `cep`, `uf`, `localidade`, `logradouro`, `bairro`,
`numeroLocalidade` (int), `tipoLogradouro`, `nomeLogradouro`, `tipoCEP` (int 1–6),
`clique`, `locker`, `agenciaModular` (indicadores).

**LocalidadeResponse**: `numero` (int), `uf`, `localidade`, `tipo` (`M`/`D`/`P`),
`codificada`, `faixas[]` (`FaixaCepResponse`: `cepInicial`, `cepFinal`).

**BairroResponse**: `bairro`, `numeroBairro` (int), `faixas[]`.

## Endpoints deprecated
`GET /v1/enderecos/{cep}`, `GET /v1/enderecos`, `GET /v1/enderecos/intervalo`
(retornam `CepResponse`). Prefira os **v2**.

## UF (enum)
AC, AL, AM, AP, BA, CE, DF, ES, GO, MA, MG, MS, MT, PA, PB, PE, PI, PR, RJ, RN, RS, RO, RR, SC, SE, SP, TO.

## Códigos de resposta
200 ok · 400 validação · 401/403 auth · 429 rate limit · 500 erro.
