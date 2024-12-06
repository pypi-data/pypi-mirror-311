#!/usr/bin/env python3

from mintii import MintiiTracker
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

def main():
    """
    Main function to demonstrate Mintii Tracker usage with LangChain.
    """
    try:
        # Load environment variables
        load_dotenv()

        # Get API keys from environment
        mintii_api_key = os.getenv('MINTII_API_KEY')
        openai_api_key = os.getenv('OPENAI_API_KEY')

        # Validate API keys
        if not mintii_api_key:
            raise ValueError("MINTII_API_KEY not found in environment variables")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        # Initialize the tracker
        tracker = MintiiTracker(api_key=mintii_api_key)

        # Create LangChain components with the tracker
        llm = ChatOpenAI(
            api_key=openai_api_key,
            model="gpt-4",
            callbacks=[tracker]
        )

        # Create and set up the chain
        prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
        chain = prompt | llm

        # Run the chain
        print("Generating response...")
        response = chain.invoke({"topic": "programming"})
        print("\nResponse received:", response)

        # Get and display tracking info
        tracking_info = tracker.get_tracking_info()
        print("\nTracking Information:")
        print("Model Info:", tracking_info['model_info'])
        print("Prompts:", tracking_info['prompts'])
        print("Responses:", tracking_info['responses'])

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 1

    return 0

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)