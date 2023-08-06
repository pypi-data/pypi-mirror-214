import logging
from dataclasses import dataclass
from typing import List

import config
from domain.equipment_management import Equipments

logging.basicConfig(level=config.debug_level,
                    format='%(asctime)s %(levelname)s %(pathname)s %(funcName)s %(lineno)d : %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    filename=config.logs_file_path,
                    filemode='a')


@dataclass
class Building:
    equipments: List[Equipments] = None
    id: int = None
    name: str = ""

    def create(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass

    @staticmethod
    def get_by_name(name: str):
        pass

    @staticmethod
    def get_by_id(b_id: int):
        pass

    @staticmethod
    def get_all():
        pass

    def toggle_building_equipment_link(self, equipment):
        if equipment in self.equipments:
            self.equipments.remove(equipment)
        else:
            self.equipments.append(equipment)

    def execute(self, *args):
        pass
