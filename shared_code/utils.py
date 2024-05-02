from sqlalchemy import create_engine
from sqlalchemy import engine

def create_sql_alchemy_engine(db_server_connection_name:str) -> engine: 
    '''Creates an sql alchemy engine to process transactions in python to db_server_connection_name \n
    Parameters: \n 
        - db_server_connection_name `str`: name of the server host with which to spin up engine \n \n 
    Returns: \n
        `engine`: SQLalchemy engine object initialized to the database server
    '''
    sql_alchemy_engine = create_engine(db_server_connection_name,echo=True)
    return sql_alchemy_engine