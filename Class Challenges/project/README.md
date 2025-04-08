# YOUR PROJECT TITLE
## Video Demo:  <URL https://youtu.be/aUr5Z94uEto>
### Description: The **Web Vacation** is an interactive and intuitive application developed using Python and Streamlit, designed to manage employee vacations. This application is suitable for organizations looking for a streamlined way to track, approve, and visualize vacation schedules. It incorporates features for user authentication, role-based access control (manager and employee roles), and an interactive calendar to manage and visualize employee vacations.
---
## Key Features
### 1. **User Management**
The application provides robust user management functionalities, allowing managers to:

- **Create new users**:
  - Add employees to the system with essential information like name, email, password, profession, and start date in the company.
  - Specify whether the user has managerial access or is a regular employee.

- **Modify existing users**:
  - Update user details, including profession, start date, and password.
  - Assign managerial privileges when necessary.

- **Delete users**:
  - Remove employees from the system if they are no longer part of the organization.

### 2. **Vacation Management**

Managers and employees can interact with an advanced calendar interface to manage vacations:

- **Add Vacations**:
  - Employees can select start and end dates for their vacation requests.
  - Managers can approve or deny vacation requests based on company policies.

- **View Vacations**:
  - A shared calendar displays all scheduled vacations, categorized by user and profession.
  - Each event includes details such as the employee's name and vacation dates.

- **Modify or Delete Vacations**:
  - Managers can click on a scheduled vacation on the calendar to update the vacation dates or delete it entirely.

### 3. **Role-Based Access Control**
The system distinguishes between managers and employees:

- **Managers**:
  - Have access to all functionalities, including creating, modifying, and deleting users or vacations.
  - Can view unencrypted passwords for security and recovery purposes.

- **Employees**:
  - Can log in to view their vacation days, request new vacations, and manage their personal data.
  - Have limited access to only their personal vacation details.

### 4. **Interactive Calendar**
The calendar is a central feature of the system:

- Displays all vacations in a visual format.
- Allows users to interact with events by clicking on them to edit or delete.
- Profession-based color coding (e.g., veterinarians in green, nurses in blue, interns in purple).

### 5. **Vacation Days Calculation**
The system calculates available vacation days for each employee based on their start date in the company. Employees and managers can view:

- Total vacation days earned.
- Vacation days already taken.
- Remaining vacation days available for request
---
###Architecture

###1. **Backend**

- **Database**: SQLite is used to store user data and vacation records.
- **SQLAlchemy ORM**: Manages interactions between the Python code and the database.
- **CRUD Functions**:
  - Implemented for creating, reading, updating, and deleting users and vacations.
  - Ensures smooth database operations.

### 2. **Frontend**
- **Streamlit Framework**:
  - Provides an interactive web interface.
  - Features such as tabs, buttons, and forms enable a user-friendly experience.

- **Streamlit Calendar**:
  - Custom interactive calendar widget for managing and viewing vacations.

### 3. **Security**
- Passwords are hashed using the Werkzeug library for secure storage.
- Managers can access unencrypted passwords when necessary for recovery purposes.

---

## Files and Structure

1. **`web_vacation.py`**:
   - The main entry point for running the application.
   - Manages routing between the calendar page and user management page.

2. **`calendar_page.py`**:
   - Contains the implementation for the interactive calendar.
   - Handles vacation addition, modification, and deletion functionalities.

3. **`management_page.py`**:
   - Manages the creation, modification, and deletion of user accounts.
   - Includes profession-based color coding and role management.

4. **`crud.py`**:
   - Implements the backend logic for database operations.
   - Contains functions for creating, reading, updating, and deleting users and vacations.

5. **`calendar_options.json`**:
   - JSON file defining configuration options for the calendar widget, such as time slots and display settings.

6. **`db_users.sqlite`**:
   - SQLite database file storing user and vacation data.

7. **`requirements.txt`**:
   - Lists the dependencies required to run the project, including Streamlit, SQLAlchemy, and Werkzeug.

---

## How to Run the Application

### Prerequisites
- Python 3.8 or later.
- Required dependencies (listed in `requirements.txt`).

### Setup
1. Clone the repository to your local machine.
2. Install the dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run web_vacation.py
   ```
4. Access the application in your web browser at `http://localhost:8501`.

---

## Use Cases

1. **Human Resources Management**:
   - Streamline vacation scheduling and tracking for employees.
   - Provide an overview of all employee vacations to avoid scheduling conflicts.

2. **Employee Self-Service**:
   - Enable employees to request vacations and track their remaining vacation days.

3. **Role-Based Permissions**:
   - Ensure that sensitive operations, such as viewing unencrypted passwords, are restricted to managers.

---
