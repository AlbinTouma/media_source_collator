import streamlit as st
from db.db import connect_to_db, create_temporary_table, query_for_mentions 
from psycopg2.extensions import connection as  Psycopg2Connection
import pandas as pd
from io import StringIO
from utils.main import check_articles

uploaded_file = st.file_uploader(label="Upload coverage sheet")

if st.button("Check for articles"):

    if uploaded_file is None:
        st.write("⚠️ UPLOAD YOUR WORKBOOK")
        exit()

    uploaded_file: pd.DataFrame = pd.read_excel(uploaded_file, sheet_name="main")
    conn: Psycopg2Connection | Exception = connect_to_db()

    if isinstance(conn, Psycopg2Connection):
        create_temporary_table("Ireland", conn)
        sql_result: list[tuple] = query_for_mentions(conn)
        st.write(sql_result)
        conn.close()
