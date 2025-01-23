import pandas as pd
import sqlalchemy as sqal
import logging
from datetime import datetime
from config import *

# Configure info logging
current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
logging_name = f'data/logs/data_ingestion_log_{current_datetime}.txt'
logging.basicConfig(filename=logging_name, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Extract data function
def read_csv_to_df(filepath):
    """Read a csv to a pandas Dataframe
    Parameters:
        filepath: str, relative path to the csv file
    Returns:
        df: pd.DataFrame
    """

    try:
        df = pd.read_csv(filepath)
        logging.info(f' Reading data from file: {filepath.split("/")[-1]}. Number of records: {len(df)}')
        logging.info(f'\n {df.head(5)}')
        return df
    except Exception as e:
        logging.error(f'\n  Error extracting data from CSV: \n{e}', exc_info=False)
        raise e
    
# Validate csv data
def summarize(df, df_name='table'):
    """Simple summary the given DataFrame.
    Parameters:
        df: pd.DataFrame, raw df to analyse
        df_name: str, name of df
        n_rows_to_show: int, number of rows to show 
    """

    logging.info(f"=====Summary of {df_name}=====")
    logging.info(f" Shape: {df.shape}")
    
    nan_ratio = pd.isna(df).sum() / len(df) * 100
    nan_ratio.sort_values(ascending=False, inplace=True)
    nan_ratio = nan_ratio.to_frame(name='NaN Ratio').T
    logging.info(f'\n{nan_ratio}')
    duplicate_count = df.duplicated().sum()
    logging.info(f'Number of duplicate records: {duplicate_count}')

# Connect to mysql db
def connect_to_mysql(conn_string):
    """ Connect to mysql database check tables inside
    Parameters:
        conn_string = str, mysql connection string of the db
    Returns:
        engine: sqlalchemy.engine, engine of the mysql db
    """
    try:
        # create the engine object
        engine = sqal.create_engine(conn_string)
        # Check the connection by reading the tables in the database
        metadata = sqal.MetaData()
        metadata.reflect(engine)
        for table_name, table in metadata.tables.items():
            logging.info(f"Table in database: {table_name}")
            for column in table.columns:
                logging.info(f" - Column: {column.name}, Type: {column.type}")      
        # Check examples table
        examples_table = metadata.tables['examples']
        with engine.connect() as connection:
            rows = connection.execute(sqal.sql.select(examples_table)).fetchall()
            logging.info(f' Printing table examples:')
            for row in rows:
                logging.info(f' {row}')
        return engine
    
    except Exception as e:
        logging.error(f'\nError during mysql connection: \n{e}', exc_info=False)
        raise e

# Ingest DF to mysql
def ingest_df_to_mysql(df, table_name, engine):
    """Ingest DF to mysql table
    Parameters:
        df: pd.DataFrame, raw df to upload
        table_name: str, name of the table to insert
        engine: sqlalchemy.engine, engine of the mysql database
    """

    try:
        df.to_sql(table_name, con=engine, if_exists='append', index=False) # Not working, dont kow why
        # Log success message
        logging.info(f"""\nData ingestion successful for table: {table_name}. Number of records inserted: {len(df)}""")
    except Exception as e:
        logging.error(f'\nError during ingestion of df: \n{e}', exc_info=True)
        raise e

# Validate ingested data
def validate_mysql_data(table_name, engine):
    """Read from mysql db and validate data
    Parameters: 
        table_name: str, name of the mysql table
        engine: sqlalchemy.engine, engine of the mysql database
    """
    try:
        logging.info(f' Validating data in table: {table_name}')
        # Checking for NULL values
        query = f"""SELECT * FROM {table_name}"""
        df = pd.read_sql_query(query, engine)
        summarize(df, table_name)
    except Exception as e:
        logging.error(f'\nError during validation of mysql data: \n{e}', exc_info=False)
        raise e

def pipeline(filepath, table_name, conn_string):
    """
    Pipeline that executes the ingestion, trasformation and loading to database
    """
    df_test = read_csv_to_df(filepath)
    summarize(df_test, table_name)
    engine = connect_to_mysql(conn_string)
    ingest_df_to_mysql(df_test, table_name, engine)
    validate_mysql_data(table_name, engine)

if __name__ == "__main__":
    pipeline(filepath, table_name, conn_string)
