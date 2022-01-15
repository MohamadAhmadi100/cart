"""
FastAPI
"""
import uvicorn
from fastapi import FastAPI, responses
from starlette.exceptions import HTTPException as starletteHTTPException

from app.controllers.cart_controller import router

TAGS = [
    {
        "name": "Cart",
        "description": "Cart CRUD"
    }
]

app = FastAPI(
    title="Cart API",
    description="This is Cart MicroService",
    version="0.1.0",
    openapi_tags=TAGS,
    docs_url="/api/v1/docs/"
)

app.include_router(router)


@app.exception_handler(starletteHTTPException)
def validation_exception_handler(request, exc):
    return responses.JSONResponse(exc.detail, status_code=exc.status_code)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
