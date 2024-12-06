import hmac
import base64
import json
import httpx
from datetime import datetime, timezone


class OKXClient:
    def __init__(self, api_key, secret_key, passphrase, project_id=None, base_url="https://www.okx.com"):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase
        self.project_id = project_id
        self.base_url = base_url

    def _generate_signature(self, timestamp, method, request_path, body=""):
        """生成签名"""
        pre_hash = f"{timestamp}{method}{request_path}{body}"
        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            pre_hash.encode("utf-8"),
            digestmod="sha256"
        ).digest()
        return base64.b64encode(signature).decode("utf-8")

    async def request(self, method, endpoint, params=None, body=None):
        """发送 HTTP 请求"""
        url = f"{self.base_url}{endpoint}"
        timestamp = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
        body_str = "" if not body else json.dumps(body)
        signature = self._generate_signature(timestamp, method.upper(), endpoint, body_str)

        headers = {
            "OK-ACCESS-KEY": self.api_key,
            "OK-ACCESS-SIGN": signature,
            "OK-ACCESS-TIMESTAMP": timestamp,
            "OK-ACCESS-PASSPHRASE": self.passphrase,
            "Content-Type": "application/json",
        }
        if self.project_id:
            headers["OK-ACCESS-PROJECT"] = self.project_id

        async with httpx.AsyncClient() as client:
            try:
                if method.upper() == "GET":
                    response = await client.get(url, headers=headers, params=params)
                elif method.upper() == "POST":
                    response = await client.post(url, headers=headers, json=body)
                else:
                    raise ValueError("Unsupported HTTP method")

                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                raise RuntimeError(f"HTTP request failed: {e}")
            except httpx.HTTPStatusError as e:
                raise RuntimeError(f"HTTP error: {e.response.text}")
