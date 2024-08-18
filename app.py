# app.py

import logging
import uuid
from uuid import UUID
from fastapi import FastAPI

from models.user import User
from models.budget import Budget
from models.transaction import Transaction
from models.wallet import Wallet

from util.util import initialize_logger
from database.database import Database

# initialize the logger
initialize_logger()
app_logger = logging.getLogger("app")

# initialize the database connection
database_conn = Database()

# initialize the app
app = FastAPI()

# Homepage
@app.get("/")
def root():
    app_logger.info("homepage loaded")
    return {"message":"Welcome to JAEBKATRA"}


################################################## CRUD FOR USERS TABLE ####################################################

@app.get("/users")
def list_users() -> list:
    try:
        app_logger.info(f"listing all users")
        list_users_query = f""" SELECT * FROM users LIMIT 20; """
        users_list_data = database_conn.fetch_all(query=list_users_query)
        app_logger.info(users_list_data)
        return users_list_data
    except Exception as e:
        app_logger.error("failed to get user list", exc_info=e)

@app.get("/users/{user_id}")
def get_user_details(user_id:UUID) -> dict:
    try:
        app_logger.info(f"get user details for user_id: {user_id}")
        get_user_query = f""" SELECT * FROM users WHERE user_id = %s;"""
        user_data = database_conn.fetch_one(query=get_user_query, values=[user_id.hex])
        return user_data
    except Exception as e:
        app_logger.error(f"failed to fetch user details for user_id: {user_id}", exc_info=e)

@app.post("/users")
def create_user(user: User):
    try:
        app_logger.info(f"creating new user with name: {user.name}")        
        user_model_dump = user.model_dump()

        create_user_query = f"""INSERT INTO users (user_id, name, created_ts, phone, wallets, family_members) 
                                    VALUES (%(user_id)s, %(name)s, %(created_ts)s, %(phone)s, %(wallets)s, %(family_members)s);"""
        
        database_conn.insert_one(create_user_query, user_model_dump)
    except Exception as e:
        app_logger.error(f"failed to create user: {user.name}", exc_info=e)

# @app.patch("/users/update")
# def modify_user(payload:dict)

@app.delete("/users/{user_id}")
def delete_user(user_id:UUID):
    try:
        app_logger.info(f"Deleting user with user_id: {user_id}")
        delete_user_query = """DELETE FROM users WHERE user_id = %s"""
        database_conn.delete_one(query=delete_user_query, values=[user_id.hex])
    except Exception as e:
        app_logger.error(f"failed to delete user: {user_id}", exc_info=e)
    return 

################################################## CRUD FOR WALLETS TABLE ####################################################

@app.get("/wallets")
def list_wallets() -> list:
    try:
        app_logger.info(f"listing all wallets")
        list_wallets_query = f""" SELECT * FROM wallets LIMIT 20; """
        wallets_list_data = database_conn.fetch_all(query=list_wallets_query)
        return wallets_list_data
    except Exception as e:
        app_logger.error("failed to get wallets list", exc_info=e)

@app.get("/wallets/{wallet_id}")
def get_wallet_details(wallet_id:UUID) -> dict:
    try:
        app_logger.info(f"get wallet details for wallet_id: {wallet_id}")
        get_wallet_query = f""" SELECT * FROM wallets WHERE wallet_id = %s;"""
        wallet_data = database_conn.fetch_one(query=get_wallet_query, values=[wallet_id.hex])
        return wallet_data
    except Exception as e:
        app_logger.error(f"failed to get wallet details for wallet_id: {wallet_id}", exc_info=e)

@app.post("/wallets")
def create_wallet(wallet:Wallet):
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
        database_conn.execute_transaction([create_wallet_query, update_user_query], wallet_model_dump)
    except Exception as e:
        app_logger.error(f"failed to create wallet: {wallet.name}", exc_info=e)

# @app.patch("/wallets/update")
# def modify_user(payload:dict)

@app.delete("/wallets/{wallet_id}")
def delete_wallet(wallet_id:UUID):
    try:
        app_logger.info(f"Deleting wallet with wallet_id: {wallet_id}")
        delete_wallet_query = """DELETE FROM wallets where wallet_id = %s;"""
        database_conn.delete_one(query=delete_wallet_query, values=[wallet_id.hex])
    except Exception as e:
        app_logger.error(f"failed to delete wallet: {wallet_id}", exc_info=e)

################################################## CRUD FOR TRANSACTIONS TABLE ####################################################
@app.get("/transactions")
def list_transactions() -> list:
    try:
        app_logger.info(f"listing all transactions")
        list_transactions_query = f""" SELECT transaction_id, user_id, wallet_id, transaction_amount FROM transactions LIMIT 20; """
        transactions_list_data = database_conn.fetch_all(query=list_transactions_query)
        return transactions_list_data
    except Exception as e:
        app_logger.error("failed to get transactions list", exc_info=e)

