# API Correios — Rastreamento (SRO - Rastro v3)

Documentação de referência para uso futuro da API de rastreamento de objetos.

- **Fonte:** https://apihom.correios.com.br/srorastro/v3/api-docs
- **Serviço:** SRO - Rastro (`srorastro`)
- **Versão da API:** 3.5.38
- **Ambiente:** HOMOLOGAÇÃO (staging)
- **Base URL (homologação):** `https://apihom.correios.com.br/srorastro`
- **Base URL (produção):** `https://api.correios.com.br/srorastro`

---

## Autenticação

Esta API exige o **Bearer token** obtido no [serviço de Token](./api-correios-token.md).

```
Authorization: Bearer <token>
```

> O spec OpenAPI não declara o esquema de auth explicitamente, mas todas as APIs
> de negócio dos Correios consomem o token do serviço `token`.

---

## Endpoints

### 1. `GET /v1/objetos/{codigoObjeto}` — Rastreio de um objeto

Consulta os eventos de um único objeto.

**Path params:**

| Param | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `codigoObjeto` | string (13) | sim | Código do objeto. Ex.: `AA123456789BR` |

**Query params:**

| Param | Tipo | Obrigatório | Default | Descrição |
|-------|------|-------------|---------|-----------|
| `resultado` | enum `T`/`P`/`U` | não | `T` | `T`=todos os eventos, `P`=primeiro, `U`=último |

```bash
curl "https://apihom.correios.com.br/srorastro/v1/objetos/AA123456789BR?resultado=U" \
  -H "Authorization: Bearer <token>"
```

