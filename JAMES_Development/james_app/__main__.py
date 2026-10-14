"""Server entrypoint launcher supporting 0.0.0.0 binding and environment configuration."""

import os
import uvicorn

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "true").lower() in ("true", "1", "yes")
    uvicorn.run("james_app.main:app", host=host, port=port, reload=reload)

