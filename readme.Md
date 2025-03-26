# Project Setup Guide

## Step 1: Clone the Project
Clone the repository to your local machine:
```sh
git clone <repository_url>
cd <repository_folder>
```

## Step 2: Create a `.env` File
In the root directory, create a `.env` file and copy the contents of `example.env` into it as it is.

## Step 3: Set Up a Virtual Environment

### Using `uv` (Recommended)
[uv](https://github.com/astral-sh/uv) is a fast and efficient package manager that helps with dependency management and virtual environment setup automatically.

To create a virtual environment and install dependencies, open the terminal and run:
```sh
uv sync
```
This will create a virtual environment and install dependencies automatically. No need to run `pip install -r requirements.txt` separately.

### Without `uv`
If you don’t have `uv`, you can manually create a virtual environment:
```sh
python -m venv .venv
```

Activate the virtual environment:
- **Windows:**
  ```sh
  .venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```sh
  source .venv/bin/activate
  ```

Once inside the virtual environment, install the required dependencies:
```sh
pip install -r requirements.txt
```

## Step 4: Run the Django Server
Start the Django server by running:
```sh
python manage.py runserver
```

## Step 5: Verify the Setup
After running the server, you will see a link in your terminal. Click on the link and navigate to:
```
http://127.0.0.1:8000/test/
```
You should see a message saying:
```
Django server is running
```

## Alternative: Setting Up from a ZIP File
If you have the project as a ZIP file, follow these steps:
1. Extract the ZIP file to a folder.
2. Open a terminal and navigate to the extracted folder.
3. Activate the virtual environment:
   - **Windows:**
     ```sh
     .venv\Scripts\activate
     ```
   - **Mac/Linux:**
     ```sh
     source .venv/bin/activate
     ```
4. Install dependencies using one of the following:
   - If using `uv` (recommended):
     ```sh
     uv sync
     ```
   - If using `pip`:
     ```sh
     pip install -r requirements.txt
     ```
5. Run the Django server:
   ```sh
   python manage.py runserver
   ```

## Conclusion
Your Django server is now up and running!

## Note:
To go to the full documentation of the APIs, visit:
```
http://127.0.0.1:8000/redoc/
```


## API Endpoints
Base URL: http://127.0.0.1:8000
### **Authentication APIs**

#### **Register User**
**Endpoint:** `POST /auth/register`

**Description:** Registers a new user with a username, email, and password.

**Request Body:**
```json
{
  "username": "testuser",
  "email": "testuser@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "Message": "Register Success",
  "status": true,
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "testuser@example.com"
  },
  "token": "generated_token"
}
```

#### **User Login**
**Endpoint:** `POST /auth/login`

**Description:** Authenticates a user using email and password.

**Request Body:**
```json
{
  "email": "testuser@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "message": "Logged In Success",
  "status": true,
  "token": "generated_token",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "testuser@example.com"
  }
}
```

### **Task Management APIs**

#### **Create Task**
**Endpoint:** `POST tasks/create_task`

**Description:** Allows an admin to create a new task.

**Headers:**
```json
{
  "Authorization": "Bearer <token>"
}
```

**Request Body:**
```json
{
  "title": "New Task",
  "description": "Task details",
  "priority": "high",
  "due_date": "2025-04-01"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Task assigned successfully",
  "task": {
    "id": 1,
    "title": "New Task",
    "admin_id": "admin_user",
    "priority": "high",
    "due_date": "2025-04-01"
  }
}
```

#### **Assign Task**
**Endpoint:** `POST /tasks/assign_task`

**Description:** Allows an admin to assign a task to a user.

**Headers:**
```json
{
  "Authorization": "Bearer <token>"
}
```

**Request Body:**
```json
{
  "task_id": 1,
  "assigned_to": 2
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Task assigned successfully",
  "task": {
    "id": 1,
    "title": "New Task",
    "assigned_by": "admin@example.com",
    "assigned_to": "user@example.com",
    "priority": "high",
    "due_date": "2025-04-01",
    "status": "pending"
  }
}
```

#### **Get Tasks Created by Admin**
**Endpoint:** `GET /tasks/get_tasks`

**Description:** Fetches all tasks created by the admin.

**Headers:**
```json
{
  "Authorization": "Bearer <token>"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Tasks retrieved successfully",
  "task": [
    {
      "id": 1,
      "title": "New Task",
      "priority": "high",
      "due_date": "2025-04-01"
    }
  ]
}
```

#### **Get Assigned Tasks**
**Endpoint:** `GET /tasks/get_assigned_tasks`

**Description:** Fetches all tasks assigned by the admin.

**Headers:**
```json
{
  "Authorization": "Bearer <token>"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Tasks retrieved successfully",
  "task": [
    {
      "id": 1,
      "task_title": "New Task",
      "status": "pending",
      "assigned_to_username": "testuser",
      "assigned_to_email": "testuser@example.com",
      "assigned_by_username": "admin",
      "assigned_by_email": "admin@example.com",
      "created_at": "2025-03-25T12:00:00Z"
    }
  ]
}
```

#### **Get Assigned Tasks by Status**
**Endpoint:** `GET /tasks/get_assigned_tasks/<str:status>`
example: GET /tasks/get_assigned_tasks/pending

**Description:** Fetches all assigned tasks filtered by status.

**Headers:**
```json
{
  "Authorization": "Bearer <token>"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Tasks retrieved successfully",
  "task": [
    {
      "id": 1,
      "task_title": "New Task",
      "status": "pending",
      "assigned_to_username": "testuser",
      "assigned_to_email": "testuser@example.com",
      "assigned_by_username": "admin",
      "assigned_by_email": "admin@example.com",
      "created_at": "2025-03-25T12:00:00Z"
    }
  ]
}
```

#### **Get Tasks Assigned to a Specific User**
**Endpoint:** `GET /get_assigned_task_by_userid/<int:user_id>`
example: GET /tasks/get_assigned_task_by_userid/1

**Description:** Fetches all tasks assigned to a particular user.

**Headers:**
```json
{
  "Authorization": "Bearer <token>"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Tasks retrieved successfully",
  "task": [
    {
      "id": 1,
      "task_title": "New Task",
      "status": "pending",
      "assigned_to_username": "testuser",
      "assigned_to_email": "testuser@example.com",
      "assigned_by_username": "admin",
      "assigned_by_email": "admin@example.com",
      "created_at": "2025-03-25T12:00:00Z"
    }
  ]
}
```

## License
This project is for JoshTalks backend task submission.







