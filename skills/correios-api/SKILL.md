---
name: correios-api
description: Connect to the Brazilian Correios REST APIs (api.correios.com.br). Use this skill whenever the user wants to integrate with Correios — generate an authentication Bearer token, track packages/objects (rastreamento), calculate shipping price/freight (preço), or query delivery deadlines (prazo). Triggers include "rastrear encomenda", "calcular frete", "prazo de entrega Correios", "token Correios", "API Correios", a 13-char tracking code like AA123456789BR, or a request to call any *.correios.com.br endpoint.
---

# Correios API integration

Helps connect to the Brazilian postal service (Correios) REST APIs. There are four
services, all on the same host:

| Service | Path | Purpose |
|---------|------|---------|
| Token | `/token` | Authentication — issues the Bearer token the others require |
| SRO - Rastro | `/srorastro` | Package tracking (events, AR digital, images) |
| Preço | `/preco` | Shipping price / freight quote |
| Prazo | `/prazo` | Delivery deadline |

## Prerequisites (the user must have these)

Correios APIs are **not public** — the user needs a registered account and credentials:

1. A **Meu Correios** account (https://www.correios.com.br/).
2. An **API access code** (`código de acesso à API`) generated in the developer portal
   (`cws`/`cwshom`) under "Gestão de acesso a APIs". **This is NOT the website login
   password** — it is a separate token.
3. For most price/deadline/posting operations, a **contract** (`contrato`) and/or
   **postage card** (`cartão de postagem`).

If the user does not have these, tell them they must obtain them first — there is no
public/anonymous access. Never invent or hardcode credentials.

## Environments — two hosts, two roles (do not mix them)

| Host | Role | Used by |
|------|------|---------|
| `cws.correios.com.br` / `cwshom.correios.com.br` | **Developer portal** (browser CAS login) | The human: generate the API access code, read manuals, manage/subdelegate keys |
| `api.correios.com.br` / `apihom.correios.com.br` | **REST API gateway** | Your code: `/token`, `/srorastro`, `/preco`, `/prazo` |

The official manual documents the **portal** (`cws`), which requires login. All
programmatic REST calls go to the **gateway** (`api`/`apihom`) — that is the host used
throughout this skill. Hitting `cwshom/.../api-docs` from code returns a 302 redirect to
the login page, not JSON.

| Environment | Portal | API gateway (calls) |
|-------------|--------|---------------------|
| Homologação (sandbox/testing) | `https://cwshom.correios.com.br` | `https://apihom.correios.com.br` |
| Produção | `https://cws.correios.com.br` | `https://api.correios.com.br` |

Always develop and test against **homologação** first. Paths (`/token`, `/srorastro`,
`/preco`, `/prazo`) are identical in both environments; only the host changes.

## The core flow

```
1. Basic Auth (usuario + código de acesso)  ──►  POST /token/v1/autentica  ──►  Bearer token
2. Bearer token  ──►  /srorastro · /preco · /prazo   (header: Authorization: Bearer <token>)
```

Every business call needs `Authorization: Bearer <token>`. Get the token first, then
reuse it until it is close to expiring.

## How to use this skill

1. Confirm which operation the user wants: authenticate, track, price, or deadline.
2. Confirm the **environment** (homologação vs produção) — default to homologação.
3. Read the matching reference file for exact endpoints, params and schemas:
   - `reference/token.md` — authentication, the three token endpoints, token schema.
   - `reference/rastreamento.md` — tracking, AR digital, batch limits, image flow.
   - `reference/preco-prazo.md` — price and deadline endpoints and params.
4. To produce runnable code, adapt `scripts/correios_client.py` (Python, stdlib-only)
   or `scripts/correios_client.mjs` (Node, no deps). Both implement token caching and
   the main calls. Pass credentials via environment variables — never inline them.

## Critical gotchas (read before writing any integration)

- **Token reuse & rate limit.** The token is **valid for 24 hours**. The token endpoint
  allows **3 requests/second** and returns **HTTP 429** if exceeded. Cache the token and
  reuse it; only request a new one within the **30 minutes before** the `expiraEm`
  timestamp. Do not authenticate per call.
- **Three authorization types** (per the official manual): by user/access-code, by
  **contract**, or by **postage card** — matching the three `/token/v1/autentica*`
  endpoints. A contract holder can **subdelegate** granular per-API access keys to third
  parties (created/managed in the portal, with expiry and email notifications).
- **Legacy SOAP still exists.** This skill targets the modern **REST** API; prefer it for
  new integrations.
- **Credentials.** Basic Auth user = Meu Correios username; password = the **API access
  code**, not the site password. Base64-encode `usuario:codigoDeAcesso`.
- **Date formats differ between endpoints.** Most preço/prazo params use **`DD-MM-YYYY`**
  (`dtEvento`, `dtPostagem`), but `GET /preco/v1/servicos-adicionais/{coProduto}` uses
  **`YYYY-MM-DD`** for `dtEvento`. Check the reference before formatting dates.
- **Batch limits.** Tracking batch (`GET /srorastro/v1/objetos`) accepts **up to 50**
  objects; AR digital (`GET /srorastro/v1/ar-digital`) accepts **up to 10**.
- **Image-of-delivery is async.** `POST /srorastro/v1/objetos/imagens` returns a
  **receipt** (HTTP 202), not the image. Poll `GET /srorastro/v1/recibo/{recibo}` after.
- **Deprecated prazo endpoints.** Avoid `GET/POST /prazo/v1/internacional`; use the
  **v2** import/export endpoints instead.
- **`coProduto` varies by contract** (PAC, SEDEX, etc.). Use the user's contracted
  product table; do not guess codes.
- **Never log or echo the token or credentials.** Treat them as secrets.

## Error handling

Business APIs return errors as `MessageResponse`: `msgs[]`, `date`, `method`, `path`,
`causa`, `stackTrace`. Common HTTP codes: 400 (validation), 401 (not authenticated),
403 (access denied), 429 (rate limited), 500 (server error). On 401/403 from a business
call, the token is likely expired or lacks scope for that API — re-authenticate or check
which `apis` the token authorizes (see the token schema).
