import logging
import time
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from fastapi.responses import UJSONResponse

from routes import setup_routes
from middlewares import setup_middlewares
from services.db import DB
from services.redis import Redis
import exceptions

app = FastAPI()
setup_routes(app)
setup_middlewares(app)


@app.on_event("startup")
async def startup() -> None:
    await DB.connect()
    await Redis.get_client()


@app.on_event("shutdown")
async def shutdown() -> None:
    await DB.close()
    await Redis.close()


@app.exception_handler(Exception)
async def unicorn_base_exception_handler(request: Request, exc: Exception):
    error = exceptions.ServerError(debug=str(exc))

    return UJSONResponse(
        status_code=error.status_code,
        content=error.to_json(),
    )


@app.exception_handler(exceptions.ApiException)
async def unicorn_api_exception_handler(request: Request, exc: exceptions.ApiException):
    return UJSONResponse(
        status_code=exc.status_code,
        content=exc.to_json()
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8087)
