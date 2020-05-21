# properties-dataflow

Tiny example for querying a BigQuery table and sending enrichment requests to Google Places API. External data is landed in raw JSON form to the specified `output` table in BigQuery for further processing later on. The URL from the _source_ table was used as an identifier in the output table so that it can be joined.

## Running it

In Cloud Shell:

```
git clone git@github.com:AlexJReid/properties-dataflow.git
cd properties-dataflow
virtualenv -p python3.7 venv
source venv/bin/activate

pip install requirements.txt
```

To run locally (replacing the values in <>, i.e. `--output test_project:mydata:output`)

```
python process.py --output <your project>:<your dataset>.<output_table_name> --project <your project> --gmaps_key <your API key>
```
Note that the _local_ Apache Beam runner is only suitable for testing a very small number of records. When ready to execute it on Cloud Dataflow, [follow this guide](https://cloud.google.com/dataflow/docs/quickstarts/quickstart-python#run-wordcount-on-the-dataflow-service). (Long story short, specify `--runner DataflowRunner`).

## But first

Read the small Beam program and amend the input query, at least replacing the source table name. Remember to add a `LIMIT` to your query when testing.

## Improvements
- Raw data is landed as a blob of JSON. This can be queried with `JSON_EXTRACT` and so on, but it is a little awkward to work with. You could extract relevant parts of it in this program and populate an easier to use table with a more specialised schema.
