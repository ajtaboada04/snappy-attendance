import os
import datetime
import logging
import azure.functions as func
from azure.cosmosdb.table.tableservice import TableService

def delete_code_from_table(table_service, table_name, partition_key, row_key):
    table_service.delete_entity(table_name, partition_key, row_key)

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Initialize table service
        table_service = TableService(connection_string=os.environ['AzureWebJobsStorage'])
        table_name = "TempCodes"
        partition_key = "Codes"

        # Get all entities in the table
        entities = table_service.query_entities(table_name, filter=f"PartitionKey eq '{partition_key}'")

        # Get the current time in UTC
        current_time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)

        if entities.items:
            # Iterate over entities and delete codes older than 30 seconds
            for entity in entities:
                
                code_timestamp_aware = entity.Timestamp.replace(tzinfo=datetime.timezone.utc)

                time_difference = current_time - code_timestamp_aware
                if time_difference.total_seconds() > 30:
                    delete_code_from_table(table_service, table_name, partition_key, entity.RowKey)
                    log_msg = f"Deleted code: {entity.RowKey}"
                    logging.info(log_msg)

            return func.HttpResponse("Cleanup completed successfully.", status_code=200)
        
        else:
            # No code found in the table
            return func.HttpResponse("No code found in the table.", status_code=400)
        
    except Exception as e:
        return func.HttpResponse(f"An error occurred: {str(e)}", status_code=500)
