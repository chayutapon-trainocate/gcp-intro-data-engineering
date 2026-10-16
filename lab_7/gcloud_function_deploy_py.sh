#!/bin/bash

gcloud functions deploy loadBigQueryFromAvroPy \
    --gen2 \
    --runtime python311 \
    --source . \
    --region $REGION \
    --trigger-resource gs://$PROJECT_ID \
    --trigger-event google.storage.object.finalize \
    --memory=512Mi \
    --timeout=540s \
    --service-account=$PROJECT_NUMBER-compute@developer.gserviceaccount.com 
