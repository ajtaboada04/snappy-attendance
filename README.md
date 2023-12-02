# Attendance Management System

## Overview

The Attendance Management System is a digital platform designed to enhance the management and tracking of students' attendance. It's built upon the concept of the "Qwickly" application, but with several advancements for accuracy and user experience. This system employs a combination of authentication methods, requiring individual accounts validated through university email credentials.

## Features

- **Account Creation & Authentication**: Users create accounts authenticated via university email, ensuring secure access.
- **Three-State Attendance Verification**: Incorporates Red, Orange, and Green statuses to accurately reflect student attendance.
  - **Red Status**: Marks students absent if not registered in the building by the Face ID system and no code input.
  - **Orange Status**: For students who input the code but aren't registered by Face ID. Requires manual verification by the teacher.
  - **Green Status**: Students who input the code and are verified by Face ID are automatically marked present.
- **Manual Attendance Adjustment**: Teachers can manually alter attendance records for flexibility and accuracy.
- **Dynamic Verification Code**: Uses a serverless function to generate a new verification code every 30 seconds for enhanced security.
- **Time Tracking**: Marks students late based on their entry time into the classroom.


## How to Navigate the System:

<img width="1152" alt="Screenshot 2023-12-02 at 16 15 34" src="https://github.com/rorosaga/Classlink/assets/133862511/3bca3278-c29c-4db1-a6d7-6e28927dddf3">
<img width="1152" alt="Screenshot 2023-12-02 at 16 17 36" src="https://github.com/rorosaga/Classlink/assets/133862511/cf78ce40-ed1a-4428-a3db-22409f4a3a2d">
<img width="1146" alt="Screenshot 2023-12-02 at 16 17 42" src="https://github.com/rorosaga/Classlink/assets/133862511/17f73cb4-52ae-4657-8bc9-028114d9ad8f">
<img width="1147" alt="Screenshot 2023-12-02 at 16 17 55" src="https://github.com/rorosaga/Classlink/assets/133862511/81625926-6d20-4f01-b6b5-5c9f22052024">
<img width="1109" alt="Screenshot 2023-12-02 at 16 18 09" src="https://github.com/rorosaga/Classlink/assets/133862511/f6b55581-0c18-4140-b630-17b3f5f8a7c1">
<img width="1158" alt="Screenshot 2023-12-02 at 16 18 13" src="https://github.com/rorosaga/Classlink/assets/133862511/b561b5a2-fd3c-41ba-ba95-630514068223">
<img width="1140" alt="Screenshot 2023-12-02 at 16 18 18" src="https://github.com/rorosaga/Classlink/assets/133862511/64a67dd7-5d94-4cee-9a74-727e7de04a62">
<img width="1151" alt="Screenshot 2023-12-02 at 16 18 27" src="https://github.com/rorosaga/Classlink/assets/133862511/46e846a2-79aa-46fb-9ff7-bd29d5c74eea">
<img width="1172" alt="Screenshot 2023-12-02 at 16 18 34" src="https://github.com/rorosaga/Classlink/assets/133862511/a27df24d-9a92-48e0-8741-83d14f4a9fbc">
<img width="1056" alt="Screenshot 2023-12-02 at 16 18 38" src="https://github.com/rorosaga/Classlink/assets/133862511/41bda402-bfe7-4233-81e1-182b90f81aaf">
<img width="1228" alt="Screenshot 2023-12-02 at 16 15 09" src="https://github.com/rorosaga/Classlink/assets/133862511/95518a91-c386-4c65-b723-1a501f3dfacd">
<img width="1078" alt="Screenshot 2023-12-02 at 16 15 20" src="https://github.com/rorosaga/Classlink/assets/133862511/0c848caa-ba66-43f1-bda0-d7172cced1ac">




## Acknowledgments

- Credits to the original "Qwickly" application for inspiration.
- Thanks to all contributors who have invested their time in improving this project.
