# app.py

import os
import logging
from fastapi import FastAPI
from psycopg.rows import dict_row
from fastapi.middleware.cors import CORSMiddleware


from .routers import (users,
                      wallets,
                      budgets,
                      transactions)

from util.util import initialize_logger
from .database.database import Database
from psycopg_pool import ConnectionPool

# initialize the logger
initialize_logger()

# initialize a database connection pool for the whole lifespan
# def init_database_conn(app: FastAPI):
#     db_conn = Database()
#     db_conn.pool_open()
#     yield
#     db_conn.pool_close()

app_logger = logging.getLogger("app")

# initialize the app
# app = FastAPI(lifespan=init_database_conn)
app = FastAPI()

# origins = [
#     "http://localhost",
#     "http://localhost:8080",
#     "http://localhost:8000",
#     "http://127.0.0.1:8000/"
# ]

# app.add_middleware(CORSMiddleware,
#                    allow_origins = origins,
#                    allow_credentials = True,
#                    allow_methods=["*"],
#                    allow_header = ["*"],
#                    )

app.include_router(users.router)
app.include_router(wallets.router)
app.include_router(budgets.router)
app.include_router(transactions.router)
# Homepage
@app.get("/")
def root():
    app_logger.info("homepage loaded")
    return {"message":"Welcome to JAEBKATRA"}


################################################## CRUD FOR USERS TABLE ####################################################



################################################## CRUD FOR WALLETS TABLE ####################################################



################################################## CRUD FOR TRANSACTIONS TABLE ####################################################


################################################## CRUD FOR BUDGETS TABLE ####################################################
