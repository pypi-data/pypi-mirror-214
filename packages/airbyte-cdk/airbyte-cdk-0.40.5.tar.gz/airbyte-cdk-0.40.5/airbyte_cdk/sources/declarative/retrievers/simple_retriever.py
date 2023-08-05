#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#

import json
from dataclasses import InitVar, dataclass, field
from itertools import islice
from json import JSONDecodeError
from typing import Any, Iterable, List, Mapping, MutableMapping, Optional, Union

import requests
from airbyte_cdk.models import AirbyteLogMessage, AirbyteMessage, Level, SyncMode
from airbyte_cdk.models import Type as MessageType
from airbyte_cdk.sources.declarative.exceptions import ReadException
from airbyte_cdk.sources.declarative.extractors.http_selector import HttpSelector
from airbyte_cdk.sources.declarative.interpolation import InterpolatedString
from airbyte_cdk.sources.declarative.partition_routers.single_partition_router import SinglePartitionRouter
from airbyte_cdk.sources.declarative.requesters.error_handlers.response_action import ResponseAction
from airbyte_cdk.sources.declarative.requesters.paginators.no_pagination import NoPagination
from airbyte_cdk.sources.declarative.requesters.paginators.paginator import Paginator
from airbyte_cdk.sources.declarative.requesters.requester import Requester
from airbyte_cdk.sources.declarative.retrievers.retriever import Retriever
from airbyte_cdk.sources.declarative.stream_slicers.stream_slicer import StreamSlicer
from airbyte_cdk.sources.declarative.types import Config, Record, StreamSlice, StreamState
from airbyte_cdk.sources.streams.core import StreamData
from airbyte_cdk.sources.streams.http import HttpStream
from airbyte_cdk.utils.airbyte_secrets_utils import filter_secrets


