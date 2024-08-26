# wallets.py


import logging
from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, status, Depends

from ..database.database import Database, get_database_connection
from ..models.wallet import Wallet
from ..repositories.user_api_operations import UserApiOperations
from ..repositories.wallet_api_operations import WalletApiOperations



router = APIRouter(
    prefix="/wallets",
    tags=["wallets"]
)


app_logger = logging.getLogger("app")

UserApiOperation = Annotated[UserApiOperations, Depends(UserApiOperations)]
WalletApiOperation = Annotated[WalletApiOperations, Depends(WalletApiOperations)]
DbConn =  Annotated[Database, Depends(get_database_connection)]


@router.get("/", status_code=status.HTTP_200_OK)
def list_wallets(wallet_api_operation: WalletApiOperation, db_conn: DbConn) -> list:
    try:
        
        list_wallets_query, values = wallet_api_operation.get_all()
        wallets_list_data = db_conn.fetch_all(query=list_wallets_query, values=values)
        return wallets_list_data
    except Exception as e:
        app_logger.error("failed to get wallets list", exc_info=e)


@router.get("/{wallet_id}", status_code=status.HTTP_200_OK)
def get_wallet_details(wallet_id:UUID, wallet_api_operation: WalletApiOperation, db_conn: DbConn) -> dict:
    try:
        get_wallet_query, values = wallet_api_operation.get_one(wallet_id)
        wallet_data = db_conn.fetch_one(query=get_wallet_query, values=values)
        return wallet_data
    except Exception as e:
        app_logger.error(f"failed to get wallet details for wallet_id: {wallet_id}", exc_info=e)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_wallet(wallet:Wallet, wallet_api_operation: WalletApiOperation, user_api_operation:UserApiOperation, db_conn: DbConn):
    try:

        create_wallet_query_value = wallet_api_operation.create(wallet)
        update_user_query_value = user_api_operation.append_to_wallets(user_id=wallet.user_id, wallet_id=wallet.wallet_id)
        db_conn.execute_transaction([create_wallet_query_value, update_user_query_value])
    except Exception as e:
        app_logger.error(f"failed to create wallet: {wallet.name}", exc_info=e)

# @router.patch("/wallets/update")
# def modify_user(payload:dict)

@router.delete("/{wallet_id}", status_code=status.HTTP_200_OK)
def delete_wallet(wallet_id:UUID, wallet_api_operation: WalletApiOperation, db_conn: DbConn):
    try:
        delete_wallet_query, values = wallet_api_operation.delete(wallet_id)
        db_conn.delete_one(query=delete_wallet_query, values=values)
    except Exception as e:
        app_logger.error(f"failed to delete wallet: {wallet_id}", exc_info=e)