**Resposta 200:** objeto [`SRO`](#schema-sro).

---

### 2. `GET /v1/objetos` — Rastreio em lote

Consulta os eventos de uma lista de objetos (até 50).

**Query params:**

| Param | Tipo | Obrigatório | Default | Descrição |
|-------|------|-------------|---------|-----------|
| `codigosObjetos` | array de string (13) | sim | — | 1 a 50 códigos. Ex.: `AA123456789BR` |
| `resultado` | enum `T`/`P`/`U` | não | `U` | `T`=todos, `P`=primeiro, `U`=último |

```bash
curl "https://apihom.correios.com.br/srorastro/v1/objetos?codigosObjetos=AA123456789BR&codigosObjetos=AA987654321BR&resultado=U" \
  -H "Authorization: Bearer <token>"
```

**Resposta 200:** objeto [`SRO`](#schema-sro).

---

### 3. `GET /v1/ar-digital` — AR Digital (Aviso de Recebimento)

Consulta a imagem do AR digital (comprovante de entrega) do objeto.

**Query params:**

| Param | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `objetos` | array de string (13) | sim | Até 10 códigos separados por vírgula. Ex.: `AA123456789BR,AA987654321BR` |

**Resposta 200:** array de `ArDigitalTO`:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `objeto` | string | Código do objeto |
| `dataBaixa` | string | Data da entrega |
| `contentType` | string | MIME type da imagem |
| `imagemBase64` | string | Imagem em base64 |

---

### 4. `POST /v1/objetos/imagens` — Solicita imagens de baixa

Solicita o processamento das imagens de baixa de uma lista de objetos.
Retorna um **recibo** que deve ser consultado depois (processamento assíncrono).

**Body:** array de strings (códigos de 13 caracteres).

```bash
curl -X POST "https://apihom.correios.com.br/srorastro/v1/objetos/imagens" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '["AA123456789BR","AA987654321BR"]'
```

**Resposta 202 Accepted:** objeto `Recibo`:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `numero` | string (32) | Número do recibo |
| `dtCriacao` | date-time | Data de criação |
| `dtValidade` | date-time | Data de validade |
| `qtdObjetos` | integer | Quantidade de objetos |
| `resultado` | enum `P`/`U`/`T` | Tipo de resultado (primeiro/último/todos) |
| `idioma` | enum `PT`/`EN`/`ES` | Idioma |

---

### 5. `GET /v1/recibo/{recibo}` — Consulta recibo de imagens

Consulta o resultado do processamento de um recibo (gerado pelo endpoint anterior).

**Path params:**

| Param | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `recibo` | string | sim | Número do recibo. Ex.: `d2ddbca351cf455c939d694cefb23611` |

**Resposta 200:** array de `ObjetoImagemTO`:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `objeto` | string (13) | Código do objeto |
| `observacao` | string (40) | Observação da imagem |
| `imagens` | array de `ImagemTO` | `imagem` (byte base64), `comentario` (string 20) |

---

## Schema: SRO

Objeto retornado nos endpoints de rastreio (1 e 2).

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `versao` | string (8) | Versão da API |
| `quantidade` | integer | Quantidade de objetos rastreados |
| `objetos` | array de [`Objeto`](#schema-objeto) | Objetos consultados |
| `tipoResultado` | string | Descrição do tipo de resultado |

### Schema: Objeto

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `codObjeto` | string (13) | Código do objeto |
| `tipoPostal` | object | Tipo postal |
| `dtPrevista` | date-time | Entrega prevista |
| `multiVolume` | string (5) | Quantidade de volumes |
| `afterschedule` | enum `S`/`N` | Postado fora do horário |
| `volume` | integer | Número do volume |
| `valorRecebido` | string (11) | Valor recebido |
| `entregaProgramada` | date-time | Entrega programada |
| `prazoTratamento` | integer | Prazo de tratamento (dias) |
| `contrato` | string (15) | Número do contrato |
| `peso` | number | Peso em gramas |
| `valorDeclarado` | number | Valor declarado |
| `eventos` | array de [`Evento`](#schema-evento) | Eventos do objeto |
| `servico` | object | Dados do serviço |

### Schema: Evento

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `codigo` | string (3) | Código do evento |
| `tipo` | string (2) | Tipo/motivo do evento |
| `dtHrCriado` | date-time | Data/hora do evento |
| `descricao` | string (80) | Descrição do evento |
| `estacao` | string (3) | Estação de trabalho |
| `usuario` | string (8) | Usuário responsável |
| `carteiro` | string (8) | ID do carteiro |
| `latitude` / `longitude` | string | Geolocalização |
| `detalhe` | string (80) | Detalhe do evento |
| `recebedor` | object | Dados do recebedor |
| `unidade` | object | Unidade de tratamento |
| `entregadorExterno` | object | Entregador externo |
| `contrato` | string (15) | Número do contrato |
| `servico` | object | Dados do serviço |
| `remetente` | object | Dados do remetente |
| `destinatario` | object | Dados do destinatário |

### Campos do serviço (Servico) — flags `S`/`N`

`ar` (tem AR), `tipoAr` (`N`/`C`/`D`/`E`/`V`), `mp` (mão própria), `vd` (valor
declarado), `eVizinho` (entrega ao vizinho), `fotoFachada`, `eControlada`,
`eInterativa`, `eLocker`, `devDocumento`, `dgr` (transporte de perigosos).

### Campos de endereço (Endereco)

`cep` (8), `logradouro` (80), `complemento` (60), `numero` (12), `bairro` (60),
`cidade` (60), `uf` (2), `pais`, `telefone` (13), `erro` (array).

---

## Códigos de resposta

| Código | Significado |
|--------|-------------|
| 200    | Consulta com sucesso |
| 202    | Solicitação aceita (processamento de imagens) |
| 400    | Requisição inválida |
| 500    | Erro interno do servidor |

---

## Notas

- Use `resultado=U` para obter apenas o **último evento** (mais leve) quando só
  precisa do status atual.
- O rastreio em lote aceita **até 50 objetos**; o AR digital, **até 10**.
- As imagens de baixa são **assíncronas**: `POST /objetos/imagens` retorna um
  recibo, e você consulta o resultado em `GET /recibo/{recibo}`.
