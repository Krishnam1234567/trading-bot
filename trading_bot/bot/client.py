import time
import hmac
import hashlib
from typing import Dict, Any, Optional
from urllib.parse import urlencode

import requests

from .logging_config import log_api_call


class BinanceTestnetClient:
    BASE_URL = "https://testnet.binancefuture.com"

    def __init__(self, api_key: str, api_secret: str):
        if not api_key or not api_secret:
            raise ValueError("API Key and Secret must be provided")
        
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})
        self.time_offset = 0
        self._sync_time()
        
    def _sync_time(self):
        try:
            res = requests.get(f"{self.BASE_URL}/fapi/v1/time").json()
            if "serverTime" in res:
                server_time = res["serverTime"]
                local_time = int(time.time() * 1000)
                self.time_offset = server_time - local_time
        except Exception:
            pass

    def _generate_signature(self, query_string: str) -> str:
        return hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

    def request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        params = params or {}
        
        params["timestamp"] = int(time.time() * 1000) + self.time_offset
        params = {k: v for k, v in params.items() if v is not None}
        
        query_string = urlencode(params)
        signature = self._generate_signature(query_string)
        query_string += f"&signature={signature}"
        url = f"{self.BASE_URL}{endpoint}?{query_string}"
        
        payload_for_log = params.copy()
        payload_for_log["signature"] = signature
        
        try:
            response = self.session.request(method, url)
            
            try:
                data = response.json()
            except ValueError:
                data = {"text": response.text}
            
            if response.status_code >= 400:
                error_msg = data.get('msg', 'Unknown Error')
                error_code = data.get('code', response.status_code)
                full_error_msg = f"Binance API Error [{error_code}]: {error_msg}"
                
                log_api_call(
                    method=method, 
                    endpoint=endpoint, 
                    payload=payload_for_log,
                    response=data,
                    status_code=response.status_code,
                    error=full_error_msg
                )
                raise Exception(full_error_msg)
            
            log_api_call(
                method=method,
                endpoint=endpoint,
                payload=payload_for_log,
                response=data,
                status_code=response.status_code
            )
            return data
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Network Error: {str(e)}"
            log_api_call(
                method=method,
                endpoint=endpoint,
                payload=payload_for_log,
                error=error_msg
            )
            raise Exception(error_msg)
