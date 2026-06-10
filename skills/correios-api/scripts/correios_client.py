#!/usr/bin/env python3
"""
Minimal Correios API client — Python standard library only (no pip installs).

Implements the core flow:
  1. Authenticate (Basic Auth) -> Bearer token, cached and auto-renewed.
  2. Track objects (rastreamento).
  3. Quote price (preco) and deadline (prazo).

Credentials come from environment variables — never hardcode them:
  CORREIOS_USER          Meu Correios username
  CORREIOS_ACCESS_CODE   API access code (NOT the website password)
  CORREIOS_ENV           "hom" (default) or "prod"
  CORREIOS_CONTRATO      optional contract number (for /autentica/contrato)
  CORREIOS_DR            optional DR number

Usage examples:
  python correios_client.py track AA123456789BR
  python correios_client.py price 03220 01310100 20010000 500
  python correios_client.py deadline 03220 01310100 20010000
"""
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

HOSTS = {
    "hom": "https://apihom.correios.com.br",
    "prod": "https://api.correios.com.br",
}


class CorreiosError(Exception):
    pass


class CorreiosClient:
    def __init__(self, user=None, access_code=None, env=None):
        self.user = user or os.environ.get("CORREIOS_USER")
        self.access_code = access_code or os.environ.get("CORREIOS_ACCESS_CODE")
        self.env = (env or os.environ.get("CORREIOS_ENV") or "hom").lower()
        if self.env not in HOSTS:
            raise CorreiosError(f"CORREIOS_ENV must be 'hom' or 'prod', got {self.env!r}")
        if not self.user or not self.access_code:
            raise CorreiosError(
                "Missing credentials. Set CORREIOS_USER and CORREIOS_ACCESS_CODE."
            )
        self.base = HOSTS[self.env]
        self._token = None
        self._expira_em = None  # datetime (UTC)

    # ---- HTTP helper -----------------------------------------------------
    def _request(self, method, path, *, headers=None, body=None, query=None):
        url = self.base + path
        if query:
            # drop None values, keep arrays as repeated params
            pairs = []
            for k, v in query.items():
                if v is None:
                    continue
                if isinstance(v, (list, tuple)):
                    pairs.extend((k, str(item)) for item in v)
                else:
                    pairs.append((k, str(v)))
            url += "?" + urllib.parse.urlencode(pairs)
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Accept", "application/json")
        if data is not None:
            req.add_header("Content-Type", "application/json")
        for k, v in (headers or {}).items():
            req.add_header(k, v)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw else None
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")
            raise CorreiosError(f"HTTP {e.code} on {method} {path}: {detail}") from None
        except urllib.error.URLError as e:
            raise CorreiosError(f"Network error on {method} {path}: {e.reason}") from None

    # ---- Auth ------------------------------------------------------------
    def _authenticate(self):
        basic = base64.b64encode(
            f"{self.user}:{self.access_code}".encode("utf-8")
        ).decode("ascii")
        headers = {"Authorization": f"Basic {basic}"}

        contrato = os.environ.get("CORREIOS_CONTRATO")
        dr = os.environ.get("CORREIOS_DR")
        if contrato:
            path = "/token/v1/autentica/contrato"
            body = {"numero": contrato}
            if dr:
                body["dr"] = int(dr)
        else:
            path = "/token/v1/autentica"
            body = None

        data = self._request("POST", path, headers=headers, body=body)
        self._token = data["token"]
        self._expira_em = _parse_dt(data.get("expiraEm"))
        return self._token

    def token(self):
        """Return a valid Bearer token, reusing/renewing as needed.

        Renews only within the 30 minutes before expiry (per Correios guidance),
        avoiding the 3 req/s rate limit on the token endpoint.
        """
        if self._token and self._expira_em:
            remaining = (self._expira_em - _now()).total_seconds()
            if remaining > 30 * 60:
                return self._token
        return self._authenticate()

    def _auth_headers(self):
        return {"Authorization": f"Bearer {self.token()}"}

    # ---- Business calls --------------------------------------------------
    def track(self, *codigos, resultado="U"):
        """Track one or many objects (up to 50). resultado: T=all, P=first, U=last."""
        if not codigos:
            raise CorreiosError("Provide at least one object code.")
        if len(codigos) > 50:
            raise CorreiosError("Tracking batch limit is 50 objects.")
        if len(codigos) == 1:
            return self._request(
                "GET", f"/srorastro/v1/objetos/{codigos[0]}",
                headers=self._auth_headers(), query={"resultado": resultado},
            )
        return self._request(
            "GET", "/srorastro/v1/objetos",
            headers=self._auth_headers(),
            query={"codigosObjetos": list(codigos), "resultado": resultado},
        )

    def price(self, co_produto, cep_origem, cep_destino, peso_g, *, tp_objeto="2",
              comprimento=None, largura=None, altura=None, diametro=None, **extra):
        """Quote national price. Dimensions in cm, weight in grams."""
        query = {
            "cepOrigem": cep_origem, "cepDestino": cep_destino, "psObjeto": peso_g,
            "tpObjeto": tp_objeto, "comprimento": comprimento, "largura": largura,
            "altura": altura, "diametro": diametro,
        }
        query.update(extra)
        return self._request(
            "GET", f"/preco/v1/nacional/{co_produto}",
            headers=self._auth_headers(), query=query,
        )

    def deadline(self, co_produto, cep_origem, cep_destino, *, dt_evento=None):
        """Query national delivery deadline. dt_evento format: DD-MM-YYYY."""
        return self._request(
            "GET", f"/prazo/v1/nacional/{co_produto}",
            headers=self._auth_headers(),
            query={"cepOrigem": cep_origem, "cepDestino": cep_destino, "dtEvento": dt_evento},
        )


def _now():
    return datetime.now(timezone.utc)


def _parse_dt(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    client = CorreiosClient()
    cmd = argv[1]
    if cmd == "track":
        result = client.track(*argv[2:])
    elif cmd == "price":
        # price <coProduto> <cepOrigem> <cepDestino> <pesoG>
        result = client.price(argv[2], argv[3], argv[4], argv[5])
    elif cmd == "deadline":
        result = client.deadline(argv[2], argv[3], argv[4])
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(_main(sys.argv))
    except CorreiosError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
