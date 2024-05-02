# This application creates an SQL alchemy instance onto routes of FASTAPI 
# This application interacts with MYSQL server to ensure proper data management of financial transactions 

from shared_code.utils import create_sql_alchemy_engine
from urllib.parse import quote_plus
from fastapi import FastAPI
import uvicorn
import json

# SQLALchemy Imports
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
# --------------------------------------- END IMPORTS ------------------------------------ #

# --------------------------------------- CUSTOM METHODS------------------------------------ #
sql_al_engine = create_sql_alchemy_engine(db_server_connection_name='mysql+mysqlconnector://jimCramerFinance:%s@localhost/newFinMgmt' % quote_plus('fin@MGMT_wsb_2023'))
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
app = FastAPI()

@app.get('/allowable_transaction_categories')
async def test_method():
    session_for_query_all_trans_cats = session_creator()
    all_transaction_categories = session_for_query_all_trans_cats.query(Transaction_categories).all()
    list_all_trans_cat_name = []
    for transaction_category_row in all_transaction_categories:
        list_all_trans_cat_name.append(transaction_category_row.category_name)
    return (list_all_trans_cat_name)
# Test an endpoint to return a record by a name
# --------------------------------------- END FASTAPI IMPLEMENTATION ------------------------------------ #