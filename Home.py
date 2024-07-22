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


There are two postgres databases in adverse media:

- **Source Metadata** contains all of the domains that we scrape. This is useful for finding the media sources covered by adverse media.
- **Articles** contains the articles that we scrape. 

Submit correct credentials if warning persists when VPN is on.
"""
form = st.form(key="db")
database_selector = form.radio("Which database would you like to add your credentials to?", options=["Source Metadata", "Articles"])
host = form.text_input(label="HOST")
port = form.text_input(label="PORT")
user_name = form.text_input(label="USERNAME")
password = form.text_input(label="PASSWORD", type="password")
submit_button = form.form_submit_button(label="Submit")
fields = [host, port, user_name, password]


if submit_button:
    if any(field == "" for field in fields):
        st.error("❌ Missing field!")
    else:
        if database_selector == "Source Metadata":
            with open(".secrets_source_metadata", "w") as secrets:
                secrets.write(
                        f'HOST="{host}"\nPORT="{port}"\nPASSWORD="{password}"\nUSERNAME="{user_name}"\nDATABASE="metadata"'
                )
                secrets.close()
                test_db_credentials(database_selector)
        if database_selector == "Articles":
            with open(".secrets_articles", "w") as secrets:
                secrets.write(
                        f'HOST="{host}"\nPORT="{port}"\nPASSWORD="{password}"\nUSERNAME="{user_name}"\nDATABASE="article_storage"'
                )
                secrets.close()
                test_db_credentials(database_selector)


