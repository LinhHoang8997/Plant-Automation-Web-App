import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='C:/Users/linhd/PycharmProjects/big-query-first/big-query-plant-project-c0be32d1e67a.json'

from google.cloud import bigquery
client = bigquery.Client()

query = (
    "SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` "
    'WHERE state = "TX" '
    "LIMIT 100"
)

query_job = client.query(
    query,
    # Location must match that of the dataset(s) referenced in the query.
    location="US",
)  # API request - starts the query

df = query_job.to_dataframe()
print(df.head(5))

#
# for row in query_job:  # API request - fetches results
#     # Row values can be accessed by field name or index
#     assert row[0] == row.name == row["name"]
#     print(row)