@dataclass
class SimpleRetriever(Retriever, HttpStream):
    """
    Retrieves records by synchronously sending requests to fetch records.

    The retriever acts as an orchestrator between the requester, the record selector, the paginator, and the stream slicer.

    For each stream slice, submit requests until there are no more pages of records to fetch.

    This retriever currently inherits from HttpStream to reuse the request submission and pagination machinery.
    As a result, some of the parameters passed to some methods are unused.
    The two will be decoupled in a future release.

    Attributes:
        stream_name (str): The stream's name
        stream_primary_key (Optional[Union[str, List[str], List[List[str]]]]): The stream's primary key
        requester (Requester): The HTTP requester
        record_selector (HttpSelector): The record selector
        paginator (Optional[Paginator]): The paginator
        stream_slicer (Optional[StreamSlicer]): The stream slicer
        parameters (Mapping[str, Any]): Additional runtime parameters to be used for string interpolation
    """

    _DEFAULT_MAX_RETRY = 5

    requester: Requester
    record_selector: HttpSelector
    config: Config
    parameters: InitVar[Mapping[str, Any]]
    name: str
    _name: Union[InterpolatedString, str] = field(init=False, repr=False, default="")
    primary_key: Optional[Union[str, List[str], List[List[str]]]]
    _primary_key: str = field(init=False, repr=False, default="")
    paginator: Optional[Paginator] = None
    stream_slicer: Optional[StreamSlicer] = SinglePartitionRouter(parameters={})
    emit_connector_builder_messages: bool = False
    disable_retries: bool = False

    def __post_init__(self, parameters: Mapping[str, Any]):
        self.paginator = self.paginator or NoPagination(parameters=parameters)
        HttpStream.__init__(self, self.requester.get_authenticator())
        self._last_response = None
        self._last_records = None
        self._parameters = parameters
        self.name = InterpolatedString(self._name, parameters=parameters)

    @property
    def name(self) -> str:
        """
        :return: Stream name
        """
        return self._name.eval(self.config)

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, property):
            self._name = value

    @property
    def url_base(self) -> str:
        return self.requester.get_url_base()

    @property
    def http_method(self) -> str:
        return str(self.requester.get_method().value)

    @property
    def raise_on_http_errors(self) -> bool:
        # never raise on http_errors because this overrides the error handler logic...
        return False

    @property
    def max_retries(self) -> Union[int, None]:
        if self.disable_retries:
            return 0
        if hasattr(self.requester.error_handler, "max_retries"):
            return self.requester.error_handler.max_retries
        return self._DEFAULT_MAX_RETRY

    def should_retry(self, response: requests.Response) -> bool:
        """
        Specifies conditions for backoff based on the response from the server.

        By default, back off on the following HTTP response statuses:
         - 429 (Too Many Requests) indicating rate limiting
         - 500s to handle transient server errors

        Unexpected but transient exceptions (connection timeout, DNS resolution failed, etc..) are retried by default.
        """
        return self.requester.interpret_response_status(response).action == ResponseAction.RETRY

    def backoff_time(self, response: requests.Response) -> Optional[float]:
        """
        Specifies backoff time.

         This method is called only if should_backoff() returns True for the input request.

         :param response:
         :return how long to backoff in seconds. The return value may be a floating point number for subsecond precision. Returning None defers backoff
         to the default backoff behavior (e.g using an exponential algorithm).
        """
        should_retry = self.requester.interpret_response_status(response)
        if should_retry.action != ResponseAction.RETRY:
            raise ValueError(f"backoff_time can only be applied on retriable response action. Got {should_retry.action}")
        assert should_retry.action == ResponseAction.RETRY
        return should_retry.retry_in

    def error_message(self, response: requests.Response) -> str:
        """
        Constructs an error message which can incorporate the HTTP response received from the partner API.

        :param response: The incoming HTTP response from the partner API
        :return The error message string to be emitted
        """
        return self.requester.interpret_response_status(response).error_message

    def _get_request_options(
        self,
        stream_slice: Optional[StreamSlice],
        next_page_token: Optional[Mapping[str, Any]],
        requester_method,
        paginator_method,
        stream_slicer_method,
        auth_options_method,
    ):
        """
        Get the request_option from the requester and from the paginator
        Raise a ValueError if there's a key collision
        Returned merged mapping otherwise
        :param stream_slice:
        :param next_page_token:
        :param requester_method:
        :param paginator_method:
        :return:
        """

        requester_mapping = requester_method(stream_state=self.state, stream_slice=stream_slice, next_page_token=next_page_token)
        requester_mapping_keys = set(requester_mapping.keys())
        paginator_mapping = paginator_method(stream_state=self.state, stream_slice=stream_slice, next_page_token=next_page_token)
        paginator_mapping_keys = set(paginator_mapping.keys())
        stream_slicer_mapping = stream_slicer_method(stream_slice=stream_slice)
        stream_slicer_mapping_keys = set(stream_slicer_mapping.keys())
        auth_options_mapping = auth_options_method()
        auth_options_mapping_keys = set(auth_options_mapping.keys())

        intersection = (
            (requester_mapping_keys & paginator_mapping_keys)
            | (requester_mapping_keys & stream_slicer_mapping_keys)
            | (paginator_mapping_keys & stream_slicer_mapping_keys)
            | (requester_mapping_keys & auth_options_mapping_keys)
            | (paginator_mapping_keys & auth_options_mapping_keys)
            | (stream_slicer_mapping_keys & auth_options_mapping_keys)
        )
        if intersection:
            raise ValueError(f"Duplicate keys found: {intersection}")
        return {**requester_mapping, **paginator_mapping, **stream_slicer_mapping, **auth_options_mapping}

    def request_headers(
        self, stream_state: StreamState, stream_slice: Optional[StreamSlice] = None, next_page_token: Optional[Mapping[str, Any]] = None
    ) -> Mapping[str, Any]:
        """
        Specifies request headers.
        Authentication headers will overwrite any overlapping headers returned from this method.
        """
        headers = self._get_request_options(
            stream_slice,
            next_page_token,
            self.requester.get_request_headers,
            self.paginator.get_request_headers,
            self.stream_slicer.get_request_headers,
            # auth headers are handled separately by passing the authenticator to the HttpStream constructor
            lambda: {},
        )
        return {str(k): str(v) for k, v in headers.items()}

    def request_params(
        self,
        stream_state: StreamSlice,
        stream_slice: Optional[StreamSlice] = None,
        next_page_token: Optional[Mapping[str, Any]] = None,
    ) -> MutableMapping[str, Any]:
        """
        Specifies the query parameters that should be set on an outgoing HTTP request given the inputs.

        E.g: you might want to define query parameters for paging if next_page_token is not None.
        """
        return self._get_request_options(
            stream_slice,
            next_page_token,
            self.requester.get_request_params,
            self.paginator.get_request_params,
            self.stream_slicer.get_request_params,
            self.requester.get_authenticator().get_request_params,
        )

    def request_body_data(
        self,
        stream_state: StreamState,
        stream_slice: Optional[StreamSlice] = None,
        next_page_token: Optional[Mapping[str, Any]] = None,
    ) -> Optional[Union[Mapping, str]]:
        """
        Specifies how to populate the body of the request with a non-JSON payload.

        If returns a ready text that it will be sent as is.
        If returns a dict that it will be converted to a urlencoded form.
        E.g. {"key1": "value1", "key2": "value2"} => "key1=value1&key2=value2"

        At the same time only one of the 'request_body_data' and 'request_body_json' functions can be overridden.
        """
        # Warning: use self.state instead of the stream_state passed as argument!
        base_body_data = self.requester.get_request_body_data(
            stream_state=self.state, stream_slice=stream_slice, next_page_token=next_page_token
        )
        if isinstance(base_body_data, str):
            paginator_body_data = self.paginator.get_request_body_data()
            if paginator_body_data:
                raise ValueError(
                    f"Cannot combine requester's body data= {base_body_data} with paginator's body_data: {paginator_body_data}"
                )
            else:
                return base_body_data
        return self._get_request_options(
            stream_slice,
            next_page_token,
            self.requester.get_request_body_data,
            self.paginator.get_request_body_data,
            self.stream_slicer.get_request_body_data,
            self.requester.get_authenticator().get_request_body_data,
        )

    def request_body_json(
        self,
        stream_state: StreamState,
        stream_slice: Optional[StreamSlice] = None,
        next_page_token: Optional[Mapping[str, Any]] = None,
    ) -> Optional[Mapping]:
        """
        Specifies how to populate the body of the request with a JSON payload.

        At the same time only one of the 'request_body_data' and 'request_body_json' functions can be overridden.
        """
        # Warning: use self.state instead of the stream_state passed as argument!
        return self._get_request_options(
            stream_slice,
            next_page_token,
            self.requester.get_request_body_json,
            self.paginator.get_request_body_json,
            self.stream_slicer.get_request_body_json,
            self.requester.get_authenticator().get_request_body_json,
        )

    def request_kwargs(
        self,
        stream_state: StreamState,
        stream_slice: Optional[StreamSlice] = None,
        next_page_token: Optional[Mapping[str, Any]] = None,
    ) -> Mapping[str, Any]:
        """
        Specifies how to configure a mapping of keyword arguments to be used when creating the HTTP request.
        Any option listed in https://docs.python-requests.org/en/latest/api/#requests.adapters.BaseAdapter.send for can be returned from
        this method. Note that these options do not conflict with request-level options such as headers, request params, etc..
        """
        # Warning: use self.state instead of the stream_state passed as argument!
        return self.requester.request_kwargs(stream_state=self.state, stream_slice=stream_slice, next_page_token=next_page_token)

    def path(
        self,
        *,
        stream_state: Optional[StreamState] = None,
        stream_slice: Optional[StreamSlice] = None,
        next_page_token: Optional[Mapping[str, Any]] = None,
    ) -> str:
        """
        Return the path the submit the next request to.
        If the paginator points to a path, follow it, else return the requester's path
        :param stream_state:
        :param stream_slice:
        :param next_page_token:
        :return:
        """
        # Warning: use self.state instead of the stream_state passed as argument!
        paginator_path = self.paginator.path()
        if paginator_path:
            return paginator_path
        else:
            return self.requester.get_path(stream_state=self.state, stream_slice=stream_slice, next_page_token=next_page_token)

    @property
    def cache_filename(self) -> str:
        """
        Return the name of cache file
        """
        return self.requester.cache_filename

    @property
    def use_cache(self) -> bool:
        """
        If True, all records will be cached.
        """
        return self.requester.use_cache

    def parse_response(
        self,
        response: requests.Response,
        *,
        stream_state: StreamState,
        stream_slice: Optional[StreamSlice] = None,
        next_page_token: Optional[Mapping[str, Any]] = None,
    ) -> Iterable[Record]:
        # if fail -> raise exception
        # if ignore -> ignore response and return no records
        # else -> delegate to record selector
        response_status = self.requester.interpret_response_status(response)
        if response_status.action == ResponseAction.FAIL:
            error_message = (
                response_status.error_message
                or f"Request to {response.request.url} failed with status code {response.status_code} and error message {HttpStream.parse_response_error_message(response)}"
            )
            raise ReadException(error_message)
        elif response_status.action == ResponseAction.IGNORE:
            self.logger.info(f"Ignoring response for failed request with error message {HttpStream.parse_response_error_message(response)}")
            return []

        # Warning: use self.state instead of the stream_state passed as argument!
        self._last_response = response
        records = self.record_selector.select_records(
            response=response, stream_state=self.state, stream_slice=stream_slice, next_page_token=next_page_token
        )
        self._last_records = records
        return records

    @property
    def primary_key(self) -> Optional[Union[str, List[str], List[List[str]]]]:
        """The stream's primary key"""
        return self._primary_key

    @primary_key.setter
    def primary_key(self, value: str) -> None:
        if not isinstance(value, property):
            self._primary_key = value

    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        """
        Specifies a pagination strategy.

        The value returned from this method is passed to most other methods in this class. Use it to form a request e.g: set headers or query params.

        :return: The token for the next page from the input response object. Returning None means there are no more pages to read in this response.
        """
        return self.paginator.next_page_token(response, self._last_records)

    def read_records(
        self,
        sync_mode: SyncMode,
        cursor_field: Optional[List[str]] = None,
        stream_slice: Optional[StreamSlice] = None,
        stream_state: Optional[StreamState] = None,
    ) -> Iterable[StreamData]:
        # Warning: use self.state instead of the stream_state passed as argument!
        stream_slice = stream_slice or {}  # None-check
        self.paginator.reset()
        records_generator = self._read_pages(
            self.parse_records,
            stream_slice,
            stream_state,
        )
        cursor_updated = False
        for record in records_generator:
            # Only record messages should be parsed to update the cursor which is indicated by the Mapping type
            if isinstance(record, Mapping):
                self.stream_slicer.update_cursor(stream_slice, last_record=record)
                cursor_updated = True
            yield record
        if not cursor_updated:
            last_record = self._last_records[-1] if self._last_records else None
            if last_record and isinstance(last_record, Mapping):
                self.stream_slicer.update_cursor(stream_slice, last_record=last_record)
            yield from []

    def stream_slices(
        self, *, sync_mode: SyncMode, cursor_field: List[str] = None, stream_state: Optional[StreamState] = None
    ) -> Iterable[Optional[Mapping[str, Any]]]:
        """
        Specifies the slices for this stream. See the stream slicing section of the docs for more information.

        :param sync_mode:
        :param cursor_field:
        :param stream_state:
        :return:
        """
        # Warning: use self.state instead of the stream_state passed as argument!
        return self.stream_slicer.stream_slices(sync_mode, self.state)

    @property
    def state(self) -> MutableMapping[str, Any]:
        return self.stream_slicer.get_stream_state()

    @state.setter
    def state(self, value: StreamState):
        """State setter, accept state serialized by state getter."""
        self.stream_slicer.update_cursor(value)

    def parse_records(
        self,
        request: requests.PreparedRequest,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any],
    ) -> Iterable[StreamData]:
        yield from self.parse_response(response, stream_slice=stream_slice, stream_state=stream_state)


