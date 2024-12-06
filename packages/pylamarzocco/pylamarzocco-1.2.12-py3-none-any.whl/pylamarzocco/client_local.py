"""Interact with the local API of La Marzocco machines."""

import asyncio
import logging
from typing import Any, Callable

from httpx import AsyncClient, RequestError
from websockets.asyncio.client import connect, ClientConnection
from websockets.exceptions import (
    ConnectionClosed,
    InvalidHandshake,
    InvalidURI,
    WebSocketException,
)

from .client_cloud import LaMarzoccoCloudClient
from .const import DEFAULT_PORT, WEBSOCKET_RETRY_DELAY
from .exceptions import AuthFail, RequestNotSuccessful

_LOGGER = logging.getLogger(__name__)


class LaMarzoccoLocalClient:
    """Class to interact with machine via local API."""

    def __init__(
        self,
        host: str,
        local_bearer: str,
        local_port: int = DEFAULT_PORT,
        client: AsyncClient | None = None,
    ) -> None:
        self._host = host
        self._local_port = local_port
        self._local_bearer = local_bearer

        self.websocket: ClientConnection | None = None
        self.terminating: bool = False

        if client is None:
            self._client = AsyncClient()
        else:
            self._client = client

    async def get_config(self) -> dict[str, Any]:
        """Get current config of machine from local API."""
        return await self._get_config(
            self._client,
            self._host,
            self._local_bearer,
            self._local_port,
        )

    @staticmethod
    async def validate_connection(
        client: AsyncClient,
        host: str,
        token: str,
        port: int = DEFAULT_PORT,
        cloud_details: tuple[LaMarzoccoCloudClient, str] | None = None,
    ) -> bool:
        """Validate the connection details to the local API."""
        try:
            await LaMarzoccoLocalClient._get_config(client, host, token, port)
        except AuthFail:
            # try to activate the local API
            if cloud_details is not None:
                cloud_client, serial = cloud_details
                try:
                    await cloud_client.token_command(serial)
                    await LaMarzoccoLocalClient._get_config(client, host, token, port)
                except (AuthFail, RequestNotSuccessful) as ex:
                    _LOGGER.error(ex)
                    return False
        except RequestNotSuccessful as ex:
            _LOGGER.error(ex)
            return False
        return True

    @staticmethod
    async def _get_config(
        client: AsyncClient,
        host: str,
        token: str,
        port: int = DEFAULT_PORT,
    ) -> dict[str, Any]:
        """Get current config of machine from local API."""
        headers = {"Authorization": f"Bearer {token}"}

        try:
            response = await client.get(
                f"http://{host}:{port}/api/v1/config", headers=headers
            )
        except RequestError as ex:
            raise RequestNotSuccessful(
                f"Requesting local API failed with exception: {ex}"
            ) from ex
        if response.is_success:
            return response.json()
        if response.status_code == 403:
            raise AuthFail("Local API returned 403.")
        raise RequestNotSuccessful(
            f"Querying local API failed with statuscode: {response.status_code}"
            + f"response: {response.text}"
        )

    async def websocket_connect(
        self,
        callback: Callable[[str | bytes], None] | None = None,
    ) -> None:
        """Connect to the websocket of the machine."""

        headers = {"Authorization": f"Bearer {self._local_bearer}"}
        try:
            async for websocket in connect(
                f"ws://{self._host}:{self._local_port}/api/v1/streaming",
                additional_headers=headers,
            ):
                self.websocket = websocket
                try:
                    # Process messages received on the connection.
                    async for message in websocket:
                        if self.terminating:
                            return
                        if callback is not None:
                            try:
                                callback(message)
                            except Exception as ex:  # pylint: disable=broad-except
                                _LOGGER.exception("Error during callback: %s", ex)
                except ConnectionClosed:
                    if self.terminating:
                        return
                    _LOGGER.debug(
                        "Websocket disconnected, reconnecting in %s",
                        WEBSOCKET_RETRY_DELAY,
                    )
                    await asyncio.sleep(WEBSOCKET_RETRY_DELAY)
                    continue
                except WebSocketException as ex:
                    _LOGGER.warning("Exception during websocket connection: %s", ex)
        except (TimeoutError, OSError, InvalidHandshake) as ex:
            _LOGGER.error("Error establishing the websocket connection: %s", ex)
        except InvalidURI:
            _LOGGER.error("Invalid URI passed to websocket connection: %s", self._host)
