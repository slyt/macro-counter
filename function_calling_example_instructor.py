import openai
import instructor

from pydantic import BaseModel

MODEL = "function-calling"  # see server_config.json for model alias

client = openai.OpenAI(
    api_key = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # can be anything
    base_url = "http://localhost:8080/v1" # NOTE: Replace with IP address and port of your llama-cpp-python server
)

# Enables `response_model`
client = instructor.patch(client=client)

class UserDetail(BaseModel):
    name: str
    age: int

user = client.chat.completions.create(
    model=MODEL,
    response_model=UserDetail,
    messages=[
        {"role": "user", "content": "Extract Jason is 25 years old"},
    ]
)

assert isinstance(user, UserDetail)
assert user.name == "Jason"
assert user.age == 25

print(user)
