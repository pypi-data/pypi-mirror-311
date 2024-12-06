from __future__ import annotations
import warnings
from typing import Union, Callable, Optional, Type, Any
import logging
from pathlib import Path
from abc import ABC, abstractmethod

from clients_core.authentication.token_handler import OIDCTokenHandler, TokenHandler
from clients_core.rest_client import RestClient
from clients_core.secured_rest_client import SecuredRestClient
from clients_core.authentication.cache import DictCache
from clients_core.authentication.token_cache import TokenCache
from clients_core.api_match_client import (
    ServiceDirectoryMatchClient,
    MatchSpec,
    GatewayMatchClient,
    ApiMatchClient,
)
from clients_core.exceptions import ClientValueError
from clients_core.service_clients import E360ServiceClient
from sd_clients import ApiGatewayProvider, ServiceDirectoryClient
from sd_clients.settings import Settings


logger = logging.getLogger(__name__)


class Connector(ABC):
    _match_client: ApiMatchClient
    _verify_ssl: bool = True

    def __init__(self, match_client: ApiMatchClient, verify_ssl: bool = True) -> None:
        self._match_client = match_client
        self._verify_ssl = verify_ssl

    @abstractmethod
    def get_rest_client(self, match_spec: MatchSpec) -> RestClient:
        raise NotImplementedError()

    def _get_service_client(
        self,
        ServiceClass: Type[E360ServiceClient],
        rest_client: RestClient,
        user_id: Union[str, None] = None,
        **kwargs: Any,
    ) -> E360ServiceClient:
        return ServiceClass(rest_client, user_id=user_id, **kwargs)  # type: ignore


class OIDCConnector(Connector):
    _token_cache: Optional[TokenHandler] = None
    _oidc_user_id: Optional[str] = None

    def __init__(
        self,
        match_client: ApiMatchClient,
        token_cache: TokenHandler,
        oidc_user_id: Union[str, None] = None,
        **kwargs: Any,
    ) -> None:
        self._token_cache = token_cache
        self._oidc_user_id = oidc_user_id
        if not self._oidc_user_id:
            warnings.warn(
                "OIDC authentication set-up, but no `oidc_user_id` provided. Some features may not work as expected."
            )
        super().__init__(match_client, **kwargs)

    @property
    def oidc_user_id(self) -> Optional[str]:
        return self._oidc_user_id

    @classmethod
    def create_with_oidc(
        cls,
        service_directory_url: str,
        oidc_endpoint: str,
        client_id: str,
        client_secret: str,
        oidc_user_id: Union[str, None] = None,
        verify_ssl: bool = True,
        token_cache_callback: Union[Callable, None] = None,
    ) -> OIDCConnector:
        token_handler = OIDCTokenHandler(
            f"{oidc_endpoint.rstrip('/')}/connect/token",
            client_id,
            client_secret,
            verify_ssl,
        )
        token_cache = (
            token_cache_callback(token_handler)
            if token_cache_callback
            else TokenCache(DictCache(), token_handler)
        )
        rest_client = SecuredRestClient(
            service_directory_url,
            ["service-directory-service"],
            token_cache,
            verify_ssl=verify_ssl,
        )
        sd_client = ServiceDirectoryClient(rest_client)
        match_client = ServiceDirectoryMatchClient(sd_client)
        return cls(
            match_client=match_client,
            token_cache=token_cache,
            oidc_user_id=oidc_user_id,
            verify_ssl=verify_ssl,
        )

    def get_rest_client(self, match_spec: MatchSpec) -> RestClient:
        return self._match_client.get_secured_client(
            match_spec, self._token_cache, verify_ssl=self._verify_ssl
        )

    def _get_service_client(
        self,
        ServiceClass: Type[E360ServiceClient],
        rest_client: RestClient,
        user_id: Union[str, None] = None,
        **kwargs: Any,
    ) -> E360ServiceClient:
        if not user_id:
            user_id = self._oidc_user_id
        return super()._get_service_client(ServiceClass, rest_client, user_id, **kwargs)


class ApiGatewayConnector(Connector):
    _api_gateway_key: Optional[str] = None

    def __init__(
        self, match_client: ApiMatchClient, api_gateway_key: str, **kwargs: Any
    ) -> None:
        self._api_gateway_key = api_gateway_key
        super().__init__(match_client, **kwargs)

    @classmethod
    def create_with_gateway(
        cls,
        api_key: str,
        gateway_url: str = Settings.api_gateway_url,
        verify_ssl: bool = True,
    ) -> ApiGatewayConnector:
        provider = ApiGatewayProvider(gateway_url)
        match_client = GatewayMatchClient(provider)
        return cls(match_client, api_key, verify_ssl=verify_ssl)

    def get_rest_client(self, match_spec: MatchSpec) -> RestClient:
        return self._match_client.get_simple_client(
            match_spec,
            extra_params={"apiKey": self._api_gateway_key},
            verify_ssl=self._verify_ssl,
        )


