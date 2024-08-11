# HELP!!

Use our Help file if you want to troubleshoot your issue or know more about the functions and workflow powering Cartier. In addition to common human errors, the troubleshooting list includes scenarios that may happen if our db changes or if DBPeida changes something on their server. DBPeida is not in your control. What you can do here is simply update mappings and ensure endpoints are correct. 

<b> Likely problems and troubleshooting<b>

<dl>
<dt><b>Credentials aren't working</b></dt>
<dd>1. You've put in the wrong credentials. Cartier will try to connect and ask you for credentials again</dd>
<dd>2. You've previously saved the correct credentials but now, your database credentials have changed by your db administrator. Please update your credentials. Ask a PM or engineer for new credentials. </dd>
<dt><b>Creating a workbook!</b></dt>
<dd>1. If you want to create a workbook from scratch, please select a country for review and press create workbook button</dd>
<dd>2. If you are uploading a workbook please make sure you press create workbook after uploading the file. Streamlit still requiers this.</dd>

<dt><b>Getting domains from Comply's table isn't working</b></dt>
<dd>1. The database table has been altered. To fix this, please update the SQL query inside queries.py to ensure that you're querying the right column names.</dd>

<dt><b>Scraping Wikipedia isn't working!</b></dt>
<dd>1. DBPedia failed to return data! Please make sure that you copied the name of the wikipedia page and not the url. Keep in mind that red hyperlinks are empty page and will only return the name of the link. Also remember that DBPedia is poorly organised structured data. What's on Wikipedia page may not be on DBPedia leading to unclean and sometimes patchy results. Try with the text input "List of newspapers in the United Kingdom"</dd>
<dd>2. It may be that DBPedia change endpoint or mappings in the future. This is unlikely. If it does happen or if you want to scrape an endpoint in a language other than English or French, please update endpoints and yml mappings to reflect any changes on DBPedia or to add language pages.</dd>

<dt><b>I can't collate my worksheets into a master list</b></dt>
<dd>
   1. Collation only fails if any of your worksheets in your workbook is missing a value in the name field. We match sources by grouping the sources by their names. 
</dd>
</dl>


----
The rest of HELP walks you through functions associated with each step, from adding your secrets for authentication to getting comply and dbpedia data, downloading your workbook and then uploading your workbook again for collation and ultimately download again.

## Secrets & Authentication

At the Home page, Users are promted by a form to input credentials to access Source Metadata and Articles tables in our Postgres database.

Credentials are written to their respective files

1. ``.secrets_source_metadata``
2. ``.secrets_articles``

Upon submitting the form, we make sure that credentials are not blank and that they work. To test that credentials are correct, we call ``test_db_credentials()`` and pass which database a user wants to test to the function (Source Metadata or Articles).


```python
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
```

The test_db_credentials function lives in our db module. It simply tries to connect and registers success/failure of the connection.



```python
def test_db_credentials(db_name) -> None:
    """Try to connect to db. Toasts success/warning if credentials provided are correct/incorrect.""" 
    secrets: dict = select_db(db_name)
    st.toast("Checking credentials")
    try:
        conn = psycopg2.connect(
            database = secrets['DATABASE'], 
            user = secrets['USERNAME'], 
            host = secrets['HOST'], 
            password = secrets['PASSWORD'], 
            port = secrets['PORT']
        )
        st.toast("✅ VALID CREDENTIALS")
        conn.close()
    except Exception as e:
        st.toast(f"ENSURE CREDENTIALS ARE VALID AND THAT VPN IS ON", icon="🚨")
        st.exception(e)
        st.warning("Have you checked your VPN and credentials?")


```

## Country Reviews

### Session state

When a user enters the country review page, they are met with the option to upload or create a workbook. For the user to manipulate the workbook in session, we save the file to session state.

> If there's an error with the workbook it is likely due to cache. Clear cache and refresh your page.



