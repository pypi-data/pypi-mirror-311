import pytz
from datetime import datetime, timedelta
from azure.storage.blob import BlobSasPermissions, BlobServiceClient, generate_blob_sas

class AzureBlobStorage:
    def __init__(self, connection_string, container_name):
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_client = self.blob_service_client.get_container_client(container_name)

    def upload_blob(self, filename: str, data):
        blob_client = self.container_client.get_blob_client(filename)
        blob_client.upload_blob(data, overwrite=True)
        return blob_client

    def generate_sas_url(self, blob_name: str, expiry_days=14):
        timezone = pytz.timezone('US/Eastern')  # Replace with your desired timezone
        current_time = datetime.now(timezone)
        sas_token = generate_blob_sas(
            account_name=self.blob_service_client.account_name,
            container_name=self.container_client.container_name,
            blob_name=blob_name,
            account_key=self.blob_service_client.credential.account_key,
            permission=BlobSasPermissions(read=True),
            expiry=current_time + timedelta(days=expiry_days),
            start=current_time - timedelta(minutes=1)
        )
        sas_url = f"https://{self.blob_service_client.account_name}.blob.core.windows.net/{self.container_client.container_name}/{blob_name}?{sas_token}"
        return sas_url