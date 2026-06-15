from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from app.adapters.controllers.user_controller import router as user_router
from app.adapters.controllers.task_controller import router as task_router
from app.adapters.controllers.auth_controller import router as auth_router
from app.adapters.controllers.google_auth_controller import router as google_auth_router
from app.adapters.controllers.comment_controller import router as comment_router
from app.infrastructure.database.connection import Base, engine
from app.infrastructure.database.models import role_model, user_model, status_model, task_model, comment_model
from app.infrastructure.logging_config import logger, setup_logging

setup_logging()
logger.info("Starting Collaborative Task Manager API")

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Collaborative Task Manager",
    description="API RESTful to manage collaborative tasks",
    version="1.0.0"
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error on {request.method} {request.url}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal serve error"}
    )

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    logger.warning(f"ValueError on {request.method} {request.url}: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(task_router)
app.include_router(comment_router)
app.include_router(google_auth_router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Collaborative Task Manager",
        version="1.0.0",
        description="API RESTful to manage collaborative tasks",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi