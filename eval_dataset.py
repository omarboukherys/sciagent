import opik
from sciagents.config import settings  # noqa: F401  (loads Opik env vars)

client = opik.Opik()

dataset = client.get_or_create_dataset(
    name="sciagents-eval",
    description="Evaluation questions for the scientist agents.",
)

items = [
    {"scientist_id": "curie", "question": "What elements did you discover?"},
    {"scientist_id": "einstein", "question": "Is the universe deterministic or random?"},
    {"scientist_id": "newton", "question": "What are your laws of motion about?"},
    {"scientist_id": "darwin", "question": "How does evolution explain complex life?"},
    {"scientist_id": "feynman", "question": "What is light, really?"},
]

dataset.insert(items)
print(f"Inserted {len(items)} items into dataset 'sciagents-eval'.")