from src.models import Secrets

from src.utils.repository import SqlAlchemyRepository
from sqlalchemy import update


class SecretsRepository(SqlAlchemyRepository):
    model = Secrets

    async def update_secrets_by_id(self, _id, **values) -> type(model) | None:
        query = update(self.model).filter(self.model.account_id == _id).values(**values)
        await self.session.execute(query)
