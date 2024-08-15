# app.py

import sys
print(sys.path)

from pathlib import Path
import logging
from uuid import UUID
from logging.config import dictConfig

import requests
from fastapi import FastAPI

from models.user import User
from models.budget import Budget
from models.transaction import Transaction
from models.wallet import Wallet

from model.xyz import XYZ


from util.util import read_app_log_config_file
from database.database import Database

# initialize the logger
# filepath = Path(__file__).resolve()
# log_config_dict = read_app_log_config_file(filepath=filepath/'conf/app_log_connfig.yaml')
# logger = dictConfig(log_config_dict)
# app_logger = logging.getLogger("app")
# print(app_logger)

# initialize the app
app = FastAPI()

database = Database()
# Homepage
@app.get("/")
def root():
    return {"message":"Welcome to JAEBKATRA"}


@app.get("/users/{user_id}")
def get_user_details(user_id:UUID) -> User:
    
    return user_data