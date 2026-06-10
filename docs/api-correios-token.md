# API Correios — Serviço de Token (v3)

Documentação de referência para uso futuro das APIs dos Correios.

- **Fonte:** https://apihom.correios.com.br/token/v3/api-docs
- **Serviço:** Token (`token`)
- **Versão da API:** 1.21.13
- **Ambiente:** HOMOLOGAÇÃO (staging)
- **Base URL (homologação):** `https://apihom.correios.com.br/token`
- **Base URL (produção):** `https://api.correios.com.br/token`

> **Portal vs Gateway:** o código de acesso à API é gerado no **portal** do
> desenvolvedor (`cws.correios.com.br` / `cwshom.correios.com.br`, com login CAS no
> navegador). Já as **chamadas REST** abaixo vão para o **gateway** `api`/`apihom`.
> O **token retornado vale 24 horas**.

---

## Visão geral

O serviço de Token é a **porta de entrada** para todas as demais APIs dos Correios.
Você primeiro autentica neste serviço para obter um **Bearer token**, e depois usa
esse token no header `Authorization` das chamadas às APIs de negócio (rastreamento,
preço, prazo, etc.).

### Fluxo de autenticação

```
1. Credenciais Meu Correios  ──►  POST /token/v1/autentica         ──►  Bearer Token
   (Basic Auth)                   (ou /contrato, ou /cartaopostagem)
2. Bearer Token              ──►  Demais APIs Correios (Authorization: Bearer <token>)
```

---

## Autenticação

Todos os endpoints de geração de token exigem **HTTP Basic Auth** com as credenciais
do **Meu Correios**:

- **Usuário:** seu usuário do Meu Correios
- **Senha:** seu **código de acesso à API** (não é a senha de login do site)

Header:

```
Authorization: Basic base64(usuario:codigoDeAcesso)
```

> O token retornado deve ser enviado nas demais APIs como:
> `Authorization: Bearer <token>`

---

## Endpoints

### 1. `POST /v1/autentica`

Gera token a partir das credenciais do usuário (sem vínculo a contrato/cartão).

- **Operation ID:** `token`
- **Auth:** Basic Auth
- **Body:** nenhum
- **Resposta 201:** objeto [`Token`](#schema-token)

```bash
curl -X POST "https://apihom.correios.com.br/token/v1/autentica" \
  -H "Authorization: Basic <base64(usuario:codigoDeAcesso)>" \
  -H "Content-Type: application/json"
```

---

### 2. `POST /v1/autentica/contrato`

Gera token vinculado a um **contrato**.

- **Operation ID:** `tokenPorContrato`
- **Auth:** Basic Auth
- **Body:** `ContratoInput`

| Campo    | Tipo    | Obrigatório | Descrição                |
|----------|---------|-------------|--------------------------|
| `numero` | string  | sim         | Número do contrato       |
| `dr`     | integer | não         | Número da DR/SE/Regional |

```bash
curl -X POST "https://apihom.correios.com.br/token/v1/autentica/contrato" \
  -H "Authorization: Basic <base64(usuario:codigoDeAcesso)>" \
  -H "Content-Type: application/json" \
  -d '{ "numero": "9912345678", "dr": 72 }'
```

---

### 3. `POST /v1/autentica/cartaopostagem`

Gera token vinculado a um **cartão de postagem**.

- **Operation ID:** `tokenPorCartao`
- **Auth:** Basic Auth
- **Body:** `CartaoPostagemInput`

| Campo      | Tipo    | Obrigatório | Descrição                |
|------------|---------|-------------|--------------------------|
| `numero`   | string  | sim         | Número do cartão de postagem |
| `contrato` | string  | não         | Número do contrato       |
| `dr`       | integer | não         | Número da DR/SE/Regional |

```bash
curl -X POST "https://apihom.correios.com.br/token/v1/autentica/cartaopostagem" \
  -H "Authorization: Basic <base64(usuario:codigoDeAcesso)>" \
  -H "Content-Type: application/json" \
  -d '{ "numero": "0012345678", "contrato": "9912345678", "dr": 72 }'
```

---

## Schema: Token

Objeto retornado nas respostas `201` de todos os endpoints de autenticação.

| Campo            | Tipo       | Descrição                                              |
|------------------|------------|--------------------------------------------------------|
| `token`          | string     | Bearer token a ser usado nas demais APIs               |
| `expiraEm`       | date-time  | Data/hora de expiração do token                        |
| `emissao`        | date-time  | Data/hora de emissão do token                          |
| `id`             | string     | Identificador do usuário                               |
| `perfil`         | enum       | Perfil do usuário: `PF`, `PJ`, `S`, `A`                |
| `cnpj`           | string     | CNPJ (quando aplicável)                                |
| `cpf`            | string     | CPF (quando aplicável)                                 |
| `cie`            | string     | CIE (quando aplicável)                                 |
| `contrato`       | object     | Dados do contrato associado (quando aplicável)         |
| `cartaoPostagem` | object     | Dados do cartão de postagem associado (quando aplicável) |
| `apis`           | array      | Lista de APIs autorizadas para este token              |
| `tipoUnidade`    | object     | Permissões por tipo de unidade                         |

Exemplo (parcial):

```json
{
  "token": "eyJhbGciOiJSUzI1Ni␣...",
  "emissao": "2026-06-10T09:00:00Z",
  "expiraEm": "2026-06-11T09:00:00Z",
  "perfil": "PJ",
  "cnpj": "00000000000000",
  "apis": ["..."]
}
```

---

## Códigos de resposta

| Código | Significado                          |
|--------|--------------------------------------|
| 201    | Token gerado com sucesso             |
| 400    | Erro de validação                    |
| 401    | Não autenticado (credenciais inválidas) |
| 403    | Acesso negado                        |
| 429    | Limite de requisições excedido       |
| 500    | Erro interno do servidor             |

---

## Limites e boas práticas (rate limiting)

- **Limite:** **3 requisições por segundo** no endpoint de token.
- HTTP **429** é retornado quando o limite é excedido.
- **Reaproveite o token** enquanto válido — não gere um novo a cada chamada.
- Um novo token só deve ser solicitado **dentro dos 30 minutos** que antecedem a
  expiração.
- Sempre **verifique o campo `expiraEm`** antes de solicitar um novo token.

---

## Notas

- Ambiente de **homologação** (`apihom`) deve ser usado para testes; produção usa
  o host `api.correios.com.br`.
- O **código de acesso à API** é gerado/gerenciado no portal Meu Correios e é
  distinto da senha de login do site.
- Para descobrir o esquema completo (todos os campos aninhados de `contrato`,
  `cartaoPostagem`, `apis` e `tipoUnidade`), consulte o `api-docs` JSON original:
  https://apihom.correios.com.br/token/v3/api-docs