@app.get("/transactions/{transaction_id}")
def get_transaction_details(transaction_id:UUID) -> dict:
    try:
        app_logger.info(f"get transaction details for transaction_id: {transaction_id}")
        get_transaction_query = f""" SELECT * FROM transactions WHERE transaction_id = %s;"""
        transaction_data = database_conn.fetch_one(query=get_transaction_query, values=[transaction_id.hex])
        return transaction_data
    except Exception as e:
        app_logger.error(f"failed to get transaction details for transaction_id: {transaction_id}", exc_info=e)

@app.post("/transactions")
def create_transaction(transaction:Transaction):
    try:
        app_logger.info(f"creating a new transaction for user_id: {transaction.user_id}")
        transaction_model_dump = transaction.model_dump()
        app_logger.info(transaction_model_dump)         
        insert_transaction_table_query = """
            INSERT INTO transactions (transaction_id, user_id, wallet_id, transaction_amount,
                                            transaction_category, transaction_ts, wallet_type)
                VALUES (%(transaction_id)s, %(user_id)s, %(wallet_id)s, %(transaction_amount)s,
                            %(transaction_category)s, %(transaction_ts)s, %(wallet_type)s);
"""
        update_wallets_query = """
            UPDATE wallets
            SET consumed_balance = consumed_balance + %(transaction_amount)s
            WHERE wallet_id = %(wallet_id)s;
"""
        database_conn.execute_transaction([insert_transaction_table_query, update_wallets_query], transaction_model_dump)
    except Exception as e:
        app_logger.error(f"failed to create transaction for user_id: {transaction.user_id}", exc_info=e)

# You cannot update a transaction
# @app.patch("/transactions/update")
# def modify_user(payload:dict)

# you cannot delete a transaction until and unless a user is deleted
# @app.delete("/transactions/{transaction_id}")
# def delete_transaction(transaction_id:UUID):
#     try:
#         app_logger.info(f"Deleting transaction with transaction_id: {transaction_id}")
#         delete_transaction_query = """DELETE FROM transactions where transaction_id = %s;"""
#         database_conn.delete_one(query=delete_transaction_query, values=[transaction_id.hex])
#     except Exception as e:
#         app_logger.error(f"failed to delete transaction: {transaction_id}", exc_info=e)

################################################## CRUD FOR BUDGETS TABLE ####################################################
@app.get("/budgets")
def list_budgets() -> list:
    try:
        app_logger.info(f"listing all budgets")
        list_budgets_query = f""" SELECT * FROM budgets LIMIT 20; """
        budgets_list_data = database_conn.fetch_all(query=list_budgets_query)
        return budgets_list_data
    except Exception as e:
        app_logger.error("failed to get budgets list", exc_info=e)

@app.get("/budgets/{budget_id}")
def get_budget_details(budget_id:UUID) -> dict:
    try:
        app_logger.info(f"get budget details for budget_id: {budget_id}")
        get_budget_query = f""" SELECT * FROM budgets WHERE budget_id = %s;"""
        budget_data = database_conn.fetch_one(query=get_budget_query, values=[budget_id.hex])
        return budget_data
    except Exception as e:
        app_logger.error(f"failed to get budget details for budget_id: {budget_id}", exc_info=e)

@app.post("/budgets")
def create_budget(budget:Budget):
    try:
        app_logger.info(f"creating a new budget for user_id: {budget.user_id}")
        budget_model_dump = budget.model_dump()
        app_logger.info(budget_model_dump)
        create_budget_query = f"""INSERT INTO budgets (budget_id, user_id, wallet_id, created_ts, start_date,
                                                            end_date, budget_amount)
                                    VALUES (%(budget_id)s, %(user_id)s, %(wallet_id)s, %(created_ts)s,
                                                %(start_date)s, %(end_date)s, %(budget_amount)s);"""
        update_wallet_query  ="""
            UPDATE wallets
            SET allocated_balance = %(budget_amount)s
            WHERE wallet_id = %(wallet_id)s;
"""
        database_conn.execute_transaction([create_budget_query, update_wallet_query], budget_model_dump)
    except Exception as e:
        app_logger.error(f"failed to create budget for user_id: {budget.user_id}", exc_info=e)

# @app.patch("/budgets/update")
# def modify_user(payload:dict)

@app.delete("/budgets/{budget_id}")
def delete_budget(budget_id:UUID):
    try:
        app_logger.info(f"Deleting budget with budget_id: {budget_id}")
        delete_budget_query = """DELETE FROM budgets where budget_id = %s;"""
        database_conn.delete_one(query=delete_budget_query, values=[budget_id.hex])
    except Exception as e:
        app_logger.error(f"failed to delete budget: {budget_id}", exc_info=e)