from ollama import Client

client = Client(host="http://127.0.0.1:11434")

response = client.chat(
    model="qwen3-vl:4b",
    messages=[
        {
            "role": "user",
            "content": 'Devuelve únicamente este JSON: {"name":"Edgar","skills":[]} /no_think'
        }
    ],
    think=False,
    format="json"
)

print("CONTENT:")
print(repr(response.message.content))

print("\nTHINKING:")
print(repr(response.message.thinking))

print("\nREASON:")
print(response.done_reason)