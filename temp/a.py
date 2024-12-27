import re
from flask import Flask, request, jsonify, render_template
import requests
import os

# Initialize Flask app
app = Flask(__name__)

# Set your API Key for the flight tracking service (e.g., AviationStack)
API_KEY = "b5311e08d9232bb2d85da628a1530c9e"
FLIGHT_API_URL = "http://api.aviationstack.com/v1/flights"

@app.route('/')
def home():
    """
    Render the homepage with the chat interface.
    """
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handle user input and return the assistant's response.
    """
    user_input = request.json.get('message', '')
    
    if not user_input:
        return jsonify({"response": "Please enter a valid message."})

    # Check if the user is asking for flight status (by looking for flight number)
    flight_number = extract_flight_number(user_input)
    if flight_number:
        response = get_flight_status(flight_number)
        return jsonify({"response": response})

    # Process the input and generate a response for other inquiries (e.g., farm equipment troubleshooting)
    response = "I'm sorry, I don't have information about that."
    return jsonify({"response": response})

def extract_flight_number(user_input):
    """
    Extract flight number from user input using regex.
    Example formats: AA1234, DL5678, etc.
    """
    flight_regex = r'\b([A-Z]{2,3}\d{1,4})\b'  # Matches flight numbers like AA1234, DL5678, etc.
    match = re.search(flight_regex, user_input)
    if match:
        return match.group(0)  # Return the flight number if found
    return None  # Return None if no flight number is found

def get_flight_status(flight_number):
    """
    Fetch flight status from the flight tracking API.
    """
    params = {
        'access_key': API_KEY,
        'flight_iata': flight_number
    }

    try:
        response = requests.get(FLIGHT_API_URL, params=params)
        data = response.json()

        # Check if data is available and return the status
        if data.get('data'):
            flight = data['data'][0]
            departure_airport = flight['departure']['airport']
            departure_time = flight['departure']['estimated'].get('departure', 'Not Available')
            arrival_airport = flight['arrival']['airport']
            arrival_time = flight['arrival']['estimated'].get('arrival', 'Not Available')

            return f"Flight {flight_number} is currently on time. It is scheduled to depart from {departure_airport} at {departure_time} and arrive at {arrival_airport} at {arrival_time}."
        else:
            return f"Sorry, I couldn't find information for flight {flight_number}. Please check the flight number and try again."
    except Exception as e:
        return f"An error occurred while retrieving flight status: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
