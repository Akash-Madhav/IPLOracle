from fastapi import APIRouter
import subprocess
import logging
import gc
import psutil

logger = logging.getLogger(__name__)
admin_router = APIRouter()

@admin_router.post("/admin/rebuild-index")
def rebuild_index():
    """
    Trigger a rebuild of the Pinecone index by running build_index.py.
    """
    try:
        logger.info("🔄 Rebuilding Pinecone index...")
        subprocess.run(["python", "build_index.py"], check=True)
        gc.collect()
        logger.info("✅ Pinecone index rebuilt successfully")
        return {"status": "success", "message": "Pinecone index rebuilt"}
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Index rebuild failed: {e}")
        return {"status": "error", "message": str(e)}

@admin_router.get("/admin/memory")
def memory_usage():
    """
    Report current backend memory usage in MB.
    """
    mem = psutil.Process().memory_info().rss / 1024**2
    return {
        "status": "ok",
        "memory_usage_mb": round(mem, 2)
    }