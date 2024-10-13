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

# initialize the logger
initialize_logger()

app_logger = logging.getLogger("app")


# initialize the app
# app = FastAPI(lifespan=db_pool_lifespan)
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
