import os
import json
import azure.functions as func
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        received_code = req_body.get('code')

        if not received_code:
            return func.HttpResponse("Please provide a 'code' in the request body.", status_code=400)

        # Retrieve the latest code from Azure Table Storage
        table_service = TableService(connection_string=os.environ['AzureWebJobsStorage'])
        table_name = "TempCodes"
        partition_key = "Codes"
        
        entities = table_service.query_entities(table_name, filter=f"PartitionKey eq '{partition_key}'")

        
        if entities.items:

            for entity in entities:

                if received_code == entity['RowKey']:
                    # Code is valid
                    return func.HttpResponse("true", status_code=200)
            
            return func.HttpResponse("false", status_code=200)
        else:
            # No code found in the table
            return func.HttpResponse("No code found in the table.", status_code=400)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return func.HttpResponse(f"An error occurred: {str(e)}", status_code=500)

