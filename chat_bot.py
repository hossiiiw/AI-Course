import dotenv
import os
import time
from openai import OpenAI
import tiktoken

dotenv.load_dotenv()


class ChatBot:
    def __init__(self):
        self.llm = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )

        self.messages_history = [{"role": "system",
                                  "content": "you are a helpful assistant. Your name is Hossiiw_bot.in first response, introduce yourself give short and concise answers . "},
                                 {"role": "system",
                                  "content": "At the end of each answer, state the time and Iranian time. "}]

        self.totol_tokens = 0
        self.input_token = 0
        self.output_token = 0
        self.iteration = 0

    def trim_message(self, max_number=4):
        if len(self.messages_history) < max_number:
            return

        system_messages = [
            m for m in self.messages_history if m["role"] == "system"]
        other_message = [
            m for m in self.messages_history if m["role"] != "system"]
        trimed_message = other_message[-max_number:]

        self.messages_history = [*system_messages, *trimed_message]

    def summarize_message(self):
        if self.iteration % 5 != 0:
            return

        system_messages = [
            m for m in self.messages_history if m["role"] == "system"]
        other_messages = [
            m for m in self.messages_history if m["role"] != "system"]
        early_messages, last_messages = (
            other_messages[0:5], other_messages[5:])

        response = self.llm.chat.completions.create(
            model="openai/gpt-oss-20b",
            temperature=0.5,
            messages=[
                {'role': 'system', 'content': 'Summarize these messages concisely, kepping key facts and information'},
                *early_messages
            ]
        )

        summarized_message = {
            'role': 'system',
            'content': f'this is a summary of 5 early messages: {
                response.choices[0].message.content}'}

        self.messages_history = [
            *system_messages,
            summarized_message,
            *last_messages]
        print('Summarization was successful')

    def bot(self, message):
        self.messages_history.append({
            "role": "user", "content": message
        })
        response = self.llm.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=self.messages_history,
            temperature=0.7,
            stream=True,

        )
        # response_text = response.choices[0].message.content
        # self.messages_history.append({"role": "assistant", "content": response_text})

        # self.totol_tokens += response.usage.total_tokens
        # self.input_token += response.usage.prompt_tokens
        # self.output_token += response.usage.completion_tokens

        response_text = ""
        for chunk in response:
            if chunk.choices:
                delta = chunk.choices[0].delta.content

                if delta:
                    print(delta, end="", flush=True)
                    response_text += delta
                    time.sleep(0.05)
            if chunk.usage:
                self.totol_tokens += chunk.usage.total_tokens
                self.input_token += chunk.usage.prompt_tokens
                self.output_token += chunk.usage.completion_tokens

        print()

        self.messages_history.append(
            {"role": "assistant", "content": response_text})

        # self.trim_message()
        self.summarize_message()
        print("-------------------------------------------")
        return response_text

    def chat(self):
        encoding = tiktoken.get_encoding("cl100k_base")

        while True:
            self.iteration += 1
            user_input = input(
                "Ask your question ('q' to termitate) : ").strip().lower()
            if user_input == "q":
                print("Thank for use me")
                break

            token_count = len(encoding.encode(user_input))
            if token_count > 10:
                print("Please insert short prompt")
                continue

            if self.totol_tokens > 10_000:
                print(
                    "your token is high than your account balance please insert short prompt")
                break

            self.bot(user_input)
            # print(bot_answerd)

    def report(self):
        for message in self.messages_history:
            print(f"{message}\n\n")
        print(f"Input tokens : {self.input_token}")
        print(f"Output tokens : {self.output_token}")
        print(f"Consumed tokens : {self.totol_tokens} ")
        print(f"Rials {((self.input_token *
                         0.05 +
                         self.output_token *
                         0.08) /
                        1_000_000) *
                       2_700_000} ")


def main():
    bot = ChatBot()
    bot.chat()
    bot.report()


if __name__ == "__main__":
    main()
