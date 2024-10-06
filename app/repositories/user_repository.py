# user_api_operations.py


import logging
from uuid import UUID

from .repository_interface import Repository
from ..models.user import User
from ..database.database import Database

app_logger = logging.getLogger("app")

class UserRepository(Repository):

    def __init__(self):
        return

    def get_all(self, db_conn:Database) -> list:
        list_users_query = """SELECT * FROM users;"""
        user_list = db_conn.fetch_all(list_users_query)
        return user_list

    def get_one(self, db_conn:Database, user_id:UUID) -> dict:
        app_logger.info(f"get user details for user_id: {user_id}")
        get_user_query = f""" SELECT * FROM users WHERE user_id = %(user_id)s;"""
        user_data = db_conn.fetch_one(query=get_user_query, values={'user_id':user_id.hex})
        return user_data

    def create(self, db_conn:Database, user: User):
        app_logger.info(f"creating new user with name: {user.name}")
        user_model_dump = user.model_dump()

        create_user_query = f"""INSERT INTO users (user_id, name, created_ts, phone, wallets, family_members) 
                                    VALUES (%(user_id)s, %(name)s, %(created_ts)s, %(phone)s, %(wallets)s, %(family_members)s);"""
        db_conn.execute_query(query=create_user_query, values=user_model_dump)
        return 
    
    def update(self, db_conn:Database, user:User):
        app_logger.info(f"updating user with user_id: {user.user_id}")
        user_model_dump = user.model_dump()
        update_user_query = f"""
            UPDATE users
            SET name=%(name)s,
                phone=%(phone)s,
                wallets=%(wallets)s,
                family_members=%(family_members)
            WHERE user_id=%(user_id)s;
"""
        db_conn.execute_query(query=update_user_query, values=user_model_dump)
        return
    
    def update_part(self, db_conn:Database, user_id:UUID, update_dict:dict):
        app_logger.info(f"updating user with user_id: {user_id} with key,value pair {update_dict}")
        update_partial_user_query = """
            UPDATE users
            SET {},
            WHERE user_id = %(user_id)s,
""".format(", ".join([f"{key} = {value}" for key,value in update_dict.items()]))
        
        db_conn.execute_query(query=update_partial_user_query, values=update_dict)
        return

    def delete(self, db_conn:Database, user_id: UUID):
        app_logger.info(f"Deleting user with user_id: {user_id}")
        delete_user_query = """DELETE FROM users WHERE user_id = %(user_id)s"""
        db_conn.execute_query(query=delete_user_query, values={"user_id":user_id.hex})
        return
    
    def append_to_wallets(self, db_conn:Database, user_id:UUID, wallet_id: UUID):
        app_logger.info(f"Appending to wallets for user_id: {user_id}")
        append_to_wallet_query = """
        UPDATE users
        set wallets = ARRAY_APPEND(wallets, %(wallet_id)s)
        WHERE user_id = %(user_id)s;
"""
        db_conn.execute_query(query=append_to_wallet_query, values={"user_id":user_id, "wallet_id":wallet_id})
        return
    
    def append_to_family_members(self, db_conn:Database, user_id:UUID, family_member_id:UUID):
        app_logger.info(f"Appending to family_members for user_id: {user_id}")
        append_to_family_members_query = """
        UPDATE users
        set family_members = ARRAY_APPEND(family_members, %(family_member_id)s)
        WHERE user_id = %(user_id)s;
"""
        db_conn.execute_query(query=append_to_family_members_query, values={"user_id":user_id, "family_member_id":family_member_id})
        return