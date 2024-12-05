#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import typing
from urllib.parse import urljoin

import httpx


class Client:
    """
    HTTPX client wrapper class for controlling requests to the external
    service APIs. Basic method control is managed through http methods
    for a specified domain determined by the app runtime environment.

    Args:
        domain (str): Environment-dependent app domain url.
        service_domain (str): Service prefix domain and version.
        access_token (str, optional): Token for authenticated requests.
    """

    _timeout: int = 10

    def __init__(
        self,
        *,
        domain: str,
        service_domain: str,
        access_token: typing.Optional[str] = None,
    ):
        self._domain: str = domain
        self._service_domain: str = service_domain
        self._access_token: typing.Optional[str] = access_token
        self._client: httpx.Client = self._setup_client()

    def _setup_client(self) -> httpx.Client:
        """
        Initialisation of the HTTPX client instance for the specific
        service domain. The optional access token header can be given
        as the header fields used in all requests to the domain.

        Returns:
            httpx.Client: Initialised HTTPX client instance.
        """
        headers: typing.Dict[str, str] = {}
        if self._access_token is not None:
            headers["Authorization"] = f"Bearer {self._access_token}"
        url: str = urljoin(self._domain, self._service_domain)
        return httpx.Client(base_url=url, headers=headers, timeout=self._timeout)

    def __del__(self) -> None:
        """Client connection is closed once the instance is OOM."""
        self._client.close()

    def get(self, *args, **kwargs) -> httpx.Response:
        """Client method wrapper for making a `GET` request."""
        return self._client.get(*args, **kwargs)

    def post(self, *args, **kwargs) -> httpx.Response:
        """Client method wrapper for making a `POST` request."""
        return self._client.post(*args, **kwargs)

    def patch(self, *args, **kwargs) -> httpx.Response:
        """Client method wrapper for making a `PATCH` request."""
        return self._client.patch(*args, **kwargs)

    def put(self, *args, **kwargs) -> httpx.Response:
        """Client method wrapper for making a `PUT` request."""
        return self._client.put(*args, **kwargs)

    def delete(self, *args, **kwargs) -> httpx.Response:
        """Client method wrapper for making a `DELETE` request."""
        return self._client.delete(*args, **kwargs)

    def options(self, *args, **kwargs) -> httpx.Response:
        """Client method wrapper for making a `OPTIONS` request."""
        return self._client.options(*args, **kwargs)

    def head(self, *args, **kwargs) -> httpx.Response:
        """Client method wrapper for making a `HEAD` request."""
        return self._client.head(*args, **kwargs)


__all__: typing.List[str] = ["Client"]
