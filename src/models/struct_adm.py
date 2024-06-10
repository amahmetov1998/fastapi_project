from typing import Any

from sqlalchemy import Sequence, Integer, Column, String, func, Index, ForeignKey
from sqlalchemy.orm import relationship, foreign, remote, mapped_column
from sqlalchemy_utils import LtreeType, Ltree


from src.models import Base

id_seq = Sequence('struct_adm_id_seq')


class StructAdm(Base):
    __tablename__ = 'struct_adm'

    id = Column(Integer, id_seq, primary_key=True)
    name = Column(String)
    path = Column(LtreeType, nullable=False)

    user_position_id = mapped_column(ForeignKey("users_positions.id", ondelete="CASCADE"))

    parent = relationship('StructAdm',
                          primaryjoin=remote(path) == foreign(func.subpath(path, 0, -1)),
                          backref='children',
                          viewonly=True)

    __table_args__ = Index('ix_user_path', path, postgresql_using="gist"),

    def __init__(self, _id, name=None, user_position_id=None, parent=None, **kw: Any):
        super().__init__(**kw)
        self.user_position_id = user_position_id
        self.id = _id
        self.name = name
        ltree_id = Ltree(str(_id))
        self.path = ltree_id if parent is None else parent.path + ltree_id
