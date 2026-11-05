"""
AuditAgent - ChromaDB Inspector & Live Vector Search Demo
Run: python show_chromadb.py
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import chromadb
from src.config import settings

# Locate chroma directory
APP_DIR = Path(__file__).resolve().parent
CHROMA_PATH = APP_DIR / "chroma_db" / "chroma"
if not CHROMA_PATH.exists():
    CHROMA_PATH = Path(settings.CHROMA_PERSIST_DIR) / "chroma"


def inspect_chromadb():
    print("=" * 80)
    print("             AUDITAGENT: CHROMADB VECTOR DATABASE INSPECTION            ")
    print("=" * 80)
    print(f"[+] Physical Location: {CHROMA_PATH.resolve()}")
    
    sqlite_db = CHROMA_PATH / "chroma.sqlite3"
    if sqlite_db.exists():
        print(f"[+] SQLite Metadata Store: {sqlite_db.name} ({sqlite_db.stat().st_size:,} bytes)")
    
    hnsw_dirs = [d for d in CHROMA_PATH.iterdir() if d.is_dir()]
    print(f"[+] HNSW Binary Index Folders: {len(hnsw_dirs)} index(es)")

    if not CHROMA_PATH.exists():
        print("[-] ChromaDB directory not found. Please ingest documents first.")
        return

    # Connect to persistent ChromaDB client
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    collections = client.list_collections()
    print(f"[+] Active Collections Found: {[c.name for c in collections]}")
    
    if not collections:
        print("[-] No collections found.")
        return

    collection = client.get_collection("auditagent_evidence")
    count = collection.count()
    print(f"[+] Target Collection: 'auditagent_evidence'")
    print(f"[+] Total Indexed Chunks / Vectors: {count}")
    print("-" * 80)

    # Peek at all documents
    data = collection.peek(limit=count or 10)
    ids = data["ids"]
    docs = data["documents"]
    metas = data["metadatas"]
    embeddings = data.get("embeddings")

    dim = len(embeddings[0]) if embeddings is not None and len(embeddings) > 0 else "Unknown"
    print(f"[+] Embedding Dimensions: {dim} float32 values (FastEmbed BAAI/bge-small-en-v1.5)")
    print("-" * 80)
    print(f"{'Chunk ID':<35} | {'Section':<25} | {'Page':<5} | {'Excerpt':<40}")
    print("-" * 115)

    for i in range(len(ids)):
        cid = ids[i]
        meta = metas[i] if i < len(metas) else {}
        doc = docs[i].replace("\n", " ") if i < len(docs) else ""
        section = meta.get("section_title", "GENERAL")[:23]
        page = str(meta.get("page_number", "-"))
        excerpt = (doc[:37] + "...") if len(doc) > 40 else doc
        print(f"{cid:<35} | {section:<25} | {page:<5} | {excerpt:<40}")

    print("=" * 115)
    
    # Interactive / Sample Vector Query
    print("\n[+] DEMO: Live Cosine Distance Search on ChromaDB Vectors")
    query = "How long must access logs be retained?"
    print(f"    Sample Query: '{query}'")
    
    try:
        from fastembed import TextEmbedding
        embedder = TextEmbedding(model_name=settings.EMBEDDING_MODEL_NAME)
        q_vec = [float(x) for x in next(iter(embedder.query_embed(query)))]
        results = collection.query(query_embeddings=[q_vec], n_results=min(2, count), include=["documents", "metadatas", "distances"])
        
        print(f"\n    Top {min(2, count)} Nearest Neighbors in Vector Space (Cosine Distance):")
        for rank in range(len(results["ids"][0])):
            cid = results["ids"][0][rank]
            dist = results["distances"][0][rank]
            doc = results["documents"][0][rank].replace("\n", " ")
            print(f"    {rank+1}. [Distance: {dist:.4f}] Chunk: {cid}")
            print(f"       Text: {doc[:100]}...")
    except Exception as e:
        print(f"    (Live query preview skipped: {e})")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    inspect_chromadb()
