from qdrant_client import QdrantClient, models
from get_embeddings import hf_mpnet_embed
client = QdrantClient(url="https://", api_key="", prefer_grpc=False)

collection_name = "test_collection123"
# client.create_collection(
#     collection_name=collection_name,
#     vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
# )
client.upsert(
    collection_name=collection_name,
    points=[
        models.PointStruct(
            id=1,
            payload={
                "color": "red",
                "country": "UK",
                "city": "London",
            },
            vector=hf_mpnet_embed("London is the capital of England and the United Kingdom."),
        ),
        models.PointStruct(
            id=2,
            payload={
                "color": "green",
                "country": "India",
                "city": "Delhi",
            },
            vector=hf_mpnet_embed("Delhi is the capital of India."),
        ),
        models.PointStruct(
            id=3,
            payload={
                "color": "blue",
                "country": "France",
                "city": "Paris",
            },
            vector=hf_mpnet_embed("Paris is the capital of France."),
        ),
    ],
)



res =client.query_points(
    collection_name=collection_name,
    query=hf_mpnet_embed("London is the capital of England and the United Kingdom."),

    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="country",
                match=models.MatchValue(
                    value="UK",
                ),
            )
        ]
    ),
    search_params=models.SearchParams(hnsw_ef=128, exact=False),
    limit=3,
)

print(res)