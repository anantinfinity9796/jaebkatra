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
    
    def list_users(self, db:Database):
        with db.pool.connection() as db_conn:      
            users_list = self.user_repo.get_all(db_conn)
        return users_list
    
    def get_user(self, db:Database, user_id:UUID):
        with db.pool.connection() as db_conn:
            user_data = self.user_repo.get_one(db_conn, user_id)
        return user_data
    
    def create_user(self, db:Database, user:User):
        with db.pool.connection() as db_conn:
            self.user_repo.create(db_conn, user)
        return
    
    def update_user(self, db:Database, user:User):
        with db.pool.connection() as db_conn:
            self.user_repo.update(db_conn, user)
        return
    
    def update_part_user(self, db:Database, user_id:UUID, update_dict:dict):
        with db.pool.connection() as db_conn:
            self.user_repo.update_part(db_conn, user_id, update_dict)
        return
    
    def delete_user(self, db:Database, user_id:UUID):
        with db.pool.connection() as db_conn:
            self.user_repo.delete(db_conn, user_id)
        return
    
    def update_wallets(self, db:Database, user_id:UUID, wallet_id:UUID):
        with db.pool.connection() as db_conn:
            self.user_repo.append_to_wallets(db_conn, user_id, wallet_id)
        return

    def update_family_members(self, db:Database, user_id:UUID, family_member_id:UUID):
        with db.pool.connection() as db_conn:
            self.user_repo.append_to_family_members(db_conn, user_id, family_member_id)
        return
