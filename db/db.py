from dotenv import dotenv_values
import os
import psycopg2
from psycopg2.extensions import connection 
import streamlit as st

secrets: dict = dotenv_values(".secrets")

def connect_to_db() -> connection | Exception:
    try:
        conn = psycopg2.connect(database = "article_storage", user = secrets['USERNAME'], host = secrets['HOST'], password = secrets['PASSWORD'], port = secrets['PORT'])
        return conn
    except Exception as e:
        st.write("⚠️WARNING", str(e)) 
        return e

def create_temporary_table(country_code: str, conn: connection):
    cur = conn.cursor()
    try:
        cur.execute(queries_dict['temp_table'])
        conn.commit()
        print("Data inserted into temp table")
    except Exception as e:
        print("Error inserting into temp table", e)
        conn.rollback()
        return e
    finally:
        cur.close()

        
