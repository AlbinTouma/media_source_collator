import streamlit as st
import pycountry


st.set_page_config(
        page_title="Coverage research",
        page_icon="🔬"
)


st.title("Country Reviews")


st.header("Set up Research Sheet", divider="rainbow")


option = st.selectbox(label="Country", options=pycountry.countries, index=None, placeholder="Select Country for Review")



st.header("Extract Data", divider="rainbow")

st.subheader("Extact Comply data")
