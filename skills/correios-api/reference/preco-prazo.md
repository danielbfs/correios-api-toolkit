# Reference — Price (`/preco`) and Deadline (`/prazo`)

- Preço spec: `https://apihom.correios.com.br/preco/v3/api-docs` (v3.18.15)
- Prazo spec: `https://apihom.correios.com.br/prazo/v3/api-docs` (v3.9.26)
- Auth: `Authorization: Bearer <token>` (from `/token`)

---

# Preço (`/preco`)

### GET /v1/nacional/{coProduto}
Path: `coProduto` (string, required). Main query params:

| Param | Description |
|-------|-------------|
| `cepOrigem` / `cepDestino` | Origin / destination CEP |
| `psObjeto` | Weight in grams |
| `tpObjeto` | `1`=Envelope, `2`=Pacote, `3`=Rolo |
| `comprimento` / `largura` / `altura` / `diametro` | Dimensions in cm |
| `psCubico` | Cubic weight (g) |
| `nuContrato` / `nuDR` | Contract / DR number |
| `nuRequisicao` | Request number |
| `nuUnidade` | Number of units |
| `servicosAdicionais` | array[string] additional services |
| `criterios` | array[string] discount criteria |
| `vlDeclarado` | Declared value |
| `dtEvento` | Calc date — format `DD-MM-YYYY` |
| `coUnidadeOrigem` | MCMCU unit code |
| `dtArmazenagem` | Storage date `DD-MM-YYYY` |
| `vlRemessa` | Remittance value |

```bash
curl ".../preco/v1/nacional/03220?cepOrigem=01310100&cepDestino=20010000&psObjeto=500&tpObjeto=2&comprimento=20&largura=15&altura=10" \
  -H "Authorization: Bearer <token>"
```

### POST /v1/nacional — batch
Body `LotePrecoNacionalParam`: `idLote` (string, req), `parametrosProduto` (array of
`PrecoNacionalParam`, each = the params above with `coProduto` required). Returns array.

### GET /v1/internacional/{coProduto} — same as nacional + required `sgPaisDestino`.
### POST /v1/internacional — batch international (`PrecoInternacionalParam` needs `sgPaisDestino`).
### GET /v1/servicos-adicionais/{coProduto}
Query: `vlDeclarado` (opt), `dtEvento` (**`YYYY-MM-DD`**, opt), `sgPais` (opt).
Returns array of `ServicoAdicionalResponse`.

## Schema: PrecoProdutoResponse (key fields)
`coProduto`, `noProduto`, `pcBase`, `pcBaseGeral`, `pcReferencia`, `psCobrado`(g),
`inPesoCubico`(`S`/`N`), `peAdValorem`, `vlSeguroAutomatico`, `pcProduto`,
`pcTotalServicosAdicionais`, **`pcFinal`** (final price), `servicoAdicional[]`,
`beneficios[]`, `vlTotalBeneficios`, `taxaExtra[]`, `infoAdicional[]`, `txErro`.

- `PrecoServicoAdicional`: `coServAdicional`, `tpServAdicional`, `pcServicoAdicional`.
- `BeneficioResponse`: `codigo`, `tipoBeneficio`(`DP`/`DF`/`BP`/`BF`/`BC`),
  `abrangencia`(`O`=oferta,`N`=negociação), `percentual`, `valor`, `criterio[]`.
- `TaxaExtraResponse`: `codigo`, `tipo`, `vlTaxa`.

---

# Prazo (`/prazo`)

### GET /v1/nacional/{coProduto}
Path: `coProduto` (req). Query: `cepOrigem`(8, req), `cepDestino`(8, req),
`dtEvento` (`DD-MM-YYYY`, opt).

Response `PrazoNacional`: `coProduto`, `prazoEntrega`(int business days),
`dataMaxima`, `entregaDomiciliar`, `entregaSabado`, `entregaDomingo`, `msgPrazo`, `txErro`.

```bash
curl ".../prazo/v1/nacional/03220?cepOrigem=01310100&cepDestino=20010000" \
  -H "Authorization: Bearer <token>"
```

### POST /v1/nacional — batch
Body: `idLote` (req) + `parametrosPrazo` (array, req). Returns array of `PrazoNacional`.

### GET /v1/data-prevista — predicted delivery date
Query: `cepOrigem`(`\d{8}`, req), `cepDestino`(`\d{8}`, req), `prazo`(int days, req),
`dtPostagem` (`DD-MM-YYYY`, req), `isEncomendaUPU`/`isSabadoDiaUtil`/`isDomingoDiaUtil`/`isPostagemDH` (bool, opt).
Response `DataPrevistaResponse`: `dataPrevista`.

### GET /v1/coleta/{cep} — collection deadline
Path: `cep` (req). Response `PrazoColeta`: `prazoColeta`(int days), `txErro`.

### International
- `GET /v1/internacional/{coProduto}` — **DEPRECATED**
- `POST /v1/internacional` — **DEPRECATED**
- `GET /v2/internacional/importacao/{coProduto}` — query `cepOrigem`,`cepDestino`(req), `dtEvento`(opt). Returns `PrazoNacional`.
- `GET /v2/internacional/exportacao/{coProduto}` — query `sgPaisOrigem`,`sgPaisDestino`,`dtPostagem` (all req). Returns `PrazoInternacionalV2` (`prazoMinimo`,`prazoMaximo`,`dataMinEntrega`,`dataMaxEntrega`).

---

## Error response (MessageResponse)
`msgs[]`, `date`, `method`, `path`, `causa`, `stackTrace`.
Codes: 200 ok · 400 validation · 500 server error.

## Gotchas
- **Date format differs**: most use `DD-MM-YYYY`; `servicos-adicionais` uses `YYYY-MM-DD`.
- `coProduto` varies by contract (PAC, SEDEX, ...). Use the contracted product table.
- Prefer batch `POST` endpoints to cut request count when quoting many products.
- Prefer prazo **v2** international endpoints over the deprecated v1.
