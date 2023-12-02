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
    table_name = 'TempCodes'  
    entity = Entity()
    entity.PartitionKey = 'Codes'
    entity.RowKey = six_digit_code
    entity.Timestamp = datetime.datetime.utcnow()
    table_service.insert_entity(table_name, entity)

    response_body = json.dumps({"code": six_digit_code})
    
    return func.HttpResponse(response_body, mimetype="application/json")