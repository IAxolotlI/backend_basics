from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .dependencies import SettingsDep
from .exceptions import OrderAlreadyCompletedError, OrderNotFoundError
from .routers import orders

app = FastAPI(
    title="Учёт заказов кофейни",
    description=(
        "Сервис учёта заказов для одной точки кофейни: "
        "создание, просмотр, изменение и отмена заказов баристой."
    ),
    version="1.0.0",
)

app.include_router(orders.router)


@app.exception_handler(OrderNotFoundError)
async def order_not_found_handler(request: Request, exc: OrderNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": f"Заказ с id={exc.order_id} не найден"},
    )


@app.exception_handler(OrderAlreadyCompletedError)
async def order_already_completed_handler(
    request: Request, exc: OrderAlreadyCompletedError
):
    return JSONResponse(
        status_code=409,
        content={
            "detail": f"Заказ {exc.order_id} уже выполнен и не может быть изменён"
        },
    )


@app.get("/", tags=["Сервис"], summary="Приветствие сервиса")
def read_root(settings: SettingsDep):
    return {"message": f"{settings.app_name} на связи"}


@app.get("/info", tags=["Сервис"], summary="Информация о сервисе")
def get_info(settings: SettingsDep):
    return {
        "app_name": settings.app_name,
    }