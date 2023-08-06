from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import config

engine = create_engine(f'{config.database_resource}:///{config.database_file}')
Session = sessionmaker(bind=engine)()
Base = declarative_base()
