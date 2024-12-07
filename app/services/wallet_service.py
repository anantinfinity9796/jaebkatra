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

    def list_wallets(self, db_conn:Database) -> list:
        with db_conn.cursor() as cur:
            wallets_list = self.wallet_repo.get_all(cur)
        return wallets_list
    
    def get_wallet(self, db_conn:Database, wallet_id:UUID):
        with db_conn.cursor() as cur:
            wallet_data = self.wallet_repo.get_one(cur, wallet_id)
        return wallet_data
    
    def create_wallet(self, db_conn:Database, wallet:Wallet):
        with db_conn.cursor() as cur:
            self.wallet_repo.create(cur, wallet)
        return
    
    def update_wallet(self, db_conn:Database, wallet:Wallet):
        with db_conn.cursor() as cur:
            self.wallet_repo.update(cur, wallet)
        return
    
    def update_part_wallet(self, db_conn:Database, wallet_id:UUID, update_dict:dict):
        with db_conn.cursor() as cur:
            self.wallet_repo.update_part(cur, wallet_id, update_dict)
        return
    
    def delete_wallet(self, db_conn:Database, wallet_id:UUID):
        with db_conn.cursor() as cur:
            self.wallet_repo.delete(cur, wallet_id)
        return