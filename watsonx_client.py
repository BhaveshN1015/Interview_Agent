from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from dotenv import load_dotenv
import os

load_dotenv()

def get_client():
    creds = Credentials(
        url=os.getenv("WATSONX_URL"),
        api_key=os.getenv("IBM_API_KEY")
    )
    return APIClient(creds)

def get_model():
    creds = Credentials(
        url=os.getenv("WATSONX_URL"),
        api_key=os.getenv("IBM_API_KEY")
    )
    model = ModelInference(
        model_id="ibm/granite-8b-code-instruct",
        credentials=creds,
        project_id=os.getenv("WATSONX_PROJECT_ID"),
        params={
            GenParams.MAX_NEW_TOKENS: 1024,
            GenParams.TEMPERATURE: 0.7,
            GenParams.TOP_P: 0.9,
            GenParams.REPETITION_PENALTY: 1.1,
        }
    )
    return model

def generate_response(prompt: str) -> str:
    try:
        model = get_model()
        response = model.generate_text(prompt=prompt)
        return response
    except Exception as e:
        return f"Error generating response: {str(e)}"


if __name__ == "__main__":
    test_prompt = "You are an interview coach. Give me one sample interview question for a software engineer fresher."
    print("Testing IBM Granite model...")
    print("-" * 50)
    result = generate_response(test_prompt)
    print(result)
    print("-" * 50)
    print("✅ Model working correctly!")
