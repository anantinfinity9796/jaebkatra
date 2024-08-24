# wallets.py


import logging
from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, status, Depends

from ..database.database import Database, get_database_connection
from ..models.wallet import Wallet



router = APIRouter(
    prefix="/wallets",
    tags=["wallets"]
)




app_logger = logging.getLogger("app")



@router.get("/", status_code=status.HTTP_200_OK)
def list_wallets(db_conn: Annotated[Database, Depends(get_database_connection)]) -> list:
    try:
        app_logger.info(f"listing all wallets")
        list_wallets_query = f""" SELECT * FROM wallets ;"""
        wallets_list_data = db_conn.fetch_all(query=list_wallets_query)
        return wallets_list_data
    except Exception as e:
        app_logger.error("failed to get wallets list", exc_info=e)


@router.get("/{wallet_id}", status_code=status.HTTP_200_OK)
def get_wallet_details(wallet_id:UUID, db_conn: Annotated[Database, Depends(get_database_connection)]) -> dict:
    try:
        app_logger.info(f"get wallet details for wallet_id: {wallet_id}")
        get_wallet_query = f""" SELECT * FROM wallets WHERE wallet_id = %s;"""
        wallet_data = db_conn.fetch_one(query=get_wallet_query, values=[wallet_id.hex])
        return wallet_data
    except Exception as e:
        app_logger.error(f"failed to get wallet details for wallet_id: {wallet_id}", exc_info=e)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_wallet(wallet:Wallet, db_conn: Annotated[Database, Depends(get_database_connection)]):
    try:
        app_logger.info(f"creating a new wallet with name: {wallet.name}")
        wallet_model_dump = wallet.model_dump()
        create_wallet_query = f"""INSERT INTO wallets (wallet_id, user_id, name, created_ts, allocated_balance,
                                                            consumed_balance, wallet_type)
                                    VALUES (%(wallet_id)s, %(user_id)s, %(name)s, %(created_ts)s,
                                                %(allocated_balance)s, %(consumed_balance)s, %(wallet_type)s);"""
        update_user_query  = """
            UPDATE users
            SET wallets = ARRAY_APPEND(wallets, %(wallet_id)s)
            WHERE user_id = %(user_id)s;
"""
        db_conn.execute_transaction([create_wallet_query, update_user_query], wallet_model_dump)
    except Exception as e:
        app_logger.error(f"failed to create wallet: {wallet.name}", exc_info=e)

# @router.patch("/wallets/update")
# def modify_user(payload:dict)

@router.delete("/{wallet_id}", status_code=status.HTTP_200_OK)
def delete_wallet(wallet_id:UUID, db_conn: Annotated[Database, Depends(get_database_connection)]):
    try:
        app_logger.info(f"Deleting wallet with wallet_id: {wallet_id}")
        delete_wallet_query = """DELETE FROM wallets where wallet_id = %s;"""
        db_conn.delete_one(query=delete_wallet_query, values=[wallet_id.hex])
    except Exception as e:
        app_logger.error(f"failed to delete wallet: {wallet_id}", exc_info=e)