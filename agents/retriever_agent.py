from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import faiss
import numpy as np
from datetime import datetime
import json
import os

class Document(BaseModel):
    text: str
    metadata: Dict
    embedding: List[float]

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    threshold: float = 0.7

class IndexInfo(BaseModel):
    dimension: int
    total_documents: int
    last_updated: str

app = FastAPI()

class VectorStore:
    def __init__(self, dimension: int = 768):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []
        self.last_updated = datetime.now()

    def add_documents(self, documents: List[Document]):
        if not documents:
            return

        embeddings = [doc.embedding for doc in documents]
        embeddings_array = np.array(embeddings).astype('float32')
        
        self.index.add(embeddings_array)
        self.documents.extend(documents)
        self.last_updated = datetime.now()

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict]:
        query_array = np.array([query_embedding]).astype('float32')
        distances, indices = self.index.search(query_array, top_k)
        
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.documents):
                doc = self.documents[idx]
                results.append({
                    "text": doc.text,
                    "metadata": doc.metadata,
                    "score": float(1 / (1 + distance))  # Convert distance to similarity score
                })
        
        return results

    def get_info(self) -> IndexInfo:
        return IndexInfo(
            dimension=self.dimension,
            total_documents=len(self.documents),
            last_updated=self.last_updated.isoformat()
        )

# Initialize vector store
vector_store = VectorStore()

@app.post("/add-documents")
async def add_documents(documents: List[Document]):
    try:
        vector_store.add_documents(documents)
        return {"status": "success", "documents_added": len(documents)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search")
async def search(request: QueryRequest):
    try:
        # Note: In a real implementation, you would use a language model
        # to convert the query text to an embedding here
        # For now, we'll assume the query is already an embedding
        results = vector_store.search(
            query_embedding=request.query,
            top_k=request.top_k
        )
        
        # Filter results based on similarity threshold
        filtered_results = [r for r in results if r["score"] >= request.threshold]
        
        return {"results": filtered_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/info")
async def get_info():
    return vector_store.get_info()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}