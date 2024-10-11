# user_service.py


from uuid import UUID
from fastapi import Depends
from typing import Annotated


from ..models.user import User
from psycopg_pool import ConnectionPool
from ..repositories.repository_interface import Repository
from ..repositories.user_repository import UserRepository


class UserService:

    def __init__(self, user_repo: Annotated[UserRepository, Depends(UserRepository)]):
        self.user_repo = user_repo
        return
    
    def list_users(self, db_pool):
        users_list = self.user_repo.get_all(db_pool)
        return users_list
    
    def get_user(self, db_pool, user_id:UUID):
        user_data = self.user_repo.get_one(db_pool, user_id)
        return user_data
    
    def create_user(self, db_pool, user:User):
        self.user_repo.create(db_pool, user)
        return
    
    def update_user(self, db_pool, user:User):
        self.user_repo.update(db_pool, user)
        return
    
    def update_part_user(self, db_pool, user_id:UUID, update_dict:dict):
        self.user_repo.update_part(db_pool, user_id, update_dict)
        return
    
    def delete_user(self, db_pool, user_id:UUID):
        self.user_repo.delete(db_pool, user_id)
        return
    
    def update_wallets(self, db_pool, user_id:UUID, wallet_id:UUID):
        self.user_repo.append_to_wallets(db_pool, user_id, wallet_id)
        return

    def update_family_members(self, db_pool, user_id:UUID, family_member_id:UUID):
        self.user_repo.append_to_family_members(db_pool, user_id, family_member_id)
        return
