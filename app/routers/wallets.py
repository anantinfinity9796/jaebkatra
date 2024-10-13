# wallets.py


import logging
from uuid import UUID
from typing import Annotated, Any
from fastapi import APIRouter, status, Depends, HTTPException

from ..models.wallet import Wallet
from ..database.database import Database
from ..services.wallet_service import WalletService

app_logger = logging.getLogger("app")
app_logger.info("In the wallets router")

router = APIRouter(
    prefix="/wallets",
    tags=["wallets"]
)


WalletsService = Annotated[WalletService, Depends(WalletService)]
Db =  Annotated[Database, Depends(Database)]


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Wallet])
def list_wallets(wallet_service: WalletsService, db: Db) -> Any:
    try:
        wallets_list = wallet_service.list_wallets(db)
        return wallets_list
    except Exception as e:
        app_logger.error("failed to get wallets list", exc_info=e)


@router.get("/{wallet_id}", status_code=status.HTTP_200_OK, response_model=Wallet)
def get_wallet_details(wallet_id:UUID, wallet_service: WalletsService, db: Db) -> Any:
    wallet_data = wallet_service.get_wallet(db, wallet_id)
    if wallet_data is None:
        raise HTTPException(status_code=404, detail=f"wallet with wallet_id: {wallet_id} not found")
    return wallet_data


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_wallet(wallet:Wallet, wallet_service: WalletsService, db: Db):
    try:
        wallet_service.create_wallet(db, wallet)
    except Exception as e:
        app_logger.error(f"failed to create wallet: {wallet.name}", exc_info=e)

# @router.patch("/wallets/update")
# def modify_user(payload:dict)

@router.delete("/{wallet_id}", status_code=status.HTTP_200_OK)
def delete_wallet(wallet_id:UUID, wallet_service: WalletsService, db: Db):
    try:
        wallet_service.delete_wallet(db, wallet_id)
    except Exception as e:
        app_logger.error(f"failed to delete wallet: {wallet_id}", exc_info=e)