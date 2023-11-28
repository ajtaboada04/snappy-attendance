import os
import datetime
import json
import azure.functions as func
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
from azure.storage.queue import QueueClient


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        received_code = req_body.get('code')

        if not received_code:
            return func.HttpResponse("Please provide a 'code' in the request body.", status_code=400)

        table_service = TableService(connection_string=os.environ['AzureWebJobsStorage'])
        table_name = "TempCodes"
        partition_key = "Codes"
        
        entities = table_service.query_entities(table_name, filter=f"PartitionKey eq '{partition_key}'")

        log_table_name = "LogAttempts"
        error_queue_name = "log-error-attempts"

        
        if entities.items:

            for entity in entities:

                if received_code == entity['RowKey']:
                    # Code is valid
                    log_result = "true"
                    log_entity = Entity()
                    log_entity.PartitionKey = "Attempts"
                    log_entity.RowKey = str(datetime.datetime.utcnow())
                    log_entity.ReceivedCode = received_code
                    log_entity.Result = log_result
                    table_service.insert_entity(log_table_name, log_entity)

                    return func.HttpResponse("true", status_code=200)
            
            log_result = "false"

            # Logging False attempt in "LogAttempts" table
            log_entity = Entity()
            log_entity.PartitionKey = "Attempts"
            log_entity.RowKey = str(datetime.datetime.utcnow())
            log_entity.ReceivedCode = received_code
            log_entity.Result = log_result
            table_service.insert_entity(log_table_name, log_entity)

            # Logging the error attempt in the log-error-attempts queue
            error_attempt = {
                "ReceivedCode": received_code,
                "Timestamp": str(datetime.datetime.utcnow())
            }
            connection_string = os.environ['AzureWebJobsStorage']
            queue_service = QueueClient.from_connection_string(connection_string, error_queue_name)
            queue_service.send_message(json.dumps(error_attempt))

            return func.HttpResponse("false", status_code=400)
        else:
            # No code found in the table
            return func.HttpResponse("No code found in the table.", status_code=400)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return func.HttpResponse(f"An error occurred: {str(e)}", status_code=500)

