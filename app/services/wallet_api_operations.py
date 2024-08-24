# wallet_api_operations.py

import logging
from uuid import UUID

from ..repositories.api_operations import ApiOperations
from ..models.wallet import Wallet

app_logger = logging.getLogger("app")

class WalletApiOperations(ApiOperations):

    def get_all(self, db_conn) -> list[Wallet]:
        app_logger.info(f"listing all wallets")
        list_wallets_query = f""" SELECT * FROM wallets ;"""
        wallets_list_data = db_conn.fetch_all(query=list_wallets_query)
        return wallets_list_data
    
    def get_one(self, db_conn, wallet_id: UUID) -> Wallet:
        app_logger.info(f"get wallet details for wallet_id: {wallet_id}")
        get_wallet_query = f""" SELECT * FROM wallets WHERE wallet_id = %s;"""
        wallet_data = db_conn.fetch_one(query=get_wallet_query, values=[wallet_id.hex])
        return wallet_data
    
    def create(self, db_conn, wallet:Wallet):
        app_logger.info(f"creating a new wallet with name: {wallet.name}")
        wallet_model_dump = wallet.model_dump()
        create_wallet_query = f"""INSERT INTO wallets (wallet_id, user_id, name, created_ts, allocated_balance,
                                                            consumed_balance, wallet_type)
                                    VALUES (%(wallet_id)s, %(user_id)s, %(name)s, %(created_ts)s,
                                                %(allocated_balance)s, %(consumed_balance)s, %(wallet_type)s);"""
        db_conn.insert_one(create_wallet_query, wallet_model_dump)
        return
    
    def update(self, db_conn, wallet:Wallet):
        app_logger.info(f"updating wallet with wallet_id: {wallet.wallet_id}")
        wallet_model_dump = wallet.model_dump()
        update_wallet_query = f"""
            UPDATE wallets
            SET user_id=%(user_id)s,
                name=%(name)s,
                allocated_balance=%(allocated_balance)s,
                consumed_balance=%(consumed_balance),
            WHERE wallet_id=%(wallet_id)s;
"""
        db_conn.insert_one(update_wallet_query, wallet_model_dump)
        return

    def delete(self, db_conn, wallet_id:UUID):
        app_logger.info(f"Deleting wallet with wallet_id: {wallet_id}")
        delete_wallet_query = """DELETE FROM wallets where wallet_id = %s;"""
        db_conn.delete_one(query=delete_wallet_query, values=[wallet_id.hex])
        return