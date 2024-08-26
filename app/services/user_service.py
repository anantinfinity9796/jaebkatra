# user_service.py

from uuid import UUID
from ..models.user import User
from ..database.database import Database
from ..repositories.repository_interface import Repository



class UserService:
    
    def list_users(self, db_conn:Database, user_repo:Repository):
        users_list = user_repo.get_all(db_conn)
        return users_list
    
    def get_user(self, db_conn:Database, user_repo:Repository, user_id:UUID):
        user_data = user_repo.get_one(db_conn, user_id)
        return user_data
    
    def create_user(self, db_conn:Database, user_repo:Repository, user:User):
        user_repo.create(db_conn, user)
        return
    
    def update_user(self, db_conn:Database, user_repo:Repository, user:User):
        user_repo.update(db_conn, user)
        return
    
    def update_part_user(self, db_conn:Database, user_repo:Repository, user_id:UUID, update_dict:dict):
        user_repo.update_part(db_conn, user_id, update_dict)
        return
    
    def delete_user(self, db_conn:Database, user_id:UUID, user_repo:Repository):
        user_repo.delete(db_conn, user_id)
        return
    
    def update_wallets(self, db_conn:Database, user_id:UUID, wallet_id:UUID, user_repo:Repository):
        user_repo.append_to_wallets(db_conn, user_id, wallet_id)
        return

    def update_family_members(self, db_conn:Database, user_id:UUID, family_member_id:UUID, user_repo:Repository):
        user_repo.append_to_family_members(db_conn, user_id, family_member_id)
        return
