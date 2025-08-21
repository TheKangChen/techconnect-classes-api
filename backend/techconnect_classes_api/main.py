from fastapi import FastAPI

from techconnect_classes_api.api import course_router, recommendation_router, user_router
from techconnect_classes_api.core.log import setup_rich_logger

app = FastAPI()
setup_rich_logger()

app.include_router(course_router)
app.include_router(user_router)
app.include_router(recommendation_router)


@app.get("/")
def root():
    return {"message": "Server running."}
