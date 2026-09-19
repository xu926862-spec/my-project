from groq import Groq

client = Groq(api_key="gsk_你的新Key")

response = client.chat.completions.create(
    model="mixtral-8x7b-32768",
    messages=[{"role": "user", "content": "Hello, who are you?"}],
    max_tokens=100
)

print(response.choices[0].message.content)
