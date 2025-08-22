import streamlit as st
import nltk, string
from heapq import nlargest

# First time downloads
nltk.download('punkt')
nltk.download('stopwords')

def summarize_text(text):
    if text.count(". ") > 20:
        length = int(round(text.count(". ")/10, 0))
    else:
        length = 1

    nopuch = [ch for ch in text if ch not in string.punctuation]
    nopuch = "".join(nopuch)

    processed_text = [word for word in nopuch.split() 
                      if word.lower() not in nltk.corpus.stopwords.words('english')]

    word_freq = {}
    for word in processed_text:
        word_freq[word] = word_freq.get(word, 0) + 1

    max_freq = max(word_freq.values())
    for word in word_freq.keys():
        word_freq[word] /= max_freq

    sent_list = nltk.sent_tokenize(text)
    sent_score = {}

    for sent in sent_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_freq:
                sent_score[sent] = sent_score.get(sent, 0) + word_freq[word]

    summary_sents = nlargest(length, sent_score, key=sent_score.get)
    summary = " ".join(summary_sents)
    return summary


# ----------------- STREAMLIT UI -------------------
st.title("📝 Simple Text Summarizer")
st.write("Paste your text below and get a concise summary!")

text = st.text_area("Enter your text here:", height=300)

if st.button("Summarize"):
    if len(text.strip()) == 0:
        st.warning("⚠ Please enter some text to summarize.")
    else:
        summary = summarize_text(text)
        st.subheader("📌 Summary:")
        st.write(summary)