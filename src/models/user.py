from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import TYPE_CHECKING

from src.models.mixins.custom_types import pk, custom_string
from src.models.base import Base

if TYPE_CHECKING:
    from src.models import Account, Company, Position


class User(Base):
    __tablename__ = "user"

    id: Mapped[pk]
    first_name: Mapped[custom_string]
    last_name: Mapped[custom_string]
    is_admin: Mapped[bool] = mapped_column(default=False)
    account: Mapped["Account"] = relationship(secondary="secrets", back_populates="user")
    company: Mapped["Company"] = relationship(secondary="members", back_populates="users")
    position: Mapped["Position"] = relationship(secondary="users_positions")

    task_author_id: Mapped[int | None] = mapped_column(ForeignKey("task.id", ondelete="SET NULL"), unique=True)

    task_responsible_id: Mapped[int | None] = mapped_column(ForeignKey("task.id", ondelete="SET NULL"), unique=True)

    task_observer_id: Mapped[int | None] = mapped_column(ForeignKey("task.id", ondelete="SET NULL"))

    task_executor_id: Mapped[int | None] = mapped_column(ForeignKey("task.id", ondelete="SET NULL"))
