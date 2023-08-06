import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.sql import text


def query(sql, connection_string):
    engine = create_engine(connection_string)
    s = text(sql)
    with engine.connect() as conn:
        result = conn.execute(s)
    df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df


def insert_update(sql, data, connection_string):
    sql_data = data.to_dict(orient='records')
    engine = create_engine(connection_string)
    s = text(sql)
    with engine.connect() as conn:
        try:
            conn.execute(s, sql_data)
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
