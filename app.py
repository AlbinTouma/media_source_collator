import streamlit as st
from db.db import connect_to_db 
from psycopg2.extensions import connection
import pandas as pd
from io import StringIO


uploaded_file = st.file_uploader(label="Upload coverage sheet")

if st.button("Check for articles"):
    conn: connection | Exception = connect_to_db()

    if uploaded_file is None
        st.write("⚠️ Upload ayour research workbook")
        exit()

    uploaded_file = pd.read_excel(uploaded_file, sheet_name="main")


    if conn := connection:
        st.write("✅ - Connected to DB!")
        st.write(uploaded_file)
       
