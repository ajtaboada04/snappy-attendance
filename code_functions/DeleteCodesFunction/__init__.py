import os
import datetime
import azure.functions as func
from azure.cosmosdb.table.tableservice import TableService

def delete_code_from_table(table_service, table_name, partition_key, row_key):
    table_service.delete_entity(table_name, partition_key, row_key)

def main (req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Initialize table service
        table_service = TableService(connection_string=os.environ['AzureWebJobsStorage'])
        table_name = "TempCodes"
        partition_key = "Codes"

        # Get all entities in the table
        entities = table_service.query_entities(table_name, filter=f"PartitionKey eq '{partition_key}'")

        # Get the current time
        current_time = datetime.datetime.utcnow()

        # Iterate over entities and delete codes older than 30 seconds
        for entity in entities:
            code_timestamp = entity.Timestamp
            time_difference = current_time - code_timestamp
            if time_difference.total_seconds() > 30:
                delete_code_from_table(table_service, table_name, partition_key, entity.RowKey)
                print(f"Deleted code: {entity.RowKey}")
        return func.HttpResponse("Cleanup completed successfully.", status_code=200)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
