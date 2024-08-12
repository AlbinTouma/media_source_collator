from dotenv import dotenv_values
import pandas as pd
import psycopg2
from psycopg2.extensions import connection as Psycopg2Connection 
import streamlit as st
from db.queries import get_db_domains

def select_db(db_name: str):
    """Selects the correct .secrets file depending on the db selected"""    
    if db_name == "Source Metadata":
        secrets: dict = dotenv_values(".secrets_source_metadata")
    if db_name == "Articles":
        secrets: dict = dotenv_values(".secrets_articles")
    
    return secrets


def connect_to_db(db_name: str) -> Psycopg2Connection | Exception:
    """Connect to Postgres db. Returns conn or exception"""
    secrets = select_db(db_name)
    st.toast("Connecting to db")
    try:
        conn = psycopg2.connect(database = secrets["DATABASE"] , user = secrets['USERNAME'], host = secrets['HOST'], password = secrets['PASSWORD'], port = secrets['PORT'])
        return conn

    except Exception as e:
        st.write("⚠️WARNING", str(e)) 
        return e


def test_db_credentials(db_name) -> None:
    """Try to connect to db. Toasts success/warning if credentials provided are correct/incorrect.""" 
    secrets: dict = select_db(db_name)
    st.toast("Checking credentials")
    try:
        conn = psycopg2.connect(
            database = secrets['DATABASE'], 
            user = secrets['USERNAME'], 
            host = secrets['HOST'], 
            password = secrets['PASSWORD'], 
            port = secrets['PORT']
        )
        st.toast("✅ VALID CREDENTIALS")
        conn.close()
    except Exception as e:
        st.toast(f"ENSURE CREDENTIALS ARE VALID AND THAT VPN IS ON", icon="🚨")
        st.exception(e)
        st.warning("Have you checked your VPN and credentials?")


def db_get_country_domains(country: str) -> list[tuple] | Exception:
    """This fetches the domains from SourceMetadata table for a given country"""
    
    conn: Psycopg2Connection | Exception = connect_to_db(db_name="Source Metadata")
    if isinstance(conn, Psycopg2Connection):
        try:
            cur = conn.cursor()
            cur.execute(get_db_domains, (country,))
            sql_response = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]
            return pd.DataFrame(sql_response, columns=colnames)
        except Exception as e:
            st.warning(str(e))
            conn.rollback()
        finally:
            conn.close()

''''

The functions below would be part of looking at how many articles we're scraping per domain, how many articles have mentions and other aggregations.

To do these aggregations we: 
    1. Create a temporary table on a country in the articles with mentions table
    2 .Run aggregations against the temp table


def create_temporary_table(country_name: str, conn: Psycopg2Connection) -> None:
    cur = conn.cursor()
    try:
        st.toast("Fetching data please wait")
        cur.execute(temp_table, (country_name,))
        conn.commit()
        st.toast("Data inserted into temp table")
    except Exception as e:
        print("Error inserting into temp table", e)
        conn.rollback()
    finally:
        cur.close()

def vectorize_searchfield(conn: Psycopg2Connection) -> None:
    cur = conn.cursor()
    vectorize_query = """ALTER TABLE country_review ADD COLUMN search tsvector;
    UPDATE country_review SET search = to_tsvector(host)
    """
    try:
        cur.execute(vectorize_query)
        conn.commit()
        st.toast("Vectorized domains")
    except Exception as e:
        st.toast(f"Failed vectorising domains {e}")
        conn.rollback()

def query_for_mentions(conn: Psycopg2Connection) -> list[tuple]:

    st.toast("Querying data")

    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM country_review;")
        sql_response = cur.fetchall()
        return sql_response
    except Exception as e:
        return e
    finally:
        cur.close()

'''
