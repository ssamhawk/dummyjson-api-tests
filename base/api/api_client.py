import logging
import time
from typing import Any

from httpx import Client, HTTPStatusError, Response

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class APIClient:
    """Base API wrapper for HTTP requests with retry logic and logging"""

    def __init__(self, base_url: str, retries: int = 3, retry_interval: float = 1.0, enable_logging: bool = True):
        self.base_url = base_url.rstrip("/")
        self.retries = max(0, retries)
        self.retry_interval = max(0.0, retry_interval)
        self.enable_logging = enable_logging
        self.client = Client(base_url=self.base_url, timeout=10.0)
        # Default headers applied to every request unless overridden by explicit headers
        self.default_headers: dict[str, str] = {}

    def _log(self, level: str, message: str):
        if self.enable_logging:
            getattr(logger, level)(message)

    def request(self, method: str, endpoint: str, **kwargs: Any) -> Response:
        """
        HTTP request method with certain amount of retries
        Returns API Response
        Raises: HTTPStatusError in case all attempts failed
        """
        url = endpoint.lstrip("/")
        attempt = 0

        while attempt <= self.retries:
            try:
                self._log("info", f"Request: {method} {self.base_url}/{url}, attempt {attempt + 1}")
                # Merge default headers with per-call headers if provided
                if self.default_headers:
                    call_headers = kwargs.get("headers")
                    if call_headers:
                        merged = {**self.default_headers, **call_headers}
                        kwargs["headers"] = merged
                    else:
                        kwargs["headers"] = self.default_headers

                response = self.client.request(method, url, **kwargs)
                response.raise_for_status()
                self._log("info", f"Response: {method} {self.base_url}/{url} - {response.status_code}")
                return response
            except HTTPStatusError as e:
                attempt += 1
                if attempt > self.retries:
                    self._log("error", f"Failed after {self.retries} retries: {method} {self.base_url}/{url} - {e!s}")
                    raise
                self._log("warning", f"Retry {attempt}:{self.retries}")
                time.sleep(self.retry_interval)
            except Exception as e:
                self._log("error", f"Unexpected error: {e!s}")
                raise

    def get(self, endpoint: str, **kwargs: Any) -> Response:
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs: Any) -> Response:
        return self.request("POST", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs: Any) -> Response:
        return self.request("DELETE", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs: Any) -> Response:
        return self.request("PUT", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs: Any) -> Response:
        return self.request("PATCH", endpoint, **kwargs)

    # --- Default headers and auth helpers -----------------------------------
    def set_default_headers(self, headers: dict[str, str]) -> None:
        """Replace default headers applied to every request."""
        self.default_headers = dict(headers) if headers else {}

    def update_default_headers(self, headers: dict[str, str]) -> None:
        """Update default headers, overriding existing keys."""
        if headers:
            self.default_headers.update(headers)

    def clear_default_headers(self) -> None:
        """Clear all default headers."""
        self.default_headers.clear()

    def set_bearer_token(self, token: str) -> None:
        """Set Authorization: Bearer <token> in default headers."""
        self.update_default_headers({"Authorization": f"Bearer {token}"})

    def set_x_auth_token(self, token: str) -> None:
        """Set X-Auth-Token: <token> in default headers (custom header scheme)."""
        self.update_default_headers({"X-Auth-Token": token})

    def __enter__(self):
        """Support of context manager by class"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self) -> None:
        """Close underlying HTTP client."""
        self.client.close()
