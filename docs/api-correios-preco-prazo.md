# API Correios — Preço e Prazo (v3)

Documentação de referência para uso futuro das APIs de cálculo de **preço** e
**prazo** de entrega.

- **Fontes:**
  - Preço: https://apihom.correios.com.br/preco/v3/api-docs
  - Prazo: https://apihom.correios.com.br/prazo/v3/api-docs
- **Ambiente:** HOMOLOGAÇÃO (staging)
- **Produção:** trocar host `apihom.correios.com.br` por `api.correios.com.br`

---

## Autenticação

Ambas as APIs exigem o **Bearer token** obtido no
[serviço de Token](./api-correios-token.md):

```
Authorization: Bearer <token>
```

---

# Preço v3

- **Serviço:** `preco` — versão 3.18.15
- **Descrição:** Consulta de preços de produtos e serviços
- **Base URL:** `https://apihom.correios.com.br/preco`

## Endpoints

### 1. `GET /v1/nacional/{coProduto}` — Preço de um produto (nacional)

**Path params:**

| Param | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `coProduto` | string | sim | Código do produto/serviço |

**Query params (principais):**

| Param | Tipo | Descrição |
|-------|------|-----------|
| `cepOrigem` | string | CEP de origem |
| `cepDestino` | string | CEP de destino |
| `psObjeto` | string | Peso do objeto em gramas |
| `tpObjeto` | string | `1`=Envelope, `2`=Pacote, `3`=Rolo |
| `comprimento` | string | Comprimento (cm) |
| `largura` | string | Largura (cm) |
| `altura` | string | Altura (cm) |
| `diametro` | string | Diâmetro (cm) |
| `psCubico` | string | Peso cúbico (g) |
| `nuContrato` | string | Número do contrato |
| `nuDR` | integer | Número da DR do contrato |
| `nuRequisicao` | string | Número da requisição |
| `nuUnidade` | string | Número de unidades prestadas |
| `servicosAdicionais` | array[string] | Lista de serviços adicionais |
| `criterios` | array[string] | Critérios de desconto |
| `vlDeclarado` | string | Valor declarado |
| `dtEvento` | string | Data p/ cálculo (`DD-MM-YYYY`) |
| `coUnidadeOrigem` | string | Código MCMCU da unidade |
| `dtArmazenagem` | string | Data de armazenagem (`DD-MM-YYYY`) |
| `vlRemessa` | string | Valor de remessa |

```bash
curl "https://apihom.correios.com.br/preco/v1/nacional/03220?cepOrigem=01310100&cepDestino=20010000&psObjeto=500&tpObjeto=2&comprimento=20&largura=15&altura=10" \
  -H "Authorization: Bearer <token>"
```

