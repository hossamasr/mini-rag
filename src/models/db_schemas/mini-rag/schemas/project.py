from .minirag_base import SqlAlchemyBase
from sqlalchemy import Column,Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid
class project(SqlAlchemyBase):
    __tablename__="projects"

    project_id=Column(Integer,primary_key=True,autoincrement=True)

    project_uuid=Column(UUID,default=uuid.uuid4,unique=True,nullable=False)
    # didn't complete postgres migration