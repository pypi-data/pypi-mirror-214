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

    def get_units(self, account_id: int) -> any:
        """Get the user's units from the API."""
        url = f"{self._base_url}/unit?customerAccountId={account_id}"
        units_response = self._read_response(self._session.get(url), url)

        _LOGGER.debug("Units: %s", units_response)

        if (
            units_response is not None
            and "units" in units_response
            and units_response["units"] is not None
        ):
            return units_response["units"]

        _LOGGER.error("Failed to retrieve units")

    def get_account(self) -> any:
        """Get the user's account data from the API."""
        url = f"{self._base_url}/customerAccount"

        account_response = self._read_response(self._session.get(url), url)

        _LOGGER.debug("Account: %s", account_response)

        if (
            account_response is not None
            and "customerAccount" in account_response
            and "id" in account_response["customerAccount"]
            and account_response["customerAccount"]["id"] is not None
        ):
            return {
                "id": account_response["customerAccount"]["id"],
                "accountName": account_response["customerAccount"]["accountName"],
            }

        _LOGGER.error("Failed to retrieve account")

    def _read_response(self, response: requests.Response, url):
        """Reads the response, logging any json errors"""

        text = response.text

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
