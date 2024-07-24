import streamlit as st
import pycountry
from utils.country_review import db_get_country_domains, excel_writer, init_workbook, collate_sources 
import pandas as pd
from io import BytesIO
from utils.db_pedia import get_db_data

st.set_page_config(
        page_title="Coverage research",
        page_icon="🔬"
)

# Initialise workbook in session memory
if "workbook" not in st.session_state:
    st.session_state.workbook = init_workbook()


st.title("Country Reviews")
st.header("Get started", divider="rainbow")


countries = [i.name for i in pycountry.countries]

with st.form("init_research"):
    country_selectbox = st.selectbox(label="Select country to research", options=countries, index=None, placeholder="Select Country for Review")
    uploaded_file = st.file_uploader("Upload existing research sheet", type=['xlsx'])
    st.subheader("Create or upload workbook")
    create_worksheet_btn = st.form_submit_button("Create workbook", use_container_width=True)
            
# Create worksheet
if create_worksheet_btn:
    if uploaded_file is None:
        if country_selectbox is None:
            st.toast("Select country")
            st.stop()
        workbook: BytesIO = init_workbook()
        st.session_state.workbook = workbook
        st.toast("Workbook created")
    else:
            st.session_state.workbook = init_workbook(uploaded_file)
            st.toast("Workbook uploaded successfully")


st.header("Get data", divider="rainbow")
st.subheader("Comply") 

with st.form("Comply Advantage"):
    query_comply_btn = st.form_submit_button(label="Populate Comply worksheet")
    
st.subheader("Wikipedia") 
with st.form("DbPedia"):
    dbPedia_lang = st.radio("Language", ["English", "French"], horizontal=True)
    dbPedia_query = st.text_input(label="Name of wikipedia page")
    dbPedia_btn = st.form_submit_button(label="Populate Wikipedia worksheet")


if query_comply_btn:
    if country_selectbox is None:
        st.toast("⚠️ Select Country!")
        st.stop()
    country_code = pycountry.countries.get(name=country_selectbox).alpha_2 
    sql_response_country: pd.DataFrame = db_get_country_domains(country_code)
    st.write(sql_response_country)
    st.session_state.workbook = excel_writer(workbook_stream=st.session_state.workbook, sheet_name="comply", df=sql_response_country)
    st.toast("Successfully loaded comply data")

if dbPedia_btn:
    match dbPedia_lang:
        case "English":
            yaml_file = "en.yml"
            endpoint = "https://dbpedia.org/sparql"
            lng = "@en"
        case "French":
            yaml_file = "fr.yml"
            lng = "@fr"

    dbPedia_response: pd.DataFrame | None = get_db_data(yaml_file, dbPedia_query, lng, endpoint)
    if dbPedia_response.empty:
        st.stop()
    
    st.session_state.workbook = excel_writer(workbook_stream=st.session_state.workbook, sheet_name="wikipedia", df=dbPedia_response)
    st.dataframe(dbPedia_response)

st.header("Matching", divider="rainbow")
st.markdown("""

### Steps

We need to validate the data in our worksheets before collating them into a master list. This part of the process requires that you label your media sources and clean your worksheets by making sure that each media sources has a name.

### Checklist

""")

st.checkbox("Ensure that every newspaper has a name. We collate media sources into one list by matching sources by their names. ")
st.checkbox("Label sources using the Adverse Media Taxonomy")


match_btn = st.button(label="Create source of truth", use_container_width=True)

st.write("Download your research sheet")

if match_btn:
    master_sheet: pd.DataFrame | None = collate_sources(st.session_state.workbook)
    if master_sheet.empty:
        st.stop()
    st.session_state.workbook = excel_writer(workbook_stream=st.session_state.workbook, sheet_name="main", df=master_sheet)




st.download_button(
        label="Download research sheet", 
        data=st.session_state.workbook, 
        file_name=f"AM Coverage in {country_selectbox}.xlsx", 
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        use_container_width=True,
    )


