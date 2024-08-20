# app.py

import logging
from fastapi import FastAPI

from .routers import (users,
                      wallets,
                      budgets,
                      transactions)

from util.util import initialize_logger

# initialize the logger
initialize_logger()
app_logger = logging.getLogger("app")

# initialize the app
app = FastAPI()

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
