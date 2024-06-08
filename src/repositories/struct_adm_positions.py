from src.models import StructAdmPositions
from src.utils.repository import SqlAlchemyRepository


class StructAdmPositionRepository(SqlAlchemyRepository):
    model = StructAdmPositions
