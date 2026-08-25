import os
from google.cloud import bigquery
import functions_framework

# Initialize the BigQuery client
bigquery_client = bigquery.Client()

@functions_framework.cloud_event
def loadBigQueryFromAvroPy(cloud_event):
    """
    Cloud Function - Avro on GCS to BQ
    Triggered by a change to a Cloud Storage bucket.
    Args:
         cloud_event: The CloudEvent object.
    """
    data = cloud_event.data
    try:
        # Check for valid event data and extract bucket name
        if not data or 'bucket' not in data:
            raise ValueError('Invalid event data. Missing bucket information.')

        bucket_name = data['bucket']
        file_name = data['name']

        # BigQuery configuration
        dataset_id = 'loadavro'
        table_id = file_name.replace('.avro', '')

        # Construct the table reference
        table_ref = bigquery_client.dataset(dataset_id).table(table_id)

        # Configure the load job
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.AVRO,
            autodetect=True,
            create_disposition=bigquery.CreateDisposition.CREATE_IF_NEEDED,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        )

        # Load data from the GCS URI
        uri = f"gs://{bucket_name}/{file_name}"
        load_job = bigquery_client.load_table_from_uri(
            uri, table_ref, job_config=job_config
        )

        # Wait for the job to complete
        load_job.result()
        print(f"Job {load_job.job_id} completed. Created table {table_id}.")

    except Exception as e:
        print(f"Error loading data into BigQuery: {e}")
        raise e