```python
# Initialise workbook in session memory
if "workbook" not in st.session_state:
    st.session_state.workbook = init_workbook()
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    Cell In[9], line 3
          1 # Initialise workbook in session memory
          2 if "workbook" not in st.session_state:
    ----> 3     st.session_state.workbook = init_workbook()


    NameError: name 'init_workbook' is not defined



### Countries

Users need to select a country they want to query. The country selected will be the name of their workbook ie ``"AM in xxx"``. The country selected is also the code sent to query the database.

We use ``pycountry.countries`` to get the name and iso-2 code of the country that user wants to investigate.

> If there's an error in fetching data it might be because we don't have the country in our db or we are not using the iso-2 code (this scenario is only likely if the country is disputed like Kosovo.)


```python
#Extract name from pycountry
countries = [i.name for i in pycountry.countries]
with st.form("init_research"):
    country_selectbox = st.selectbox(label="Select country to research", options=countries, index=None, placeholder="Select Country for Review")
    uploaded_file = st.file_uploader("Upload existing research sheet", type=['xlsx'])
    st.subheader("Create or upload workbook")
    create_worksheet_btn = st.form_submit_button("Create workbook", use_container_width=True)

if create_worksheet_btn:

    # If user is not uploading a file and wants to create one, we run init_workbook()
    if uploaded_file is None:
        if country_selectbox is None:
            st.toast("Select country")
            st.stop()
        ## Create workbook by calling init_workbook from the country_review module and save the workbook as a BytesIO object to current session.
        workbook: BytesIO = init_workbook()
        st.session_state.workbook = workbook
        st.toast("Workbook created")

    #If User has uploaded a file, pass the file to init_workbook() and save the BytesIO object to session state
    else:
            st.session_state.workbook = init_workbook(uploaded_file)
            st.toast("Workbook uploaded successfully")


```

## Create Workbook

We create a workbook with the ``init_workbook()`` command.



```python
def init_workbook(file=None) -> BytesIO:
    if file:
        #If we upload a file read and return the file as BytesIO
        return BytesIO(file.read())
    else:
        # If we need to create a file, create a workbook.
        wb = openpyxl.Workbook()

        # Opynpyxl always creates a default sheet. We don't want "Sheet" because it adds tabs to our workbook and causes empty sheet errors when writing to the file.
        # To only have relevant sheets, set Openpyxl's default Sheet as comply so we can overwrite this and avoid empty sheet errors.
        for w in wb.worksheets:
            w.title = "comply"

        stream = BytesIO()
        wb.save(stream)

        stream.seek(0)
        return stream
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    Cell In[11], line 1
    ----> 1 def init_workbook(file=None) -> BytesIO:
          2     if file:
          3         #If we upload a file read and return the file as BytesIO
          4         return BytesIO(file.read())


    NameError: name 'BytesIO' is not defined


## Get Data

We're back in the Country Review page. After you create your workbook, you'll want to get relevant data. 
The Comply Advantage button and the Wikipedia button fetch data on newspapers and domains.


```python

with st.form("Comply Advantage"):
    query_comply_btn = st.form_submit_button(label="Populate Comply worksheet")
    
st.subheader("Wikipedia") 
with st.form("DbPedia"):
    dbPedia_lang = st.radio("Language", ["English", "French"], horizontal=True)
    dbPedia_query = st.text_input(label="Name of wikipedia page")
    dbPedia_btn = st.form_submit_button(label="Populate Wikipedia worksheet")



```

### Comply

The Comply button requires that you select the country that you want to review or else an error is thrown.

#### Convert Country name to Country Code

Our Source Metadata Table lists countries in the ``ISO-2 code`` so our first step is to use the name of the country that the user selected and fetch the relevant ISO to code. Fortunately, the pycountry module comes with a ``get`` method for looking up country codes based on country name.



