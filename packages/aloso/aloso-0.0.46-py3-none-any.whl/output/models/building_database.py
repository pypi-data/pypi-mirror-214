from typing import Optional, List

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

import config
from domain.building import Building
from output.database.database_base import Base, Session
from output.database.repository import RepositoryDB
from output.models.equipments_database import EquipmentsData
from output.shell.shell import Shell


class BuildingData(Base, Building):
    __tablename__ = "Building"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    equipments = relationship("EquipmentsData", back_populates="building")

    @property
    def repository(self):
        return RepositoryDB(model=self)

    # OK
    def create(self, session=Session):
        try:
            assert self.name != ""
            return self.repository.save(db_session=session)
        except AssertionError:
            return False

    # OK
    def delete(self, session=Session):
        return self.repository.delete(db_session=session)

    # OK
    def update(self, session=Session):
        return self.repository.save(db_session=session)

    # OK
    @classmethod
    def get_by_id(cls, b_id: int, session=Session):
        repository = RepositoryDB(model=cls())
        return repository.get_by_id(obj_id=b_id, db_session=session, load_related=True)

    # OK
    @classmethod
    def get_all(cls, session=Session) -> Optional[dict]:
        repository = RepositoryDB(model=cls())
        return repository.get_all_obj(load_related=True, db_session=session)

    # OK
    def update_building_equipment_link(self, equipments: List[EquipmentsData], session=Session):
        return self.repository.link(second_relation_objects=equipments, method=self.toggle_building_equipment_link,
                                    db_session=session)

    # OK
    def execute(self, *args):
        conn = Shell.ssh_connection(host=self.equipment.ip,
                                    username=config.ssh_equipment_username,
                                    password=config.ssh_equipment_password,
                                    port=config.ssh_equipment_port)

        cmd = "energywise query importance 75 name set level 10" if args[0] is None else args[0]

        try:
            with conn:
                conn.run(cmd)
            print(f"Commande {cmd} executé avec succès")
        except Exception as e:
            print(f"Erreur d'execution de la commande : {e}")
