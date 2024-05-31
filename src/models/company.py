from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship, mapped_column
from src.models.mixins.custom_types import pk, custom_string
from src.models.base import Base

if TYPE_CHECKING:
    from src.models.user import User


class Company(Base):
    __tablename__ = "company"

    id: Mapped[pk]
    company_name: Mapped[custom_string] = mapped_column(unique=True)
    users: Mapped[list["User"]] = relationship(secondary="members", back_populates="company")
