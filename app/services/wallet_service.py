# wallet_service.py


import logging
from uuid import UUID
from fastapi import Depends
from typing import Annotated


from ..models.wallet import Wallet
from ..database.database import Database
from ..repositories.user_repository import UserRepository
from ..repositories.wallet_repository import WalletRepository


app_logger = logging.getLogger("app")


class WalletService:
    def __init__(self, 
                 user_repo: Annotated[UserRepository, Depends(UserRepository)], 
                 wallet_repo: Annotated[WalletRepository, Depends(WalletRepository)]):
        
        self.user_repo = user_repo
        self.wallet_repo = wallet_repo
        return

    def list_wallets(self, db:Database) -> list:
        with db.pool.connection() as db_conn:
            wallets_list = self.wallet_repo.get_all(db_conn)
        return wallets_list
    
    def get_wallet(self, db:Database, wallet_id:UUID):
        with db.pool.connection() as db_conn:
            wallet_data = self.wallet_repo.get_one(db_conn, wallet_id)
        return wallet_data
    
    def create_wallet(self, db:Database, wallet:Wallet):
        try:
            with db.pool.connection() as db_conn:
                self.wallet_repo.create(db_conn, wallet)
                self.user_repo.append_to_wallets(db_conn, wallet.user_id, wallet.wallet_id)
        except Exception as e:
            app_logger.error(f"failed to create wallet with wallet_id: {wallet.wallet_id} for user_id: {wallet.user_id}")
        return
    
    def update_wallet(self, db:Database, wallet:Wallet):
        with db.pool.connection() as db_conn:
            self.wallet_repo.update(db_conn, wallet)
        return
    
    def update_part_wallet(self, db:Database, wallet_id:UUID, update_dict:dict):
        with db.pool.connection() as db_conn:
            self.wallet_repo.update_part(db_conn, wallet_id, update_dict)
        return
    
    def delete_wallet(self, db:Database, wallet_id:UUID):
        try:
            with db.pool.connection() as db_conn:
                wallet = self.wallet_repo.get_one(db_conn, wallet_id)
                self.user_repo.delete_wallet(db_conn, user_id=wallet.get('user_id'), wallet_id=wallet_id)
                self.wallet_repo.delete(db_conn, wallet_id)
        except Exception as e:
            app_logger.error(f"error deleting the wallet: {wallet_id}", exc_info=e)
            raise
        return