from techconnect_classes.api.routes.courses import router as course_router
from techconnect_classes.api.routes.users import router as user_router
from techconnect_classes.api.routes.recommendations import router as recommendation_router

__all__ = [
    "course_router",
    "user_router",
    "recommendation_router"
]
