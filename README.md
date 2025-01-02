
 Airport AI Agent 

Project Description

The Airport AI Agent is an AI-powered virtual assistant designed to streamline airport operations by providing conversational support for passengers. It utilizes advanced natural language processing (NLP) models and integrates third-party APIs to offer services such as flight schedules, health recommendations, and task automation.




Features

1. Flight Schedule Assistance:

Provides up-to-date flight information using AviationStack API.



2. Conversation Memory:

Maintains and uses conversation context to deliver personalized responses using LangChain's entity memory.



3. Health Recommendations:

Handles queries related to common health concerns.



4. Report Generation:

Generates conversation summaries and graphical reports for user insights.



5. Activity Logs:

Tracks and displays user activity for better monitoring.





---

Project Structure

|-- app.py                 # Main Flask application  
|-- templates/             # HTML files for web interface  
|   |-- index.html         # Main chat interface  
|   |-- report.html        # Report page  
|   |-- activity.html      # Activity log page  
|-- requirements.txt       # Project dependencies  
|-- README.txt             # Documentation file  
|-- .env                   # Environment variables (API keys)


---

Prerequisites

Python 3.10 or higher

Pip package manager

Internet access for API calls



---

Installation and Setup

1. Clone the repository:

git clone <>  
cd Airport_Agent


2. Create and activate a virtual environment:

python -m venv venv  
source venv/bin/activate  # On Windows: venv\Scripts\activate


3. Install dependencies:

pip install -r requirements.txt


4. Set up environment variables:

Create a .env file in the root directory.

Add the following keys:

GOOGLE_API_KEY=<your_google_api_key>  
AVIATIONSTACK_API_KEY=<your_aviationstack_api_key>



5. Run the application:

python app.py

Access the app at http://127.0.0.1:5000 in your browser.





---

Usage

Chat Interface

Ask queries about flight schedules, health advice, or general information.

Example inputs:

"What is the status of flight AA123?"

"What are common symptoms of the flu?"



Activity Log

View logged activities by navigating to /activity.


Generate Reports

Access summarized conversation reports at /report.



---

Troubleshooting

1. ModuleNotFoundError:

Ensure all dependencies are installed using pip install -r requirements.txt.



2. API Key Errors:

Verify the keys in the .env file.



3. NumPy Warnings:

Ensure the correct Python and NumPy versions are installed.



4. Server Issues:

Check if the Flask app is running and accessible at the specified URL.





---

Technologies Used

Python

Flask

LangChain

Google Gemini API

AviationStack API

Matplotlib

HTML/CSS



---

License

This project is licensed under the MIT License. See LICENSE.txt for details.


---

Contributor

Minnu Anna Siby



---

For any queries or issues, feel free to raise them in the project's repository or contact the contributor.

