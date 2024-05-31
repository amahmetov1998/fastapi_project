from src.models.secrets import Secrets

from src.utils.repository import SqlAlchemyRepository


class SecretsRepository(SqlAlchemyRepository):
    model = Secrets
