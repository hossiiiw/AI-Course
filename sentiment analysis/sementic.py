import dotenv
import os
from openai import OpenAI
from transformers import pipeline



dotenv.load_dotenv()

class Analyzer :
  def __init__(self):
    self.classifier = pipeline("zero-shot-classification" , model="typeform/distilbert-base-uncased-mnli")



  def  sentiment_analyzer(self):
    labels = ["positive" , "negetive" , "neutral"]
    while True :
      user_input = input("Enter your sentance : ").strip().lower()

      if user_input == "q":
        print("Thanks for using distilbert-base-uncased-mnli model")
        break


      result = self.classifier(user_input , candidate_labels = labels)
      print({
        result["labels"][0],
        result["scores"][0]
      })







def main():
  analyzer_bot = Analyzer()
  analyzer_bot.sentiment_analyzer()


if __name__ == "__main__":
  main()

