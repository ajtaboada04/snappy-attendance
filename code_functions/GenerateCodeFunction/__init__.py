import os
import json
import datetime
import random
import azure.functions as func
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Generate a six-digit code
    six_digit_code = str(random.randint(100000, 999999))

    # Save the code to Azure Table Storage
    table_service = TableService(connection_string=os.environ['AzureWebJobsStorage'])
    table_name = 'TempCodes'  # Replace with your table name
    entity = Entity()
    entity.PartitionKey = 'Codes'
    entity.RowKey = six_digit_code
    entity.Timestamp = datetime.datetime.utcnow()
    table_service.insert_entity(table_name, entity)

    # Return the generated code in the HTTP response
    return func.HttpResponse(f"Generated Code: {six_digit_code}")
