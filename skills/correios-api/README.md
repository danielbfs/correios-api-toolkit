# Skill: correios-api

Uma **Claude Code Skill** compartilhável para integrar com as APIs REST dos Correios
(Brasil): autenticação (token), rastreamento, preço (frete) e prazo de entrega.

Pode ser usada por qualquer pessoa — basta ter credenciais válidas dos Correios.

## Conteúdo

```
correios-api/
├─ SKILL.md                       # ponto de entrada (lido pelo Claude)
├─ README.md                      # este arquivo
├─ reference/
│  ├─ token.md                    # autenticação + schema do token
│  ├─ rastreamento.md             # SRO - Rastro (tracking)
│  └─ preco-prazo.md              # preço e prazo
└─ scripts/
   ├─ correios_client.py          # cliente Python (stdlib, sem deps)
   └─ correios_client.mjs         # cliente Node (sem deps, Node 18+)
```

## Pré-requisitos (do usuário)

As APIs dos Correios **não são públicas**. Você precisa de:

1. Conta **Meu Correios** (https://www.correios.com.br/).
2. **Código de acesso à API** gerado no **portal do desenvolvedor**
   (`cws`/`cwshom.correios.com.br`, login no navegador) em "Gestão de acesso a APIs"
   — não é a senha de login do site.
3. Para preço/prazo/postagem na maioria dos casos: **contrato** e/ou **cartão de postagem**.

> **Portal vs Gateway:** você gera/gerencia credenciais no **portal** `cws/cwshom`
> (login CAS no navegador), mas as **chamadas REST** vão para o **gateway**
> `api/apihom` — que é o host usado pelos clientes deste pacote. O token vale **24h**.
> O titular do contrato pode **subdelegar** chaves de acesso a terceiros, com permissões
> granulares por API e data de expiração.

## Como instalar a skill

Copie a pasta `correios-api/` para o diretório de skills do Claude Code:

| Escopo | Local |
|--------|-------|
| Pessoal (todos os projetos) | `~/.claude/skills/correios-api/` |
| Projeto (compartilhada no repo) | `<projeto>/.claude/skills/correios-api/` |

No Windows, `~` corresponde a `C:\Users\<voce>`. Depois reinicie a sessão do
Claude Code; a skill é ativada automaticamente quando o assunto for Correios.

## Como usar os clientes (standalone)

Os scripts em `scripts/` funcionam de forma independente da skill. Configure as
credenciais por **variáveis de ambiente** (nunca hardcode):

```powershell
# PowerShell (Windows)
$env:CORREIOS_USER = "seu_usuario"
$env:CORREIOS_ACCESS_CODE = "seu_codigo_de_acesso"
$env:CORREIOS_ENV = "hom"          # "hom" (homologação) ou "prod"
# opcionais:
# $env:CORREIOS_CONTRATO = "9912345678"
# $env:CORREIOS_DR = "72"
```

```bash
# bash/zsh (Linux/macOS)
export CORREIOS_USER="seu_usuario"
export CORREIOS_ACCESS_CODE="seu_codigo_de_acesso"
export CORREIOS_ENV="hom"
```

### Python (sem dependências)

```bash
python scripts/correios_client.py track AA123456789BR
python scripts/correios_client.py price 03220 01310100 20010000 500
python scripts/correios_client.py deadline 03220 01310100 20010000
```

### Node (sem dependências, Node 18+)

```bash
node scripts/correios_client.mjs track AA123456789BR
node scripts/correios_client.mjs price 03220 01310100 20010000 500
node scripts/correios_client.mjs deadline 03220 01310100 20010000
```

Ambos os clientes já implementam **cache e renovação do token** (renovam só nos 30 min
antes de expirar, respeitando o limite de 3 req/s do endpoint de token).

## Boas práticas / avisos

- Comece sempre em **homologação** (`CORREIOS_ENV=hom`).
- **Nunca** versione credenciais nem o token; trate-os como segredo.
- `coProduto` (PAC, SEDEX, etc.) varia conforme o contrato — use sua tabela de produtos.
- Atenção aos **formatos de data** divergentes entre endpoints (`DD-MM-YYYY` x `YYYY-MM-DD`)
  — detalhes em `reference/preco-prazo.md`.

## Fontes

Specs OpenAPI (homologação):
`/token`, `/srorastro`, `/preco`, `/prazo` em `https://apihom.correios.com.br/<servico>/v3/api-docs`.
