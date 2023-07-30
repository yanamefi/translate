from models import UsersTable
from settings import session
from JWT_OP import create_access_token


class UserActions():
    def add_user(self, name, password):
        x = session.query(UsersTable).filter(UsersTable.login==name).all()
        if x:
            return "this name is already registered"
        else:
            session.add(UsersTable(login=name, password=password, points=0))
            session.commit()
            jwt_payload = {"login": name}
            jwt_token = create_access_token(jwt_payload)
            return f"account created, your token is: ' {jwt_token} '"

    def login(self, login, password):
        info = session.query(UsersTable).filter(UsersTable.login == login, UsersTable.password == password).first()
        if info:
            jwt_payload = {"login": login}
            jwt_token = create_access_token(jwt_payload)
            return f"your token is: ' {jwt_token} '"
        else:
            return "that`s wrong information"


acts = UserActions()