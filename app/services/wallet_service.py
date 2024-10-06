# wallet_service.py


import logging
from uuid import UUID
from fastapi import Depends
from typing import Annotated


from ..models.wallet import Wallet
from ..database.database import Database
from ..repositories.repository_interface import Repository
from ..repositories.user_repository import UserRepository
from ..repositories.wallet_repository import WalletRepository


app_logger = logging.getLogger("app")


class WalletService:
    def __init__(self, user_repo: Annotated[UserRepository, Depends(UserRepository)], wallet_repo: Annotated[WalletRepository, Depends(WalletRepository)]):
        self.user_repo = user_repo
        self.wallet_repo = wallet_repo
        return

    def list_wallets(self, db_conn:Database) -> list:
        wallets_list = self.wallet_repo.get_all(db_conn)
        return wallets_list
    
    def get_wallet(self, db_conn:Database, wallet_id:UUID):
        wallet_data = self.wallet_repo.get_one(db_conn, wallet_id)
        return wallet_data
    
    def create_wallet(self, db_conn:Database, wallet:Wallet):
        try:
            self.wallet_repo.create(db_conn, wallet)
            self.user_repo.append_to_wallets(db_conn, wallet.user_id, wallet.wallet_id)
            # db_conn.commit()
        except Exception as e:
            # db_conn.rollback()
            app_logger.error(f"failed to create wallet with wallet_id: {wallet.wallet_id} for user_id: {wallet.user_id}")
        return
    
    def update_wallet(self, db_conn:Database, wallet:Wallet):
        self.wallet_repo.update(db_conn, wallet)
        return
    
    def update_part_wallet(self, db_conn:Database, wallet_id:UUID, update_dict:dict):
        self.wallet_repo.update_part(db_conn, wallet_id, update_dict)
        return
    
    def delete_wallet(self, db_conn:Database, wallet_id:UUID):
        self.wallet_repo.delete(db_conn, wallet_id)
        return