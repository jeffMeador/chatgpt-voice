import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

messages = []
message_limit = 20

while True:

    del messages[message_limit:]
    print(len(messages))
    content = input("User: ")
    messages.append({"role": "user", "content": content})
    
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )

    chat_response = completion.choices[0].message.content
    print(f'ChatGPT: {chat_response}')
    messages.append({"role": "assistant", "content": chat_response})