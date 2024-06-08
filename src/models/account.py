from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship, mapped_column
from src.models.mixins.custom_types import pk, custom_string
from src.models.base import Base
from src.models.user import User

if TYPE_CHECKING:
    from src.models.user import User
    from src.models.invite import Invite


class Account(Base):
    __tablename__ = "account"

    id: Mapped[pk]
    mail: Mapped[custom_string] = mapped_column(unique=True)
    user: Mapped["User"] = relationship(secondary="secrets", back_populates="account")
    invite_token: Mapped["Invite"] = relationship(back_populates="account")
