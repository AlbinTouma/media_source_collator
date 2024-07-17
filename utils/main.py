import pandas as pd
import streamlit as st
from psycopg2.extensions import connection 
from db.db import create_temporary_table, query_for_mentions
import streamlit as st
import numpy as np
from ast import literal_eval


def country_code_validator(codes: pd.Series) -> str | None:
    
    flatten_list = [item for sublist in codes for item in sublist]
    cleaned_list = [code for code in flatten_list if pd.notna(code)]
    unique_codes = set(cleaned_list)
    if len(unique_codes) == 1:
        country_code = unique_codes.pop()
        return country_code.capitalize()
    else:
        return None


def check_articles(uploaded_file: pd.DataFrame, conn: connection | Exception):
    uploaded_file['country']: pd.Series[list] = uploaded_file['country'].apply(lambda x: literal_eval(x.replace('nan', 'None')))
    country_code: str | None = country_code_validator(uploaded_file['country'])
    
    if country_code is None:
        st.warning("Warning, more than one country code!")
   
    create_temporary_table("Ireland", conn)

    st.toast("Querying data")
    sql_result: list = query_for_mentions(conn)
    st.write(sql_result)

