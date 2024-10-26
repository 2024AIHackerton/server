from groq import Groq

client = Groq(
    api_key = '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'
)

client_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content" : "who are you?"
            }
        ],
        model = 'llama3-8b-8192',
)

print(client_completion)