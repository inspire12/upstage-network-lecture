import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app.api.routes.user_routes import router as user_router
from app.api.routes.chat_routes import router as chat_router
from app.core.exceptions import (
    BusinessException,
    ValidationException,
    NotFoundError,
    ConflictError,
    DatabaseError
)

app = FastAPI(
    title="LLM Agent CRUD API",
    description="A simple CRUD API for LLM Agent management",
    version="1.0.0"
)


@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=400,
        content={
            "error": "Validation Error",
            "message": exc.message,
            "details": exc.details
        }
    )


@app.exception_handler(NotFoundError)
async def not_found_exception_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": exc.message,
            "details": exc.details
        }
    )


@app.exception_handler(ConflictError)
async def conflict_exception_handler(request: Request, exc: ConflictError):
    return JSONResponse(
        status_code=409,
        content={
            "error": "Conflict",
            "message": exc.message,
            "details": exc.details
        }
    )


@app.exception_handler(DatabaseError)
async def database_exception_handler(request: Request, exc: DatabaseError):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Database Error",
            "message": "An internal database error occurred",
            "details": None
        }
    )


@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    return JSONResponse(
        status_code=400,
        content={
            "error": "Business Logic Error",
            "message": exc.message,
            "details": exc.details
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "details": None
        }
    )


app.include_router(user_router)
app.include_router(chat_router)


@app.get("/")
async def root():
    return {"message": "LLM Agent CRUD API is running"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
