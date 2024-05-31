from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base
from src.models.mixins.custom_types import pk


class Secrets(Base):
    __tablename__ = 'secrets'

    id: Mapped[pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), unique=True)
    password: Mapped[bytes] = mapped_column(nullable=True)
