# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .search_result_snippet import SearchResultSnippet

__all__ = ["SearchResultSnippets"]


class SearchResultSnippets(BaseModel):
    result_count: int = FieldInfo(alias="resultCount")

    results: Optional[List[SearchResultSnippet]] = None
