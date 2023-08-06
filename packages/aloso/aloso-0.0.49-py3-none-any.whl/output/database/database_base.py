import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import config

engine = create_engine(f'{config.database_resource}:///{config.database_file}')
Session = sessionmaker(bind=engine)()


class MyBase:

    def save(self, db_session):
        try:
            with db_session as session:
                session.merge(self)
                session.commit()
                logging.info(f"{type(self).__name__} sauvegardé dans la base de données")
                return True
        except Exception as e:
            session.rollback()
            logging.error(f"Erreur lors de la sauvegarde dans la base de données : {e}")
            return False


Base = declarative_base(cls=MyBase)
