from simple_salesforce import Salesforce 
import time
import json
import pandas
from google.cloud import kms_v1
from google.cloud import bigquery as bq
from google.cloud import storage as gcs
import os
import paramiko
import requests
from datetime import date, datetime
import numpy as np
import google.auth


DistributionList="antonio.bitonti@jakala.com"
cc=""
bcc=""
object="Pipeline Status"
PipelineStatus="OK"
PipelineName="Test"
Message="Nice job your pipeline is great"
BUCKET_MAIL_LIST = f'brico_io_dev'
MAIL_LIST_PATH = 'MailList.json'

def send_email_new(category: str, body_message: str, object: str, gcs_client: callable, bucket_name_mail_list: str, path_mail_list: str , status: str) -> None:
    """
        Send email with alerts using Application Integration.

        Args:
            PROJECT_ID (str): The GCP project ID.
            body_message (str): The email body content.
            subject_message (str): The email subject.
            gcs_client (callable): The GCS client object.
            bucket_name_mail_list (str): The GCS bucket name containing the email list.
            path_mail_list (str): The path to the email list file in the GCS bucket.
            object (str): The email object.
            category (str): The category of the email list to use.
        Returns:
            str: A response indicating the status code and text from the API call.

        Raises:
            requests.exceptions.HTTPError: If an HTTP error occurs during the API request.
    """
    
    GCP_CREDENTIALS, PROJECT_ID = google.auth.default()
    auth_req = google.auth.transport.requests.Request()
    GCP_CREDENTIALS.refresh(auth_req)
    mail_to, cc, bcc = get_mail_list(gcs_client,bucket_name_mail_list, path_mail_list, category)
    ENV = PROJECT_ID.split('-')[-1]

    id_access_token = GCP_CREDENTIALS.token

    # Definisci l'URL, l'header e i dati
    url = f"https://integrations.googleapis.com/v1/projects/{PROJECT_ID}/locations/europe-west6/integrations/-:execute"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {id_access_token}"
    }

    if ENV == 'prd' :
        trigger_id = 'api_trigger/SendMailAlert_API_1'
        dl=mail_to
    else:
        trigger_id = 'api_trigger/SendMailAlert_API_1'
        dl='antonio.bitonti@jakala.com'
        cc=""
        bcc=""

    mail_information = {
        "PipelineStatus": status,
        "Message": body_message,
        "DistributionList": dl,
        "cc": cc,
        "bcc": bcc,
        "object": object,
        "PipelineName": f"ETL-BRICOIO-{ENV.upper()}"
    }
    
    data = {
        "trigger_id": trigger_id,
        "inputParameters": {
                "mail_information":{"jsonValue": json.dumps(mail_information)}
                }
            }

    # Invia la richiesta POST
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.text)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"Errore HTTP: {err}")
        raise err

    # Ritorna la risposta
    return None

def get_mail_list(gcs_client,bucket_name, path, category):
    bucket = gcs_client.get_bucket(bucket_name)
    blob = gcs.Blob(path, bucket)
    mail_lists =json.loads(blob.download_as_string())
    mail_to = mail_lists[category]['mail_to']
    Cc = mail_lists[category]['cc'] 
    Bcc = mail_lists[category]['bcc']
    return mail_to, Cc, Bcc


send_email_new("PROVA", Message, object, gcs.Client(), BUCKET_MAIL_LIST, MAIL_LIST_PATH, PipelineStatus)