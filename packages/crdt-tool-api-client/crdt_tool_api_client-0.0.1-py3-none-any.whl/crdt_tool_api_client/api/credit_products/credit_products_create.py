from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.credit_product import CreditProduct
from ...types import Response


def _get_kwargs(
    *,
    body: Union[
        CreditProduct,
        CreditProduct,
        CreditProduct,
    ],
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/credit-products/",
    }

    if isinstance(body, CreditProduct):
        _json_body = body.to_dict()

        _kwargs["json"] = _json_body
        headers["Content-Type"] = "application/json"
    if isinstance(body, CreditProduct):
        _data_body = body.to_dict()

        _kwargs["data"] = _data_body
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, CreditProduct):
        _files_body = body.to_multipart()

        _kwargs["files"] = _files_body
        headers["Content-Type"] = "multipart/form-data"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[CreditProduct]:
    if response.status_code == 201:
        response_201 = CreditProduct.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[CreditProduct]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: Union[
        CreditProduct,
        CreditProduct,
        CreditProduct,
    ],
) -> Response[CreditProduct]:
    """API endpoint that allows organisation to be CRUDed.

    Args:
        body (CreditProduct): Serializer for the CreditProduct model.
        body (CreditProduct): Serializer for the CreditProduct model.
        body (CreditProduct): Serializer for the CreditProduct model.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreditProduct]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: Union[
        CreditProduct,
        CreditProduct,
        CreditProduct,
    ],
) -> Optional[CreditProduct]:
    """API endpoint that allows organisation to be CRUDed.

    Args:
        body (CreditProduct): Serializer for the CreditProduct model.
        body (CreditProduct): Serializer for the CreditProduct model.
        body (CreditProduct): Serializer for the CreditProduct model.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreditProduct
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: Union[
        CreditProduct,
        CreditProduct,
        CreditProduct,
    ],
) -> Response[CreditProduct]:
    """API endpoint that allows organisation to be CRUDed.

    Args:
        body (CreditProduct): Serializer for the CreditProduct model.
        body (CreditProduct): Serializer for the CreditProduct model.
        body (CreditProduct): Serializer for the CreditProduct model.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreditProduct]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: Union[
        CreditProduct,
        CreditProduct,
        CreditProduct,
    ],
) -> Optional[CreditProduct]:
    """API endpoint that allows organisation to be CRUDed.

    Args:
        body (CreditProduct): Serializer for the CreditProduct model.
        body (CreditProduct): Serializer for the CreditProduct model.
        body (CreditProduct): Serializer for the CreditProduct model.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreditProduct
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
