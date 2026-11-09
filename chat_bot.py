import dotenv
import os
from openai import OpenAI

dotenv.load_dotenv()

llm = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

messages_history = [{
    "role": "system", "content": "you are a helpful assistant. Your name is Hossiiw_bot.in first response, introduce yourself give short and concise answers . "}]


def bot(message):
    messages_history.append({
        "role": "user", "content": message
    })
    response = llm.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages_history,
        temperature=0.7,


    )

    response_text = response.choices[0].message.content
    messages_history.append({"role": "assistant", "content": response_text})
    return response_text


def chat():
    while True:
        user_input = input(
            "Ask your question ('q' to termitate) : ").strip().lower()
        if user_input == "q":
            print("Thank for use me")
            break
        bot_answerd = bot(user_input)
        print(bot_answerd)


def main():
    chat(),
    print(messages_history)


if __name__ == "__main__":
    main()
