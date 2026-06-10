# correios-api-toolkit

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](./LICENSE)
[![Status: community](https://img.shields.io/badge/status-community%20%2F%20experimental-orange.svg)](#aviso)
[![Unofficial](https://img.shields.io/badge/correios-unofficial-lightgrey.svg)](./DISCLAIMER.md)

Documentação de referência, clientes prontos e uma skill para integrar com as **APIs REST
dos Correios** (Brasil): autenticação (token), rastreamento, preço (frete) e prazo de entrega.

> ## Aviso
> Projeto **independente e NÃO-OFICIAL**, sem vínculo com a Empresa Brasileira de Correios
> e Telégrafos. A documentação é um **resumo da comunidade** feito a partir das specs
> OpenAPI públicas e do manual de desenvolvedores; **pode conter imprecisões** e não foi
> totalmente testada contra a API real. Veja [`DISCLAIMER.md`](./DISCLAIMER.md).

## O que tem aqui

| Caminho | Conteúdo |
|---------|----------|
| [`docs/`](./docs/) | Documentação dos serviços: [token](./docs/api-correios-token.md), [rastreamento](./docs/api-correios-rastreamento.md), [preço/prazo](./docs/api-correios-preco-prazo.md) e o [índice](./docs/README.md) |
| [`skills/correios-api/`](./skills/correios-api/) | Skill para Claude Code + **clientes** Python e Node sem dependências |
| `.env.example` | Modelo de variáveis de ambiente para as credenciais |

## Serviços cobertos

| Serviço | Path (gateway) | Função |
|---------|----------------|--------|
| Token | `/token` | Autenticação — emite o Bearer token usado pelos demais |
| SRO - Rastro | `/srorastro` | Rastreamento de objetos |
| Preço | `/preco` | Cálculo de preço / frete |
| Prazo | `/prazo` | Prazo de entrega |

## Pré-requisitos

As APIs dos Correios **não são públicas**. Você precisa de:

1. Conta **Meu Correios**.
2. **Código de acesso à API**, gerado no **portal do desenvolvedor**
   (`cws`/`cwshom.correios.com.br`) em "Gestão de acesso a APIs" — não é a senha do site.
3. Para preço/prazo na maioria dos casos: **contrato** e/ou **cartão de postagem**.

## Portal vs Gateway (não confunda os hosts)

| Host | Papel |
|------|-------|
| `cws` / `cwshom.correios.com.br` | **Portal** (login no navegador) — gerar credenciais e gerenciar/subdelegar chaves |
| `api` / `apihom.correios.com.br` | **Gateway REST** — as chamadas do seu código |

## Quickstart

```bash
cp .env.example .env     # preencha CORREIOS_USER e CORREIOS_ACCESS_CODE

# Python (só stdlib)
python skills/correios-api/scripts/correios_client.py track AA123456789BR

# Node 18+ (sem dependências)
node skills/correios-api/scripts/correios_client.mjs price 03220 01310100 20010000 500
```

Os clientes já cuidam do **cache e renovação do token** (válido por 24h; renovam só nos
30 min antes de expirar, respeitando o limite de 3 req/s do endpoint de token).

## Contribuindo

Veja [`CONTRIBUTING.md`](./CONTRIBUTING.md). Correções de divergências de schema (testadas
contra a API real) são especialmente bem-vindas. **Nunca** inclua credenciais em issues/PRs.

## Licença

[Apache License 2.0](./LICENSE) — veja também [`NOTICE`](./NOTICE).
