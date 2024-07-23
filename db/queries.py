temp_table = f"""
CREATE TEMPORARY TABLE country_review (
    uuid TEXT,
    source_name TEXT,
    url TEXT,
    host TEXT, 
    country TEXT, 
    article_created_datetime TEXT,
    collection_datetime TEXT, 
    publish_datetime TEXT
    );

INSERT INTO country_review
SELECT uuid, source_name, url, host, country, article_created_datetime, collection_datetime, publish_datetime
FROM articles_with_mentions
WHERE country = %s LIMIT 10;
"""

get_db_domains = f"""
    SELECT * FROM website WHERE country = %s LIMIT 2;
"""
