import pandas as pd
import sqlite3
import os

def csv_to_sqlite(csv_path, db_path=None, table_name=None):
    base_name = os.path.splitext(os.path.basename(csv_path))[0]
    db_path = db_path or f"{base_name}.db"
    table_name = table_name or base_name

    df = pd.read_csv(csv_path)
    connection = sqlite3.connect(db_path)
    df.to_sql(table_name, connection, if_exists='replace', index=False)

    return connection, table_name

if __name__ == "__main__":
    db_name = input("csv name: ")
    connection, table_name = csv_to_sqlite(db_name)

    # test_df = pd.read_sql("SELECT * FROM {} LIMIT 5".format(table_name), connection)
    # print(test_df)
    connection.close()