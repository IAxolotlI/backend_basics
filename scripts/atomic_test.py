from decimal import Decimal

from sqlalchemy import select

from app.db import SessionLocal
from app.models import Order, User
from app.service import create_order


def seed() -> int:
    with SessionLocal() as s:
        user = User(email="test@example.com", balance=Decimal("100.00"))
        s.add(user)
        s.commit()
        return user.id


def test_atomic_failure(user_id: int) -> None:
    from app import service

    original_add = service.OrderRepository.add

    def broken_add(self, *a, **kw):
        raise RuntimeError("injected failure between debit and insert")

    service.OrderRepository.add = broken_add
    try:
        with SessionLocal() as s:
            try:
                create_order(s, user_id, Decimal("30.00"))
            except RuntimeError:
                pass
    finally:
        service.OrderRepository.add = original_add

    # 2. Проверяем НОВОЙ сессией
    with SessionLocal() as s:
        user = s.get(User, user_id)
        orders = s.scalars(select(Order).where(Order.user_id == user_id)).all()
        print("balance:", user.balance)
        print("orders:", len(orders))
        assert user.balance == Decimal("100.00")
        assert orders == []


if __name__ == "__main__":
    uid = seed()
    test_atomic_failure(uid)
    print("OK: транзакция откатилась")