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

# Your Project Title

## Subsection Title

Text introducing your project or section.

```swift
// Your Swift code goes here
import SwiftUI
import YourLibraryName // Replace with the actual library name if needed

struct ContentView: View {
    @State var text = ""

    var body: some View {
        // Your SwiftUI code for the view
    }
}


## Acknowledgments

- Credits to the original "Qwickly" application for inspiration.
- Thanks to all contributors who have invested their time in improving this project.
