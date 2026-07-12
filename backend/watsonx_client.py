from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from dotenv import load_dotenv
import os

load_dotenv()

# NOTE: This file is a standalone connection helper / smoke-test utility.
# The live ARIA backend (main.py) uses its own module-level singleton — do NOT
# call get_model() from main.py or you will get a second ModelInference object.

def get_model():
    """Returns a lightweight ModelInference instance aligned with main.py's
    model choice and conservative token limits."""
    creds = Credentials(
        url=os.getenv("WATSONX_URL"),
        api_key=os.getenv("IBM_API_KEY")
    )
    model = ModelInference(
        model_id="meta-llama/llama-3-3-70b-instruct",  # same model as main.py
        credentials=creds,
        project_id=os.getenv("WATSONX_PROJECT_ID"),
        params={
            GenParams.MAX_NEW_TOKENS: 300,   # matched to main.py's max_tokens budget
            GenParams.TEMPERATURE: 0.3,      # low — keeps responses on-format
            GenParams.TOP_P: 0.85,
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
    print("Testing Meta Llama 3.3 70B model via watsonx.ai...")
    print("-" * 50)
    result = generate_response(test_prompt)
    print(result)
    print("-" * 50)
    print("✅ Model working correctly!")
