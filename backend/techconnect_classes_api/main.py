from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from techconnect_classes_api.api import (
    course_router,
    recommendation_router,
    user_router,
)
from techconnect_classes_api.api.routes.limiter import limiter
from techconnect_classes_api.core.log import setup_rich_logger

setup_rich_logger()

app = FastAPI()

app.include_router(course_router)
app.include_router(user_router)
app.include_router(recommendation_router)

app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/")
def root():
    return {"message": "Server running."}
