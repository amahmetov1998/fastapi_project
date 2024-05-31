from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base
from src.models.mixins.custom_types import pk


class Members(Base):
    __tablename__ = 'members'

    id: Mapped[pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
