from flask_login import UserMixin
from .firestore_service import get_user, user_put

class UserData:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserModel(UserMixin):
    def __init__(self, user_data):
        self.id = user_data.username
        self.password = user_data.password

    @staticmethod
    def query(user_id):
        user_doc = get_user(user_id)
        if not user_doc.exists:
            return None
        user_data = UserData(
            username=user_doc.id,
            password=user_doc.to_dict()['password']
        )
        return UserModel(user_data)
    
    @staticmethod
    def create(user_id, password):
        user_data = UserData(username=user_id, password=password)
        user_model = UserModel(user_data)
        user_put(user_data)
        return user_model

    def check_password(self, password):
        return self.password == password
