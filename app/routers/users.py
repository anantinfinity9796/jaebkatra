

import logging
from uuid import UUID
from typing import Annotated, Any
from fastapi import APIRouter, status, Depends
from ..database.database import Database, get_database_connection
from ..models.user import User

app_logger = logging.getLogger("app")


router = APIRouter(
    prefix="/users",
    tags=["users"],
    
)


@router.get("/", status_code=status.HTTP_200_OK)
def list_users(db_conn: Annotated[Database, Depends(get_database_connection)]) -> list:
    try:
        app_logger.info(f"listing all users")
        list_users_query = """ SELECT * FROM users ;"""
        users_list_data = db_conn.fetch_all(query=list_users_query)
        return users_list_data
    except Exception as e:
        app_logger.error("failed to get user list", exc_info=e)


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user_details(user_id:UUID, db_conn: Annotated[Database, Depends(get_database_connection)]) -> dict:
    try:
        app_logger.info(f"get user details for user_id: {user_id}")
        get_user_query = f""" SELECT * FROM users WHERE user_id = %s;"""
        user_data = db_conn.fetch_one(query=get_user_query, values=[user_id.hex])
        return user_data
    except Exception as e:
        app_logger.error(f"failed to fetch user details for user_id: {user_id}", exc_info=e)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: User, db_conn: Annotated[Database, Depends(get_database_connection)]):
    try:
        app_logger.info(f"creating new user with name: {user.name}")        
        user_model_dump = user.model_dump()

        create_user_query = f"""INSERT INTO users (user_id, name, created_ts, phone, wallets, family_members) 
                                    VALUES (%(user_id)s, %(name)s, %(created_ts)s, %(phone)s, %(wallets)s, %(family_members)s);"""
        
        db_conn.insert_one(create_user_query, user_model_dump)
    except Exception as e:
        app_logger.error(f"failed to create user: {user.name}", exc_info=e)

# @router.patch("/users/update")
# def modify_user(payload:dict)

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id:UUID, db_conn: Annotated[Database, Depends(get_database_connection)]):
    try:
        app_logger.info(f"Deleting user with user_id: {user_id}")
        delete_user_query = """DELETE FROM users WHERE user_id = %s"""
        db_conn.delete_one(query=delete_user_query, values=[user_id.hex])
    except Exception as e:
        app_logger.error(f"failed to delete user: {user_id}", exc_info=e)
    return 