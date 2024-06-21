# SQLALchemy Imports
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


def get_all_transactions_from_main_finance(session_creator:sessionmaker[Session],main_finance_class):
    '''
    Get all transactions from main finance tables via SQL alchemy in the pfi database. \n 
    Parameters: \n 
        - session_creator `sessionmaker[Session]`: sql-alchemy based session object against the database with which to spin up a session 
        used for querying \n 
        - main_finance_class `Any`: class object associated with the main finance table \n 
    Returns: \n 
        - all_transactions `List`: List object of all results from the main finance query 
    '''
    session_for_query_all_transactions = session_creator()
    all_transactions = session_for_query_all_transactions.query(main_finance_class).all()
    return all_transactions