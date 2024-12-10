import os
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationEntityMemory

from langchain.chains import LLMChain


# Set API Key securelyAIzaSyBu10Xc6bESbEMFiHIfqhNkqRsVG1wpSZk
os.environ["GOOGLE_API_KEY"] = ""  # Replace with a valid API key

# Initialize the Language Model
llm = GoogleGenerativeAI(
    google_api_key=os.environ["GOOGLE_API_KEY"],
    model="gemini-1.5-flash",
    temperature=0.7
)

# Define prompt templates
PROMPTS = {
    "greeting": PromptTemplate(
        input_variables=["company_name", "agent_name"],
        template="Hello, thank you for calling {company_name}. My name is {agent_name}. How may I assist you today?"
    ),
    "verification": PromptTemplate(
        input_variables=["relevant_info"],
        template="Before we proceed, may I have your full name and {relevant_info} for verification purposes?"
    ),
    "acknowledgment": PromptTemplate(
        input_variables=["customer_name", "issue_summary"],
        template="I’m sorry to hear about the inconvenience, {customer_name}. I understand you’re facing {issue_summary}. I’ll do my best to resolve this for you as quickly as possible."
    ),
    "resolution": PromptTemplate(
        input_variables=["customer_name", "time_frame"],
        template="{customer_name}, I’ve completed the necessary steps. You should see the changes/effects within {time_frame}. Is there anything else I can assist you with today?"
    ),
    "closing": PromptTemplate(
        input_variables=["company_name"],
        template="If you have any other questions in the future, please don’t hesitate to call us. Goodbye and thank you again for calling {company_name}!"
    )
}

# LLM Chains
CHAINS = {key: LLMChain(llm=llm, prompt=prompt) for key, prompt in PROMPTS.items()}


# Define functions for each interaction phase
def greeting(company_name, agent_name):
    return CHAINS["greeting"].run({"company_name": company_name, "agent_name": agent_name})


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
    if has_invoice_number and invoice_number:
        return (
            f"Agent: I'm sorry to hear about the billing discrepancy on invoice #{invoice_number}, {customer_name}. "
            "I understand this is frustrating. I'm looking into it now and will contact you within 24 hours with a resolution."
        )
    elif details_required:
        return (
            f"Agent: I'm sorry to hear about the billing discrepancy on your last invoice, {customer_name}. "
            "To help me resolve this quickly, could you please tell me more about the issue? For example, what is the discrepancy? "
            "What amount was expected versus what you were billed? Once I have this information, I can begin investigating."
        )
    else:
        return (
            f"Agent: I'm sorry to hear about the billing discrepancy on your last invoice, {customer_name}. "
            "I understand this is inconvenient. Could you please provide me with your invoice number so I can investigate this right away? "
            "I'll get back to you within 24 hours with an update."
        )


def handle_customer_call():
    """
    Simulate a customer-agent interaction based on different scenarios.
    """
    # Initial greeting
    print(greeting("TechCorp", "Alex"))

    # Simulating a customer query and verification
    print("Customer: Hi Alex, thanks for answering. I'm having trouble with my internet connection. "
          "It keeps dropping out intermittently throughout the day. I've tried restarting my modem and router several times, "
          "but the problem persists. My account number is 1234567.")
    
    print(verification(True))  # Assuming the verification is successful

    # Acknowledging customer's issue and providing assistance based on details
    customer_name = "John"
    issue_summary = "billing discrepancy on your last invoice"
    print(acknowledgment(customer_name, issue_summary, has_invoice_number=True, invoice_number="123456"))

    # Asking for more details if the customer hasn't provided them yet
    print("\nCustomer: I noticed I was charged $100 more than expected on my last invoice. Can you look into it?")
    print(acknowledgment(customer_name, issue_summary, details_required=True))


    # Final closing message
    print("\nCustomer: I'm not sure which invoice has the issue. Can you help me find it?")
    print(acknowledgment(customer_name, issue_summary))

    print("\nClosing: Goodbye and thank you again for calling TechCorp!")


if __name__ == "__main__":
    handle_customer_call()
