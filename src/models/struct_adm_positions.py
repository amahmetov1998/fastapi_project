from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base
from src.models.mixins.custom_types import pk


class StructAdmPositions(Base):
    __tablename__ = 'struct_adm_positions'

    id: Mapped[pk]
    struct_adm_id: Mapped[int] = mapped_column(ForeignKey("struct_adm.id"))
    position_id: Mapped[int] = mapped_column(ForeignKey("position.id"), unique=True)
