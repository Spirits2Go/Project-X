from data_access.data_base import init_db

# Path to your database file
db_path = 'data/database.db'

# Initialize the database, generate DDL, and populate with example data
init_db(db_path, create_ddl=True, generate_example_data=True, verbose=True)
