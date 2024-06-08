from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base
from src.models.mixins.custom_types import pk


class UserPosition(Base):
    __tablename__ = 'users_positions'

    id: Mapped[pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)
    position_id: Mapped[int] = mapped_column(ForeignKey("position.id"), unique=True)
