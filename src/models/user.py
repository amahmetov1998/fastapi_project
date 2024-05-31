from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import TYPE_CHECKING

from src.models.mixins.custom_types import pk, custom_string
from src.models.base import Base

if TYPE_CHECKING:
    from src.models.account import Account
    from src.models.company import Company


class User(Base):
    __tablename__ = "user"

    id: Mapped[pk]
    first_name: Mapped[custom_string]
    last_name: Mapped[custom_string]
    is_admin: Mapped[bool] = mapped_column(default=False)
    account: Mapped["Account"] = relationship(secondary="secrets", back_populates="user")
    company: Mapped["Company"] = relationship(secondary="members", back_populates="users")
