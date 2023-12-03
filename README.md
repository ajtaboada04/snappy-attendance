<h1 align="center">Snappy</h1>
<br>

## Overview [![Google Slides](https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Google_Slides_logo_%282014-2020%29.svg/15px-Google_Slides_logo_%282014-2020%29.svg.png)](https://docs.google.com/presentation/d/1oHVmyuj295BDY9uNqpb1K2tNeo3f6BCWNAtYgFcvDyw/edit?usp=sharing)
The Attendance Management System is a digital platform designed to enhance the management and tracking of students' attendance. It's built upon the concept of the "Qwickly" application, but with several advancements for accuracy and user experience. This system employs a combination of authentication methods, requiring individual accounts validated through university email credentials.

<br>
<br>

## Features

- **Account Creation & Authentication**: Users create accounts authenticated via university email, ensuring secure access.
- **Manual Attendance Adjustment**: Teachers can manually alter attendance records for flexibility and accuracy.
- **Dynamic Verification Code**: Uses a serverless function to generate a new verification code every 30 seconds for enhanced security.
- **Time Tracking**: Marks students late based on their entry time into the classroom.

<br>
<br>

<h1 align="center">The System Architecture:</h1>
<p align="center">
  <img width="75%" alt="architecture (1) (1)" src="https://github.com/rorosaga/snappy-attendance/assets/133862511/9fbf1b10-e51a-46ef-a6de-60f05df72bb2"><br><br>
  Django backend deployed on Azure App Service.<br>
  Three serverless functions: code generation, code deletion, code validation.<br>
  API endpoint to connect to MySQL database and to perform CRUD operations<br>
  Dead Letter Queue for logging errors<br>
  AJAX used to dynamically update the page.<br>

</p>


<br>
<br>


<h1 align="center">How to Navigate the System:</h1>

<br><br>
<h2 align="left">Homescreen</h2>
<br>
<p align="center">
  
  <img width="75%" alt="Screenshot 13" src="https://github.com/rorosaga/Classlink/assets/133862511/5ce32413-2d12-4286-9a96-16ba8a793548">
  <br><br>Snappy's homescreen presents itself as symplistic although efficient. It displays three possible paths: Login, Professor Dashboard and Student Dashboard. The user then logs in and starts the systems navigation.
</p>

<br><br>
## Professor's Navigation through the System
<br>
<p align="center">
  <img width="75%" alt="Screenshot 6" src="https://github.com/rorosaga/Classlink/assets/133862511/45c551ac-62e8-4e27-9b61-e02aa260ae42">
  <br><br>When the professor logs in the following screen is presented, displaying a successfull login and the name of the user.<br>
</p>

<br><br>
<p align="center">
  <img width="75%" alt="Screenshot 7" src="https://github.com/rorosaga/Classlink/assets/133862511/c540859e-273c-4c79-866e-7414d636fe7d">
  <br><br>The professor has the possibility to check the attendance status of a student for any specific session of the term.
  <br><br>
</p>

<p align="center">
  <img width="75%" alt="Screenshot 8" src="https://github.com/rorosaga/Classlink/assets/133862511/222e27c1-7217-478e-a6f5-04f34efecbcc">
  <br><br>Once the query is sent, snappy will present the following page displaying the Name and Surname of the student, and the status of the attendance for the specific session. In this case Rodrigo in session 1 was in fact present.
  <br><br>
</p>

<p align="center">
  <img width="75%" alt="Screenshot 9" src="https://github.com/rorosaga/Classlink/assets/133862511/f9c52dd1-f500-47c6-88af-850f991390a8">
  <br><br>It is not uncommon for a professor to be teaching more than one class throughout the semester, therefore in the case of Edoardo, the professor will select the class he is teaching and start the attendance process by pressing the button "Display Code"<br><br>
</p>

<h1 align="center">Generate Codes Functions:</h1><br><br>

| Code                                                  | Explanation                                                                   |
|-------------------------------------------------------|-------------------------------------------------------------------------------|
| `def main(req: func.HttpRequest) -> func.HttpResponse:` | Defines the main function, the entry point for the Azure Function. Takes an HTTP request as input and returns an HTTP response. |
| `six_digit_code = str(random.randint(100000, 999999))` | Generates a random six-digit code.                                             |
| `table_service = TableService(connection_string=os.environ['AzureWebJobsStorage'])`<br>`table_name = 'TempCodes'` | Establishes a connection to Azure Cosmos DB table using the provided connection string. Sets the table name to 'TempCodes'. |
| `entity = Entity()`<br>`entity.PartitionKey = 'Codes'`<br>`entity.RowKey = six_digit_code`<br>`entity.Timestamp = datetime.datetime.utcnow()` | Creates an Entity object representing a record in Azure Cosmos DB table. Sets partition key to 'Codes', row key to the generated code, and timestamp to current UTC time. |
| `table_service.insert_entity(table_name, entity)` | Inserts the created entity into 'TempCodes' table in Azure Cosmos DB.          |
| `response_body = json.dumps({"code": six_digit_code})` | Prepares a JSON response body containing the generated six-digit code.        |
| `return func.HttpResponse(response_body, mimetype="application/json")` | Returns an HTTP response with the JSON response body containing the generated code, sent back to the client. |


<br><br><br>


<p align="center">
  <img width="75%" alt="Screenshot 10" src="https://github.com/rorosaga/Classlink/assets/133862511/88d232f7-7bba-4381-9892-27f7aa0ed987">
  <br><br><br>The following page will show displaying the code necessary for the students to complete the attendance process
  <br><br>
