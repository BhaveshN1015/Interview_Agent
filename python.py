from ibm_watsonx_ai import APIClient, Credentials
from dotenv import load_dotenv
import os

load_dotenv()

creds = Credentials(
    url=os.getenv("WATSONX_URL"),
    api_key=os.getenv("IBM_API_KEY")
)

client = APIClient(creds)

print("✅ Connection successful!")
print(f"Project ID loaded: {os.getenv('WATSONX_PROJECT_ID')}")