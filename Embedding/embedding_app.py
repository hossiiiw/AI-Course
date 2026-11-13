from sentence_transformers import SentenceTransformer , util

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")



def find_closest(query , sentences):
  embedding = model.encode(sentences)
  query_embedding = model.encode(query)

  closest_index = 0
  closest_score = -1

  for index , vector in enumerate(embedding):

    similarity = util.cos_sim(vector , query_embedding).item()
    
    if similarity > closest_score:
      closest_score = similarity
      closest_index = index

  return sentences[closest_index]

def main():
    sentences = [
      "That is a happy person",
      "That is a happy dog",
      "That is a very happy person",
      "Today is a sunny day",
      "Today is a very hot",
      "Crypto is very difficult",
      "football is very good",
  ]
    query = input("Say anything : ")

    embedding = model.encode(sentences)
    query_embedding = model.encode([query])

    # similarity = find_closest(query , sentences)
    similarity = util.semantic_search(query_embedding  , embedding , top_k=1 )
    index = similarity[0][0]["corpus_id"]
    score = similarity[0][0]["score"]
    print(f"\nBest match with: {sentences[index]}")
    print(f"Similarity : {score}")
  
  


if __name__ == "__main__":
  main()
