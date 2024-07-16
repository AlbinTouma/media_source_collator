import streamlit as st
from db.db import connect_to_db 
from psycopg2.extensions import connection
import pandas as pd
from io import StringIO
from utils.main import check_articles

uploaded_file = st.file_uploader(label="Upload coverage sheet")

if st.button("Check for articles"):

    if uploaded_file is None:
        st.write("⚠️ UPLOAD YOUR WORKBOOK")
        exit()

    uploaded_file: pd.DataFrame = pd.read_excel(uploaded_file, sheet_name="main")
    conn: connection | Exception = connect_to_db()

    if conn := connection:
        st.write("✅ - Connected to DB!")
        temp_table = check_articles(uploaded_file, conn)
