
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#loadind the two file that will be compared and checked for plagiarism
with open('doc1.txt') as f1, open('doc2.txt') as f2:
    data_file = f1.read()
    data_file2 = f2.read()

#splitting text into sentences which will be compared and checked    
def split_sentences(file):
    return re.split(r'(?<=[.!?])\s+', file.strip())


lines1 = split_sentences(data_file)
lines2 = split_sentences(data_file2)

all_sentences = lines1+lines2 #combine to fit vectprizer
vectorizer = TfidfVectorizer().fit(all_sentences)

vectors1 = vectorizer.transform(lines1) 
vectors2 = vectorizer.transform(lines2)

threshold = 0.3
matched_sentences = []
total_score = 0
numMatched = 0
#go through each sentence in doc1
for i in range(vectors1.shape[0]):
    v1 = vectors1[i]  # get the TF-IDF vector for the curr sentence in doc1

    similarity_scores = []

    #compare this sentence from doc1 with every sentence in doc2
    for j in range(vectors2.shape[0]):
        v2 = vectors2[j]  # get the curr sentence from doc2
        score = cosine_similarity(v1, v2)[0][0]  # calculate cosine similarity
        similarity_scores.append(score)

    # Find the highest similarity score and the index of the matching sentence
    max_score = max(similarity_scores)
    best_match_index = similarity_scores.index(max_score)

    # If it passes the threshold, save the match
    if max_score >= threshold:
        s1 = lines1[i]
        s2 = lines2[best_match_index]
        matched_sentences.append((s1, s2, max_score))
        total_score += max_score
        numMatched += 1

# Print results
print(f"\nMatched {numMatched} sentence(s).")
if numMatched > 0:
    print(f"Average similarity score: {total_score / numMatched:.2f}\n")
    for idx, (s1, s2, score) in enumerate(matched_sentences, 1):
        print(f"{idx}. Similarity Score: {score:.2f}")
        print(f"Doc1: {s1}")
        print(f"Doc2: {s2}\n")
else:
    print("No significant matches found.")
        

# print(f"The plagiarized content is {matches*100}%")
    


