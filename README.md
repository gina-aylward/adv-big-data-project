# properties-dataflow

This is used for querying a BigQuery table and sending enrichment requests to Google Places API. External data is landed in raw JSON form to the specified `output` table in BigQuery for further processing later on. The URL from the _source_ table was used as an identifier in the output table so that it can be joined.

## Running it

In Cloud Shell:

```
git clone https://github.com/gina-aylward/adv-big-data-project
cd properties-dataflow
virtualenv -p python3.7 venv
source venv/bin/activate
pip install -r requirements.txt
```

To run locally (replacing the values in <>, i.e. `--output test_project:mydata:output`). The local version also works slightly differently than the Dataflow version - the parameters need to be inside of the function in the Dataflow version, while they can be defined earlier when running Dataflow. Just FYI - there might be errors and that is the problem.

```
python process.py \
  --output <project id>:<dataset>.<output_table_name> \
  --project <project id> \
  --gmaps_key <your API key>
```
Note that the _local_ Apache Beam runner is only suitable for testing a very small number of records. 

When ready to execute it on Cloud Dataflow, [follow this guide](https://cloud.google.com/dataflow/docs/quickstarts/quickstart-python#run-wordcount-on-the-dataflow-service).

```
python process.py \
  --output <your project>:<your dataset>.<output_table_name> \
  --project <your project> \
  --gmaps_key <your API key> \
  --runner DataflowRunner \
  --project $PROJECT \
  --temp_location gs://<your temp bucket>/dataflow/
```

This will provision several VMs to perform this batch job. You can monitor process by following the URL that appears in the terminal after issuing the above command.

## But first

Read the small Beam program and amend the input query, at least replacing the source table name. Remember to add a `LIMIT` to your query when testing.

## Improvements
- Raw data is landed as a blob of JSON. This can be queried in BigQuery with `JSON_EXTRACT` and so on, but it is a little awkward to work with. We could extract relevant parts of the JSON in this program and populate an easier to use table with a more specialised schema.
