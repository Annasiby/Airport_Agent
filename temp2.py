import os
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Set API Key securely
os.environ["GOOGLE_API_KEY"] = "AIzaSyBCxU8jKiCsN172SxmEQ14yGwQkpQsfyWM"  # Replace with a valid API key

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
        input_variables=["relevant_info", "agent_name"],
        template="{agent_name}, before we proceed, may I have your flight number and {relevant_info} for verification purposes?"
    ),
    "acknowledgment": PromptTemplate(
        input_variables=["customer_name", "issue_summary", "agent_name"],
        template="{agent_name}, I understand you're facing {issue_summary}, {customer_name}. I'll do my best to help resolve this issue."
    ),
    "resolution": PromptTemplate(
        input_variables=["customer_name", "time_frame", "agent_name"],
        template="{agent_name}, I've completed the necessary steps for {customer_name}. You should see the changes within {time_frame}."
    ),
    "closing": PromptTemplate(
        input_variables=["airport_name", "agent_name"],
        template="Thank you for contacting {airport_name}. {agent_name}, is there anything else I can assist you with before we conclude our conversation?"
    )
}

# LLM Chains
CHAINS = {key: LLMChain(llm=llm, prompt=prompt) for key, prompt in PROMPTS.items()}


# Define functions for each interaction phase
def greeting(airport_name, agent_name):
    return CHAINS["greeting"].run({"airport_name": airport_name, "agent_name": agent_name})

def verification(is_verified, relevant_info=None, agent_name="AI Assistant"):
    if is_verified:
        return f"Agent: Verification successful. Proceeding to the next step."
    else:
        return CHAINS["verification"].run({"relevant_info": relevant_info, "agent_name": agent_name})

def acknowledgment(customer_name, issue_summary, agent_name="AI Assistant"):
    return CHAINS["acknowledgment"].run({"customer_name": customer_name, "issue_summary": issue_summary, "agent_name": agent_name})

def resolution(customer_name, time_frame, agent_name="AI Assistant"):
    return CHAINS["resolution"].run({"customer_name": customer_name, "time_frame": time_frame, "agent_name": agent_name})

def closing(airport_name, agent_name="AI Assistant"):
    return CHAINS["closing"].run({"airport_name": airport_name, "agent_name": agent_name})


# Define function to handle the entire airport query interaction
def handle_airport_query():
    """
    Simulate an airport agent interaction with customer, ensuring that the agent is always involved.
    """
    # Initial greeting
    agent_name = "Andria"
    airport_name = "John F. Kennedy International Airport"
    print("Agent: Hello! Welcome to John F. Kennedy International Airport. My name is Andria and I am your AI Assistant. How can I assist you today?")

    # Simulating a customer query and verification
    print("\nCustomer: Hi Andria, I'm having trouble with my luggage handling. My flight number is AA1234.")
    print("Agent: Verification successful. Proceeding to the next step.")

    # Acknowledging customer's issue and providing assistance
    customer_name = "Sarah"
    issue_summary = "luggage handling issue"
    print(f"Agent: I understand you're facing luggage handling issue, Sarah. I'll do my best to help resolve this issue.")

    # Simulating further assistance
    print("\nCustomer: The luggage was damaged during transit. Can you help me file a claim?")
    print(f"Agent: OH sure!.")

    # Simulating flight status inquiry
    print("\nCustomer: What's the current status of my flight AA1234?")
    print(f"Agent: I've completed the necessary steps for Sarah. You should see the changes within immediately.")

    # Simulating a baggage storage inquiry
    print("\nCustomer: Can I store my luggage here while I run some errands?")
    print(f"Agent: I've completed the necessary steps for Sarah. You should see the changes within 15 minutes.")

    # Final closing message
    print(f"Agent: Thank you for contacting John F. Kennedy International Airport. AI Assistant, is there anything else I can assist you with before we conclude our conversation?")

if __name__ == "__main__":
    handle_airport_query()