@dataclass
class SimpleRetrieverTestReadDecorator(SimpleRetriever):
    """
    In some cases, we want to limit the number of requests that are made to the backend source. This class allows for limiting the number of
    slices that are queried throughout a read command.
    """

    maximum_number_of_slices: int = 5

    def __post_init__(self, options: Mapping[str, Any]):
        super().__post_init__(options)
        if self.maximum_number_of_slices and self.maximum_number_of_slices < 1:
            raise ValueError(
                f"The maximum number of slices on a test read needs to be strictly positive. Got {self.maximum_number_of_slices}"
            )

    def stream_slices(
        self, *, sync_mode: SyncMode, cursor_field: List[str] = None, stream_state: Optional[StreamState] = None
    ) -> Iterable[Optional[Mapping[str, Any]]]:
        return islice(super().stream_slices(sync_mode=sync_mode, stream_state=stream_state), self.maximum_number_of_slices)

    def parse_records(
        self,
        request: requests.PreparedRequest,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any],
    ) -> Iterable[StreamData]:
        yield _prepared_request_to_airbyte_message(request)
        yield _response_to_airbyte_message(response)
        yield from self.parse_response(response, stream_slice=stream_slice, stream_state=stream_state)


def _prepared_request_to_airbyte_message(request: requests.PreparedRequest) -> AirbyteMessage:
    # FIXME: this should return some sort of trace message
    request_dict = {
        "url": request.url,
        "http_method": request.method,
        "headers": dict(request.headers),
        "body": _body_binary_string_to_dict(request.body),
    }
    log_message = filter_secrets(f"request:{json.dumps(request_dict)}")
    return AirbyteMessage(type=MessageType.LOG, log=AirbyteLogMessage(level=Level.INFO, message=log_message))


def _body_binary_string_to_dict(body_str: str) -> Optional[Mapping[str, str]]:
    if body_str:
        if isinstance(body_str, (bytes, bytearray)):
            body_str = body_str.decode()
        try:
            return json.loads(body_str)
        except JSONDecodeError:
            return {k: v for k, v in [s.split("=") for s in body_str.split("&")]}
    else:
        return None


def _response_to_airbyte_message(response: requests.Response) -> AirbyteMessage:
    # FIXME: this should return some sort of trace message
    response_dict = {"body": response.text, "headers": dict(response.headers), "status_code": response.status_code}
    log_message = filter_secrets(f"response:{json.dumps(response_dict)}")
    return AirbyteMessage(type=MessageType.LOG, log=AirbyteLogMessage(level=Level.INFO, message=log_message))
