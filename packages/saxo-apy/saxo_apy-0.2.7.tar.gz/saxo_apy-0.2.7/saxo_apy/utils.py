"""Utils used by SaxoOpenAPIClient."""

import json
from datetime import datetime, timezone
from http import HTTPStatus
from typing import Callable, Dict, Optional, Union
from urllib.parse import urlencode

from httpx import Request, Response
from loguru import logger
from pydantic import AnyHttpUrl, parse_obj_as

from .models import APIResponseError, HttpsUrl, OpenAPIAppConfig, StreamingMessage
from .version import VERSION


def configure_logger(log_sink: Union[str, Callable], log_level: str) -> int:
    """Set defaults for log config."""
    return logger.add(
        log_sink,
        format=(
            "{time:YYYY-MM-DD HH:mm:ss.SSS!UTC}Z {thread:12} {level:8} {module:16} {line:5} {function:25} {message}"
        ),
        level=log_level,
        enqueue=True,
    )


def make_default_session_headers() -> Dict:
    """Set default HTTP session."""
    headers: Dict[str, str] = {
        "accept": "application/json; charset=utf-8",
        "accept-encoding": "gzip",
        "user-agent": f"saxo-apy/{VERSION}",
        "connection": "keep-alive",
        "cache-control": "no-cache",
    }
    return headers


def log_request(request: Request) -> None:
    """Log request details to INFO logs."""
    request_id = request.headers.get("x-request-id").split("/")[3]
    logger.info(f"{request_id:20} performing request: {request.method} {request.url}")
    logger.debug(f"{request_id:20} request headers:    {request.headers}")
    logger.debug(f"{request_id:20} request body:       {request.content.decode()}")


def log_response(response: Response) -> None:
    """Log response details to SUCCESS/ERROR logs."""
    request_id = response.request.headers.get("x-request-id").split("/")[3]
    status_code = HTTPStatus(response.status_code)
    status_phrase = status_code.name.replace("_", " ")
    server_trace_id = response.headers.get("x-correlation")
    if response.is_success:
        logger.success(
            f"{request_id:20} request succeeded with status: {status_code} {status_phrase} - server trace id: "
            f"{server_trace_id}"
        )
    elif response.is_error:
        logger.error(
            f"{request_id:20} request failed with status: {status_code} {status_phrase} - server trace id: "
            f"{server_trace_id}"
        )


def raise_api_error(response: Response) -> None:
    """Log response error to log and raise formatted exception."""
    if response.is_error:
        response.read()  # read error for possible error message

        if (  # error content exist and is of type JSON
            response.content
            and response.headers.get("content-type")
            and "application/json" in response.headers.get("content-type").lower()
        ):
            error_received = response.json()
        else:
            error_received = "No additional error details received from OpenAPI..."

        # parse details from response
        request_id = response.request.headers.get("x-request-id").split("/")[3]
        env = response.request.headers.get("x-openapi-env")
        client_ts = response.request.headers.get("x-client-timestamp")
        status_code = HTTPStatus(response.status_code)
        status_phrase = status_code.name.replace("_", " ")
        server_trace_id = response.headers.get("x-correlation")

        # construct human-friendly exception
        exc = APIResponseError(
            f"status: {status_code} - {status_phrase}\n"
            f"client request id: {request_id}\n"
            f"server trace id: {server_trace_id}\n"
            f"timestamp (UTC): {client_ts} - elapsed: {response.elapsed} - env: {env}\n"
            f"message: {error_received}"
        )
        logger.error(f"{request_id:20} error response received from API:\n{exc}")
        raise exc


def unix_seconds_to_datetime(timestamp: int) -> datetime:
    """Convert unix seconds to human-readable timestamp."""
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)


def validate_redirect_url(app_config: OpenAPIAppConfig, redirect_url: Optional[AnyHttpUrl]) -> AnyHttpUrl:
    """Check if provided redirect URL for login is valid - or default to config."""
    if not redirect_url:
        # defaults to first available localhost redirect for convenience
        _redirect_url: AnyHttpUrl = [url for url in app_config.redirect_urls if url.host == "localhost"][0]
    else:
        assert (
            redirect_url in app_config.redirect_urls
        ), f"redirect url {redirect_url} not available in app config - see client.available_redirect_urls"
        _redirect_url = redirect_url
    return _redirect_url


def construct_auth_url(app_config: OpenAPIAppConfig, redirect_url: AnyHttpUrl, state: str) -> HttpsUrl:
    """Parse app_config to generate auth URL."""
    auth_request_query_params = {
        "response_type": "code",
        "client_id": app_config.client_id,
        "state": state,
        "redirect_uri": redirect_url,
    }

    return parse_obj_as(
        HttpsUrl,
        app_config.auth_endpoint + "?" + urlencode(auth_request_query_params),
    )


def decode_streaming_message(message: bytes) -> StreamingMessage:
    """Decode streaming message byte and convert to dict."""
    message_id = int.from_bytes(message[0:8], byteorder="little")
    ref_id_len = int(message[10])
    ref_id = message[11 : 11 + ref_id_len].decode()
    format = int(message[11 + ref_id_len])
    if format != 0:
        raise RuntimeError(f"unsupported payload format received on streaming connection: {format}")
    payload_size = int.from_bytes(message[12 + ref_id_len : 16 + ref_id_len], byteorder="little")
    payload = message[16 + ref_id_len : 16 + ref_id_len + payload_size].decode()
    deserialized = json.loads(payload)
    return StreamingMessage(msg_id=message_id, ref_id=ref_id, data=deserialized)
