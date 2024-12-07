# user_service.py


from uuid import UUID
from fastapi import Depends
from typing import Annotated


from ..models.user import User
from ..database.database import Database
from ..repositories.user_repository import UserRepository


class UserService:

    def __init__(self, user_repo: Annotated[UserRepository, Depends(UserRepository)]):
        self.user_repo = user_repo
        return
    
    def list_users(self, db_conn:Database):
        with db_conn.cursor() as cur:
            users_list = self.user_repo.get_all(cur)
        return users_list
    
    def get_user(self, db_conn:Database, user_id:UUID):
        with db_conn.cursor() as cur:
            user_data = self.user_repo.get_one(cur, user_id)
        return user_data
    
    def create_user(self, db_conn:Database, user:User):
        with db_conn.cursor() as cur:
            self.user_repo.create(cur, user)
        return
    
    def update_user(self, db_conn:Database, user:User):
        with db_conn.cursor() as cur:
            self.user_repo.update(cur, user)
        return
    
    def update_part_user(self, db_conn:Database, user_id:UUID, update_dict:dict):
        with db_conn.cursor() as cur:
            self.user_repo.update_part(cur, user_id, update_dict)
        return
    
    def delete_user(self, db_conn:Database, user_id:UUID):
        with db_conn.cursor() as cur:
            self.user_repo.delete(cur, user_id)
        return
