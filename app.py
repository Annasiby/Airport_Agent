from flask import Flask, request, jsonify, render_template, session
import os
import requests
import re
from uuid import uuid4
from datetime import datetime
import random
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import io
import base64
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationEntityMemory
activity_log = []
# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for sessions

# Set API Keys

os.environ["GOOGLE_API_KEY"] = "AIzaSyBu10Xc6bESbEMFiHIfqhNkqRsVG1wpSZk"
AVIATIONSTACK_API_KEY = "b5311e08d9232bb2d85da628a1530c9e"

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

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

def get_flight_schedule(flight_number):
    """
    Fetches the schedule of the given flight using the AviationStack API.
    """
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
            airline_name = flight_info.get("airline", {}).get("name", "Unknown Airline")
            departure_airport = flight_info.get("departure", {}).get("airport", "Unknown Airport")
            departure_time = flight_info.get("departure", {}).get("estimated", "Unknown Time")
            arrival_airport = flight_info.get("arrival", {}).get("airport", "Unknown Airport")
            arrival_time = flight_info.get("arrival", {}).get("estimated", "Unknown Time")
            flight_status = flight_info.get("flight_status", "Unknown Status")

            schedule = (
                f"Flight {flight_number} by {airline_name} is scheduled as follows:\n"
                f"Departure: {departure_airport} at {departure_time}\n"
                f"Arrival: {arrival_airport} at {arrival_time}\n"
                f"Current Status: {flight_status}"
            )
            return schedule
        else:
            return f"Sorry, I couldn't find any information for flight number {flight_number}."
    except Exception as e:
        return f"An error occurred while fetching the flight schedule: {e}"



def summarize_conversation():
    """
    Summarizes the conversation history using the memory's content.
    """
    try:
        # Get the current conversation history
        memory_variables = entity_memory.load_memory_variables({})
        history = memory_variables.get("history", "")

        # Check if history exists
        if not history.strip():
            print("No history found for summarization.")  # Debug log
            return "No conversation history available to summarize."

        # Generate summary using the LLM
        summary_prompt_text = f"Summarize the following conversation:\n{history}"
        print("Summary Prompt Text:", summary_prompt_text)  # Debug log
    
        # Pass the prompt directly to the LLM
        summary = llm({"input": summary_prompt_text})  # Adjust input for LLM if necessary
        print("Generated Summary:", summary)  # Debug log
        return summary.strip()
    except Exception as e:
        print(f"Error in summarize_conversation: {e}")  # Debug log
        return f"An error occurred while summarizing: {e}"


def clean_response(response):
    """
    Cleans the response by removing unnecessary formatting.
    """
    response = re.sub(r"\*\*(.*?)\*\*", r"\1", response)  # Removes bold (**) formatting
    response = re.sub(r"^\* ", "", response, flags=re.MULTILINE)  # Removes asterisks from bullet points
    return response


@app.route('/')
def home():
    """
    Render the homepage with the chat interface.
    """
    if 'user_id' not in session:
        session['user_id'] = str(uuid4())  # Generate a unique user ID using UUID
    print("Session User ID:", session['user_id'])
    return render_template('index.html', user_id=session['user_id'])


