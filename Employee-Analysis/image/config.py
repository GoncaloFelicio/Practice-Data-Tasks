# Configuration file for the user to costumize the ETL ingestion process


# The relative path to the csv to read: examples.csv
filepath = './data/example.csv'
# Connection string to the mysql database
conn_string = 'mysql://codetest:swordfish@database/codetest' # changed previous localhost:3306 to database to match the docker env
# Table name in the mysql database to ingest data into
table_name = 'examples'