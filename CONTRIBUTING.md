# Contribuindo

Obrigado pelo interesse! Este é um projeto da comunidade para documentar e facilitar o
uso das APIs REST dos Correios. Contribuições são bem-vindas.

## Como contribuir

1. Abra uma **issue** descrevendo a correção/melhoria, ou
2. Faça um **fork**, crie um branch e abra um **pull request**.

## Tipos de contribuição mais úteis

- **Correções de schema/divergências:** se você testou um endpoint contra a API real
  (homologação ou produção) e o comportamento difere do documentado, relate — de
  preferência com o `serviceId`, a versão do `api-docs` e um exemplo de requisição
  **sem credenciais ou dados pessoais**.
- **Novos serviços:** outros `serviceId` dos Correios que exponham `/<servico>/v3/api-docs`
  e sejam de uso geral (ex.: logística reversa).
- **Exemplos de código** em outras linguagens.
- **Melhorias de redação** na documentação.

## Regras importantes

- **NUNCA** inclua credenciais, tokens, números de contrato/cartão reais ou dados
  pessoais em código, exemplos, issues ou PRs. Use placeholders.
- Não copie conteúdo proprietário **verbatim** do material dos Correios — resuma e
  reescreva com suas palavras.
- Mantenha o tom de referência **não-oficial** (ver `DISCLAIMER.md`).
- Ao alterar um arquivo, indique claramente o que mudou.

## Validação local

Os clientes em `skills/correios-api/scripts/` não têm dependências externas:

- Python: `python correios_client.py track AA123456789BR`
- Node 18+: `node correios_client.mjs track AA123456789BR`

Configure as credenciais por variáveis de ambiente (ver `.env.example`). Teste sempre
em **homologação** primeiro.

## Licença das contribuições

Ao contribuir, você concorda em licenciar sua contribuição sob a
**Apache License 2.0** (ver `LICENSE`).
