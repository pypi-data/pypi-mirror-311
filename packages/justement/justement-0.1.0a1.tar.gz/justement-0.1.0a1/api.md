# SearchEngine

Types:

```python
from justement.types import (
    Language,
    SearchResultSnippet,
    SearchResultSnippets,
    SearchEngineCountResponse,
)
```

Methods:

- <code title="get /api/count">client.search_engine.<a href="./src/justement/resources/search_engine.py">count</a>(\*\*<a href="src/justement/types/search_engine_count_params.py">params</a>) -> <a href="./src/justement/types/search_engine_count_response.py">SearchEngineCountResponse</a></code>
- <code title="get /api/search">client.search_engine.<a href="./src/justement/resources/search_engine.py">search</a>(\*\*<a href="src/justement/types/search_engine_search_params.py">params</a>) -> <a href="./src/justement/types/search_result_snippets.py">SearchResultSnippets</a></code>

# Documents

Types:

```python
from justement.types import DecisionDocument, Document
```

Methods:

- <code title="get /api/document">client.documents.<a href="./src/justement/resources/documents.py">retrieve</a>(\*\*<a href="src/justement/types/document_retrieve_params.py">params</a>) -> <a href="./src/justement/types/document.py">Document</a></code>
- <code title="get /api/documentByRef">client.documents.<a href="./src/justement/resources/documents.py">retrieve_by_reference</a>(\*\*<a href="src/justement/types/document_retrieve_by_reference_params.py">params</a>) -> <a href="./src/justement/types/document.py">Document</a></code>

# Errors

Types:

```python
from justement.types import (
    AuthenticationError,
    DocumentNotFoundError,
    InternalError,
    ValidationError,
)
```
