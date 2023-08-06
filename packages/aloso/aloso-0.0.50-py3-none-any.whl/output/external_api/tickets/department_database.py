from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from domain.tickets.departments import Department
from output.database.database_base import Base


class DepartmentData(Base, Department):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    incidents = relationship('Incident', back_populates='department')