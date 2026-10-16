/**
* index.js Cloud Function - Avro on GCS to BQ
*/
const {Storage} = require('@google-cloud/storage');
const {BigQuery} = require('@google-cloud/bigquery');

// Replace the value wih your Project ID
const projectId = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'; 

const storage = new Storage({ projectId: projectId });
const bigquery = new BigQuery({ projectId: projectId });

exports.loadBigQueryFromAvro = async (event, context) => {
    try {
        // Check for valid event data and extract bucket name
        if (!event || !event.bucket) {
            throw new Error('Invalid event data. Missing bucket information.');
        }

        const bucketName = event.bucket;
        const fileName = event.name;

        // BigQuery configuration
        const datasetId = 'loadavro';
        const tableId = fileName.replace('.avro', ''); 

        const options = {
            sourceFormat: 'AVRO',
            autodetect: true, 
            createDisposition: 'CREATE_IF_NEEDED',
            writeDisposition: 'WRITE_TRUNCATE',     
        };

        // Load job configuration
        const loadJob = bigquery
            .dataset(datasetId)
            .table(tableId)
            .load(storage.bucket(bucketName).file(fileName), options);

        await loadJob;
        console.log(`Job ${loadJob.id} completed. Created table ${tableId}.`);

    } catch (error) {
        console.error('Error loading data into BigQuery:', error);
        throw error; 
    }
};
