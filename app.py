# app.py
from fastapi import FastAPI, HTTPException
from transformers import AutoTokenizer, AutoModel
import torch
import pinecone

app = FastAPI()

# Initialize Pinecone
pinecone.init(api_key='your-api-key', environment='us-west1-gcp')
index = pinecone.Index('example-index')

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

def get_embeddings(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

@app.post("/upsert/")
async def upsert_documents(docs: list):
    embeddings = [get_embeddings(doc['text']) for doc in docs]
    vectors = [(doc['id'], emb) for doc, emb in zip(docs, embeddings)]
    index.upsert(vectors)
    return {"status": "success"}

@app.get("/search/")
async def search(query: str, top_k: int = 5):
    query_embedding = get_embeddings(query)
    result = index.query(queries=[query_embedding], top_k=top_k)
    return result['matches']

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)