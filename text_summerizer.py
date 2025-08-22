import nltk, string
from heapq import nlargest

nltk.download('punkt')
nltk.download('stopwords')

def summerize_text(text):
    # Decide summary length
    if text.count(". ") > 20:
        length = int(round(text.count(". ")/10, 0))
    else:
        length = 1
        
    # Remove punctuation    
    nopuch = [ch for ch in text if ch not in string.punctuation]
    nopuch = "".join(nopuch)

    # Remove stopwords
    processed_text = [word for word in nopuch.split() if word.lower() not in nltk.corpus.stopwords.words('english')]

    # Word frequency dictionary
    word_freq = {}
    for word in processed_text:
        word_freq[word] = word_freq.get(word, 0) + 1

    max_freq = max(word_freq.values())
    for word in word_freq.keys():
        word_freq[word] /= max_freq

    # Sentence Scoring
    sent_list = nltk.sent_tokenize(text)
    sent_score = {}

    for sent in sent_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_freq:
                sent_score[sent] = sent_score.get(sent, 0) + word_freq[word]

    # Pick top sentences
    summary_sents = nlargest(length, sent_score, key=sent_score.get)
    summary = " ".join(summary_sents)

    return summary

# Example usage
if __name__ == "__main__":
    text = """ India is a rapidly developing country. 
    It has seen tremendous economic growth in recent decades. 
    The IT sector, agriculture, and startups are booming. 
    However, challenges like unemployment and pollution remain. 
    The government is working on many schemes to address these issues."""

    print("Original Text:\n", text)
    print("\n Summary:\n",summerize_text(text))