# This application creates an SQL alchemy instance onto routes of FASTAPI 
# This application interacts with MYSQL server to ensure proper data management of financial transactions 

import shared_code.utils as tools
import shared_code.sql_alchemy_utils as sql_al_tools
from urllib.parse import quote_plus
from fastapi import FastAPI
import uvicorn
import json
import logging
import requests

# SQLALchemy Imports
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
# --------------------------------------- END IMPORTS ------------------------------------ #

# --------------------------------------- CUSTOM METHODS------------------------------------ #
sql_al_engine = tools.create_sql_alchemy_engine(db_server_connection_name='mysql+mysqlconnector://jimCramerFinance:%s@localhost/newFinMgmt' % quote_plus('fin@MGMT_wsb_2023'))
print(sql_al_engine)
sql_engine_for_pd = sql_al_engine.raw_connection()

# Map from the existing tables
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=sql_al_engine,reflect=True)
Main_finance = Base.classes.main_finance
Merchants = Base.classes.merchants 
Transaction_categories = Base.classes.transaction_categories

# Create the classes stemming from the table objects in MySQL 
session_creator = sessionmaker(bind=sql_al_engine)

# --------------------------------------- END CUSTOM METHODS ------------------------------------ #

# --------------------------------------- FASTAPI IMPLEMENTATION ------------------------------------ #
from pydantic import BaseModel


class CSVFiles(BaseModel):
    file_path: str

app = FastAPI()

# Get all the allowable transaction categories
@app.get('/allowable_transaction_categories')
async def get_all_allowable_transaction_categories():
    session_for_query_all_trans_cats = session_creator()
    all_transaction_categories = session_for_query_all_trans_cats.query(Transaction_categories).all()
    list_all_trans_cat_name = []
    for transaction_category_row in all_transaction_categories:
        list_all_trans_cat_name.append(transaction_category_row.category_name)
    return (list_all_trans_cat_name)

# Get all transactions from the database 
@app.get('/all_transactions')
async def get_all_transactions():
    all_transactions = sql_al_tools.get_all_transactions_from_main_finance(session_creator=session_creator,main_finance_class=Main_finance)
    return all_transactions

@app.post('/create_transactions_from_uploaded_files')
async def post_trasnactions_from_csvs(absolute_path_to_new_transactions:CSVFiles):
    # Pass the path to the helper method in utils
    df_of_all_trans = tools.load_csv_to_df(main_path=absolute_path_to_new_transactions.file_path,fType='.csv') 

    ## TODO: 06/20/2024 - need to ensure that the category can be populated to a file. Right now the category 
    # is blank, needs to be populated using rhe get all transactions method 
    # Get all transactions method was updated as shared, now needs to be used to filter the transactions and use the tensors to make 
    # the appropriate predictions about the category
    transactions = sql_al_tools.get_all_transactions_from_main_finance(session_creator=session_creator,main_finance_class=Main_finance)
    print(transactions)
    return df_of_all_trans.to_dict(orient='records')
# --------------------------------------- END FASTAPI IMPLEMENTATION ------------------------------------ #