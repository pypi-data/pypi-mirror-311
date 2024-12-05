#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import datetime
import time
import typing
import webbrowser

import httpx
import pydantic
from rich.console import Console

_MAX_RETRIES: int = 10

std: Console = Console()


class DeviceCode(pydantic.BaseModel):
    """Device code access token data model."""

    access_token: str
    refresh_token: str
    id_token: str
    token_type: str
    expires_in: int
    scope: str

    @pydantic.computed_field  # type: ignore
    @property
    def expires_at(self) -> int:
        """Computed field `expires_at`. Requires `expires_in`."""
        return int(
            (
                datetime.datetime.utcnow() + datetime.timedelta(seconds=self.expires_in)
            ).timestamp()
        )

    def is_expired(self) -> bool:
        """Check device code has reached `expires_at` timestamp."""
        return self.expires_at < datetime.datetime.utcnow().timestamp()


class DeviceCodeAuthorization:
    """
    Device code authentication is used wrapping the Auth0 sdk flow. The
    class instance will immediately execute the authorization process if
    given a valid domain, audience and client, retriving a device code
    token and id/refresh tokens.

    Args:
        domain (str): Auth0 domain name for the authorization flow.
        client_id (str): Application client id for a device code token.
        audience (str): Application audience being authenticated.
    """

    _scopes: str = "openid profile email offline_access"
    _grant_type: str = "urn:ietf:params:oauth:grant-type:device_code"

    def __init__(self, *, domain: str, client_id: str, audience: str):
        self._domain: str = domain
        self._client_id: str = client_id
        self._audience: str = audience

    def _request_device_code(self) -> httpx.Response:
        """
        Request for a device code from Auth0. Scopes are defined at the
        class level to include oidc response claims and an `id_token`,
        and an `offline_access` scope to get a `refresh_token`.

        Returns:
            httpx.Response: Auth0 device code response.
        """
        return httpx.post(
            url=f"https://{self._domain}/oauth/device/code",
            data={
                "client_id": self._client_id,
                "audience": self._audience,
                "scope": self._scopes,
            },
        )

    def _request_access_code(self, device_code: str) -> httpx.Response:
        """
        Request for an access token from Auth0 using the device code
        authorization flow. A `refresh_token` and `id_token` should also
        be returned by Auth0.

        Args:
            device_code (str): Device code received from requesting the
                authorization flow from Auth0.

        Returns:
            httpx.Response: Auth0 access token response.
        """
        return httpx.post(
            url=f"https://{self._domain}/oauth/token",
            data={
                "client_id": self._client_id,
                "audience": self._audience,
                "grant_type": self._grant_type,
                "device_code": device_code,
            },
        )

    def _request_refresh_token(self, refresh_token: str) -> httpx.Response:
        """
        Request for a refresh token from Auth0 using the device code
        authorization flow. A `refresh_token` and `id_token` should also
        be returned by Auth0 from the token rotation setting.

        Args:
            refresh_token (str): Refresh token.

        Returns:
            httpx.Response: Auth0 refresh token response.
        """
        return httpx.post(
            url=f"https://{self._domain}/oauth/token",
            data={
                "client_id": self._client_id,
                "audience": self._audience,
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
        )

    def execute_flow(self) -> DeviceCode:
        """
        Execute the device code authentication flow to obtain a token.

        Raises:
            RuntimeError: Authentication failed due to tenant details.
            RuntimeError: Authentication failed due to unknown errors.

        Returns:
            DeviceCode: New device code token.
        """

        # Generate the device code, request and process response
        device_code_response: httpx.Response = self._request_device_code()
        if device_code_response.status_code != 200:
            raise RuntimeError("Failed authenticating device, unauthorized access")
        device_code_data: typing.Dict[str, typing.Any] = device_code_response.json()

        # Redirect to the authentication portal for the device
        uri: str = device_code_data["verification_uri_complete"]
        std.print("1. On your computer or mobile device navigate to: ", uri)
        std.print("2. Enter the following code: ", device_code_data["user_code"])
        time.sleep(2)
        webbrowser.open(uri)

        # Ping Auth0 for the access token requiring user authentication
        retries: int = 0
        authenticated: bool = False
        device_code: str = device_code_data["device_code"]
        while not authenticated:
            if retries == _MAX_RETRIES:
                std.print("Authentication timed out with maximum retries, try again.")
                raise RuntimeError("Maximum retries timed out device authorization")
            std.print("Checking for completed device authentication...")
            access_code_response: httpx.Response = self._request_access_code(device_code)
            if access_code_response.status_code == 200:
                authenticated = True
                std.print("Successfully logged into the Pending.ai Platform")
                return DeviceCode.model_validate(access_code_response.json())
            else:
                error_data: typing.Dict[str, typing.Any] = access_code_response.json()
                if error_data["error"] == "authorization_pending":
                    time.sleep(device_code_data["interval"])
                    retries += 1
                    continue
                raise RuntimeError(error_data["error_description"])
        raise RuntimeError("Unable to authenticate user")

    def refresh_token(self, refresh_token: str) -> DeviceCode:
        """
        Execute the refresh token authentication flow to obtain a token.

        Args:
            refresh_token (str): Refresh token being refreshed.

        Returns:
            DeviceCode: New device code token.
        """
        refresh_response: httpx.Response = self._request_refresh_token(refresh_token)
        try:
            if refresh_response.status_code == 200:
                return DeviceCode.model_validate(refresh_response.json())
        except pydantic.ValidationError:
            pass
        raise RuntimeError("Failed to refresh access token")


__all__: typing.List[str] = ["DeviceCode", "DeviceCodeAuthorization"]
