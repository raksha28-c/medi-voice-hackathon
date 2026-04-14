from qdrant_service.local_store import init_data, search_data

print("Starting...")

init_data()

while True:
    user_input = input("\nEnter your query (or type 'exit'): ")

    if user_input.lower() == "exit":
        break

    print("Searching...")

    result = search_data(user_input)

    print("Answer:", result)
