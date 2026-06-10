// Minimal Correios API client — Node.js, no external dependencies (uses global fetch, Node 18+).
//
// Core flow:
//   1. Authenticate (Basic Auth) -> Bearer token, cached and auto-renewed.
//   2. Track objects (rastreamento). 3. Price (preco). 4. Deadline (prazo).
//
// Credentials come from environment variables — never hardcode them:
//   CORREIOS_USER          Meu Correios username
//   CORREIOS_ACCESS_CODE   API access code (NOT the website password)
//   CORREIOS_ENV           "hom" (default) or "prod"
//   CORREIOS_CONTRATO      optional contract number (for /autentica/contrato)
//   CORREIOS_DR            optional DR number
//
// Usage:
//   node correios_client.mjs track AA123456789BR
//   node correios_client.mjs price 03220 01310100 20010000 500
//   node correios_client.mjs deadline 03220 01310100 20010000

const HOSTS = {
  hom: "https://apihom.correios.com.br",
  prod: "https://api.correios.com.br",
};

export class CorreiosClient {
  constructor({ user, accessCode, env } = {}) {
    this.user = user ?? process.env.CORREIOS_USER;
    this.accessCode = accessCode ?? process.env.CORREIOS_ACCESS_CODE;
    this.env = (env ?? process.env.CORREIOS_ENV ?? "hom").toLowerCase();
    if (!HOSTS[this.env]) throw new Error(`CORREIOS_ENV must be 'hom' or 'prod', got '${this.env}'`);
    if (!this.user || !this.accessCode)
      throw new Error("Missing credentials. Set CORREIOS_USER and CORREIOS_ACCESS_CODE.");
    this.base = HOSTS[this.env];
    this._token = null;
    this._expiraEm = null; // Date
  }

  async _request(method, path, { headers = {}, body, query } = {}) {
    let url = this.base + path;
    if (query) {
      const params = new URLSearchParams();
      for (const [k, v] of Object.entries(query)) {
        if (v == null) continue;
        if (Array.isArray(v)) v.forEach((item) => params.append(k, String(item)));
        else params.append(k, String(v));
      }
      const qs = params.toString();
      if (qs) url += "?" + qs;
    }
    const opts = { method, headers: { Accept: "application/json", ...headers } };
    if (body !== undefined) {
      opts.headers["Content-Type"] = "application/json";
      opts.body = JSON.stringify(body);
    }
    const resp = await fetch(url, opts);
    const text = await resp.text();
    if (!resp.ok) throw new Error(`HTTP ${resp.status} on ${method} ${path}: ${text}`);
    return text ? JSON.parse(text) : null;
  }

  async _authenticate() {
    const basic = Buffer.from(`${this.user}:${this.accessCode}`).toString("base64");
    const headers = { Authorization: `Basic ${basic}` };
    const contrato = process.env.CORREIOS_CONTRATO;
    const dr = process.env.CORREIOS_DR;
    let path = "/token/v1/autentica";
    let body;
    if (contrato) {
      path = "/token/v1/autentica/contrato";
      body = { numero: contrato };
      if (dr) body.dr = Number(dr);
    }
    const data = await this._request("POST", path, { headers, body });
    this._token = data.token;
    this._expiraEm = data.expiraEm ? new Date(data.expiraEm) : null;
    return this._token;
  }

  // Returns a valid Bearer token, renewing only within 30 min before expiry
  // (avoids the 3 req/s rate limit on the token endpoint).
  async token() {
    if (this._token && this._expiraEm) {
      const remainingMs = this._expiraEm.getTime() - Date.now();
      if (remainingMs > 30 * 60 * 1000) return this._token;
    }
    return this._authenticate();
  }

  async _authHeaders() {
    return { Authorization: `Bearer ${await this.token()}` };
  }

  // Track 1..50 objects. resultado: T=all, P=first, U=last.
  async track(codigos, resultado = "U") {
    const list = Array.isArray(codigos) ? codigos : [codigos];
    if (list.length === 0) throw new Error("Provide at least one object code.");
    if (list.length > 50) throw new Error("Tracking batch limit is 50 objects.");
    const headers = await this._authHeaders();
    if (list.length === 1) {
      return this._request("GET", `/srorastro/v1/objetos/${list[0]}`, { headers, query: { resultado } });
    }
    return this._request("GET", "/srorastro/v1/objetos", {
      headers,
      query: { codigosObjetos: list, resultado },
    });
  }

  // National price quote. Dimensions in cm, weight in grams.
  async price(coProduto, cepOrigem, cepDestino, pesoG, opts = {}) {
    const { tpObjeto = "2", comprimento, largura, altura, diametro, ...extra } = opts;
    const headers = await this._authHeaders();
    return this._request("GET", `/preco/v1/nacional/${coProduto}`, {
      headers,
      query: { cepOrigem, cepDestino, psObjeto: pesoG, tpObjeto, comprimento, largura, altura, diametro, ...extra },
    });
  }

  // National delivery deadline. dtEvento format: DD-MM-YYYY.
  async deadline(coProduto, cepOrigem, cepDestino, { dtEvento } = {}) {
    const headers = await this._authHeaders();
    return this._request("GET", `/prazo/v1/nacional/${coProduto}`, {
      headers,
      query: { cepOrigem, cepDestino, dtEvento },
    });
  }
}

async function main(argv) {
  const [cmd, ...rest] = argv;
  const client = new CorreiosClient();
  let result;
  switch (cmd) {
    case "track":
      result = await client.track(rest);
      break;
    case "price":
      result = await client.price(rest[0], rest[1], rest[2], rest[3]);
      break;
    case "deadline":
      result = await client.deadline(rest[0], rest[1], rest[2]);
      break;
    default:
      console.log("Commands: track <cod...> | price <coProduto> <cepOrig> <cepDest> <pesoG> | deadline <coProduto> <cepOrig> <cepDest>");
      return 1;
  }
  console.log(JSON.stringify(result, null, 2));
  return 0;
}

// Run as CLI when invoked directly.
if (import.meta.url === `file://${process.argv[1]}`) {
  main(process.argv.slice(2))
    .then((code) => process.exit(code ?? 0))
    .catch((err) => {
      console.error(`Error: ${err.message}`);
      process.exit(1);
    });
}
