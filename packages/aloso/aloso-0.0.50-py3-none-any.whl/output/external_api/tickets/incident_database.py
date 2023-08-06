from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from output.database.database_base import Base


class IncidentData(Base):
    __tablename__ = 'incident'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    image = Column(String)
    state = Column(Enum('to_assign', 'in_progress', 'closed'))
    department_id = Column(Integer, ForeignKey('department.id'))
    department = relationship('Department', back_populates='incidents')
