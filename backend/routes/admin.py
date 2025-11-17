from fastapi import APIRouter
import subprocess
import logging, gc

logger = logging.getLogger(__name__)
admin_router = APIRouter()

@admin_router.post("/admin/rebuild-index")
def rebuild_index():
    try:
        logger.info("🔄 Rebuilding FAISS index...")
        subprocess.run(["python", "build_index.py"], check=True)
        gc.collect()
        logger.info("✅ Index rebuilt successfully")
        return {"status": "success", "message": "FAISS index rebuilt"}
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Index rebuild failed: {e}")
        return {"status": "error", "message": str(e)}