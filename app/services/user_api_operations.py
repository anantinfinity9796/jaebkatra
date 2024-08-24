# user_api_operations.py


import logging
from uuid import UUID

from ..repositories.api_operations import ApiOperations
from ..models.user import User

app_logger = logging.getLogger("app")

class UserApiOperations(ApiOperations):

    def get_all(self, db_conn) -> list[User]:
        list_users_query = """ SELECT * FROM users ;"""
        users_list_data = db_conn.fetch_all(query=list_users_query)
        return users_list_data

    def get_one(self, db_conn, user_id:UUID) -> User:
        app_logger.info(f"get user details for user_id: {user_id}")
        get_user_query = f""" SELECT * FROM users WHERE user_id = %s;"""
        user_data = db_conn.fetch_one(query=get_user_query, values=[user_id.hex])
        return user_data

    def create(self, db_conn, user:User):
        app_logger.info(f"creating new user with name: {user.name}")
        user_model_dump = user.model_dump()

        create_user_query = f"""INSERT INTO users (user_id, name, created_ts, phone, wallets, family_members) 
                                    VALUES (%(user_id)s, %(name)s, %(created_ts)s, %(phone)s, %(wallets)s, %(family_members)s);"""
        
        db_conn.insert_one(create_user_query, user_model_dump)
        return
    
    def update(self, db_conn, user:User):
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
        db_conn.insert_one(update_user_query, user_model_dump)
        return
    
    def update_part(self, db_conn, user_id, update_dict:dict):
        app_logger.info(f"updating user with user_id: {user_id} with key,value pair {update_dict}")
        update_partial_user_query = """
            UPDATE users
            SET {},
            WHERE user_id = %(user_id)s,
""".format(", ".join([f"{key} = {value}" for key,value in update_dict.items()]))
        
        db_conn.insert_one(update_partial_user_query, {"user_id":user_id})
        return

    def delete(self, db_conn, user_id: UUID):
        app_logger.info(f"Deleting user with user_id: {user_id}")
        delete_user_query = """DELETE FROM users WHERE user_id = %s"""
        db_conn.delete_one(query=delete_user_query, values=[user_id.hex])
        return