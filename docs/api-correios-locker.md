# API Correios — Locker (v1)

Integração com lockers (armários inteligentes) dos Correios: validação de postagem,
movimentações, disponibilidade de gavetas, QR Code, SMS e coleta reversa.

- **Fonte:** https://apihom.correios.com.br/locker/v3/api-docs
- **Serviço:** Locker (`locker`) — versão 1.3.43
- **Base URL:** `https://apihom.correios.com.br/locker` (hom) / `https://api.correios.com.br/locker` (prod)
- **Auth:** `Authorization: Bearer <token>` — voltada a **parceiros/empresas credenciadas**.

---

## Endpoints

### Disponibilidade / consultas
- `GET /v1/lockers` — disponibilidade por `cepLocker` ou `cepARE`; `codigoObjeto` (obrig.).
  Retorna `Locker[]` (`ativo`, `gavetaDisponivel`, `codigoGavetaDisponivel`,
  `enderecoLocker`, `faixasCep[]`, `mcmcu`, `horarioFuncionamento`).
- `GET /v1/lockers/{cepLocker}/objetos/{codigoObjeto}/qrcode` — QR Code e short link.
- `GET /v1/lockers/coleta/consulta/pre-postagem` — consulta pré-postagem p/ autorizar coleta.

### Postagem e movimentação
- `POST /v1/lockers/postagens` — valida se o objeto pode ir ao locker
  (`RequestDadosPostagemDTO`: `destinatario`, `objeto` com `codigoServico`/`formato`/`peso`).
  `formato`: 1-Envelope, 2-Caixa/Pacote, 3-Cilindro/rolo.
- `POST /v1/lockers/movimentacoes` — registra movimentação e gera evento SRO.
  `codigoEvento` ∈ [`BDE77`, `FC57`, `BDE1`, `BDI26`].
- `POST /v1/lockers/coleta` — cria coleta reversa no locker
  (query `cepLocker`, `codigoObjeto` obrig.; `gavetaLocker` opc.).
- `POST /v1/lockers/dados-autenticacao` — envia dados de autenticação do usuário.

### Notificações / SMS
- `GET /v1/lockers/sms` — envia/reenvia SMS (`cepLocker`, `codigoObjeto`).
- `GET /v1/lockers/envio/sms/objetos/{codigoObjeto}` — consulta SMS por objeto.
- `GET /v1/lockers/envio/notificacoes` — notificações por período/status.

### Resultados / suporte
- `GET /v1/lockers/coleta/resultados` — resultados de processamento de coletas (`dtInicio`, `dtFim`).
- `GET /v1/lockers/orientacaotecnica` — arquivo de orientação técnica de integração.

---

## Erros
`MessageResponse`: `msgs[]`, `date`, `method`, `path`, `causa`, `stackTrace`.

## Notas
- API de nicho: pensada para **e-commerces/parceiros credenciados** que operam lockers,
  não para o desenvolvedor geral.
- Algumas localidades com locker podem ser descobertas via
  `GET /cep/v1/localidades/lockers` (ver [CEP](./api-correios-cep.md)).