```python
country_code = pycountry.countries.get(name=country_selectbox).alpha_2 
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    Cell In[14], line 1
    ----> 1 country_code = pycountry.countries.get(name=country_selectbox).alpha_2 


    NameError: name 'pycountry' is not defined


#### Query Source Metadata Table

Now that we have the ISO code that our Source Metadata Table requires in order to filter domains by country, we'll call the ``db_get_country_domains(country_code)`` and pass our ISO-2 code to the function.

The result of the query is stored in a pd.DataFrame which is passed to our ``excel_writer`` function which we use to write the result to our workbook.

> Query will fail if you provide an invalid country code or fail to connect to the db because you don't have a VPN on or because credentials are not up to date.




```python
# If user queries comply, we convert name of country to iso-2 code, pass code to db query and write results from dataframe to our file.
if query_comply_btn:
    if country_selectbox is None:
        st.toast("⚠️ Select Country!")
        st.stop()
    country_code = pycountry.countries.get(name=country_selectbox).alpha_2 
    sql_response_country: pd.DataFrame = db_get_country_domains(country_code)
    st.write(sql_response_country)
    st.session_state.workbook = excel_writer(workbook_stream=st.session_state.workbook, sheet_name="comply", df=sql_response_country)
    st.toast("Successfully loaded comply data")


```

The ``db_get_country_domains(country_code)`` exists inside the utils module and country_reviews.py


```python
def db_get_country_domains(country: str) -> list[tuple] | Exception:
    conn: Psycopg2Connection | Exception = connect_to_db(db_name="Source Metadata")
    if isinstance(conn, Psycopg2Connection):
        try:
            cur = conn.cursor()
            cur.execute(get_db_domains, (country,))
            sql_response = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]
            return pd.DataFrame(sql_response, columns=colnames)
        except Exception as e:
            st.warning(str(e))
            conn.rollback()
        finally:
            conn.close()
```

The function creates a session by calling the ``connect_to_db`` from our db module (db.py file) and executes the ``get_db_domains`` query inside the queries.py


```python
def connect_to_db(db_name: str) -> Psycopg2Connection | Exception:
    secrets = select_db(db_name)
    st.toast("Connecting to db")
    try:
        conn = psycopg2.connect(database = secrets["DATABASE"] , user = secrets['USERNAME'], host = secrets['HOST'], password = secrets['PASSWORD'], port = secrets['PORT'])
        return conn

    except Exception as e:
        st.write("⚠️WARNING", str(e)) 
        return e


```


```python
get_db_domains = f"""
    SELECT * FROM website WHERE country = %s;
"""
```

#### Write to Workbook

Whenever we fetch data, we pass the data to the ``excel_writer`` function. This function writes dataframes to sheet and requires the name of the worksheet, the dataframe, and the workbook from streamlit session (as BytesIO). 

After we recieve the data from Source Metadata, we pass the dataframe to the ``excel_writer.``


```python
def excel_writer(
    workbook_stream: BytesIO, sheet_name: str, df: pd.DataFrame
) -> BytesIO:

    #Excel doesn't accept NaN so replacing with None
    df = df.where(pd.notnull(df), "")

    workbook_stream.seek(0)
    workbook = openpyxl.load_workbook(workbook_stream)
    if sheet_name in workbook.sheetnames:
        del workbook[sheet_name]

    sheet = workbook.create_sheet(title=sheet_name)

    # Write columns
    for col_idx, col_name in enumerate(df.columns, 1):
        sheet.cell(row=1, column=col_idx, value=col_name)

    # Write rows
    '''Dealing with ValueError cannot convert[nan] to Excel indicates that there is an issue with converting a list containing nan. Excel doesn't support NaN so we convert [nan, nan, x] to str.'''


    for r_idx, row in enumerate(df.itertuples(index=False), 2):
        for c_idx, value in enumerate(row, 1):
            if isinstance(value, list):
                value = ', '.join(map(str, value))
            if value is None:
                value = ''

            sheet.cell(row=r_idx, column=c_idx, value=value)

    output_stream = BytesIO()
    workbook.save(output_stream)
    output_stream.seek(0)
    return output_stream


```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    Cell In[18], line 2
          1 def excel_writer(
    ----> 2     workbook_stream: BytesIO, sheet_name: str, df: pd.DataFrame
          3 ) -> BytesIO:
          4 
          5     #Excel doesn't accept NaN so replacing with None
          6     df = df.where(pd.notnull(df), "")
          8     workbook_stream.seek(0)


    NameError: name 'BytesIO' is not defined


## Query DBPedia

Cartier has a built in DBPedia scraper for scraping the page for a country - this page is usually phrased as ``List of newspaper in xxxx`` where xxxx is the name of the country.

Inside the ```mappings`` folder are yaml files for mapping English language and French language DBPedia.

