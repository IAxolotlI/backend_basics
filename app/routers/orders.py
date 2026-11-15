from fastapi import APIRouter, Response, status

from ..dependencies import ServiceDep
from ..schemas import Order, OrderCreate, OrderStatus, OrderUpdate

router = APIRouter(prefix="/orders", tags=["Заказы"])


@router.post(
    "",
    response_model=Order,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый заказ",
)
def create_order(payload: OrderCreate, service: ServiceDep):
    return service.create_order(payload)


@router.get(
    "",
    response_model=list[Order],
    summary="Список заказов с фильтром и пагинацией",
)
def list_orders(
    service: ServiceDep,
    status_filter: OrderStatus | None = None,
    limit: int = 10,
    offset: int = 0,
):
    return service.list_orders(status_filter=status_filter, limit=limit, offset=offset)


@router.get(
    "/{order_id}",
    response_model=Order,
    summary="Получить заказ по идентификатору",
)
def get_order(order_id: int, service: ServiceDep):
    return service.get_order(order_id)


@router.patch(
    "/{order_id}",
    response_model=Order,
    summary="Частично обновить заказ",
)
def update_order(order_id: int, payload: OrderUpdate, service: ServiceDep):
    return service.update_order(order_id, payload)


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Отменить заказ",
)
def delete_order(order_id: int, service: ServiceDep):
    service.cancel_order(order_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)