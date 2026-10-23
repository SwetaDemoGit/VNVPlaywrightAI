
from pathlib import Path
import numpy as np
from openai import OpenAI

# Path helps Python locate and read files.
# numpy helps perform mathematical calculations on vectors.
# OpenAI provides access to OpenAI's embedding and text-generation APIs.
# client = OpenAI() creates the client used to communicate with the API. It reads your API key from the environment.

client = OpenAI()

# 1. Read an existing text document
document = Path("documents/company_policy.txt").read_text()

# 2. Split it into chunks (paragraphs)
chunks = [p.strip() for p in document.split("\n\n") if p.strip()]
print("Chunks:", chunks)

# 3. Create embeddings for the chunks
chunk_vectors = client.embeddings.create(
    model="text-embedding-3-small",
    input=chunks
).data

chunk_vectors = np.array([item.embedding for item in chunk_vectors])

# 4. Get the user's question and embed it
question = input("\nAsk a question about the policy: ")

question_vector = client.embeddings.create(
    model="text-embedding-3-small",
    input=question
).data[0].embedding

question_vector = np.array(question_vector)

# 5. Retrieve the most similar chunk
scores = chunk_vectors @ question_vector / (
    np.linalg.norm(chunk_vectors, axis=1)
    * np.linalg.norm(question_vector)
)

best_chunk = chunks[int(np.argmax(scores))]
print("\nRetrieved context:", best_chunk)

# 6. Send the retrieved context and question to OpenAI
response = client.responses.create(
    model="gpt-4.1",
    instructions=(
        "Answer using only the context. "
        "If it doesn't contain the answer, say you don't know."
    ),
    input=f"Context: {best_chunk}\nQuestion: {question}"
)

# 7. Display the answer
print("\nAnswer:", response.output_text)