The user simply selects the language they want to scrape (each have different endpoints on DBPedia and different data columns/mappings). 

The relevant language mappings, language, endpoint are passed to the ``get-db_data`` function and the data returned is stored in a pd.DataFrame and passed to excel_writer with the sheet_name set as 'Wikipedia'.

> If the DBPedia scraper stops working, make sure that the endpoint and relevant mappings are up to date by querying DBPedia from their website. Update mappings and endpoint if need be.




```python

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



```

## Collate Sources & Download Workbook

### Download Button

Now that we have queried Comply data and data from DBPedia and created respective worksheets in our workbook for their data, we'll want to label our sources and create a source of truth.

Labrelling requires that you download the file first with the ``Download research sheet`` button


```python
st.download_button(
        label="Download research sheet", 
        data=st.session_state.workbook, 
        file_name=f"AM Coverage in {country_selectbox}.xlsx", 
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        use_container_width=True,
    )


```

## Collate Sources into a Masterlist

As you can see from the sturcture of this button, it takes the name from the country you selected at the beginning ie country_selectbox. Failing to select your country will lead to the workbook being named AM Coverage in None, but downloading the workbook will still work as will fetching data and writing sheets.

> Before you collate, make sure to create provider, typology columns for each worksheet and ensure that every domain has a name in the name field. If there's no name, the collation process will fail.

To collate a workbook that's been labelled, simply upload the workbook again, click create workbook button, and then scroll to the bottom where the Create source of truth button is. Pushing this button will collate all worksheets in your workbook (excluding master) into a master list.

We collate worksheets by pushing our workbook to the ``create a master_sheet(st.session_state.workbook)`` function. 

Collation results in either a dataframe or None. If the sheet is empty, the programme will stop. If not, st.session-state.workbook (your workbook) is updated and the master list is written to "main" sheet with the excel_writer function. 



```python
#
if match_btn:
    master_sheet: pd.DataFrame | None = collate_sources(st.session_state.workbook)
    if master_sheet.empty:
        st.stop()
    st.session_state.workbook = excel_writer(workbook_stream=st.session_state.workbook, sheet_name="main", df=master_sheet)



```

> The collation will err if there are any domains missing a value in the ``name`` field. Make sure to add a provider, typology column to your worksheets so that you can tell which domain came from which source in your master list.

### Steps in Collation

The collation process creates a column for each worksheet that runs fuzzy matching on the names of the domains and then concats the sheets and groups the concated sheet by the best matching name.

The collate sources takes your workbook and applies a number of functions to your workbook

1. Destructs your BytesIO workbook and loads your workbook as a Workbook object
2. Creates a dictionary of sheet_names and corresponding Worksheets (objects in openpyxl) 
3. Loops through each worksheet and applies normalise_domains(df) to the dataframe in the worksheet.
    - Normalise domains is applies regex to remove unwanted text like www from the domains or / at the end.
4. The worksheets dictionary with names and dfs are passed to ``match_names function``
    - The match_names function loops through keys and worksheets to create a match_name column with the fuzzy matched names.
  
5. Collate sheets is the final step. This function makes sure that all types are string (this way ciruclation 18,0999 is cast as a string. In Excel and openpyxl, it will be treated as a float by default). Once types are all cast as string, worksheets are concatenated and then grouped by match_name and aggregated into a list with a return. Any failures here are reutrned and flagged with error visible from Cartier.



```python
##This is the main function
def collate_sources(workbook: BytesIO) -> pd.DataFrame | None:
    workbook.seek(0)
    workbook: Workbook = openpyxl.load_workbook(workbook)
    sheet_names: list[str] = workbook.sheetnames
    worksheet_list: list[Worksheet] = workbook.worksheets
    worksheets: dict = read_worksheets(sheet_names, worksheet_list)

    # Clean the domains
    for df in worksheets.values():
        df = normalise_domains(df)
    
    worksheets: dict = match_names_domains(worksheets)
    df: pd.DataFrame | None = collate_sheets(worksheets) 
    st.toast("✔️ Successfully collated sources")
    return df
```

