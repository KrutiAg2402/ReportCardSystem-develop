# Student Report Card System

This project is a simple, user-friendly application that helps schools and tutors manage student records and academic results. It replaces bulky paper files with an organized digital system where each student has a single profile and a separate history of marks. The result is easier record keeping, quick access to report cards, and fewer mistakes in grading.

In daily use, teachers add student details and record marks for six core subjects. The system keeps personal information and marks in separate places so performance can be tracked over time without repeating demographic details. When marks are recorded, the system calculates totals, percentages, and a final grade automatically, removing manual math and making results consistent.

Teachers can perform all management tasks: add or update student profiles, enter or correct marks, review report cards, list all students, and remove records when needed. A convenient feature lets teachers update only the fields that change—leaving a field blank keeps the old value—so edits are quick and safe. Students have view-only access to their own report card using their unique identifier.

Report cards are presented clearly, with student information, subject-wise marks, and a summary showing total, percentage, and grade. The display is designed to be readable and suitable for sharing with parents or for printing.

Under the hood, the database enforces relationships so marks always belong to valid students, and deleting a student removes related marks automatically. The system also logs timestamps for when records are created or changed, providing a basic audit trail.

Overall, this project is aimed at small schools, coaching centers, or tutors who want a lightweight, dependable way to manage student information and results without complex setup. It is intentionally straightforward, focusing on essential features that improve accuracy, save time, and make academic record keeping more reliable.
