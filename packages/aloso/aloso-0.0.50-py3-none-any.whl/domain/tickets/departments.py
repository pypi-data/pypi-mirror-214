from dataclasses import dataclass
from typing import List

from domain.tickets.incidents import Incident


@dataclass
class Department:
    id: int
    name: str = ""
    incidents: List[Incident] = None

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
