import dotenv
import os
from openai import OpenAI


dotenv.load_dotenv()
llm = OpenAI(
  api_key=os.getenv("GROQ_API_KEY"),
  base_url="https://api.groq.com/openai/v1"
)


def bot(message):
  response =llm.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
      {
        "role" : "user" , "content" : message
      }
    ]
  )
  

  return response.choices[0].message.content



def main():
  user_input = input("Ask your question : ")
  bot_answerd = bot(user_input)
  print(bot_answerd)

if __name__ == "__main__":
  main()
