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

<!-- Image on the left, text on the right -->
<p align="left">
  <img src="https://github.com/rorosaga/Classlink/assets/133862511/c1df9948-70c9-40b8-94c6-7c1f530f7c0e" alt="Screenshot" width="50%">
  <span>Your Text Here</span>
</p>

<!-- Text on the left, image on the right -->
<p align="right">
  <span>Your Text Here</span>
  <img src="https://github.com/rorosaga/Classlink/assets/133862511/32d44463-d570-47f1-98fe-ea10bf551c22" alt="Screenshot" width="50%">
</p>

<!-- Continue this pattern for other images and text -->




## Acknowledgments

- Credits to the original "Qwickly" application for inspiration.
- Thanks to all contributors who have invested their time in improving this project.
