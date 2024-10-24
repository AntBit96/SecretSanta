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

region_id="your gcp region" #europe-west1 for example
trigger_id = 'api_trigger/SendMaiSecretSanta' #application integration trigger


def send_email(gifter_mail, gifter_name, gifted_name) -> None:
    """
        Send email with alerts using Application Integration.

        Args:
            PROJECT_ID (str): The GCP project ID.
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

    mail_to= gifter_mail
    
    cc="myBoss@mail.com"
    bcc="my@mail.com"
    id_access_token = GCP_CREDENTIALS.token

    # Definisci l'URL, l'header e i dati
    url = f"https://integrations.googleapis.com/v1/projects/{PROJECT_ID}/locations/{region_id}/integrations/-:execute"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {id_access_token}"
    }


    with open('mail_message.html', 'r', encoding='utf-8') as file:
        html_body = file.read().replace("@@GIFTER@@",gifted_name).replace("@@GIFTED@@",gifted_name)
    
    data = {
        "trigger_id": trigger_id,
        "inputParameters": {
                "html_body":{"stringValue": html_body}
                }
            }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.text)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"Errore HTTP: {err}")
        raise err

    return None

