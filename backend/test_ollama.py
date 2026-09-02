from ollama import Client

client = Client(
    host="http://127.0.0.1:11434"
)

response = client.chat(
    model="qwen3-vl:4b",
    messages=[
        {
            "role": "user",
            "content": "Mira esta imagen y responde únicamente con: OK",
            "images": []
        }
    ],
    think=False,
    options={
        "num_predict": 20
    }
)

print("CONTENT:")
print(repr(response.message.content))

print("THINKING:")
print(repr(response.message.thinking))