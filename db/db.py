from dotenv import dotenv_values
import os
import psycopg2
import streamlit as st

secrets: dict = dotenv_values(".secrets")
def connect_to_db():
    try:
        conn = psycopg2.connect(database = "article_storage", user = secrets['USERNAME'], host = secrets['HOST'], password = secrets['PASSWORD'], port = secrets['PORT'])
        return conn
    except Exception as e:
        st.write("⚠️WARNING", str(e)) 
        return e
    

