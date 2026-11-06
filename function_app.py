import azure.functions as func
import os
from azure.storage.blob import BlobServiceClient
import pandas as pd
import io
import json

# Initialize the Azure Function App
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="get_nutrition_data")
def get_nutrition_data(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # 1. Connect to Azure Blob Storage
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        if not connect_str:
            return func.HttpResponse("Connection string not found.", status_code=500)
            
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        
        container_name = 'datasets'
        blob_name = 'All_Diets.csv'
        
        # 2. Download and Read the CSV
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        
        stream = blob_client.download_blob().readall()
        df = pd.read_csv(io.BytesIO(stream))
        
        # 3. Process the Data
        avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()
        
        # 4. Convert to JSON and return to the frontend
        result = avg_macros.reset_index().to_dict(orient='records')
        
        return func.HttpResponse(
             json.dumps(result),
             mimetype="application/json",
             status_code=200
        )
        
    except Exception as e:
        return func.HttpResponse(
             f"Error processing data: {str(e)}",
             status_code=500
        )