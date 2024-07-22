import streamlit as st
import pycountry
from utils.country_review import db_get_country_domains
import pandas as pd

st.set_page_config(
        page_title="Coverage research",
        page_icon="🔬"
)


st.title("Country Reviews")
st.header("Set up Your Research Sheet", divider="rainbow")

st.subheader("Select Country for Review")
countries = []
for i in pycountry.countries:
    countries.append(i.name)

selected_country = st.selectbox(label="Select country", options=countries, index=None, placeholder="Select Country for Review")

st.subheader("Extract Comply Data")
st.write("Extract domains from Comply Advantage db")
query_comply_country = st.button(label="Get domains")

if query_comply_country:
    country_data: list[tuple] = db_get_country_domains(selected_country)
    st.write(country_data)
