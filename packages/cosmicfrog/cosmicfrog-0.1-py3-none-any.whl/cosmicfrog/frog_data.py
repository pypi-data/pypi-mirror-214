import json
import numpy as np
import os
import pandas as pd
import sqlalchemy
import pkg_resources
import uuid

from psycopg2 import sql
from sqlalchemy import text
from sqlalchemy.engine import Engine
from io import StringIO 
from typing import Type
from collections.abc import Iterable

from .frog_log import get_logger

# TODO: Long term aim : Head this to a library, can be re-used for various projects (e.g. tadpole, io, scenario gen)

# Questions: 
# More useful to validate table names against anura, or allow to work for all tables?
# How much parallelisation to do on upsert, particularly for xls?
# Currently put some batching where possible on file read, for mem  overhead.. may
# also need to look at batch inside writes, to allow feedback to UI
# test files with bad column names - missing, or sql injection 


# Define chunk size (number of rows to write per chunk)
UPSERT_CHUNK_SIZE = 100000

MASTER_LIST_PATH = 'anura/table_masterlists/anuraMasterTableList.json'
TABLES_DIR = 'anura/table_definitions'

class ValidationError(Exception):
    """Exception raised for validation errors.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class frog_model:

    tables = []
    table_keys = {}

    @classmethod
    def _read_anura(cls: Type['frog_model']):
        frog_model._read_tables()
        frog_model._read_pk_columns()

        print(frog_model.table_keys['facilities'])
        
    
    @classmethod
    def _read_tables(cls: Type['frog_model']):

        file_path = pkg_resources.resource_filename(__name__, MASTER_LIST_PATH)
        
        with open(file_path, 'r') as file:
            data = json.load(file)
            frog_model.tables = [item["Table"].lower() for item in data]


    @classmethod 
    def _read_pk_columns(cls: Type['frog_model']):

        file_path = pkg_resources.resource_filename(__name__, TABLES_DIR)

        # Iterate over each file in the directory
        for filename in os.listdir(file_path):

            filepath = os.path.join(file_path, filename)

            with open(filepath, 'r') as f:
                data = json.load(f)
                
            table_name = data.get("TableName").lower()
            
            # Extract the column names where "PK" is "Yes"
            pk_columns = [field["Column Name"].lower() for field in data.get("fields", []) if field.get("PK") == "Yes"]
            
            frog_model.table_keys[table_name] = pk_columns


    def __init__(self) -> None:

        # One time read in of Anura data
        if not frog_model.tables:
            frog_model._read_anura()

        self.engine = None
        self.connection = None
        self.transaction = None
        self.log = get_logger()

    
    def db_connect_eng(self, engine: Engine):
        try:
            self.engine = engine
            self.connection = self.engine.connect()
            
        except Exception as e:
            self.log.error(f"An exception occurred: {e}")
            return False

        return True

    def db_connect(self, connection_string: str):

        try:
            self.engine = sqlalchemy.create_engine(connection_string, connect_args={'connect_timeout': 15}) 
            self.connection = self.engine.connect()
            
        except Exception as e:
            self.log.error(f"An exception occurred: {e}")
            return False

        return True

    def start_transaction(self):
        assert(self.connection is not None)
        self.transaction = self.connection.begin()

    def commit_transaction(self):
        self.transaction.commit()
        self.transaction = None

    def rollback_transaction(self):
        self.transaction.rollback()
        self.transaction = None


    def write_table(self, table_name: str, data: pd.DataFrame | Iterable):
        
        self.log.info("Writing table: " + table_name)

        if isinstance(data, pd.DataFrame) == False:
            data = pd.DataFrame(data)

        # Initial implementation - pull everything into a df and dump with to_sql
        data.to_sql(table_name, con=self.engine, if_exists="append", index=False)

        # Note: tried a couple of ways to dump the generator rows directly, but didn't
        # give significant performance over dataframe (though may be better for memory)
        # Decided to leave as is for now 


    def read_table(self, table_name: str):
        return pd.read_sql(table_name, self.engine)

    def clear_table(self, table):

        assert(self.connection is not None)

        # delete any existing data data from the table
        self.connection.execute(text("delete from " + table))

        return True

    def exec_sql(self, sql: str):

        assert(self.connection is not None)

        self.connection.execute(text(sql))

    def get_dataframe(self, sql: str):

        return pd.read_sql_query(sql, self.engine)

    # Upsert from a file
    def upsert_csv(self, table_name: str, filename: str):

        for chunk in pd.read_csv(filename, chunksize=UPSERT_CHUNK_SIZE, dtype=str, skipinitialspace=True):
            chunk.columns = chunk.columns.str.strip()
            chunk.replace("", np.nan, inplace=True)
            self.upsert(table_name, chunk)

    # Upsert from an xls
    def upsert_excel(self, filename: str):

        # TODO: If an issue could consider another way to load/stream from xlsx maybe?

        xls = pd.ExcelFile(filename)

        # For each sheet in the file
        for sheet_name in xls.sheet_names:

            # read the entire sheet into a DataFrame
            df = pd.read_excel(xls, sheet_name=sheet_name, dtype=str)

            df.columns = df.columns.str.strip()

            for i in range(0, len(df), UPSERT_CHUNK_SIZE):
                chunk = df[i:i+UPSERT_CHUNK_SIZE]
                chunk.replace("", np.nan, inplace=True)
                self.upsert(sheet_name, chunk)

    # Upsert from a dataframe
    def upsert(self, table_name: str, data: pd.DataFrame | Iterable):

        # TODO: Not sure what validation to do here
        # TODO: Anura only, or custom tables?  (can pass in keys for those)
        # TODO: Custom columns and how to handle
        # TODO: up front validation, what are the rules?

        assert(table_name in frog_model.tables)
        
        key_columns = frog_model.table_keys[table_name]
        non_key_columns = [col for col in data.columns if col not in key_columns]
        all_columns = key_columns + non_key_columns
        
        print("Using key columns:")
        print(key_columns)

        assert(self.connection is not None)

        temp_table_name = "temp_table_" + str(uuid.uuid4()).replace('-', '')

        with self.engine.begin() as connection:
        
            # Create temporary table
            # Note: this will also clone custom columns
            create_temp_table_sql = text(f"""
                CREATE TEMPORARY TABLE {temp_table_name} AS
                SELECT *
                FROM {table_name}
                WITH NO DATA;
                """)
            
            connection.execute(create_temp_table_sql)

            # Copy data from df to temporary table
            copy_sql = sql.SQL("COPY {table} ({fields}) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)").format(
                table=sql.Identifier(temp_table_name),
                fields=sql.SQL(', ').join(map(sql.Identifier, data.columns))
            )

            cursor = connection.connection.cursor()
            cursor.copy_expert(copy_sql, StringIO(data.to_csv(index=False)))
            del data

            # Now upsert from temporary table to final table

            # Note: Looked at ON CONFLICT for upsert here, but seems not possible without defining constraints on target table
            # so doing insert and update separately

            # Note: For SQL injection, columns here are from Anura, also target table name. Temp table name is above.
            # non_key_columns are vulnerable (from import) so protected

            # Do not trust column names from user:
            safe_all_columns_list = sql.SQL(", ").join([sql.Identifier(col_name) for col_name in all_columns])
            safe_update_column_clause = sql.SQL(", ").join([sql.SQL('{0} = {1}.{0}').format(sql.Identifier(col_name), sql.Identifier(temp_table_name)) for col_name in non_key_columns])

            if key_columns:

                key_condition = " AND ".join([f"{table_name}.{key_col} = {temp_table_name}.{key_col}" for key_col in key_columns])

                print("keycondition:")
                print(key_condition)

                placeholder = "{0}"

                update_query = sql.SQL(f"""
                    UPDATE {table_name}
                    SET {placeholder}
                    FROM {temp_table_name}
                    WHERE {key_condition}
                """).format(safe_update_column_clause)

                insert_query = sql.SQL(f"""
                    INSERT INTO {table_name} ({placeholder})
                    SELECT {placeholder} FROM {temp_table_name}
                    WHERE NOT EXISTS (
                        SELECT 1 FROM {table_name}
                        WHERE {key_condition}
                    )
                """).format(safe_all_columns_list)
                
                cursor.execute(update_query)
                updated_rows = cursor.rowcount

                cursor.execute(insert_query)
                inserted_rows = cursor.rowcount 

            else:
                insert_query = sql.SQL(f"""
                    INSERT INTO {table_name} ({placeholder})
                    SELECT {placeholder} FROM {temp_table_name}
                """).format(safe_all_columns_list)
                
                updated_rows = 0
                cursor.execute(insert_query)
                inserted_rows = cursor.rowcount 
                
                print()  # prints number of inserted rows
                connection.execute(insert_query)

        print("Updated rows  = {}".format(updated_rows))
        print("Inserted rows = {}".format(inserted_rows))