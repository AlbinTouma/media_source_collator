import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON, N3
import yaml
import streamlit as st
import numpy as np

def open_mappings(yaml_file: str) -> dict:
    with open(f"mappings/{yaml_file}") as stream:
        yml = yaml.safe_load(stream)
        mappings = yml['newspaper']
        return mappings


def values(key: str, value: str | list) -> str | list[str]:
    if isinstance(value, list):
        ls = []
        for item in value:
            string = f"\nOPTIONAL{{?papers {item} ?{key}.}}"
            ls.append(string)
        return ls

    return f"\nOPTIONAL{{?papers {value} ?{key}.}}"


def buildQuery(mapping: dict, query: str, language: str) -> str:

    select = "SELECT ?source ?papers "
    where = f'''WHERE {{
    \n?source rdfs:label \"{query}\"{language};
    dbo:wikiPageWikiLink ?papers.'''
    query = ""

    for key, value in mapping.items():
        select = select + f"?{key} "
        x = values(key, value)
        if isinstance(x, list):
            for item in x:
                query += item
        else:
            query += x
    sparsql = select + where + query + "\n}"
    return sparsql


def make_query(sparsql: str, endpoint: str) -> dict | Exception:
    try:
        sparql = SPARQLWrapper(endpoint)
        sparql.setQuery(sparsql)
        sparql.setReturnFormat(JSON)
        qres = sparql.query().convert()
        return qres
    except Exception as e:
        st.warning(f"Failed query {e}")
        return e

def create_dataframe(qres: dict) -> pd.DataFrame | None:
    if isinstance(qres, Exception):
        pass

    extracted_data = []
    for dictionary in qres['results']['bindings']:
        extracted_values = {}
        for key, value in dictionary.items():
            extracted_values[key] = value['value']
        extracted_data.append(extracted_values)
    return pd.DataFrame(extracted_data)
    



def get_db_data(yaml_file: str, query: str, language: str, endpoint: str) -> pd.DataFrame | None:
    mappings: dict = open_mappings(yaml_file)
    sparsql: str = buildQuery(mappings, query, language)
    qres: dict | Exception = make_query(sparsql, endpoint)
    df: pd.DataFrame | None = create_dataframe(qres)
    return df
