import uvicorn

from techconnect_classes_api.core.config import settings
from techconnect_classes_api.core.log import setup_logger

if __name__ == "__main__":
    setup_logger()
    uvicorn.run(
        "techconnect_classes_api.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.ENV in ["test", "dev"],
        log_level=settings.LOG_LEVEL.lower(),
    )
