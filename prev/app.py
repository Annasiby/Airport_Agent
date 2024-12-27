
from flask import Flask, request, jsonify, render_template, session
import os
import requests
import re
from uuid import uuid4  # To generate unique user IDs
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationEntityMemory

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for sessions

# Set API Keys

os.environ["GOOGLE_API_KEY"] = "AIzaSyBu10Xc6bESbEMFiHIfqhNkqRsVG1wpSZk"
AVIATIONSTACK_API_KEY = "b5311e08d9232bb2d85da628a1530c9e"

# Initialize the Language Model with Chat capabilities
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Prompt Template for Memory
template = """
The following is a conversation between an AI assistant and a user. The AI uses the entities and conversation history to provide helpful contextual responses.
Entities: {entities}
Conversation History: {history}
User: {input}
AI:
"""
prompt = PromptTemplate(input_variables=["entities", "history", "input"], template=template)

# Initialize Entity Memory
entity_memory = ConversationEntityMemory(llm=llm)

# Initialize Conversation Memory
conversation_memory = ConversationChain(llm=llm, memory=entity_memory, prompt=prompt)

# Function to generate a unique user ID if one doesn't exist
def get_user_id():
    if 'user_id' not in session:
        session['user_id'] = str(uuid4())  # Generate a unique user ID using UUID
    return session['user_id']

# Function to clean and format responses
def clean_response(response):
    # Remove bold formatting and extra asterisks
    response = re.sub(r"\*\*(.*?)\*\*", r"\1", response)  # Removes bold (**) formatting
    response = re.sub(r"^\* ", "", response, flags=re.MULTILINE)  # Removes asterisks (*) from bullet points
    return response
# Function to get flight status from AviationStack API
def get_flight_status(flight_number):
    url = "http://api.aviationstack.com/v1/flights"
    params = {
        "access_key": AVIATIONSTACK_API_KEY,
        "flight_iata": flight_number
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()

        # Log response for debugging
        print("AviationStack API Response:", data)

        if "data" in data and len(data["data"]) > 0:
            flight_info = data["data"][0]
            departure_airport = flight_info.get("departure", {}).get("airport", "unknown airport")
            departure_time = flight_info.get("departure", {}).get("estimated", "unknown time")
            arrival_airport = flight_info.get("arrival", {}).get("airport", "unknown airport")
            arrival_time = flight_info.get("arrival", {}).get("estimated", "unknown time")
            flight_status = flight_info.get("flight_status", "unknown status")
            return (
                f"Flight {flight_number} is currently {flight_status}. It is scheduled to depart from "
                f"{departure_airport} at {departure_time} and arrive at {arrival_airport} at {arrival_time}."
            )
        else:
            return f"Sorry, I couldn't find any information for flight number {flight_number}."
    except Exception as e:
        return f"An error occurred while fetching flight data: {e}"

@app.route('/')
def home():
    """
    Render the homepage with the chat interface.
    """
    user_id = get_user_id()  # Get the user's ID for the session
    return render_template('index.html', user_id=user_id)

@app.route('/activity')
def activity():
    return render_template('activity.html')

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handle user input and return the assistant's response.
    """
    user_input = request.json.get('message', '')

    if not user_input:
        return jsonify({"response": "Please enter a valid message."})

    # Check if user is asking about flight status and ensure a valid flight number is provided
    if 'flight' in user_input.lower():
        # Extract flight number using regex (for example, AA100, BA200)
        match = re.search(r"\b[A-Z]{2}\d{3,4}\b", user_input)
        if match:
            flight_number = match.group(0)
            flight_status = get_flight_status(flight_number)
            return jsonify({"response": clean_response(flight_status).strip()})
        else:
            return jsonify({"response": "Please provide a valid flight number (e.g., AA100, BA200)."})

    # Otherwise, process the input and generate a response
    response = conversation_memory.run(input=user_input)
    response = clean_response(response)
    return jsonify({"response": response.strip()})

@app.route('/entities', methods=['GET'])
def get_entities():
    """
    Debug endpoint to retrieve stored entities.
    """
    entities = entity_memory.load_memory_variables({})
    return jsonify({"entities": entities})

if __name__ == '__main__':
    app.run(debug=True)
