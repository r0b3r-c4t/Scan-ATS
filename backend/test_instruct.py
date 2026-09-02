from ollama import Client

client = Client(host="http://127.0.0.1:11434")

response = client.chat(
    model="scan-ats-qwen3-vl-instruct:4b",
    messages=[
        {
            "role": "user",
            "content": 'Devuelve únicamente este JSON: {"name":"Edgar","skills":[]}'
        }
    ],
    format="json",
    options={
        "num_predict": 500,
        "temperature": 0
    }
)

print("CONTENT:")
print(repr(response.message.content))

print("\nTHINKING:")
print(repr(response.message.thinking))

print("\nREASON:")
print(response.done_reason)