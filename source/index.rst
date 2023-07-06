.. Khungulanga Backend API Documentation
=======================================

Overview
--------
The Khungulanga backend API serves as the server-side component for the Khungulanga mobile application. It provides the necessary functionality for early diagnosis of skin diseases using the ResNet50v2 architecture. The API allows users to interact with the machine learning models, store diagnostic history, and connect with dermatologists for further analysis.

Getting Started
---------------
To get started with the Khungulanga backend API, follow these steps:

1. Install Dependencies
   - Make sure you have Python and Django installed on your system.
   - Create a virtual environment and activate it.

2. Clone the Repository
   - Clone the Khungulanga backend repository from the Git repository.

     ```
     git clone https://github.com/jahnical/khungulanga.git
     ```

3. Install Requirements
   - Navigate to the project directory and install the required Python packages using pip.

     ```
     cd khungulanga-backend
     pip install -r requirements.txt
     ```

4. Configure the Database
   - Open the settings.py file and configure the database settings according to your setup.

5. Migrate Database
   - Run the migration command to create the necessary database tables.

     ```
     python manage.py migrate
     ```

6. Start the Development Server
   - Start the development server to run the API locally.

     ```
     python manage.py runserver 8000
     ```

7. Access the API
   - The API will be accessible at `http://localhost:8000`.

API Endpoints
-------------
The following endpoints are available in the Khungulanga backend API:

- `/api/diagnosis/`: Endpoint for diagnosing skin diseases.
- `/api/history/`: Endpoint for managing diagnostic history.
- `/api/users/`: Endpoint for managing user accounts.
- `/api/dermatologists/`: Endpoint for managing dermatologist profiles.

Refer to the API documentation for detailed information on each endpoint.

Indices and Tables
------------------
The following indices and tables provide quick access to different sections of the documentation:

* :ref:`genindex`: General Index
* :ref:`modindex`: Module Index
* :ref:`search`: Search
