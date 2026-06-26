import asyncio
import requests

from langchain_core.documents import Document

from sciagents.application.rag.retrievers import get_vector_store
from sciagents.application.rag.splitters import get_splitter
from sciagents.domain.scientist_factory import ScientistFactory, SCIENTIST_NAMES


def fetch_wikipedia_summary(name: str) -> str:
    """Fetch the intro text of a Wikipedia article via the REST API."""
    title = name.replace(" ", "_")
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
    resp = requests.get(url, headers={"User-Agent": "sciagents/0.1"})
    resp.raise_for_status()
    return resp.json().get("extract", "")


async def main():
    splitter = get_splitter()
    vector_store = get_vector_store()

    all_chunks = []
    for scientist_id in SCIENTIST_NAMES:
        name = ScientistFactory.get_scientist(scientist_id).name
        print(f"Loading Wikipedia for {name}...")

        text = fetch_wikipedia_summary(name)
        if not text:
            print(f"  (no text for {name}, skipping)")
            continue

        doc = Document(page_content=text, metadata={"scientist_id": scientist_id, "name": name})
        chunks = splitter.split_documents([doc])
        all_chunks.extend(chunks)

    print(f"Adding {len(all_chunks)} chunks to MongoDB...")
    vector_store.add_documents(all_chunks)
    print("Done.")


asyncio.run(main())