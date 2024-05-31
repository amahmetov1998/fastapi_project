from src.models.members import Members

from src.utils.repository import SqlAlchemyRepository


class MembersRepository(SqlAlchemyRepository):
    model = Members
