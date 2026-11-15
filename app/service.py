from decimal import Decimal

from sqlalchemy.orm import Session

from .repositories import OrderRepository, UserRepository


def create_order(session: Session, user_id: int, amount: Decimal):
    if amount <= 0:
        raise ValueError("Сумма заказа должна быть положительной")

    user_repo = UserRepository(session)
    order_repo = OrderRepository(session)

    user = user_repo.get_by_id(user_id)
    if user is None:
        raise LookupError("Пользователь не найден")
    if user.balance < amount:
        raise ValueError("Недостаточно средств")

    try:
        user.balance -= amount
        order = order_repo.add(user_id=user_id, amount=amount, status="pending")
        session.commit()
    except Exception:
        session.rollback()
        raise

    session.refresh(order)
    return order