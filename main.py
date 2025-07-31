from difflib import SequenceMatcher
from fpdf import FPDF
import re

#loadind the two file that will be compared and checked for plagiarism
with open('doc1.txt') as f1, open('doc2.txt') as f2:
    data_file = f1.read()
    data_file2 = f2.read()

#splitting text into sentences which will be compared and checked    
def split_sentences(file):
    return re.split(r'(?<=[.!?])\s+', file.strip())

def highlight(s1, s2, threshold = 0.7):
    matcher = SequenceMatcher(None, s1, s2)
    ratio = matcher.ratio() 
    if ratio<threshold:
        return None, ratio
    highlighted = ""
    matches = matcher.get_matching_blocks() # gets a list of all the matching chunks
                                            #each match is a tuple (start_index_in_s1, start_index_in_s2, length_of_match)

    prev_end = 0
    
    for i in matches:
        start1, _, size = i
        highlighted += s1[prev_end:start1] #this fills in the gaps between highlighted parts
        highlighted += f"[=={s1[start1:start1+size]}==]" #the actual highlighted portion
        prev_end = start1 + size #updates the end of the current match, for the next start
    return highlighted, ratio

line1 = split_sentences(data_file)
line2 = split_sentences(data_file2)

matched_sentences = []
total_score = 0
numMatched = 0
# continue to compare sentences to one another and find rhe similarty score of each line 
for s1 in line1:
    for s2 in line2:
        highlighted, score = highlight(s1, s2)
        if highlighted:
            matched_sentences.append((highlighted, score))
            total_score += score
            numMatched += 1
            break  # move to next sentence after first match

# Print results
print(f"\nMatched {numMatched} sentence(s).")
if numMatched > 0:
    print(f"Average similarity score: {total_score / numMatched:.2f}\n")
    for idx, (sentence, score) in enumerate(matched_sentences, 1):
        print(f"{idx}. Score: {score:.2f}")
        print(f"{sentence}\n")
else:
    print("No significant matches found.")
        
        

# print(f"The plagiarized content is {matches*100}%")
    


