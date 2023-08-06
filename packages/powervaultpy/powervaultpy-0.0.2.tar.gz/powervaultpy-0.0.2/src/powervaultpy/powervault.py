"""Sample API Client."""

import requests
import json

import logging

_LOGGER = logging.getLogger(__name__)


class PowerVaultApiClientError(Exception):
    """Exception to indicate a general API error."""


class PowerVaultApiClientCommunicationError(PowerVaultApiClientError):
    """Exception to indicate a communication error."""


class PowerVaultApiClientAuthenticationError(PowerVaultApiClientError):
    """Exception to indicate an authentication error."""


class ServerError(Exception):
    ...


class RequestError(Exception):
    ...


class PowerVault:
    """API Client."""

    def __init__(
        self,
        api_key: str,
        session: requests.Session = None,
    ) -> None:
        """API Client."""
        self._api_key = api_key
        self._base_url = "https://api.p3.powervault.co.uk/v3"
        self._session = session or requests.Session()

        self._session.headers.update(
            {
                "x-api-key": self._api_key,
                "accept": "application/json",
            }
        )

    def get_account(self) -> any:
        """Get the user's account data from the API."""
        url = f"{self._base_url}/customerAccount"
        account_response = self._session.get(url)

        # Check the result
        if account_response.status_code != 200:
            _LOGGER.error("Failed to retrieve account")
            return None

        account_response_body = account_response.json()

        _LOGGER.debug("Account: %s", account_response_body)

        if (
            account_response_body is not None
            and "customerAccount" in account_response_body
            and "id" in account_response_body["customerAccount"]
            and account_response_body["customerAccount"]["id"] is not None
        ):
            return {
                "id": account_response_body["customerAccount"]["id"],
                "accountName": account_response_body["customerAccount"]["accountName"],
            }

        _LOGGER.error("Failed to retrieve account")

    async def __async_read_response__(self, response: requests.Response, url):
        """Reads the response, logging any json errors"""

        text = await response.text

        if response.status_code >= 400:
            if response.status_code >= 500:
                msg = (
                    f"DO NOT REPORT - PowerVault server error ({url}):"
                    f" {response.status_code}; {text}"
                )
                _LOGGER.debug(msg)
                raise ServerError(msg)
            if response.status_code not in [401, 403, 404]:
                msg = f"Failed to send request ({url}): {response.status_code}; {text}"
                _LOGGER.debug(msg)
                raise RequestError(msg)
            return None

        try:
            return json.loads(text)
        except:
            raise Exception(f"Failed to extract response json: {url}; {text}")
