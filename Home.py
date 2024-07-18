import streamlit as st
from db.db import test_db_credentials 
from psycopg2.extensions import connection as  Psycopg2Connection
import pandas as pd
from io import StringIO
from utils.main import check_articles


st.set_page_config(
        page_title="Home",
        page_icon="🔬"
)




st.title("Cartier")
st.header("Streamline country and quality reviews", divider="rainbow")

"""

Cartier streamlines coverage and quality assurance for adverse media. Use Cartier to build a master list of the media sources that exist in a country or to anlayse the quality of our adverse media sources in a country.
"""

st.subheader("Get started")
"""
Behind Cartier is the adverse media postgres database and ElasticSearch. 
In order to run Cartier, you must give Cartier your database credentials. Ask an engineer or your product manager for credentials.

🔑 **You only need to submit your credentials once.**


Please ensure your VPN is working. 

Submit correct credentials if warning persists when VPN is on.
"""

form = st.form(key="db")
host = form.text_input(label="HOST")
port = form.text_input(label="PORT")
user_name = form.text_input(label="USERNAME")
password = form.text_input(label="PASSWORD", type="password")
submit_button = form.form_submit_button(label="Submit")

if submit_button:
    with open(".secrets", "w") as secrets:
        secrets.write(
                f'HOST="{host}"\nPORT="{port}"\nPASSWORD="{password}"\nUSERNAME="{user_name}"'
        )
        test_db_credentials()


