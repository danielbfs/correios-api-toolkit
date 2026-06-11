# APIs dos Correios — Documentação de referência

Documentação consolidada das APIs dos Correios para uso futuro no projeto.
Specs extraídos do ambiente de **homologação** (`apihom.correios.com.br`).

## Índice

| Documento | Serviço | Versão | O que cobre |
|-----------|---------|--------|-------------|
| [api-correios-token.md](./api-correios-token.md) | `token` | 1.21.13 | **Autenticação** — gera o Bearer token usado por todas as outras APIs |
| [api-correios-rastreamento.md](./api-correios-rastreamento.md) | `srorastro` (SRO - Rastro) | 3.5.38 | **Rastreamento** — eventos de objetos, AR digital, imagens de baixa |
| [api-correios-preco-prazo.md](./api-correios-preco-prazo.md) | `preco` + `prazo` | 3.18.15 / 3.9.26 | **Preço e Prazo** — cotação e prazo de entrega (nacional/internacional) |
| [api-correios-cep.md](./api-correios-cep.md) | `cep` | 3.13.16 | **CEP / Endereços** — busca de endereço, localidades, bairros, faixas de CEP |
| [api-correios-prepostagem.md](./api-correios-prepostagem.md) | `prepostagem` | 2.0.32 | **Pré-Postagem** — preparar envios, rótulos/etiquetas, declaração de conteúdo |
| [api-correios-coleta.md](./api-correios-coleta.md) | `coleta` | 1.0.6 | **Coleta** — solicitação e gestão de coletas/retiradas |
| [api-correios-locker.md](./api-correios-locker.md) | `locker` | 1.3.43 | **Locker** — armários inteligentes (parceiros credenciados) |
| [api-correios-ster.md](./api-correios-ster.md) | STER (serviceId 288) | — | **STER** — registro de atendimentos por contratados (nicho; ponteiro, sem api-docs) |

## Fluxo geral de uso

```
1. Credenciais Meu Correios  ──►  POST /token/v1/autentica   ──►  Bearer Token
   (HTTP Basic Auth)
2. Bearer Token              ──►  /srorastro, /preco, /prazo  (Authorization: Bearer <token>)
```

Primeiro autentique no serviço de **Token**; depois use o token retornado no header
`Authorization: Bearer <token>` das chamadas de rastreamento, preço e prazo.

## Ambientes e hosts

Há **dois hosts com papéis diferentes** — não confunda:

| Host | Papel | Quem usa |
|------|-------|----------|
| `cws.correios.com.br` / `cwshom.correios.com.br` | **Portal do desenvolvedor** (login CAS/SSO no navegador) | Você: gerar o código de acesso à API, ler manuais, gerenciar/subdelegar chaves |
| `api.correios.com.br` / `apihom.correios.com.br` | **Gateway de API REST** | Seu código: `POST /token/v1/autentica`, rastreio, preço, prazo |

> O manual oficial (https://www.correios.com.br/atendimento/developers/manuais/correioswebservice)
> documenta o **portal** (`cws`), que exige login. As **chamadas REST de integração**
> vão para o **gateway** (`api`/`apihom`) — host usado em toda esta documentação.
> Acessar `cwshom/.../api-docs` por código resulta em redirect 302 para a tela de login.

| Ambiente | Portal | Gateway de API (chamadas) |
|----------|--------|---------------------------|
| Homologação (testes) | `https://cwshom.correios.com.br` | `https://apihom.correios.com.br` |
| Produção | `https://cws.correios.com.br` | `https://api.correios.com.br` |

Os caminhos por serviço no gateway são `/token`, `/srorastro`, `/preco`, `/prazo`,
`/cep`, `/prepostagem`, `/coleta` e `/locker`. Para produção, troque apenas o host
(`apihom` → `api`).

---

## ⚠️ Observações importantes

Pontos de atenção levantados durante a extração dos specs:

### Autenticação
- O **usuário** é o do **Meu Correios**, mas a **senha** é o **código de acesso à API**
  (gerado em "Gestão de acesso a APIs" no portal Meu Correios) — **não** é a senha de
  login do site.
- **Três tipos de autorização** (conforme manual oficial): por usuário/código de acesso,
  por **contrato** ou por **cartão de postagem** — correspondem aos três endpoints de
  `/token/v1/autentica*`.
- O **token é válido por 24 horas**. Reaproveite-o; veja o campo `expiraEm`.
- Os specs OpenAPI das APIs de negócio (`srorastro`, `preco`, `prazo`) **não declaram
  o esquema de autenticação explicitamente**, mas na prática todas consomem o Bearer
  token do serviço `token`.

### Portal vs Gateway (não confundir hosts)
- **Gerar credenciais e gerenciar acesso** acontece no **portal** `cws/cwshom` (login no
  navegador). **Chamar as APIs** acontece no **gateway** `api/apihom` (com Bearer token).
- **Subdelegação:** o titular do contrato pode criar **chaves de acesso para terceiros**
  com permissões granulares por API (criar/editar/revogar, com data de expiração e
  notificação por e-mail) — útil para distribuir a integração.
- A plataforma também mantém um **SOAP legado**; para projetos novos use o **REST**
  (que é o documentado aqui).

### Rate limiting / token
- O endpoint de token tem limite de **3 requisições por segundo** → retorna **HTTP 429**
  se excedido.
- **Reaproveite o token** enquanto válido; não gere um novo a cada chamada.
- Um novo token só deve ser solicitado **dentro dos 30 minutos** que antecedem a
  expiração — sempre verifique o campo `expiraEm` antes de renovar.

### Formatos de data divergentes
- A maioria dos endpoints de preço/prazo usa **`DD-MM-YYYY`** (`dtEvento`, `dtPostagem`).
- Mas **serviços adicionais de preço** (`GET /preco/v1/servicos-adicionais/{coProduto}`)
  usa **`YYYY-MM-DD`** em `dtEvento`. Atenção ao montar as requisições.

### Limites de lote
- Rastreio em lote (`GET /srorastro/v1/objetos`): **até 50 objetos**.
- AR digital (`GET /srorastro/v1/ar-digital`): **até 10 objetos**.

### Processamento assíncrono (imagens de baixa)
- `POST /srorastro/v1/objetos/imagens` **não** retorna a imagem direto: retorna um
  **recibo** (HTTP 202). Consulte o resultado depois em `GET /srorastro/v1/recibo/{recibo}`.

### Endpoints deprecated (prazo internacional)
- `GET /prazo/v1/internacional/{coProduto}` e `POST /prazo/v1/internacional` estão
  **deprecated**. Prefira os endpoints **v2** de importação/exportação:
  `GET /prazo/v2/internacional/importacao/{coProduto}` e
  `GET /prazo/v2/internacional/exportacao/{coProduto}`.

### Códigos de produto
- O `coProduto` é o código do serviço dos Correios (ex.: PAC, SEDEX) e **varia conforme
  o contrato**. Consulte sua tabela de produtos contratados.

---

## Fontes (api-docs)

- Token: https://apihom.correios.com.br/token/v3/api-docs
- Rastreamento: https://apihom.correios.com.br/srorastro/v3/api-docs
- Preço: https://apihom.correios.com.br/preco/v3/api-docs
- Prazo: https://apihom.correios.com.br/prazo/v3/api-docs
