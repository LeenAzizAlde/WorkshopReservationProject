# KSU Workshop Reservation System

## Project Description
The KSU Workshop Reservation System is a Python application designed to manage workshops for King Saud University students.  
Students can register, log in, book workshops, and view their reservations.  
Admins can create new workshops and back up data easily.

---

## Features
- Student registration with input validation (ID, email, phone)
- Secure login with password hashing
- Workshop booking with capacity management
- View upcoming and booked workshops for each student
- Graphical User Interface (GUI) built with Tkinter
- Data backup to CSV files
- Transaction logging in `Transactions.log.txt`

---

## Requirements
- Python 3.x
- Python libraries:
  - `sqlite3`
  - `tkinter`
  - `hashlib`
  - `csv`
  - `datetime`
  - `random`
  - `re`

---
## Database
The system uses **SQLite** as its database to store all information securely.  
It has three main tables:

1. **stu** – stores student information including ID, first and last name, hashed password, email, and mobile number.
2. **workshop** – stores workshop details such as workshop ID, name, location, capacity, and schedule (date & time).
3. **reservation** – tracks which students have booked which workshops, linking the `stu` and `workshop` tables.
---
## How to Run
Clone the repository

