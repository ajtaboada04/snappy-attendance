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

## Initial Screen

<div style="display: flex; flex-wrap: wrap;">

  <div style="flex: 1; order: 1; margin-right: 20px;">
    <img width="300" src="https://github.com/rorosaga/Classlink/assets/133862511/a27df24d-9a92-48e0-8741-83d14f4a9fbc" alt="Image 1">
  </div>

  <div style="flex: 1; order: 2;">
    <!-- Your code goes here -->
    ```python
    print("Hello, World!")
    ```
  </div>

  <div style="flex: 1; order: 3; margin-right: 20px;">
    <img width="300" alt="Image 2" src="https://github.com/rorosaga/Classlink/assets/133862511/3bca3278-c29c-4db1-a6d7-6e28927dddf3">
  </div>

  <div style="flex: 1; order: 4;">
    <!-- Your code goes here -->
    ```python
    print("Another code example")
    ```
  </div>

  <!-- Continue this pattern for additional images and code blocks -->

</div>





## Acknowledgments

- Credits to the original "Qwickly" application for inspiration.
- Thanks to all contributors who have invested their time in improving this project.
