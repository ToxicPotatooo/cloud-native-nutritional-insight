from azure.storage.blob import BlobServiceClient

connect_str = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"

blob_service_client = BlobServiceClient.from_connection_string(connect_str)

container_name = "datasets"
try:
    container_client = blob_service_client.create_container(container_name)
    print(f"Container '{container_name}' created.")
except Exception as e:
    print(f"Container '{container_name}' already exists or error: {e}")
    container_client = blob_service_client.get_container_client(container_name)

blob_client = container_client.get_blob_client("All_Diets.csv")
with open("All_Diets.csv", "rb") as data:
    blob_client.upload_blob(data, overwrite=True)
    print("CSV uploaded to Azurite Blob Storage successfully!")