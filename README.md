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

<img width="50%" alt="Screenshot 2023-12-02 at 16 14 43" src="https://github.com/rorosaga/Classlink/assets/133862511/c1df9948-70c9-40b8-94c6-7c1f530f7c0e">

<img width="50%" alt="Screenshot 2023-12-02 at 16 14 55" src="https://github.com/rorosaga/Classlink/assets/133862511/32d44463-d570-47f1-98fe-ea10bf551c22">

<img width="50%" alt="Screenshot 2023-12-02 at 16 15 09" src="https://github.com/rorosaga/Classlink/assets/133862511/ce815f88-0b4a-4739-a686-0a952c86e816">

<img width="50%" alt="Screenshot 2023-12-02 at 16 15 20" src="https://github.com/rorosaga/Classlink/assets/133862511/dec8a74f-8e33-43e4-9cbc-5239556ef250">

<img width="50%" alt="Screenshot 2023-12-02 at 16 15 34" src="https://github.com/rorosaga/Classlink/assets/133862511/b78ff57f-f35a-4572-b42f-c733522d3c07">

<img width="50%" alt="Screenshot 2023-12-02 at 16 17 36" src="https://github.com/rorosaga/Classlink/assets/133862511/45c551ac-62e8-4e27-9b61-e02aa260ae42">

<img width="50%" alt="Screenshot 2023-12-02 at 16 17 42" src="https://github.com/rorosaga/Classlink/assets/133862511/c540859e-273c-4c79-866e-7414d636fe7d">

<img width="50%" alt="Screenshot 2023-12-02 at 16 17 55" src="https://github.com/rorosaga/Classlink/assets/133862511/222e27c1-7217-478e-a6f5-04f34efecbcc">

<img width="50%" alt="Screenshot 2023-12-02 at 16 18 09" src="https://github.com/rorosaga/Classlink/assets/133862511/f9c52dd1-f500-47c6-88af-850f991390a8">

<img width="50%" alt="Screenshot 2023-12-02 at 16 18 13" src="https://github.com/rorosaga/Classlink/assets/133862511/88d232f7-7bba-4381-9892-27f7aa0ed987">

<img width="50%" alt="Screenshot 2023-12-02 at 16 18 18" src="https://github.com/rorosaga/Classlink/assets/133862511/d823b01f-2c69-46fb-beac-e2f0ecb6d525">

<img width="50%" alt="Screenshot 2023-12-02 at 16 18 27" src="https://github.com/rorosaga/Classlink/assets/133862511/f4d38308-5c13-4f8a-b088-24ace9e4e351">

<img width="50%" alt="Screenshot 2023-12-02 at 16 18 34" src="https://github.com/rorosaga/Classlink/assets/133862511/5ce32413-2d12-4286-9a96-16ba8a793548">

<img width="50%" alt="Screenshot 2023-12-02 at 16 18 38" src="https://github.com/rorosaga/Classlink/assets/133862511/78d529b8-9589-47df-857b-b94f6cdabf1f">

## Acknowledgments

- Credits to the original "Qwickly" application for inspiration.
- Thanks to all contributors who have invested their time in improving this project.
