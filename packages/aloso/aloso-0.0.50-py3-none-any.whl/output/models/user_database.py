import codecs
import hashlib
import logging
from typing import Optional

from sqlalchemy import Column, String, Integer, Boolean

from domain.user import User
from output.database.database_base import Base, Session
from output.database.repository import RepositoryDB


class UserData(Base, User):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(String(50))
    admin = Column(Boolean, default=False)
    change_pwd = Column(Boolean, default=False)

    @property
    def repository(self):
        return RepositoryDB(model=self)

    @classmethod
    def get_all(cls, session=Session) -> Optional[dict]:
        repository = RepositoryDB(model=cls())
        return repository.get_all_obj(load_related=True, db_session=session)

    @classmethod
    def get_by_id(cls, u_id: int, session=Session):
        repository = RepositoryDB(model=cls())
        return repository.get_by_id(obj_id=u_id, db_session=session, load_related=True)

    def create(self, session=Session):
        return self.repository.save(db_session=session)

    def update(self, session=Session):
        return self.repository.save(db_session=session)

    def delete(self, session=Session):
        return self.repository.delete(db_session=session)

    def hash_pass(self):
        salt_phrase = f"$2a$12$/dskhjsd"
        hashed_password = hashlib.pbkdf2_hmac(hash_name='sha512', password=self.password.encode('utf-8'),
                                              salt=salt_phrase.encode('utf-8'), iterations=100000)
        encoded_hash = codecs.encode(hashed_password, "base64")
        self.password = encoded_hash

    def user_check(self, session=Session):
        try:
            with session:
                return session.query(UserData).filter(UserData.username == self.username).filter(
                    UserData.password == self.password).first()
        except Exception as e:
            logging.error(e)
