# wallet_service.py


from uuid import UUID
from ..models.wallet import Wallet
from ..database.database import Database
from ..repositories.repository_interface import Repository


class WalletService:

    def list_wallets(self, db_conn:Database, wallet_repo:Repository):
        wallets_list = wallet_repo.get_all(db_conn)
        return wallets_list
    
    def get_wallet(self, db_conn:Database, wallet_repo:Repository, wallet_id:UUID):
        wallet_data = wallet_repo.get_one(db_conn, wallet_id)
        return wallet_data
    
    def create_wallet(self, db_conn:Database, wallet_repo:Repository, user_repo:Repository, wallet:Wallet):
        wallet_repo.create(db_conn, wallet)
        return
    
    def update_wallet(self, db_conn:Database, wallet_repo:Repository, wallet:Wallet):
        wallet_repo.update(db_conn, wallet)
        return
    
    def update_part_wallet(self, db_conn:Database, wallet_repo:Repository, wallet_id:UUID, update_dict:dict):
        wallet_repo.update_part(db_conn, wallet_id, update_dict)
        return
    
    def delete_wallet(self, db_conn:Database, wallet_id:UUID, wallet_repo:Repository):
        wallet_repo.delete(db_conn, wallet_id)
        return