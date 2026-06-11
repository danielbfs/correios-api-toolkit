# API Correios — Coleta (v1/v2)

Solicitação e gestão de coletas (pedido de retirada de objetos pelos Correios).

- **Fonte:** https://apihom.correios.com.br/coleta/v3/api-docs
- **Serviço:** Coleta (`coleta`) — versão 1.0.6 (OpenAPI 3.0.1)
- **Base URL:** `https://apihom.correios.com.br/coleta` (hom) / `https://api.correios.com.br/coleta` (prod)
- **Auth:** `Authorization: Bearer <token>` — requer **contrato**.

---

## Endpoints

| Método | Path | Função |
|--------|------|--------|
| POST | `/v2/solicitacoes` | Incluir solicitação de coleta (body `SolicitacaoColeta`) |
| POST | `/v1/solicitacoes/assincrono` | Solicitação de coleta assíncrona |
| PATCH | `/v1/solicitacao` | Atualizar solicitação (body `AtualizacaoColeta`) |
| GET | `/v1/solicitacoes/{numeroColeta}` | Consultar solicitação (path `numeroColeta` int64) |
| DELETE | `/v1/solicitacoes/{numeroColeta}` | Cancelar solicitação |
| GET | `/v1/solicitacoes/resumo/{contrato}/{qtdDias}` | Resumo de postagens por período |
| GET | `/v1/servicos/coleta/a-vista` | Consultar serviço de coleta à vista |
| GET | `/v1/abrangencias` | Áreas de abrangência (query `cep` e `servico`, obrigatórios) |
| DELETE | `/v1/cancela/{numeroColeta}/{idCorreios}` | Cancelar coleta (**deprecated**) |

```bash
curl "https://apihom.correios.com.br/coleta/v1/abrangencias?cep=70150900&servico=03220" \
  -H "Authorization: Bearer <token>"
```

---

## Schemas (campos obrigatórios)

- **Cliente:** `nome`, `cnpjCpf`, `email`, `telefone`, `idCorreios`.
- **Endereco:** `logradouro`, `numero`, `bairro`, `cidade`, `uf`, `cep`.
- **ObjetoPostal:** `etiqueta`, `servicoPostal`.
- **Telefone:** `ddd`, `numero`.

## Erros
`MessageResponse`: `msgs[]`, `date`, `method`, `path`, `causa`, `stackTrace`.

## Notas
- Use `GET /v1/abrangencias` para checar se há cobertura de coleta para um CEP/serviço
  antes de criar a solicitação.
- Prefira `POST /v2/solicitacoes` e evite os endpoints **deprecated**.
