from typing import Any


class OrderRepository:
    def __init__(self) -> None:
        self._orders: list[dict] = []
        self._next_id: int = 1

    def get_all(self) -> list[dict]:
        return self._orders

    def get_by_id(self, order_id: int) -> dict | None:
        for order in self._orders:
            if order["id"] == order_id:
                return order
        return None

    def add(self, order: dict) -> dict:
        order["id"] = self._next_id
        self._next_id += 1
        self._orders.append(order)
        return order

    def update(self, order_id: int, update_data: dict) -> dict | None:
        order = self.get_by_id(order_id)
        if order is None:
            return None
        order.update(update_data)
        return order

    def delete(self, order_id: int) -> bool:
        order = self.get_by_id(order_id)
        if order is None:
            return False
        self._orders.remove(order)
        return True