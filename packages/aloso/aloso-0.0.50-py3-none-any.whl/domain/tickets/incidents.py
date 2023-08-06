from dataclasses import dataclass

from domain.tickets.departments import Department


@dataclass
class Incident:
    id: int
    description: str = ""
    image: str = ""
    state: str = ""
    department_id: int = 0
    department: Department = None

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    @staticmethod
    def get_by_id(id_departement):
        pass

    @staticmethod
    def get_all():
        pass
