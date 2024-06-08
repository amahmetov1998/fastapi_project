from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base
from src.models.mixins.custom_types import pk, custom_string
if TYPE_CHECKING:
    from src.models.struct_adm import StructAdm


class Position(Base):
    __tablename__ = 'position'
    id: Mapped[pk]
    name: Mapped[custom_string] = mapped_column(unique=True)
    department: Mapped["StructAdm"] = relationship(secondary='struct_adm_positions')
