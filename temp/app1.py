from flask import Flask, request, jsonify, render_template
import os
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationEntityMemory

# Initialize Flask app
app = Flask(__name__)

# Set Google API Key and AviationStack API Key
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

# Function to get flight status from AviationStack API
def get_flight_status(flight_number):
    url = f"http://api.aviationstack.com/v1/flights"
    params = {
        'access_key': AVIATIONSTACK_API_KEY,
        'flight_iata': flight_number
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    # Check if the response contains valid data
    if 'data' in data and len(data['data']) > 0:
        flight_info = data['data'][0]
        return f"Flight {flight_number} is currently {flight_info['status']} and is scheduled to depart from {flight_info['departure']['airport']} at {flight_info['departure']['estimated']['departure']} and arrive at {flight_info['arrival']['airport']} at {flight_info['arrival']['estimated']['arrival']}."
    else:
        return f"Sorry, I couldn't find information for flight {flight_number}."

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
    
    # Check if user is asking about flight status
    if 'flight' in user_input.lower():
        # Extract flight number (for example: AA1234)
        flight_number = user_input.split()[-1]
        flight_status = get_flight_status(flight_number)
        return jsonify({"response": flight_status.strip()})
    
    # Otherwise, process the input and generate a response
    response = conversation_memory.run(input=user_input)
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
