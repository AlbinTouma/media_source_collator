import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON, N3
import yaml

GOOGLE_URL_SHEET  = "https://docs.google.com/spreadsheets/d/1T9QQek-mP3TRBGANprrHPVmEdgi7sxdQXZ84es2fwzg/edit?gid=1832685312#gid=1832685312"
sparql = SPARQLWrapper("https://fr.dbpedia.org/sparql")


with open("france.yml") as stream:
    yml = yaml.safe_load(stream)
    newspaper = yml['newspaper']

def values(key: str, value: str | list) -> str | list[str]:
    if isinstance(value, list):
        ls = []
        for item in value:
            string = f"\nOPTIONAL{{?papers {item} ?{key}.}}"
            ls.append(string)
        return ls

    return f"\nOPTIONAL{{?papers {value} ?{key}.}}"




def buildQuery(mapping: dict) -> str:

    select = "SELECT ?source ?papers "
    where = """WHERE {\n?source rdfs:label "Presse écrite régionale en France"@fr; \ndbo:wikiPageWikiLink ?papers. \n?papers rdf:type dbo:Newspaper.  """
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


sparsql = buildQuery(newspaper)
print(sparsql)


def make_query(sparsql: str):
    endpoint = SPARQLWrapper("https://fr.dbpedia.org/sparql")
    sparql.setQuery(sparsql)
    sparql.setReturnFormat(JSON)
    qres = sparql.query().convert()
    return qres

qres = make_query(sparsql)

extracted_data = []
for dictionary in qres['results']['bindings']:
  extracted_values = {}
  for key, value in dictionary.items():
    extracted_values[key] = value['value']

  extracted_data.append(extracted_values)

df = pd.DataFrame(extracted_data)
df = df.groupby(['papers']).agg(tuple).applymap(list).reset_index()

names = df['papers'].apply(lambda x: x.split("/")[-1].replace("_", " "))
for name_item, row_set in zip(names, df['name']):
  row_set.append(name_item)


#Remove NaN values in names.
df['name'] = df['name'].apply(lambda x: [item for item in x  if item == item])
# Remove duplicates in names
df['name'] = df['name'].apply(lambda x: set(x))

#Save alias as list
df['alias'] = df['name'].apply(lambda x: list(x))

#Save name as first item in alias
df['name'] = df['alias'].apply(lambda x: x[0])

import numpy as np
def list_to_string(lst):
  for item in lst:
    if item != 'nan':
      return item


df = df.applymap(lambda x: list_to_string(x) if isinstance(x, list) else x)

df.to_excel("excel.xlsx")
