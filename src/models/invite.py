from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base
from src.models.mixins.custom_types import pk
if TYPE_CHECKING:
    from src.models.account import Account


class Invite(Base):
    __tablename__ = 'invite'

    id: Mapped[pk]
    token: Mapped[int]
    temp_mail: Mapped[str] = mapped_column(nullable=False, unique=True)

    account_id: Mapped[int | None] = mapped_column(ForeignKey("account.id"))
    account: Mapped["Account"] = relationship(back_populates="invite_token")
