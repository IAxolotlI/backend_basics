from datetime import datetime
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Response, status

from models import Order, OrderCreate, OrderStatus, OrderUpdate
from settings import Settings, get_settings

app = FastAPI(
    title="Учёт заказов кофейни",
    description="Сервис учёта заказов для одной точки кофейни.",
    version="1.0.0",
)

orders: list[dict] = []
_next_id: int = 1

SettingsDep = Annotated[Settings, Depends(get_settings)]


def _find_order(order_id: int) -> dict:
    for order in orders:
        if order["id"] == order_id:
            return order
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Заказ с id={order_id} не найден",
    )

@app.get("/", tags=["Сервис"], summary="Приветствие сервиса")
def read_root(settings: SettingsDep):
    return {"message": f"{settings.app_name} на связи"}


@app.get("/info", tags=["Сервис"], summary="Информация о сервисе")
def get_info(settings: SettingsDep):
    return {
        "app_name": settings.app_name,
        "orders_count": len(orders),
    }

@app.post(
    "/orders",
    response_model=Order,
    status_code=status.HTTP_201_CREATED,
    tags=["Заказы"],
    summary="Создать новый заказ",
)
def create_order(payload: OrderCreate):
    global _next_id

    order = {
        "id": _next_id,
        "drink": payload.drink,
        "size": payload.size,
        "quantity": payload.quantity,
        "customer_name": payload.customer_name,
        "status": OrderStatus.pending,
        "created_at": datetime.now(),
    }
    orders.append(order)
    _next_id += 1
    return order


@app.get(
    "/orders",
    response_model=list[Order],
    tags=["Заказы"],
    summary="Список заказов с фильтром и пагинацией",
)
def list_orders(
    settings: SettingsDep,
    status_filter: OrderStatus | None = None,
    limit: int = 10,
    offset: int = 0,
):
    result = orders
    if status_filter is not None:
        result = [o for o in result if o["status"] == status_filter]

    return result[offset : offset + limit]


@app.get(
    "/orders/{order_id}",
    response_model=Order,
    tags=["Заказы"],
    summary="Получить заказ по идентификатору",
)
def get_order(order_id: int):
    return _find_order(order_id)


@app.patch(
    "/orders/{order_id}",
    response_model=Order,
    tags=["Заказы"],
    summary="Частично обновить заказ",
)
def update_order(order_id: int, payload: OrderUpdate):
    order = _find_order(order_id)
    updates = payload.model_dump(exclude_unset=True)
    order.update(updates)
    return order


@app.delete(
    "/orders/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Заказы"],
    summary="Отменить заказ",
)
def delete_order(order_id: int):
    order = _find_order(order_id)
    orders.remove(order)
    return Response(status_code=status.HTTP_204_NO_CONTENT)