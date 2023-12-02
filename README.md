<h1 align="center">Snappy</h1>
<br>

## Overview
The Attendance Management System is a digital platform designed to enhance the management and tracking of students' attendance. It's built upon the concept of the "Qwickly" application, but with several advancements for accuracy and user experience. This system employs a combination of authentication methods, requiring individual accounts validated through university email credentials.

<br>
<br>

## Features

- **Account Creation & Authentication**: Users create accounts authenticated via university email, ensuring secure access.
- **Three-State Attendance Verification**: Incorporates Red, Orange, and Green statuses to accurately reflect student attendance.
  - **Red Status**: Marks students absent if not registered in the building by the Face ID system and no code input.
  - **Orange Status**: For students who input the code but aren't registered by Face ID. Requires manual verification by the teacher.
  - **Green Status**: Students who input the code and are verified by Face ID are automatically marked present.
- **Manual Attendance Adjustment**: Teachers can manually alter attendance records for flexibility and accuracy.
- **Dynamic Verification Code**: Uses a serverless function to generate a new verification code every 30 seconds for enhanced security.
- **Time Tracking**: Marks students late based on their entry time into the classroom.

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
  <br><br>When the professor logs in the following screen is presented, displaying a successfull login and the name of the user.
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

<p align="center">
  <img width="75%" alt="Screenshot 10" src="https://github.com/rorosaga/Classlink/assets/133862511/88d232f7-7bba-4381-9892-27f7aa0ed987">
  <br><br><br>The following page will show displaying the code necessary for the students to complete the attendance process
  <br><br>
</p>

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
  <br>Text for Image 1
</p>



<p align="center">
  <img width="75%" alt="Screenshot 3" src="https://github.com/rorosaga/Classlink/assets/133862511/ce815f88-0b4a-4739-a686-0a952c86e816">
  <br>Text for Image 3
</p>

<p align="center">
  <img width="75%" alt="Screenshot 4" src="https://github.com/rorosaga/Classlink/assets/133862511/dec8a74f-8e33-43e4-9cbc-5239556ef250">
  <br>Text for Image 4
</p>



<br><br>
## Snappy's Error Handling System

<p align="center">
  <img width="75%" alt="Screenshot 2" src="https://github.com/rorosaga/Classlink/assets/133862511/32d44463-d570-47f1-98fe-ea10bf551c22">
  <br>Text for Image 2
</p>

<p align="center">
  <img width="75%" alt="Screenshot 5" src="https://github.com/rorosaga/Classlink/assets/133862511/b78ff57f-f35a-4572-b42f-c733522d3c07">
  <br>Text for Image 5
</p>


## Acknowledgments
- Credits to the original "Qwickly" application for inspiration.
- Thanks to all contributors who have invested their time in improving this project.
