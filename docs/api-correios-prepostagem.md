# API Correios — Pré-Postagem (v1/v2)

Criação e gestão de pré-postagens (preparação de envios, geração de rótulos/etiquetas e
declaração de conteúdo antes de postar).

- **Fonte:** https://apihom.correios.com.br/prepostagem/v3/api-docs
- **Serviço:** Pré-postagem (`prepostagem`) — versão 2.0.32 (OpenAPI 3.1.0)
- **Base URL:** `https://apihom.correios.com.br/prepostagem` (hom) / `https://api.correios.com.br/prepostagem` (prod)
- **Auth:** `Authorization: Bearer <token>` — requer **contrato/cartão de postagem**.

---

## Endpoints principais

### `POST /v1/prepostagens` — criar pré-postagem
Body: `RequestPrePostagemExternaDTO`:

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `remetente` | `RemetenteDTO` | sim | Dados do remetente |
| `destinatario` | `DestinatarioDTO` | sim | Dados do destinatário |
| `codigoServico` | string | sim | Código do serviço (PAC, SEDEX, …) |
| `pesoInformado` | string | sim | Peso em gramas |
| `itensDeclaracaoConteudo` | array | sim | Itens da declaração de conteúdo |
| `logisticaReversa` | enum `S`/`N` | não | Indicador de logística reversa |
| `emiteDCe` | string | não | Emite declaração de conteúdo eletrônica |

### `GET /v1/prepostagens` e `GET /v2/prepostagens` — consultar
Query comuns: `page` (default `0`), `size` (default `50`),
`status` (`PREATENDIDO`/`PREPOSTADO`/`POSTADO`/`EXPIRADO`/`CANCELADO`/`ESTORNADO`/`PENDENTE`),
`tipoObjeto` (`TODOS`/`SIMPLES`/`REGISTRADO`).

### Cancelamento
- `DELETE /v1/prepostagens/{id}` — cancela por ID
- `DELETE /v1/prepostagens/objeto/{codigoObjeto}` — cancela por código do objeto

### Rótulos / etiquetas (assíncrono)
- `POST /v1/prepostagens/rotulo/range` — solicita faixa de rótulos
- `POST /v1/prepostagens/rotulo/assincrono/pdf` — gera PDF por IDs (assíncrono)
- `POST /v1/prepostagens/rotulo/lote/assincrono/pdf` — gera PDF em lote (assíncrono)

### Lote e outros
- `POST/GET /v1/prepostagens/lote` — operações em lote
- `POST /v1/prepostagens/assincrona` (+ `DELETE`) — criação assíncrona
- `POST /v1/prepostagens/lista/objetosregistrados` — importa objetos registrados
- `POST /v1/prepostagens/dce/dace/impressao` — gera impressão DACE
- `PATCH /v1/prepostagens/dce` — atualiza documento fiscal
- `PATCH /v1/prepostagens/{id}/logisticareversa` — atualiza logística reversa

---

## Schema de resposta (PrePostagem)
Objeto com 60+ campos, incluindo: `id`, `codigoObjeto`, `statusAtual`,
`dataHoraStatusAtual`, além dos dados de remetente/destinatário/serviço.

**Status (enum):** `PREATENDIDO`, `PREPOSTADO`, `POSTADO`, `EXPIRADO`, `CANCELADO`,
`ESTORNADO`, `PENDENTE`.

## Erros
`MessageResponse`: `msgs[]`, `date`, `method`, `path`, `causa`, `stackTrace`.
Códigos: 200/201 ok · 400 validação · 401/403 auth · 500 erro.

## Notas
- Vários fluxos de rótulo/PDF são **assíncronos**: você solicita e depois consulta o
  resultado/baixa o PDF.
- Exige contrato/cartão; o token precisa estar autorizado para o serviço de postagem.
