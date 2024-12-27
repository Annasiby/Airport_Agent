
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
#import langchain.schema import AIMEssage, HumanMessage
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationEntityMemory
#from dotenv import load_dotenv
os.environ["GOOGLE_API_KEY"] = "AIzaSyBu10Xc6bESbEMFiHIfqhNkqRsVG1wpSZk"
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


def summarize_conversation():
    """
    Summarizes the conversation history using the memory's content.
    """
    try:
        # Get the current conversation history
        memory_variables = entity_memory.load_memory_variables({})  # Retrieve memory variables
        history = memory_variables.get("history", "")

        if not history.strip():
            return "No conversation history available to summarize."

        # Generate summary using the LLM
        summary_prompt = f"Summarize the following conversation:\n{history}"
        summary = llm(summary_prompt)
        return summary.strip()
    except Exception as e:
        return f"An error occurred while summarizing: {e}"


def real_time_conversation():
    """
    Handles a real-time conversation with memory integration.
    """
    print("Type 'provide conversation summary' to get a conversation summary or 'exit' to end the conversation.\n")

    while True:
        user_input = input("Customer: ")
        if user_input.lower() == "exit":
            print("Agent: Thank you for contacting us. Have a great day!")
            break
        elif user_input.lower() == "provide conversation summary":
            summary = summarize_conversation()
            print(f"Agent (Summary): {summary}")
        else:
            response = conversation_memory.run(input=user_input)
            print(f"Agent: {response.strip()}")

    # At the end, display stored entities for debugging
    entities = entity_memory.load_memory_variables({})
    print(f"\nStored entities: {entities}")


if __name__ == "__main__":
    real_time_conversation()