**Resposta 200:** objeto [`PrecoProdutoResponse`](#schema-precoprodutoresponse).

---

### 2. `POST /v1/nacional` — Preço em lote (nacional)

**Body:** `LotePrecoNacionalParam`

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `idLote` | string | sim | Identificador do lote |
| `parametrosProduto` | array de `PrecoNacionalParam` | sim | Lista de produtos a cotar |

Cada `PrecoNacionalParam` aceita os mesmos campos das query params acima
(`coProduto` obrigatório).

```bash
curl -X POST "https://apihom.correios.com.br/preco/v1/nacional" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
        "idLote": "1",
        "parametrosProduto": [
          { "coProduto": "03220", "cepOrigem": "01310100", "cepDestino": "20010000", "psObjeto": "500", "tpObjeto": "2", "comprimento": "20", "largura": "15", "altura": "10" }
        ]
      }'
```

**Resposta 200:** array de `PrecoProdutoResponse`.

---

### 3. `GET /v1/internacional/{coProduto}` — Preço internacional

Igual ao nacional, **mais** o parâmetro obrigatório:

| Param | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `sgPaisDestino` | string | sim | Sigla do país de destino |

### 4. `POST /v1/internacional` — Preço internacional em lote

**Body:** `LotePrecoInternacionalParam` (`idLote` + `parametrosProduto` de
`PrecoInternacionalParam`, que exige `sgPaisDestino`).

### 5. `GET /v1/servicos-adicionais/{coProduto}` — Serviços adicionais

**Query params:** `vlDeclarado` (opc.), `dtEvento` (`YYYY-MM-DD`, opc.),
`sgPais` (opc.).

**Resposta 200:** array de `ServicoAdicionalResponse` (`codigo`, `nome`, `sigla`,
`preco`, `vlMinDeclarado`, `vlMaxDeclarado`, `requeridos`, `excludentes`,
`dtIniVigencia`, `dtFimVigencia`, …).

---

## Schema: PrecoProdutoResponse

Campos principais (há muitos campos de detalhamento de tarifa):

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `coProduto` | string | Código do produto |
| `noProduto` | string | Nome do produto |
| `pcBase` | string | Preço base (valor da proposta) |
| `pcBaseGeral` | string | Preço base + adicionais |
| `pcReferencia` | string | Preço de referência |
| `psCobrado` | string | Peso cobrado (g) |
| `inPesoCubico` | string `S`/`N` | Indicador de peso cúbico |
| `peAdValorem` | string | Percentual ad valorem |
| `vlSeguroAutomatico` | string | Valor do seguro automático |
| `pcProduto` | string | Preço do produto |
| `pcTotalServicosAdicionais` | string | Total dos serviços adicionais |
| `pcFinal` | string | **Preço final** |
| `servicoAdicional` | array de `PrecoServicoAdicional` | Serviços adicionais |
| `beneficios` | array de `BeneficioResponse` | Benefícios aplicados |
| `vlTotalBeneficios` | string | Total de benefícios |
| `taxaExtra` | array de `TaxaExtraResponse` | Taxas extras |
| `infoAdicional` | array de `InfoAdicionalResponse` | Informações adicionais |
| `txErro` | string | Descrição do erro (se houver) |

Sub-objetos relevantes:

- **`PrecoServicoAdicional`**: `coServAdicional`, `tpServAdicional`, `pcServicoAdicional`.
- **`BeneficioResponse`**: `codigo`, `tipoBeneficio` (`DP`/`DF`/`BP`/`BF`/`BC`),
  `abrangencia` (`O`=Oferta, `N`=Negociação), `percentual`, `valor`, `criterio[]`.
- **`TaxaExtraResponse`**: `codigo`, `tipo`, `vlTaxa`.

---

# Prazo v3

- **Serviço:** `prazo` — versão 3.9.26
- **Descrição:** Consulta de Prazo de entrega
- **Base URL:** `https://apihom.correios.com.br/prazo`

## Endpoints

### 1. `GET /v1/nacional/{coProduto}` — Prazo de um produto (nacional)

**Path params:** `coProduto` (string, obrigatório).

**Query params:**

| Param | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `cepOrigem` | string (8) | sim | CEP de origem |
| `cepDestino` | string (8) | sim | CEP de destino |
| `dtEvento` | string | não | Data do evento (`DD-MM-YYYY`) |

```bash
curl "https://apihom.correios.com.br/prazo/v1/nacional/03220?cepOrigem=01310100&cepDestino=20010000" \
  -H "Authorization: Bearer <token>"
```

**Resposta 200 (`PrazoNacional`):**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `coProduto` | string | Código do produto |
| `prazoEntrega` | integer | Prazo em dias úteis |
| `dataMaxima` | date-time | Data máxima de entrega |
| `entregaDomiciliar` | string | Indicador de entrega domiciliar |
| `entregaSabado` | string | Indicador de entrega aos sábados |
| `entregaDomingo` | string | Indicador de entrega aos domingos |
| `msgPrazo` | string | Mensagem sobre o prazo |
| `txErro` | string | Descrição do erro (se houver) |

---

### 2. `POST /v1/nacional` — Prazo em lote (nacional)

**Body:** `idLote` (string, obrigatório) + `parametrosPrazo` (array, obrigatório).
**Resposta 200:** array de `PrazoNacional`.

---

### 3. `GET /v1/data-prevista` — Data prevista de entrega

Calcula a data prevista a partir de origem, destino, data de postagem e prazo.

**Query params:**

| Param | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `cepOrigem` | string (`\d{8}`) | sim | CEP de origem |
| `cepDestino` | string (`\d{8}`) | sim | CEP de destino |
| `prazo` | integer | sim | Prazo em dias |
| `dtPostagem` | string | sim | Data de postagem (`DD-MM-YYYY`) |
| `isEncomendaUPU` | boolean | não | Encomenda UPU |
| `isSabadoDiaUtil` | boolean | não | Considerar sábado como dia útil |
| `isDomingoDiaUtil` | boolean | não | Considerar domingo como dia útil |
| `isPostagemDH` | boolean | não | Postagem DH |

**Resposta 200 (`DataPrevistaResponse`):** `dataPrevista` (date-time).

---

### 4. `GET /v1/coleta/{cep}` — Prazo de coleta

**Path params:** `cep` (string, obrigatório).
**Resposta 200 (`PrazoColeta`):** `prazoColeta` (integer, dias úteis), `txErro`.

---

### 5. Endpoints internacionais

| Endpoint | Observação |
|----------|------------|
| `GET /v1/internacional/{coProduto}` | **Deprecated** |
| `POST /v1/internacional` | **Deprecated** |
| `GET /v2/internacional/importacao/{coProduto}` | Prazo de importação. Params: `cepOrigem`, `cepDestino` (obrig.), `dtEvento` (opc.). Retorna `PrazoNacional` |
| `GET /v2/internacional/exportacao/{coProduto}` | Prazo de exportação. Params: `sgPaisOrigem`, `sgPaisDestino`, `dtPostagem` (todos obrig.). Retorna `PrazoInternacionalV2` (`prazoMinimo`, `prazoMaximo`, `dataMinEntrega`, `dataMaxEntrega`) |

> Para internacional, prefira os endpoints **v2** de importação/exportação — os v1
> estão marcados como deprecated.

---

## Códigos de resposta (Preço e Prazo)

| Código | Significado |
|--------|-------------|
| 200    | Consulta com sucesso |
| 400    | Erro de validação |
| 500    | Erro interno do servidor |

### Schema de erro (`MessageResponse`)

`msgs` (array de string), `date` (date-time), `method` (string), `path` (string),
`causa` (string), `stackTrace` (string).

---

## Notas

- **Formatos de data divergem entre endpoints:** preço/prazo usam `DD-MM-YYYY` em
  `dtEvento`/`dtPostagem`, mas serviços adicionais de preço usam `YYYY-MM-DD` em
  `dtEvento`. Atenção ao montar as requisições.
- O `coProduto` é o código do serviço dos Correios (ex.: PAC, SEDEX). Os códigos
  variam conforme o contrato; consulte sua tabela de produtos contratados.
- Para cotação de **vários produtos de uma vez**, use os endpoints `POST` de lote
  para reduzir o número de chamadas.
