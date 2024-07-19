import streamlit as st
from psycopg2.extensions import connection 
from db.db import connect_to_db, create_temporary_table, query_for_mentions
from db.queries import get_db_domains 
from psycopg2.extensions import connection as Psycopg2Connection 
import pandas as pd

def db_get_country_domains(country: str) -> list[tuple] | Exception:
    conn: Psycopg2Connection | Exception = connect_to_db()
    if isinstance(conn, Psycopg2Connection):
        try:
            cur = conn.cursor()
            cur.execute(get_db_domains, (country,))
            sql_response = cur.fetchall()
            return sql_response
        except Exception as e:
            conn.rollback()
        finally:
            conn.close()


        

