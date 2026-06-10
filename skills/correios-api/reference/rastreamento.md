# Reference — Tracking (SRO - Rastro, `/srorastro`)

- Spec: `https://apihom.correios.com.br/srorastro/v3/api-docs` (v3.5.38)
- Auth: `Authorization: Bearer <token>` (from `/token`)

## Endpoints

### GET /v1/objetos/{codigoObjeto} — single object
Path: `codigoObjeto` (string, 13 chars, required) e.g. `AA123456789BR`.
Query: `resultado` enum `T`/`P`/`U` (default `T`) — all / first / last event.
Returns `200` + `SRO`.

```bash
curl ".../srorastro/v1/objetos/AA123456789BR?resultado=U" \
  -H "Authorization: Bearer <token>"
```

### GET /v1/objetos — batch (up to 50)
Query:
- `codigosObjetos` (array of 13-char strings, required, 1–50 items)
- `resultado` enum `T`/`P`/`U` (default `U`)

Returns `200` + `SRO`.

### GET /v1/ar-digital — proof of delivery (up to 10)
Query: `objetos` (array of 13-char strings, required, max 10, comma-separated).
Returns array of `ArDigitalTO`: `objeto`, `dataBaixa`, `contentType`, `imagemBase64`.

### POST /v1/objetos/imagens — request delivery images (async)
Body: array of 13-char object codes. Returns `202` + `Recibo`:
`numero`(32), `dtCriacao`, `dtValidade`, `qtdObjetos`, `resultado`(`P`/`U`/`T`), `idioma`(`PT`/`EN`/`ES`).

### GET /v1/recibo/{recibo} — fetch async result
Path: `recibo` (string). Returns array of `ObjetoImagemTO`:
`objeto`(13), `observacao`(40), `imagens[]` of `ImagemTO` (`imagem` byte base64, `comentario`(20)).

## Schema: SRO

`versao`(8), `quantidade`(int), `objetos[]` (Objeto), `tipoResultado`(string).

### Objeto
`codObjeto`(13), `tipoPostal`, `dtPrevista`, `multiVolume`(5), `afterschedule`(`S`/`N`),
`volume`(int), `valorRecebido`(11), `entregaProgramada`, `prazoTratamento`(int days),
`contrato`(15), `peso`(g), `valorDeclarado`, `eventos[]` (Evento), `servico`.

### Evento
`codigo`(3), `tipo`(2), `dtHrCriado`, `descricao`(80), `estacao`(3), `usuario`(8),
`carteiro`(8), `latitude`/`longitude`, `detalhe`(80), `recebedor`, `unidade`,
`entregadorExterno`, `contrato`(15), `servico`, `remetente`, `destinatario`.

### Servico flags (`S`/`N` unless noted)
`ar`, `tipoAr`(`N`/`C`/`D`/`E`/`V`), `mp` (mão própria), `vd` (valor declarado),
`eVizinho`, `fotoFachada`, `eControlada`, `eInterativa`, `eLocker`, `devDocumento`,
`dgr` (dangerous goods).

### Endereco
`cep`(8), `logradouro`(80), `complemento`(60), `numero`(12), `bairro`(60),
`cidade`(60), `uf`(2), `pais`, `telefone`(13), `erro[]`.

## Notes
- Use `resultado=U` for just the current status (lighter payload).
- Batch tracking max **50**; AR digital max **10**.
- Delivery images are async: POST → receipt (202) → GET /recibo/{recibo}.

## Error codes
200 ok · 202 accepted · 400 bad request · 500 server error
