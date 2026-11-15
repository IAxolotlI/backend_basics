from datetime import datetime

from .exceptions import OrderAlreadyCompletedError, OrderNotFoundError
from .repository import OrderRepository
from .schemas import OrderCreate, OrderStatus, OrderUpdate


class OrderService:
    def __init__(self, repository: OrderRepository) -> None:
        self._repository = repository

    def list_orders(
        self,
        status_filter: OrderStatus | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> list[dict]:
        orders = self._repository.get_all()
        if status_filter is not None:
            orders = [o for o in orders if o["status"] == status_filter]
        return orders[offset : offset + limit]

    def get_order(self, order_id: int) -> dict:
        order = self._repository.get_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(order_id)
        return order

    def create_order(self, payload: OrderCreate) -> dict:
        order = {
            "drink": payload.drink,
            "size": payload.size,
            "quantity": payload.quantity,
            "customer_name": payload.customer_name,
            "status": OrderStatus.pending,
            "created_at": datetime.now(),
        }
        return self._repository.add(order)

    def update_order(self, order_id: int, payload: OrderUpdate) -> dict:
        order = self._repository.get_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(order_id)
        if order["status"] == OrderStatus.completed:
            raise OrderAlreadyCompletedError(order_id)

        updates = payload.model_dump(exclude_unset=True)
        return self._repository.update(order_id, updates)

    def cancel_order(self, order_id: int) -> None:
        order = self._repository.get_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(order_id)
        if order["status"] == OrderStatus.completed:
            raise OrderAlreadyCompletedError(order_id)

        self._repository.delete(order_id)