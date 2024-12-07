#
# Copyright (c) 2024 Airbyte, Inc., all rights reserved.
#

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Tuple

import pendulum
import requests
from airbyte_cdk.sources import AbstractSource
from airbyte_cdk.sources.streams import Stream
from airbyte_cdk.sources.streams.http import HttpStream
from airbyte_cdk.sources.streams.http.auth import (
    Oauth2Authenticator,
    TokenAuthenticator,
)


class WaveAuthenticator(Oauth2Authenticator):
    def __init__(self, token_refresh_endpoint: str, client_id: str, client_secret: str):
        super().__init__(
            token_refresh_endpoint=token_refresh_endpoint,
            client_id=client_id,
            client_secret=client_secret,
            refresh_token=None,
        )

    def get_refresh_request_body(self) -> Mapping[str, Any]:
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
            "scope": "openid",
        }
        return payload

    def refresh_access_token(self) -> Tuple[str, int]:
        """
        Returns a tuple of (access_token, token_lifespan_in_seconds)
        """
        try:
            payload = self.get_refresh_request_body()
            response = requests.post(
                self.token_refresh_endpoint,
                data=payload,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            response.raise_for_status()
            response_json = response.json()
            return response_json["access_token"], response_json["expires_in"]
        except Exception as e:
            raise Exception(f"Error while refreshing access token: {e}")


# Basic full refresh stream
class WaveStream(HttpStream, ABC):
    """
    Base stream class for your connector
    """

    _url_base = "https://api.alphaus.cloud"
    primary_key = ["id"]

    @property
    def url_base(self) -> str:
        return self._url_base

    @abstractmethod
    def path(self, **kwargs) -> str:
        """
        Specify the path component of the API endpoint
        """
        pass

    def next_page_token(
        self, response: requests.Response
    ) -> Optional[Mapping[str, Any]]:
        """
        Override this method to define your pagination logic
        """
        return None

    def request_params(
        self,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> MutableMapping[str, Any]:
        """
        Override this method to define the query parameters
        """
        return {}

    def parse_response(
        self, response: requests.Response, **kwargs
    ) -> Iterable[Mapping]:
        """
        Override this method to define how to parse the response
        """
        yield {}


# Basic incremental stream
class IncrementalWaveStream(WaveStream, ABC):
    """
    Base class for incremental streams
    """

    state_checkpoint_interval = 500

    @property
    def cursor_field(self) -> str:
        """
        Override to return the cursor field for your stream
        """
        return "updated_at"  # example cursor field

    @property
    def supports_incremental(self) -> bool:
        return True

    def get_updated_state(
        self,
        current_stream_state: MutableMapping[str, Any],
        latest_record: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        """
        Override to define how to update the stream state
        """
        latest_value = latest_record.get(self.cursor_field)
        current_value = current_stream_state.get(self.cursor_field)

        if current_value and latest_value:
            return {self.cursor_field: max(latest_value, current_value)}
        return {self.cursor_field: latest_value or current_value}


class WaveCostsStream(IncrementalWaveStream, ABC):
    http_method = "POST"

    def __init__(
        self, authenticator: WaveAuthenticator, config: Mapping[str, Any], vendor: str
    ):
        super().__init__(authenticator=authenticator)
        self.config = config
        self.vendor = vendor
        self._name = f"wave_{vendor}_costs_stream"

    @property
    def cursor_field(self) -> str:
        return "date"

    @property
    def name(self) -> str:
        return self._name

    def path(self, **kwargs) -> str:
        return f"/m/blue/cost/v1/{self.vendor}/costs:read"

    def request_headers(self, **kwargs) -> Mapping[str, Any]:
        headers = super().request_headers(**kwargs)
        auth_header = self.authenticator.get_auth_header()
        headers.update(auth_header)
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/json"
        return headers

    def request_body_json(
        self, stream_state: Optional[Mapping[str, Any]] = None, **kwargs
    ) -> Optional[Mapping]:
        if stream_state and stream_state.get(self.cursor_field):
            start_date = (
                pendulum.parse(stream_state[self.cursor_field])
                .add(days=1)
                .format("YYYYMMDD")
            )
        else:
            start_date = self.config.get(
                "start_date", pendulum.now().subtract(months=1).format("YYYYMMDD")
            )

        body = {
            "startTime": start_date,
            "endTime": pendulum.now().format("YYYYMMDD"),
            "billingGroupId": self.config["billing_group_id"],
        }
        self.logger.info(f"Request Body: {body}")
        return body

    def parse_response(
        self, response: requests.Response, **kwargs
    ) -> Iterable[Mapping]:
        self.logger.info(f"Status Code: {response.status_code}")

        try:
            for line in response.iter_lines():
                if not line:
                    continue

                try:
                    data = json.loads(line.decode("utf-8"))
                    if "result" in data and self.vendor in data["result"]:
                        vendor_data = data["result"][self.vendor]
                        if isinstance(vendor_data, dict):
                            yield vendor_data
                        else:
                            self.logger.warning(
                                f"Unexpected {self.vendor} data type: {type(vendor_data)}"
                            )
                    else:
                        self.logger.warning(
                            f"Unexpected response structure: {str(data)[:200]}..."
                        )

                except json.JSONDecodeError as e:
                    self.logger.warning(f"Failed to parse line: {e}")
                    self.logger.warning(f"Problematic line: {line[:200]}...")
                    continue

        except Exception as e:
            self.logger.error(f"Error processing response: {e}")
            raise

    def get_json_schema(self) -> Dict[str, Any]:
        schema_path = (
            Path(__file__).parent / "schemas" / f"wave_{self.vendor}_costs_stream.json"
        )
        return json.loads(schema_path.read_text())


class WaveAWSCostsStream(WaveCostsStream):
    primary_key = [
        "date",
        "account",
        "region",
        "zone",
        "productCode",
        "serviceCode",
        "operation",
        "usageType",
    ]

    def __init__(self, authenticator: WaveAuthenticator, config: Mapping[str, Any]):
        super().__init__(authenticator=authenticator, config=config, vendor="aws")


class WaveGCPCostsStream(WaveCostsStream):
    primary_key = [
        "date",
        "account",
        "service",
        "region",
        "zone",
        "sku",
    ]

    def __init__(self, authenticator: WaveAuthenticator, config: Mapping[str, Any]):
        super().__init__(authenticator=authenticator, config=config, vendor="gcp")


class WaveAzureCostsStream(WaveCostsStream):
    primary_key = [
        "date",
        "account",
        "serviceName",
        "region",
        "productName",
        "subscriptionId",
    ]

    def __init__(self, authenticator: WaveAuthenticator, config: Mapping[str, Any]):
        super().__init__(authenticator=authenticator, config=config, vendor="azure")


# Source
class SourceWave(AbstractSource):
    def check_connection(self, logger, config) -> Tuple[bool, any]:
        """
        Override this method to implement connection checking
        """
        try:
            # Implement your connection check logic here
            auth = WaveAuthenticator(
                token_refresh_endpoint=config.get(
                    "token_refresh_endpoint", "https://login.alphaus.cloud/access_token"
                ),
                client_id=config["client_id"],
                client_secret=config["client_secret"],
            )
            auth.get_auth_header()
            return True, None
        except Exception as e:
            return False, str(e)

    def streams(self, config: Mapping[str, Any]) -> List[Stream]:
        """
        Override this method to return a list of stream instances
        """
        auth = WaveAuthenticator(
            token_refresh_endpoint=config.get(
                "token_refresh_endpoint", "https://login.alphaus.cloud/access_token"
            ),
            client_id=config["client_id"],
            client_secret=config["client_secret"],
        )
        return [
            WaveAWSCostsStream(authenticator=auth, config=config),
            WaveGCPCostsStream(authenticator=auth, config=config),
            WaveAzureCostsStream(authenticator=auth, config=config),
        ]
