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

## Conclusion
Your Django server is now up and running!

