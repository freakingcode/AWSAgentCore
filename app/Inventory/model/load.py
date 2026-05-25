from strands.models.bedrock import BedrockModel


def load_model() -> BedrockModel:
    """Get Bedrock model client using IAM credentials."""
    return BedrockModel(model_id="openai.gpt-oss-20b-1:0")



# from openai import OpenAI
# from dotenv import load_dotenv
# import os

# load_dotenv()

# client = OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY")
# )


# class OpenAIModel:

#     def invoke(self, prompt: str):

#         response = client.chat.completions.create(
#             model="gpt-4.1-mini",

#             messages=[
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ]
#         )

#         return response.choices[0].message.content


# def load_model():
#     return OpenAIModel()


# from model.openai import OpenAIModel

# def load_model():

#     return OpenAIModel()