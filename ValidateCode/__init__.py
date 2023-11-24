import os
import json
import azure.functions as func
from azure.cosmosdb.table.tableservice import TableService

def validate_code(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        received_code = req_body.get('code')

        if not received_code:
            return func.HttpResponse("Please provide a 'code' in the request body.", status_code=400)

        # Retrieve the latest code from Azure Table Storage
        table_service = TableService(connection_string=os.environ['AzureWebJobsStorage'])
        table_name = 'TempCodes'
        partition_key = 'Codes'
        
        # Retrieve the latest entity (code) from the table
        latest_entity = table_service.query_entities(table_name, filter=f"PartitionKey eq '{partition_key}'", top=1, orderby="Timestamp desc").items

        if not latest_entity:
            # No code found in the table
            return func.HttpResponse("No code found in the table.", status_code=400)

        latest_entity = latest_entity[0]

        if received_code == latest_entity.RowKey:
            # Code is valid
            return func.HttpResponse("true", status_code=200)
        else:
            # Code is invalid
            return func.HttpResponse("false", status_code=400)

    except Exception as e:
        return func.HttpResponse(f"An error occurred: {str(e)}", status_code=500)