class BaseClientStore(ABC):
    """Base Client store, for adding custom clients as needed"""

    connector: Connector

    def __init__(self, connector: Connector):
        self.connector = connector

    def get_rest_client(self, *args: Any, **kwargs: Any) -> RestClient:
        """Pass through to a method in the connector"""
        return self.connector.get_rest_client(*args, **kwargs)

    def _get_service_client(
        self,
        match_spec: MatchSpec,
        ServiceClass: Type[E360ServiceClient],
        attr: str,
        user_id: Union[str, None] = None,
        **kwargs: Any,
    ) -> E360ServiceClient:
        """Returns an instance of a requested service client, and caches its rest client on as class attribute"""
        if not hasattr(self, attr):
            setattr(self, attr, self.get_rest_client(match_spec))
        rest_client = getattr(self, attr)
        return self.connector._get_service_client(
            ServiceClass, rest_client, user_id, **kwargs
        )


class ClientStore(BaseClientStore, ABC):
    """
    This class contains helper functions for getting hold for REST clients for various E360 services
    """

    @classmethod
    def create_from_settings(
        cls, settings_path: Union[Path, str] = Settings.settings_path
    ) -> ClientStore:
        f"""Initialze The client store using a settings file. This will be under the default location {Settings.settings_path}
        or it can be on a custom location specified as an argument.

        Args:
            settings_path: The path to the settings file

        Returns:
            New ClientStore instance

        """
        settings_path = Path(settings_path)
        settings = Settings(settings_path=settings_path)
        if settings.is_api_gateway_mode:
            connector = ApiGatewayConnector.create_with_gateway(
                settings.api_gateway_key,  # type: ignore
                settings.api_gateway_url,
                settings.verify_ssl,
            )
        elif settings.is_oidc_mode:
            connector = OIDCConnector.create_with_oidc(  # type: ignore
                settings.service_directory_url,  # type: ignore
                settings.oidc_endpoint_url,  # type: ignore
                settings.oidc_client_id,  # type: ignore
                settings.oidc_client_secret,  # type: ignore
                settings.oidc_user_id,
                settings.verify_ssl,
            )  # type: ignore
        else:
            raise ClientValueError(
                "Improperly configured, no valid OIDC or Api-Gateway settings"
            )
        return cls(connector)

    @property
    def is_api_gateway_mode(self) -> bool:
        return isinstance(self.connector, ApiGatewayConnector)

    @abstractmethod
    def get_vrs_plotly_client(
        self, user_id: Union[str, None] = None, **kwargs: Any
    ) -> E360ServiceClient:
        raise NotImplementedError("This function is not implemented")

    @abstractmethod
    def get_vrs_client(
        self, user_id: Union[str, None] = None, **kwargs: Any
    ) -> E360ServiceClient:
        raise NotImplementedError("This function is not implemented")

    @abstractmethod
    def get_workspace_asset_client(
        self, user_id: Union[str, None] = None, **kwargs: Any
    ) -> E360ServiceClient:
        raise NotImplementedError("This function is not implemented")

    @abstractmethod
    def get_workspace_container_client(
        self, user_id: Union[str, None] = None, **kwargs: Any
    ) -> E360ServiceClient:
        raise NotImplementedError("This function is not implemented")

    @abstractmethod
    def get_fs_client(
        self, user_id: Union[str, None] = None, **kwargs: Any
    ) -> E360ServiceClient:
        raise NotImplementedError("This function is not implemented")

    @abstractmethod
    def get_adt_definition_client(
        self, user_id: Union[str, None] = None, **kwargs: Any
    ) -> E360ServiceClient:
        raise NotImplementedError("This function is not implemented")

    @abstractmethod
    def get_adt_client(
        self, user_id: Union[str, None] = None, **kwargs: Any
    ) -> E360ServiceClient:
        raise NotImplementedError("This function is not implemented")

    def get_dashboard_client(
        self, user_id: Union[str, None] = None, **kwargs: Any
    ) -> E360ServiceClient:
        raise NotImplementedError("This function is not implemented")

    def get_fss_client(
        self, user_id: Union[str, None] = None, **kwargs: Any
    ) -> E360ServiceClient:
        raise NotImplementedError("This function is not implemented")
