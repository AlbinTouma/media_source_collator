import streamlit as st
from psycopg2.extensions import connection 
from db.db import connect_to_db, create_temporary_table, query_for_mentions
from db.queries import get_db_domains 
from psycopg2.extensions import connection as Psycopg2Connection 
import pandas as pd
from io import BytesIO
from openpyxl import load_workbook
import openpyxl

def db_get_country_domains(country: str) -> list[tuple] | Exception:
    conn: Psycopg2Connection | Exception = connect_to_db(db_name='Source Metadata')
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


def init_workbook(file=None) -> BytesIO:
    if file:
        return BytesIO(file.read())
    else:
        wb = openpyxl.Workbook()
        stream = BytesIO()
        wb.save(stream)
        stream.seek(0)
        return stream

def excel_writer(workbook_stream: BytesIO, sheet_name: str, df: pd.DataFrame) -> BytesIO:
    
    workbook_stream.seek(0)
    workbook = openpyxl.load_workbook(workbook_stream)
    if sheet_name in workbook.sheetnames:
        del workbook[sheet_name]

    sheet = workbook.create_sheet(title=sheet_name)
    for r_idx, row in enumerate(df.itertuples(index=False), 1):
        for c_idx, value in enumerate(row, 1):
            sheet.cell(row=r_idx, column=c_idx, value=value)

    output_stream = BytesIO()
    workbook.save(output_stream)
    output_stream.seek(0)
    return output_stream