#### Breaking down Collate Sources functions




```python

# Reads the Worksheet objects to dataframes and skips the worksheet called main in case you already have a main worksheet in your workbook. We don't want this to be collated as part of the new master list.
def read_worksheets(
    sheet_names, work_sheets: list[Worksheet]
) -> dict[str, pd.DataFrame]:

    data = {}
    for name, worksheet in zip(sheet_names, work_sheets):
        if name == "main":
            continue
        data[name] = worksheet_to_dataframe(worksheet)

    return data

## Normalise domains simply applies extract_domain lambda to each domain.
def normalise_domains(df: pd.DataFrame) -> pd.DataFrame:
    extract_domain = lambda url: re.sub(r"^(https?://)?(www\.)?|(\/)+$", "", url)
    if "domain" in df.columns:
        df["domain"] = df["domain"].apply(
            lambda x: extract_domain(x) if x is not None else None
        )
        return df
    return df

## Fuzzy matching returns the name that domain name matched with out of all domains in worksheets. Threshold is high at 90 to avoid false positives but can be lower (min 80 is recommended)
def fuzzy_matching(value_string: str, match_against: pd.Series, threshold=90) -> str:
    match, score, i = process.extractOne(value_string, match_against, scorer=fuzz.ratio)
    return match if score >= threshold else value_string

## We create a match by applying fuzzy matching to names. There's an option to add our normalised domains to the fuzzy matching by uncommenting domain series.
def create_match_col(df: pd.DataFrame, match_against: pd.DataFrame) -> pd.Series | None:
    try:
        name_series = df["name"].apply(lambda x: fuzzy_matching(x, match_against["name"]))
        #domain_series = df["domain"].apply(lambda x: fuzzy_matching(x, match_against["domain"]))
        return name_series #, domain_series
    except Exception as e:
        st.warning(f"Ensure there are no media sources with a missing name: {e}")
        st.stop()

## Match names and domains calls the create_match col function which applies fuzzy_matching function. This funcion updates our dictionary of worksheets.
def match_names_domains(worksheets: dict) -> dict | None:
    for key, df in worksheets.items():
        # if key != 'comply':
        name_series: pd.Series = create_match_col(df, worksheets["comply"])
        df["match_name"] = name_series
        worksheets[key] = df

    return worksheets

# Collate worksheets concats dataframes (ie our worksheets) and groups them by match_name. This is the final step. The result is a dataframe.
def collate_sheets(worksheets: dict) -> pd.DataFrame | None:
    try:
        # Types in Excel require exact same so circulations that are flaots and str break programme. Cast everything as str
        concat_data = pd.concat(worksheets.values()).astype(str)
        merged_df = concat_data.groupby("match_name").agg(tuple).applymap(list).reset_index()
        return merged_df
    except Exception as e:
        st.toast(f"⚠️ Failed to collate {e}")


## Collate sources reads all of the worksheets except main into dataframes and stores them in a dictionary before applying normalising_domains and fuzzy_matching.
## Final step is to collate_worksheets by concatenating them and grouping them by fuzzy matched name. Reuslt is a dataframe 
def collate_sources(workbook: BytesIO) -> pd.DataFrame | None:
    workbook.seek(0)
    workbook: Workbook = openpyxl.load_workbook(workbook)
    sheet_names: list[str] = workbook.sheetnames
    worksheet_list: list[Worksheet] = workbook.worksheets
    worksheets: dict = read_worksheets(sheet_names, worksheet_list)

    # Clean the domains
    for df in worksheets.values():
        df = normalise_domains(df)
    
    worksheets: dict = match_names_domains(worksheets)
    df: pd.DataFrame | None = collate_sheets(worksheets) 
    st.toast("✔️ Successfully collated sources")
    return df
```


```python

```
