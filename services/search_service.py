from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from app.config import SEARCH_ENDPOINT, SEARCH_KEY, INDEX_NAME
from azure.search.documents.models import VectorizedQuery

client = SearchClient(
    endpoint=SEARCH_ENDPOINT,
    index_name=INDEX_NAME,
    credential=AzureKeyCredential(SEARCH_KEY)
)

def vector_search(embedding):

    vector_query = VectorizedQuery(
        vector=embedding,
        k_nearest_neighbors=3,
        fields="embedding"
    )

    results = client.search(
        search_text=None,
        vector_queries=[vector_query]
    )

    return list(results)