import dotenv
import os
from openai import OpenAI


dotenv.load_dotenv()


class Analyzer:
    def __init__(self):
        self.llm = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )

        self.messages = [
            {"role": "system", "content": "classify the sentiment of the text as positive , negetive or neutral"},
            {"role": "user" , "content" : "this movie is perfect"},
            {"role": "assistant" , "content" : "sentiment : positive❤️ 😍"},
            {"role": "user" , "content" : "it was terrible"},
            {"role": "assistant" , "content" : "sentiment : negetive😢 😞"},
            {"role": "user" , "content" : "nothing special"},
            {"role": "assistant" , "content" : "sentiment : netural✌️ "},
        ]

    def sentiment_analysis(self, message):
        response = self.llm.chat.completions.create(
            model="openai/gpt-oss-20b",
            temperature= 0.1,
            messages=[
                *self.messages,
                {"role" : "user" , "content" : message},
            ]
        )
        return response.choices[0].message.content

    def history(self):
        print(self.messages)


def main():
    user_input = input("enter your sentences ? ")
    analyzer = Analyzer()
    print(analyzer.sentiment_analysis(user_input))


if __name__ == "__main__":
    main()
