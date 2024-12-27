import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationEntityMemory

# Set Google API Key (replace with your actual key)
os.environ["GOOGLE_API_KEY"] = "AIzaSyBu10Xc6bESbEMFiHIfqhNkqRsVG1wpSZk"

# Initialize the Language Model with Chat capabilities
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Prompt Template for Memory
template = """
The following is a conversation between an AI assistant and a user (farmer). The AI uses the entities and conversation history to provide helpful contextual responses about farm equipment troubleshooting, machinery issues, and maintenance reminders.
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

def real_time_conversation():
    """
    Handles a real-time conversation with memory integration, specifically for farm equipment troubleshooting.
    """
    print("Welcome to the Farm Equipment Troubleshooting Assistant!")
    print("Type 'exit' to end the conversation.\n")
    print("How can I assist you with your farm machinery today?\n")
    
    while True:
        # Get user input (farmer's input about machinery issues)
        user_input = input("Farmer: ")

        # Check for exit condition
        if user_input.lower() == "exit":
            print("Agent: Thank you for using the Farm Equipment Assistant. Have a great day on the farm!")
            break
        
        # Process the input and generate a response
        response = conversation_memory.run(input=user_input)
        print(f"Agent: {response.strip()}")
    
    # At the end, display stored entities for debugging
    entities = entity_memory.load_memory_variables({})
    print(f"\nStored entities: {entities}")

if __name__ == "__main__":
    real_time_conversation()
