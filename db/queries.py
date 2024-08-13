get_db_domains = f"""
    SELECT * FROM {secret_table} WHERE {secret_col} = %s;
"""
