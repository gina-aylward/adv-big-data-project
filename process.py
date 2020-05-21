import argparse
import csv
import json
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
    result = gmaps_client.places(query="restaurant", radius=RADIUS, location=f"{row['latitude']},{row['longitude']}")
    print(result)
    return {
        'id': row['id'],
        'data': json.dumps(result)
    }

def run(argv=None):                            
    parser = argparse.ArgumentParser()
    parser.add_argument('--gmaps_key', dest='gmaps_key', required=True,
                        help='Google Places API key')
    parser.add_argument('--output', dest='output', required=True,
                        help='Output BQ table to write results to.')
    known_args, pipeline_args = parser.parse_known_args(argv)

    # Create Google Maps client      
    gmaps_client = googlemaps.Client(queries_per_second=QUERIES_PER_SECOND, key=known_args.gmaps_key)

    # Create pipeline
    p = beam.Pipeline(options=PipelineOptions(pipeline_args))

    # Source data to map over from BigQuery using this SQL.
    read_query = """
    SELECT
        url as id, latitude, longitude
    FROM `changethis.properties.bypostcode`
    WHERE longitude IS NOT NULL and latitude IS NOT NULL
    LIMIT 2
    """
   
    # Specify schema of output table
    output_schema = 'id:STRING, data:STRING'

    # Pipeline to run the query, extract fields and query the API for each row. Finally write the results to BQ.
    (p
        | 'Read from BigQuery' >> beam.io.Read(beam.io.BigQuerySource(query=read_query, use_standard_sql=True))
        | 'Query Google Places API' >> beam.Map(lambda r: enrich_from_api(gmaps_client, r))
        | 'Write to BigQuery' >> bigquery.WriteToBigQuery(
                known_args.output,
                schema=output_schema,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE))

    p.run().wait_until_finish()

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