@app.route('/report', methods=['GET'])
def generate_report():
    # Sample data from a conversation with the Airport AI Agent
    queries = ['Flight Status', 'Baggage Status', 'Gate Information', 'Check-in Assistance', 'Flight Delay']
    responses = ['On Time', 'Delayed', 'Gate A5', 'Checked In', 'Delayed']
    response_times = [random.randint(1, 5) for _ in range(5)]  # Simulated response times (in seconds)
    satisfaction_scores = [random.randint(1, 5) for _ in range(5)]  # Satisfaction scores (1-5 scale)

    # Create a Bar chart for response times
    fig1 = go.Figure(data=go.Bar(x=queries, y=response_times, name='Response Time (seconds)', marker_color='blue'))
    fig1.update_layout(
        title="Response Time for Queries",
        xaxis_title="Query Type",
        yaxis_title="Response Time (seconds)",
        template="plotly_dark"
    )

    # Create a Bar chart for satisfaction scores
    fig2 = go.Figure(data=go.Bar(x=queries, y=satisfaction_scores, name='Satisfaction Score', marker_color='green'))
    fig2.update_layout(
        title="User Satisfaction Scores",
        xaxis_title="Query Type",
        yaxis_title="Satisfaction (1-5)",
        template="plotly_dark"
    )

    # Create a Pie chart for query types distribution
    query_counts = {'Flight Status': queries.count('Flight Status'), 
                    'Baggage Status': queries.count('Baggage Status'),
                    'Gate Information': queries.count('Gate Information'),
                    'Check-in Assistance': queries.count('Check-in Assistance'),
                    'Flight Delay': queries.count('Flight Delay')}

    fig3 = go.Figure(data=go.Pie(labels=list(query_counts.keys()), values=list(query_counts.values()), name="Query Distribution"))
    fig3.update_layout(
        title="Query Type Distribution",
        template="plotly_dark"
    )

    # Show the figures (graphs)
    fig1.show()
    fig2.show()
    fig3.show()

    # Generate a summary report text
    summary_report = """
    Airport AI Agent Conversation Report:
    

    1. Total Number of Queries: 5
    2. Average Response Time: {:.2f} seconds
    3. Average Satisfaction Score: {:.2f}


    Query Breakdown:
    - Flight Status: 1 query
    - Baggage Status: 1 query
    - Gate Information: 1 query
    - Check-in Assistance: 1 query
    - Flight Delay: 1 query


    Response Time and Satisfaction Scores:
    - Flight Status: 2 seconds, Satisfaction: 4
    - Baggage Status: 3 seconds, Satisfaction: 5
    - Gate Information: 1 second, Satisfaction: 4
    - Check-in Assistance: 4 seconds, Satisfaction: 3
    - Flight Delay: 5 seconds, Satisfaction: 2
    """.format(sum(response_times)/len(response_times), sum(satisfaction_scores)/len(satisfaction_scores))

    # Return the summary report text
    return summary_report



@app.route('/chat', methods=['POST'])
def chat():
    """
    Handle user input and return the assistant's response.
    """
    user_input = request.json.get('message', '')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current timestamp

    if not user_input:
        return jsonify({"response": "Please enter a valid message."})

    # Log the question and timestamp for activity tracking
    try:
        log_entry = {"user_id": session.get('user_id', 'Unknown User'), "message": user_input, "timestamp": timestamp}
        activity_log.append(log_entry)  # Log activity (replace with DB insertion for production)
    except Exception as e:
        print(f"Error logging activity: {e}")

    # Generate a conversation summary if requested
    if 'provide conversation summary' in user_input.lower():
        try:
            summary = summarize_conversation()
            user_id = session.get('user_id', 'Unknown User')  # Retrieve the user ID from the session
            response_message = (
                f"Report for User ID: {user_id}\n"
                f"Conversation Summary:\n{summary}"
            )
            return jsonify({"response": clean_response(response_message)})
        except Exception as e:
            return jsonify({"response": f"An error occurred while summarizing: {e}"})

    # Handle regular user queries
    try:
        response = conversation_memory.run(input=user_input)
        return jsonify({"response": clean_response(response.strip())})
    except Exception as e:
        return jsonify({"response": f"An error occurred: {e}"})

@app.route('/entities', methods=['GET'])
def get_entities():
    """
    Debug endpoint to retrieve stored entities.
    """
    entities = entity_memory.load_memory_variables({})
    return jsonify({"entities": entities})

@app.route('/activity', methods=['GET'])
def view_activity():
    """
    View logged user activities.
    """
    global activity_log
    return render_template('activity.html', activities=activity_log)

@app.route('/debug-history', methods=['GET'])
def debug_history():
    """
    Debug endpoint to view memory variables.
    """
    memory_variables = entity_memory.load_memory_variables({})
    return jsonify(memory_variables)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
