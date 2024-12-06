# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from justement import Justement, AsyncJustement
from tests.utils import assert_matches_type
from justement.types import Document

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSnippet:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_document(self, client: Justement) -> None:
        snippet = client.snippet.document(
            doc_id="docId",
        )
        assert_matches_type(Document, snippet, path=["response"])

    @parametrize
    def test_raw_response_document(self, client: Justement) -> None:
        response = client.snippet.with_raw_response.document(
            doc_id="docId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        snippet = response.parse()
        assert_matches_type(Document, snippet, path=["response"])

    @parametrize
    def test_streaming_response_document(self, client: Justement) -> None:
        with client.snippet.with_streaming_response.document(
            doc_id="docId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            snippet = response.parse()
            assert_matches_type(Document, snippet, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSnippet:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_document(self, async_client: AsyncJustement) -> None:
        snippet = await async_client.snippet.document(
            doc_id="docId",
        )
        assert_matches_type(Document, snippet, path=["response"])

    @parametrize
    async def test_raw_response_document(self, async_client: AsyncJustement) -> None:
        response = await async_client.snippet.with_raw_response.document(
            doc_id="docId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        snippet = await response.parse()
        assert_matches_type(Document, snippet, path=["response"])

    @parametrize
    async def test_streaming_response_document(self, async_client: AsyncJustement) -> None:
        async with async_client.snippet.with_streaming_response.document(
            doc_id="docId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            snippet = await response.parse()
            assert_matches_type(Document, snippet, path=["response"])

        assert cast(Any, response.is_closed) is True
