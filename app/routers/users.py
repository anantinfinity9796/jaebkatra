

import logging
from uuid import UUID
from typing import Annotated, Any
from fastapi import APIRouter, status, Depends


from ..database.database import Database, get_database_connection
from ..models.user import User
from ..services.user_service import UserService
from ..repositories.user_repository import UserRepository
app_logger = logging.getLogger("app")


router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# declare dependencies before hand for a cleaner code
UsersService = Annotated[UserService, Depends(UserService)]
DbConn =  Annotated[Database, Depends(get_database_connection)]

                     
@router.get("/", status_code=status.HTTP_200_OK)
def list_users(user_service: UsersService, db_conn: DbConn) -> list:
    try:
        users_list = user_service.list_users(db_conn)
        return users_list
    except Exception as e:
        app_logger.error("failed to get user list", exc_info=e)


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user_details(user_id:UUID, user_service: UsersService, db_conn: DbConn) -> dict:
    try:
        user_data = user_service.get_user(db_conn, user_id)
        return user_data
    except Exception as e:
        app_logger.error(f"failed to fetch user details for user_id: {user_id}", exc_info=e)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: User, user_service: UsersService, db_conn: DbConn):
    try:
        user_service.create_user(db_conn, user)
    except Exception as e:
        app_logger.error(f"failed to create user: {user.name}", exc_info=e)
    return

# @router.patch("/users/update")
# def modify_user(payload:dict)

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id:UUID, user_service: UsersService, db_conn: DbConn):
    try:
        user_service.delete_user(db_conn, user_id)
    except Exception as e:
        app_logger.error(f"failed to delete user: {user_id}", exc_info=e)
    return 