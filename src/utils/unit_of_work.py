from abc import abstractmethod, ABC
from src.repositories import (
    PositionRepository,
    DepartmentRepository,
    InviteRepository,
    MembersRepository,
    SecretsRepository,
    AccountRepository,
    CompanyRepository,
    UserRepository,
    StructAdmPositionRepository,
    UsersPositionsRepository,
    TaskRepository
)
from src.database.db import async_session_maker


class AbstractUnitOfWork(ABC):

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):

    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()
        self.user = UserRepository(self.session)
        self.company = CompanyRepository(self.session)
        self.account = AccountRepository(self.session)
        self.secrets = SecretsRepository(self.session)
        self.members = MembersRepository(self.session)
        self.invite = InviteRepository(self.session)
        self.department = DepartmentRepository(self.session)
        self.position = PositionRepository(self.session)
        self.struct_position = StructAdmPositionRepository(self.session)
        self.user_position = UsersPositionsRepository(self.session)
        self.task = TaskRepository(self.session)

    async def __aexit__(self, exc_type, *args):
        if not exc_type:
            await self.commit()
        else:
            await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
