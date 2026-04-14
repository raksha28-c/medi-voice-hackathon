print("VECTOR STORE LOADED")

from qdrant_client import QdrantClient
from fastembed import TextEmbedding
from qdrant_client.models import PointStruct

# Load model
model = TextEmbedding()

# Init DB
client = QdrantClient(":memory:")

client.recreate_collection(
    collection_name="healthcare",
    vectors_config={"size": 384, "distance": "Cosine"},
)

# 🔹 Load dataset
def init_data():
    print("INIT FUNCTION CALLED")

    data = []

    with open("data.txt", "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if "|" in line:
                q, a = line.strip().split("|")
                data.append({
                    "question": q.strip(),
                    "answer": a.strip()
                })

    questions = [d["question"] for d in data]
    vectors = list(model.embed(questions))

    client.upsert(
        collection_name="healthcare",
        points=[
            PointStruct(
                id=i,
                vector=vectors[i],
                payload=data[i]
            )
            for i in range(len(data))
        ]
    )

# 🔹 Search
def search_data(query):
    print("SEARCH FUNCTION CALLED")

    query_vector = list(model.embed([query]))[0]

    results = client.query_points(
        collection_name="healthcare",
        query=query_vector,
        limit=1
    ).points

    return [r.payload["answer"] for r in results]