</p>
<br><br>
<h1 align="center">Delete Codes Functions:</h1><br><br>

| Code                                           | Explanation                                                                      |
|------------------------------------------------|----------------------------------------------------------------------------------|
| `table_service = TableService(connection_string=os.environ['AzureWebJobsStorage'])` | Initializes a connection to Azure Cosmos DB table using the provided connection string. |
| `table_name = "TempCodes"`                      | Specifies the table name as "TempCodes".                                         |
| `partition_key = "Codes"`                       | Sets the partition key as "Codes".                                               |
| `entities = table_service.query_entities(...)`  | Queries entities (codes) from the table with the specified partition key.        |
| `current_time = datetime.datetime.utcnow()...` | Gets the current time in UTC.                                                   |
| `if entities.items:`                            | Checks if entities (codes) are found.                                           |
| `for entity in entities:`                       | Iterates over the retrieved entities.                                           |
| `if time_difference.total_seconds() > 30:`      | Checks if the code has expired (more than 30 seconds old).                       |
| `delete_code_from_table(...)`                   | Deletes the expired code from the table.                                        |
| `log_msg = f"Deleted code: {entity.RowKey}"`    | Logs a message for each deleted code.                                           |
| `return func.HttpResponse("Cleanup completed...` | Returns a success message if cleanup is successful, else an error message.       |


<br><br><br>
<p align="center">
  <img width="75%" alt="Screenshot 11" src="https://github.com/rorosaga/Classlink/assets/133862511/d823b01f-2c69-46fb-beac-e2f0ecb6d525">
  <br><br><br>In the case of 'orange status' students, the professor has the possibility to change manually the attendance. This would also be useful in the case in which a student has attended a seminar/presentation with IE which excuses the absences of a student.<br><br>
</p>

<p align="center">
  <img width="75%" alt="Screenshot 12" src="https://github.com/rorosaga/Classlink/assets/133862511/f4d38308-5c13-4f8a-b088-24ace9e4e351">
  <br><br><br>Once all the students have inserted the code displayed, the professor can officially submit the attendance record of the session.
  <br><br>
</p>



<br><br>
## Student's Navigation through the System

<p align="center">
  <img width="75%" alt="Screenshot 1" src="https://github.com/rorosaga/Classlink/assets/133862511/c1df9948-70c9-40b8-94c6-7c1f530f7c0e">
  <br><br>When the student logs in the following screen is presented, displaying a successfull login and the name of the user.<br><br><br>
</p>

<p align="center">
  <img width="75%" alt="Screenshot 3" src="https://github.com/rorosaga/Classlink/assets/133862511/ce815f88-0b4a-4739-a686-0a952c86e816">
  <br><br>The student will want to have the possibility to check their own attendance for a determined class, thus the student can select the course of interest and query the attendance log. The log is presented in a easy user-friendly style displaying the date of the session, the session number and the status of presenece (present/absent)<br><br><br>
</p>

<p align="center">
  <img width="75%" alt="Screenshot 4" src="https://github.com/rorosaga/Classlink/assets/133862511/dec8a74f-8e33-43e4-9cbc-5239556ef250">
  <br><br>The student will have to insert the generated code for the attendance process to be complete. 
</p>



<br><br>
## Snappy's Error Handling System

<p align="center">
  <img width="75%" alt="Screenshot 2" src="https://github.com/rorosaga/Classlink/assets/133862511/32d44463-d570-47f1-98fe-ea10bf551c22">
  <br><br><br>Once the login is done, the system is informed of the position the user holds, therefore if a student were to try and enter the professors dashboard he would recieve the following error message.<br><br>
</p>

<p align="center">
  <img width="75%" alt="Screenshot 5" src="https://github.com/rorosaga/Classlink/assets/133862511/b78ff57f-f35a-4572-b42f-c733522d3c07">
  <br><br><br>In the case in which the student submits an incorrect code the system will notify them with an error message and ask them to try again.
</p>


| Code                     | Explaination                                                                                                                                                                                                                                                                                                              |
|-----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **main(req: func.HttpRequest) -> func.HttpResponse:** | Defines the main function, which is the entry point for the Azure Function. It takes an HTTP request as input and returns an HTTP response. |
| **Try-Except Block:**        | Catches exceptions that may occur during the execution of the function.  |
| **JSON Content Retrieval:** | Attempts to get the JSON content from the HTTP request. If there's no 'code' in the request body, it returns a 400 Bad Request response asking for the 'code'.   |
| **Azure Cosmos DB Setup:**   | Establishes a connection to Azure Cosmos DB. Defines the names of tables and queues to be used (TempCodes, LogAttempts, log-error-attempts). |
| **Entity Querying:**         | Queries entities in the 'TempCodes' table where the partition key is 'Codes'. |
| **Entity Matching Loop:**    | Checks if the received code matches any of the codes in the 'TempCodes' table. If a match is found, logs the attempt as successful in the 'LogAttempts' table and returns a 200 OK response with "true". If no match is found, logs the attempt as unsuccessful and sends an error message to the 'log-error-attempts' queue. Returns a 400 Bad Request response with "false". |
| **No Entities Found:**       | If there are no entities in the 'TempCodes' table, returns a 400 Bad Request response with "No code found in the table."   |
| **Exception Handling:**      | Catches any exceptions that occur during the execution. Logs the traceback and returns a 500 Internal Server Error response with the error message. |


<br>
<br>
<br>

## Acknowledgments
- Credits to the original "Qwickly" application for inspiration.
- Thanks to all contributors who have invested their time in improving this project.
