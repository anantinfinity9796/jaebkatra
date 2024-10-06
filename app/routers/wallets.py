# wallets.py


import logging
from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, status, Depends

from ..database.database import Database, get_database_connection
from ..models.wallet import Wallet
from ..services.wallet_service import WalletService



router = APIRouter(
    prefix="/wallets",
    tags=["wallets"]
)


app_logger = logging.getLogger("app")

WalletsService = Annotated[WalletService, Depends(WalletService)]
DbConn =  Annotated[Database, Depends(get_database_connection)]


@router.get("/", status_code=status.HTTP_200_OK)
def list_wallets(wallet_service: WalletsService, db_conn: DbConn) -> list:
    try:
        wallets_list = wallet_service.list_wallets(db_conn)
        return wallets_list
    except Exception as e:
        app_logger.error("failed to get wallets list", exc_info=e)


@router.get("/{wallet_id}", status_code=status.HTTP_200_OK)
def get_wallet_details(wallet_id:UUID, wallet_service: WalletsService, db_conn: DbConn) -> dict:
    try:
        wallet_data = wallet_service.get_wallet(db_conn, wallet_id)
        return wallet_data
    except Exception as e:
        app_logger.error(f"failed to get wallet details for wallet_id: {wallet_id}", exc_info=e)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_wallet(wallet:Wallet, wallet_service: WalletsService, db_conn: DbConn):
    try:
        wallet_service.create_wallet(db_conn, wallet)
    except Exception as e:
        app_logger.error(f"failed to create wallet: {wallet.name}", exc_info=e)

# @router.patch("/wallets/update")
# def modify_user(payload:dict)

@router.delete("/{wallet_id}", status_code=status.HTTP_200_OK)
def delete_wallet(wallet_id:UUID, wallet_service: WalletsService, db_conn: DbConn):
    try:
        wallet_service.delete_wallet(db_conn, wallet_id)
    except Exception as e:
        app_logger.error(f"failed to delete wallet: {wallet_id}", exc_info=e)