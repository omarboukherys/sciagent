from pymongo import MongoClient
from pymongo.operations import SearchIndexModel

from sciagents.config import settings

client=MongoClient(settings.MONGO_URI)
collections=client[settings.MONGO_DB_NAME]['scientist_chunks']

index=SearchIndexModel(
    definition={
        "fields":[
            {
                "type":"vector",
                "path":"embedding",
                "numDimensions":settings.RAG_TEXT_EMBEDDING_MODEL_DIM,
                "similarity":"cosine",
            }
        ]
    },
    name="vector_index",
    type="vectorSearch",
)

collections.create_search_index(model=index)
print("Vector index created. It may take ~30s to become queryable.")