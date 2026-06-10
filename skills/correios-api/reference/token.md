# Reference — Token service (`/token`)

- Spec: `https://apihom.correios.com.br/token/v3/api-docs` (v1.21.13)
- Base: `https://apihom.correios.com.br/token` (hom) / `https://api.correios.com.br/token` (prod)
- Portal (gerar código de acesso, login no navegador): `cwshom`/`cws.correios.com.br`.
  As chamadas abaixo vão para o **gateway** `apihom`/`api`, não para o portal.

## Authentication

HTTP Basic Auth with **Meu Correios** credentials:

- user = Meu Correios username
- password = **API access code** (`código de acesso`), NOT the website password

```
Authorization: Basic base64("usuario:codigoDeAcesso")
```

The response returns a Bearer token used by all other services:
`Authorization: Bearer <token>`.

## Endpoints

### POST /v1/autentica
Token from user credentials only. No body. Returns `201` + `Token`.

```bash
curl -X POST "https://apihom.correios.com.br/token/v1/autentica" \
  -H "Authorization: Basic <base64(usuario:codigoDeAcesso)>" \
  -H "Content-Type: application/json"
```

### POST /v1/autentica/contrato
Token bound to a **contract**. Body `ContratoInput`:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `numero` | string | yes | Contract number |
| `dr` | integer | no | DR/SE/regional number |

```bash
curl -X POST ".../token/v1/autentica/contrato" \
  -H "Authorization: Basic <...>" -H "Content-Type: application/json" \
  -d '{ "numero": "9912345678", "dr": 72 }'
```

### POST /v1/autentica/cartaopostagem
Token bound to a **postage card**. Body `CartaoPostagemInput`:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `numero` | string | yes | Postage card number |
| `contrato` | string | no | Contract number |
| `dr` | integer | no | DR/SE/regional number |

## Schema: Token (201 response)

| Field | Type | Description |
|-------|------|-------------|
| `token` | string | Bearer token for other APIs |
| `expiraEm` | date-time | Expiration timestamp |
| `emissao` | date-time | Issue timestamp |
| `id` | string | User id |
| `perfil` | enum `PF`/`PJ`/`S`/`A` | User profile |
| `cnpj` / `cpf` / `cie` | string | User identifiers (when applicable) |
| `contrato` / `cartaoPostagem` | object | Associated contract/card |
| `apis` | array | APIs this token authorizes |
| `tipoUnidade` | object | Unit-type permissions |

## Rate limit / reuse

- Token is **valid for 24 hours**.
- **3 requests/second** → HTTP **429** if exceeded.
- Reuse the token until close to `expiraEm`; only renew within the **30 minutes**
  before expiration. Never authenticate per business call.

## Error codes

201 ok · 400 validation · 401 not authenticated · 403 access denied · 429 rate limited · 500 server error
