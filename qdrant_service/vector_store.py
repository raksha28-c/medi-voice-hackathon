print("VECTOR STORE LOADED")

from qdrant_client import QdrantClient
from fastembed import TextEmbedding
from qdrant_client.models import PointStruct

model = TextEmbedding()
client = QdrantClient(":memory:")

client.recreate_collection(
    collection_name="healthcare",
    vectors_config={"size": 384, "distance": "Cosine"},
)

def init_data():
    print("INIT FUNCTION CALLED")

    data = [
        {
            "question": "I have back pain",
            "answer": "Apply hot compress, avoid heavy lifting, and maintain proper posture."
        },
        {
            "question": "I have fever",
            "answer": "Drink fluids, take rest, and consult a doctor if it persists."
        },
        {
            "question": "I have headache",
            "answer": "Drink water, take rest, and reduce screen time."
        },
        {
            "question": "I am coughing",
            "answer": "Drink warm fluids and try steam inhalation."
        }
    ]

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

def search_data(query):
    print("SEARCH FUNCTION CALLED")

    query_vector = list(model.embed([query]))[0]

    results = client.query_points(
        collection_name="healthcare",
        query=query_vector,
        limit=1
    ).points

    return [r.payload["answer"] for r in results]