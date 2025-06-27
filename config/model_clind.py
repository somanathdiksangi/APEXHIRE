import os
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.constant import MODEL
# Load environment variables
load_dotenv()

api_key=os.getenv('GAMINI_API_KEY')

print(f"API Key: {api_key}")
def get_model_client():
    if not api_key:
        raise ValueError(f"Please set the {api_key} environment variable.")
    print(f"API Key: {api_key}")
    # Initialize the OpenAI model client
    model_client = OpenAIChatCompletionClient(model=MODEL, api_key=api_key)
    return model_client