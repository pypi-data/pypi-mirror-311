# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import snippet_document_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.document import Document

__all__ = ["SnippetResource", "AsyncSnippetResource"]


class SnippetResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SnippetResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/justement-api/justement-python#accessing-raw-response-data-eg-headers
        """
        return SnippetResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SnippetResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/justement-api/justement-python#with_streaming_response
        """
        return SnippetResourceWithStreamingResponse(self)

    def document(
        self,
        *,
        doc_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Document:
        """
        Retrieve a document by its document identifier.

        The docId is returned by the `search` endpoint as part of the result snippets.
        The response includes the full document content and metadata.

        Args:
          doc_id: The `docId` of the document that should be returned.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/document",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"doc_id": doc_id}, snippet_document_params.SnippetDocumentParams),
            ),
            cast_to=Document,
        )


class AsyncSnippetResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSnippetResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/justement-api/justement-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSnippetResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSnippetResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/justement-api/justement-python#with_streaming_response
        """
        return AsyncSnippetResourceWithStreamingResponse(self)

    async def document(
        self,
        *,
        doc_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Document:
        """
        Retrieve a document by its document identifier.

        The docId is returned by the `search` endpoint as part of the result snippets.
        The response includes the full document content and metadata.

        Args:
          doc_id: The `docId` of the document that should be returned.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/document",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"doc_id": doc_id}, snippet_document_params.SnippetDocumentParams),
            ),
            cast_to=Document,
        )


class SnippetResourceWithRawResponse:
    def __init__(self, snippet: SnippetResource) -> None:
        self._snippet = snippet

        self.document = to_raw_response_wrapper(
            snippet.document,
        )


class AsyncSnippetResourceWithRawResponse:
    def __init__(self, snippet: AsyncSnippetResource) -> None:
        self._snippet = snippet

        self.document = async_to_raw_response_wrapper(
            snippet.document,
        )


class SnippetResourceWithStreamingResponse:
    def __init__(self, snippet: SnippetResource) -> None:
        self._snippet = snippet

        self.document = to_streamed_response_wrapper(
            snippet.document,
        )


class AsyncSnippetResourceWithStreamingResponse:
    def __init__(self, snippet: AsyncSnippetResource) -> None:
        self._snippet = snippet

        self.document = async_to_streamed_response_wrapper(
            snippet.document,
        )
