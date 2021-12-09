import dash
import plotly.graph_objects as go
import dash_html_components as html
import dash_core_components as dcc

import pyarrow as pa
from pyarrow import parquet as pq
from s3fs.core import S3FileSystem
import configparser

config = configparser.ConfigParser()
config.read_file(open("local.sparkconf.cfg"))

S3_ENDPOINT = config["S3"]["spark.hadoop.fs.s3a.endpoint"]
S3_ACCESS_KEY = config["S3"]["spark.hadoop.fs.s3a.access.key"]
S3_SECRET_KEY = config["S3"]["spark.hadoop.fs.s3a.secret.key"]

s3_fs = S3FileSystem(
    key=S3_ACCESS_KEY,
    secret=S3_SECRET_KEY,
    client_kwargs={"endpoint_url": S3_ENDPOINT, "verify": False},
)

paths = s3_fs.glob("s3://dutrajardim/udacity-dl-project/users.parquet/*/*.parquet")
users_table = pq.read_table(paths, filesystem=s3_fs, columns=["gender", "user_id"])

df = users_table.to_pandas()
data = df.groupby("gender").count()["user_id"].values

fig = go.Figure(data=go.Bar(y=data))

app = dash.Dash(__name__)
app.layout = html.Div([dcc.Graph(id="graph", figure=fig)])

if __name__ == "__main__":
    app.run_server(debug=True)
