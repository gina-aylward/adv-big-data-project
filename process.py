import argparse
import csv
import logging
import time
import os
import sys

import googlemaps

import apache_beam as beam
from apache_beam.io.gcp import bigquery
from apache_beam.options.pipeline_options import PipelineOptions

QUERIES_PER_SECOND = 1
RADIUS = 100

def enrich_from_api(gmaps_client, row):
    # Ask the Google Maps API for information about this area
    # https://googlemaps.github.io/google-maps-services-python/docs/index.html#googlemaps.Client.places
    # Note that this will only fetch the first page of results. See page_token to paginate.
    print(row)
    result = gmaps_client.places(query="restaurant", location=f"{row['latitude']},{row['longitude']}")
    print(result)
    return {
        'url': row['url'],
        'data': result
    }

def run(argv=None):
    parser = argparse.ArgumentParser()

    parser.add_argument('--gmaps_key', dest='gmaps_key', required=True,
                        help='Google Places API key')

    parser.add_argument('--output', dest='output', required=True,
                        help='Output BQ table to write results to.')

    known_args, pipeline_args = parser.parse_known_args(argv)

    gmaps_client = googlemaps.Client(queries_per_second=QUERIES_PER_SECOND, key=known_args.gmaps_key)

    p = beam.Pipeline(options=PipelineOptions(pipeline_args))

    # This is the query you run on your property data.
    read_query = """
    SELECT
        url as id, latitude, longitude
    FROM `stream-test-246208.properties.bypostcode`
    WHERE longitude IS NOT NULL and latitude IS NOT NULL
    LIMIT 2
    """

    output_schema = 'id:STRING, data:STRING'
    # Pipeline to run the query, extract fields and query the API for each row. Finally write the results to BQ.
    (p
        | 'Read from BigQuery' >> beam.io.Read(beam.io.BigQuerySource(query=read_query, use_standard_sql=True))
        | 'Query Google Places API' >> beam.Map(lambda r: enrich_from_api(gmaps_client, r)))
        | 'Write to BigQuery' >> beam.io.Write(beam.io.BigQuerySink(
                known_args.output,
                schema=None,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE)))

    p.run().wait_until_finish()

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
