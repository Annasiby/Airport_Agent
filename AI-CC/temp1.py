"""import os
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import LLMChain

# Set up Google API key and model
os.environ["GOOGLE_API_KEY"] = "AIzaSyBu10Xc6bESbEMFiHIfqhNkqRsVG1wpSZk"  # Replace with actual API key

# Initialize the GoogleGenerativeAI client
llm = GoogleGenerativeAI(
    google_api_key=os.environ["GOOGLE_API_KEY"],
    model="gemini-1.5-flash",  # Ensure this is the correct model name
    temperature=0.7
)

# Define prompt templates
greeting_prompt = PromptTemplate(
    input_variables=["agent_name", "company_name"],
    template="Hello, thank you for calling {company_name}. My name is {agent_name}. How may I assist you today?"
)

flight_booking_prompt = PromptTemplate(
    input_variables=["customer_name", "destination", "flight_date"],
    template="Thank you for your interest in booking with SkyFly. {customer_name}, I can assist you with booking a flight to {destination} on {flight_date}. Let me confirm availability and finalize the booking for you."
)

flight_cancellation_prompt = PromptTemplate(
    input_variables=["customer_name", "flight_number"],
    template="I'm sorry to hear that you need to cancel your flight, {customer_name}. I will begin the cancellation process for flight {flight_number}. Please give me a moment."
)

status_update_prompt = PromptTemplate(
    input_variables=["flight_number"],
    template="I can assist you with a status update for flight {flight_number}. Please hold on while I gather the latest information."
)

closing_prompt = PromptTemplate(
    input_variables=["company_name"],
    template="Thank you for choosing {company_name}. If you have any further questions, feel free to reach out to us anytime. Safe travels!"
)

# Create LLMChain instances for each prompt template
greeting_chain = LLMChain(llm=llm, prompt=greeting_prompt)
booking_chain = LLMChain(llm=llm, prompt=flight_booking_prompt)
cancellation_chain = LLMChain(llm=llm, prompt=flight_cancellation_prompt)
status_chain = LLMChain(llm=llm, prompt=status_update_prompt)
closing_chain = LLMChain(llm=llm, prompt=closing_prompt)

# Define a function to generate AI responses using the LLMChain
def generate_response(chain, variables):
    return chain.invoke(variables)

# Customer Interaction Example
def handle_customer_call():
    # Greeting
    agent_name = "Andria"
    company_name = "SkyFly Airport Services"
    greeting_response = generate_response(greeting_chain, {"agent_name": agent_name, "company_name": company_name})
    print(f"Agent: {greeting_response}")

    # Flight Booking
    customer_name = "Ravi"
    destination = "New York"
    flight_date = "December 15, 2024"
    booking_response = generate_response(booking_chain, {"customer_name": customer_name, "destination": destination, "flight_date": flight_date})
    print(f"Agent: {booking_response}")

    # Flight Cancellation
    flight_number = "SF12345"
    cancellation_response = generate_response(cancellation_chain, {"customer_name": customer_name, "flight_number": flight_number})
    print(f"Agent: {cancellation_response}")

    # Status Update
    status_response = generate_response(status_chain, {"flight_number": flight_number})
    print(f"Agent: {status_response}")

    # Closing
    closing_response = generate_response(closing_chain, {"company_name": company_name})
    print(f"Agent: {closing_response}")

# Run the interaction
handle_customer_call()"""
import os
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationEntityMemory

from langchain.chains import LLMChain


# Set API Key securelyAIzaSyBu10Xc6bESbEMFiHIfqhNkqRsVG1wpSZk
os.environ["GOOGLE_API_KEY"] = "AIzaSyBu10Xc6bESbEMFiHIfqhNkqRsVG1wpSZk"  # Replace with a valid API key

# Initialize the Language Model
llm = GoogleGenerativeAI(
    google_api_key=os.environ["GOOGLE_API_KEY"],
    model="gemini-1.5-flash",
    temperature=0.7
)

# Define prompt templates
PROMPTS = {
    "greeting": PromptTemplate(
        input_variables=["airport_name", "agent_name"],
        template="Hello! Welcome to {airport_name} Airport. My name is {agent_name}. How can I assist you today?"
    ),
    "verification": PromptTemplate(
        input_variables=["relevant_info"],
        template="Before we proceed, may I have your flight number and {relevant_info} for verification purposes?"
    ),
    "acknowledgment": PromptTemplate(
        input_variables=["customer_name", "issue_summary"],
        template="I understand you're facing {issue_summary}, {customer_name}. I'll do my best to help resolve this issue."
    ),
    "resolution": PromptTemplate(
        input_variables=["customer_name", "time_frame"],
        template="{customer_name}, I've completed the necessary steps. You should see the changes within {time_frame}."
    ),
    "closing": PromptTemplate(
        input_variables=["airport_name"],
        template="Thank you for contacting {airport_name}. Is there anything else I can assist you with before we conclude our conversation?"
    )
}

# LLM Chains
CHAINS = {key: LLMChain(llm=llm, prompt=prompt) for key, prompt in PROMPTS.items()}


# Define functions for each interaction phase
def greeting(airport_name, agent_name):
    return CHAINS["greeting"].run({"airport_name": airport_name, "agent_name": agent_name})

def verification(is_verified, relevant_info=None):
    if is_verified:
        return "Verification successful. Proceeding to the next step."
    else:
        return CHAINS["verification"].run({"relevant_info": relevant_info})

def acknowledgment(customer_name, issue_summary, details_required=False, has_invoice_number=False, invoice_number=None):
    """
    Provide an acknowledgment response based on the situation.
    - `details_required`: If True, request more information.
    - `has_invoice_number`: If True, acknowledge with the invoice number.
    - `invoice_number`: Specific invoice number if available.
    """
    return CHAINS["acknowledgment"].run({"customer_name": customer_name, "issue_summary": issue_summary})

def handle_airport_query():
    """
    Simulate an airport agent interaction based on different scenarios.
    """
    # Initial greeting
    print(greeting("John F. Kennedy International Airport", "AI Assistant"))

    # Simulating a customer query and verification
    print("\nCustomer: Hi AI assistant, I'm having trouble with my luggage handling. "
          "My flight number is AA1234.")
    
    print(verification(True))  # Assuming the verification is successful

    # Acknowledging customer's issue and providing assistance
    customer_name = "Sarah"
    issue_summary = "luggage handling issue"
    print(acknowledgment(customer_name, issue_summary))

    # Asking for more details if the customer hasn't provided them yet
    print("\nCustomer: The luggage was damaged during transit. Can you help me file a claim?")
    print(acknowledgment(customer_name, issue_summary))

    # Simulating a flight status inquiry
    print("\nCustomer: What's the current status of my flight AA1234?")
    print(CHAINS["resolution"].run({"customer_name": customer_name, "time_frame": "immediately"}))

    # Simulating a baggage storage inquiry
    print("\nCustomer: Can I store my luggage here while I run some errands?")
    print(CHAINS["resolution"].run({"customer_name": customer_name, "time_frame": "within 15 minutes"}))

    # Final closing message
    print("\nClosing: Thank you for contacting John F. Kennedy International Airport. Is there anything else I can assist you with before we conclude our conversation?")

if __name__ == "__main__":
    handle_airport_query()
