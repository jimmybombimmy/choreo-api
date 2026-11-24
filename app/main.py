from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.api.v1.router import api_router

app = FastAPI()

app.include_router(api_router)


# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: bool | None = None


@app.get("/")
def read_root() -> dict[str, str]:
    return {"Hello": "World."}


@app.exception_handler(SQLAlchemyError)
def sqlalchemy_exception_handler(
    _request: Request,
    _exc: SQLAlchemyError,
) -> JSONResponse:

    return JSONResponse(
        status_code=503,
        content={
            "detail": "Database service unavailable",
        },
    )


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str | None = None):
#     return {"item_id": item_id, "q": q}


# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}
