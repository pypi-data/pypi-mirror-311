# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from justement import Justement, AsyncJustement
from tests.utils import assert_matches_type
from justement.types import (
    SearchResultSnippets,
    SearchEngineCountResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSearchEngine:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_count(self, client: Justement) -> None:
        search_engine = client.search_engine.count()
        assert_matches_type(SearchEngineCountResponse, search_engine, path=["response"])

    @parametrize
    def test_method_count_with_all_params(self, client: Justement) -> None:
        search_engine = client.search_engine.count(
            classification_facet=["string"],
            query="query",
        )
        assert_matches_type(SearchEngineCountResponse, search_engine, path=["response"])

    @parametrize
    def test_raw_response_count(self, client: Justement) -> None:
        response = client.search_engine.with_raw_response.count()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search_engine = response.parse()
        assert_matches_type(SearchEngineCountResponse, search_engine, path=["response"])

    @parametrize
    def test_streaming_response_count(self, client: Justement) -> None:
        with client.search_engine.with_streaming_response.count() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search_engine = response.parse()
            assert_matches_type(SearchEngineCountResponse, search_engine, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_search(self, client: Justement) -> None:
        search_engine = client.search_engine.search()
        assert_matches_type(SearchResultSnippets, search_engine, path=["response"])

    @parametrize
    def test_method_search_with_all_params(self, client: Justement) -> None:
        search_engine = client.search_engine.search(
            classification_facet=["string"],
            language="de",
            page=1,
            query="query",
        )
        assert_matches_type(SearchResultSnippets, search_engine, path=["response"])

    @parametrize
    def test_raw_response_search(self, client: Justement) -> None:
        response = client.search_engine.with_raw_response.search()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search_engine = response.parse()
        assert_matches_type(SearchResultSnippets, search_engine, path=["response"])

    @parametrize
    def test_streaming_response_search(self, client: Justement) -> None:
        with client.search_engine.with_streaming_response.search() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search_engine = response.parse()
            assert_matches_type(SearchResultSnippets, search_engine, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSearchEngine:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_count(self, async_client: AsyncJustement) -> None:
        search_engine = await async_client.search_engine.count()
        assert_matches_type(SearchEngineCountResponse, search_engine, path=["response"])

    @parametrize
    async def test_method_count_with_all_params(self, async_client: AsyncJustement) -> None:
        search_engine = await async_client.search_engine.count(
            classification_facet=["string"],
            query="query",
        )
        assert_matches_type(SearchEngineCountResponse, search_engine, path=["response"])

    @parametrize
    async def test_raw_response_count(self, async_client: AsyncJustement) -> None:
        response = await async_client.search_engine.with_raw_response.count()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search_engine = await response.parse()
        assert_matches_type(SearchEngineCountResponse, search_engine, path=["response"])

    @parametrize
    async def test_streaming_response_count(self, async_client: AsyncJustement) -> None:
        async with async_client.search_engine.with_streaming_response.count() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search_engine = await response.parse()
            assert_matches_type(SearchEngineCountResponse, search_engine, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_search(self, async_client: AsyncJustement) -> None:
        search_engine = await async_client.search_engine.search()
        assert_matches_type(SearchResultSnippets, search_engine, path=["response"])

    @parametrize
    async def test_method_search_with_all_params(self, async_client: AsyncJustement) -> None:
        search_engine = await async_client.search_engine.search(
            classification_facet=["string"],
            language="de",
            page=1,
            query="query",
        )
        assert_matches_type(SearchResultSnippets, search_engine, path=["response"])

    @parametrize
    async def test_raw_response_search(self, async_client: AsyncJustement) -> None:
        response = await async_client.search_engine.with_raw_response.search()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search_engine = await response.parse()
        assert_matches_type(SearchResultSnippets, search_engine, path=["response"])

    @parametrize
    async def test_streaming_response_search(self, async_client: AsyncJustement) -> None:
        async with async_client.search_engine.with_streaming_response.search() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search_engine = await response.parse()
            assert_matches_type(SearchResultSnippets, search_engine, path=["response"])

        assert cast(Any, response.is_closed) is True
