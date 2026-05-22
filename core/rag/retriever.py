# -*- coding: utf-8 -*-
"""
core/rag/retriever.py
Unified RAG retrieval interface integrating loader, chunker, embedder, and vector store.
"""

from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime, timezone

from .loader import load_document, is_supported_format
from .chunker import chunk_text
from .embedder import create_embedder, PROVIDER_LOCAL
from .vector_store import VectorStore


class RAGRetriever:
    """
    Unified RAG retrieval system.
    Handles document ingestion, embedding, storage, and retrieval.
    """
    
    def __init__(
        self,
        vector_store: Optional[VectorStore] = None,
        embedding_provider: str = PROVIDER_LOCAL,
        embedding_api_key: Optional[str] = None,
        embedding_model: Optional[str] = None,
        embedding_base_url: Optional[str] = None,
    ):
        """
        Initialize RAG retriever.
        
        Args:
            vector_store: VectorStore instance (creates default if None).
            embedding_provider: Embedding provider name.
            embedding_api_key: API key for embedding provider.
            embedding_model: Embedding model name.
            embedding_base_url: Base URL for OpenAI-Compatible embeddings.
        """
        self.vector_store = vector_store or VectorStore()
        self.embedder = create_embedder(
            provider=embedding_provider,
            api_key=embedding_api_key,
            model=embedding_model,
            base_url=embedding_base_url,
        )
    
    def index_document(
        self,
        file_path: Path,
        metadata: Optional[Dict] = None,
    ) -> Dict:
        """
        Index a document: load, chunk, embed, and store.
        
        Args:
            file_path: Path to the document file.
            metadata: Optional metadata to attach to chunks.
        
        Returns:
            Dict with keys: file_name, chunk_count, indexed_at, chunk_ids.
        
        Raises:
            ValueError: If file format is not supported.
            FileNotFoundError: If file does not exist.
        """
        if not is_supported_format(file_path):
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
        
        # Load document
        text = load_document(file_path)
        
        # Chunk text
        chunks = chunk_text(text)
        
        if not chunks:
            return {
                "file_name": file_path.name,
                "chunk_count": 0,
                "indexed_at": datetime.now(timezone.utc).isoformat(),
                "chunk_ids": [],
            }
        
        # Generate embeddings
        embeddings = self.embedder.embed_batch(chunks)
        
        # Prepare metadata
        base_metadata = metadata or {}
        base_metadata.update({
            "file_name": file_path.name,
            "indexed_at": datetime.now(timezone.utc).isoformat(),
        })
        
        metadatas = [
            {**base_metadata, "chunk_index": i}
            for i in range(len(chunks))
        ]
        
        # Store in vector database
        chunk_ids = self.vector_store.add_documents(
            texts=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
        )
        
        return {
            "file_name": file_path.name,
            "chunk_count": len(chunks),
            "indexed_at": base_metadata["indexed_at"],
            "chunk_ids": chunk_ids,
        }
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        filter_metadata: Optional[Dict] = None,
    ) -> List[Dict]:
        """
        Search for relevant chunks.
        
        Args:
            query: Search query string.
            top_k: Number of results to return.
            filter_metadata: Optional metadata filter.
        
        Returns:
            List of dicts with keys: id, text, metadata, distance.
        """
        if not query or not query.strip():
            return []
        
        # Generate query embedding
        query_embedding = self.embedder.embed_text(query)
        
        # Search vector store
        results = self.vector_store.similarity_search(
            query_embedding=query_embedding,
            top_k=top_k,
            filter_metadata=filter_metadata,
        )
        
        return results
    
    def delete_document(self, file_name: str) -> int:
        """
        Delete all chunks for a document by file name.
        
        Args:
            file_name: Name of the file to delete.
        
        Returns:
            Number of chunks deleted.
        """
        return self.vector_store.delete_by_metadata({"file_name": file_name})
    
    def get_stats(self) -> Dict:
        """
        Get retriever statistics.
        
        Returns:
            Dict with keys: total_chunks, embedding_provider.
        """
        return {
            "total_chunks": self.vector_store.count(),
            "embedding_provider": self.embedder.__class__.__name__,
        }
    
    def clear_all(self) -> None:
        """Clear all documents from the vector store."""
        self.vector_store.clear()
