from src.models import Members

from src.utils.repository import SqlAlchemyRepository


class MembersRepository(SqlAlchemyRepository):
    model = Members
