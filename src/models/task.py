from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship
from src.models.mixins.custom_types import custom_string
from src.models import Base
from src.models.mixins.custom_types import pk
if TYPE_CHECKING:
    from src.models import User


class Task(Base):

    __tablename__ = 'task'

    id: Mapped[pk]
    title: Mapped[custom_string]
    description: Mapped[str]

    author: Mapped["User"] = relationship(foreign_keys="User.task_author_id")

    responsible: Mapped["User"] = relationship(foreign_keys="User.task_responsible_id")

    observers: Mapped[list["User"]] = relationship(foreign_keys="User.task_observer_id")

    executors: Mapped[list["User"]] = relationship(foreign_keys="User.task_executor_id")

    deadline: Mapped[custom_string]
    status: Mapped[custom_string]
    time_estimation: Mapped[custom_string]
