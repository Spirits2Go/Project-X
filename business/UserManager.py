from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from data_models.models import Login, Role
import bcrypt

class UserManager:
    def __init__(self, db_file):
        self.__engine = create_engine(f'sqlite:///{db_file}', echo=False)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))
        self.current_user = None

    def login(self, username, password):
        user = self.__session.query(Login).filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            self.current_user = user
            return user
        return None

    def get_user_role(self, user):
        return user.role.name if user and user.role else None

    def create_user(self, username, password, role_name):
        role = self.__session.query(Role).filter_by(name=role_name).first()
        if role:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            new_user = Login(username=username, password=hashed_password.decode('utf-8'), role=role)
            self.__session.add(new_user)
            self.__session.commit()
            return new_user
        return None

    def get_roles(self):
        return self.__session.query(Role).all()

    def get_current_user(self):
        return self.current_user