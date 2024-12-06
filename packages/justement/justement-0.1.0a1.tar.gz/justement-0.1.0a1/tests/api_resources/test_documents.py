# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from justement import Justement, AsyncJustement
from tests.utils import assert_matches_type
from justement.types import Document

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDocuments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Justement) -> None:
        document = client.documents.retrieve(
            doc_id="docId",
        )
        assert_matches_type(Document, document, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Justement) -> None:
        response = client.documents.with_raw_response.retrieve(
            doc_id="docId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = response.parse()
        assert_matches_type(Document, document, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Justement) -> None:
        with client.documents.with_streaming_response.retrieve(
            doc_id="docId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = response.parse()
            assert_matches_type(Document, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve_by_reference(self, client: Justement) -> None:
        document = client.documents.retrieve_by_reference(
            doc_ref="docRef",
        )
        assert_matches_type(Document, document, path=["response"])

    @parametrize
    def test_raw_response_retrieve_by_reference(self, client: Justement) -> None:
        response = client.documents.with_raw_response.retrieve_by_reference(
            doc_ref="docRef",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = response.parse()
        assert_matches_type(Document, document, path=["response"])

    @parametrize
    def test_streaming_response_retrieve_by_reference(self, client: Justement) -> None:
        with client.documents.with_streaming_response.retrieve_by_reference(
            doc_ref="docRef",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = response.parse()
            assert_matches_type(Document, document, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDocuments:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncJustement) -> None:
        document = await async_client.documents.retrieve(
            doc_id="docId",
        )
        assert_matches_type(Document, document, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncJustement) -> None:
        response = await async_client.documents.with_raw_response.retrieve(
            doc_id="docId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = await response.parse()
        assert_matches_type(Document, document, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncJustement) -> None:
        async with async_client.documents.with_streaming_response.retrieve(
            doc_id="docId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = await response.parse()
            assert_matches_type(Document, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve_by_reference(self, async_client: AsyncJustement) -> None:
        document = await async_client.documents.retrieve_by_reference(
            doc_ref="docRef",
        )
        assert_matches_type(Document, document, path=["response"])

    @parametrize
    async def test_raw_response_retrieve_by_reference(self, async_client: AsyncJustement) -> None:
        response = await async_client.documents.with_raw_response.retrieve_by_reference(
            doc_ref="docRef",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = await response.parse()
        assert_matches_type(Document, document, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve_by_reference(self, async_client: AsyncJustement) -> None:
        async with async_client.documents.with_streaming_response.retrieve_by_reference(
            doc_ref="docRef",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = await response.parse()
            assert_matches_type(Document, document, path=["response"])

        assert cast(Any, response.is_closed) is True
