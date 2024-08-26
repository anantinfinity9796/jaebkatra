

import logging
from uuid import UUID
from typing import Annotated, Any
from fastapi import APIRouter, status, Depends
from ..database.database import Database, get_database_connection
from ..models.user import User
from ..repositories.user_api_operations import UserApiOperations
app_logger = logging.getLogger("app")


router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# declare dependencies before hand for a cleaner code
UserApiOperation = Annotated[UserApiOperations, Depends(UserApiOperations)]
DbConn =  Annotated[Database, Depends(get_database_connection)]

                     
@router.get("/", status_code=status.HTTP_200_OK)
def list_users(api_operation: UserApiOperation, db_conn: DbConn) -> list:
    try:
        query, values = api_operation.get_all()
        users_list = db_conn.fetch_all(query=query, values=values)
        return users_list
    except Exception as e:
        app_logger.error("failed to get user list", exc_info=e)


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user_details(user_id:UUID, api_operation: UserApiOperation, db_conn: DbConn) -> dict:
    try:
        query, values = api_operation.get_one(user_id)
        user_data = db_conn.fetch_one(query=query, values=values)
        return user_data
    except Exception as e:
        app_logger.error(f"failed to fetch user details for user_id: {user_id}", exc_info=e)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: User, api_operation: UserApiOperation, db_conn: DbConn):
    try:
        query, values = api_operation.create(user=user)
        db_conn.execute_query(query=query, values=values)
    except Exception as e:
        app_logger.error(f"failed to create user: {user.name}", exc_info=e)
    return

# @router.patch("/users/update")
# def modify_user(payload:dict)

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id:UUID, api_operation: UserApiOperation, db_conn: DbConn):
    try:
        query, values = api_operation.delete(user_id)
        db_conn.execute_query(query=query, values=values)
    except Exception as e:
        app_logger.error(f"failed to delete user: {user_id}", exc_info=e)
    return 