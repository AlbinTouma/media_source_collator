from dotenv import dotenv_values
import os
import psycopg2
from psycopg2.extensions import connection as Psycopg2Connection 
import streamlit as st
from db.queries import temp_table
from dataclasses import dataclass, asdict

secrets: dict = dotenv_values(".secrets")

@dataclass
class ArticleData:
    uuid: str
    source_name: str
    url: str
    host: str 
    country: str 
    article_created_datetime: str
    collection_datetime: str 
    publish_datetime: str



def connect_to_db() -> Psycopg2Connection | Exception:
    st.toast("Connecting to db")
    try:
        conn = psycopg2.connect(database = "article_storage", user = secrets['USERNAME'], host = secrets['HOST'], password = secrets['PASSWORD'], port = secrets['PORT'])
        return conn

    except Exception as e:
        st.write("⚠️WARNING", str(e)) 
        return e


def test_db_credentials() -> None:
    st.toast("Checking credentials")
    try:
        with psycopg2.connect(
            database = "article_storage", 
            user = secrets['USERNAME'], 
            host = secrets['HOST'], 
            password = secrets['PASSWORD'], 
            port = secrets['PORT']
        ) as conn:
            st.success("VALID")
    except Exception as e:
        st.warning(f"ENSURE CREDENTIALS ARE VALID AND THAT VPN IS ON", icon="🚨")

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

def find_domain(domain: str, conn: Psycopg2Connection) -> list[tuple]:
    pass



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
