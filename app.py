from flask import Flask, render_template, request
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
app = Flask(__name__)

def summarize_text(text, num_sentences=3):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))

    filtered_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
    word_freq = FreqDist(filtered_words)

    sentence_scores = {}
    for sentence in sentences:
        for word, freq in word_freq.items():
            if word in sentence.lower():
                if sentence in sentence_scores:
                    sentence_scores[sentence] += freq
                else:
                    sentence_scores[sentence] = freq

    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
    summary = ' '.join(summary_sentences)
    return summary
@app.route('/')

def index():
    return render_template('index.html') 

@app.route('/summarize', methods=['POST'])

def summarize():
    if request.method=='POST':
        text = request.form['text']
        summary = summarize_text(text)
        return render_template('summary.html', text=text, summary=summary)
if __name__=='__main__':
    app.run(debug=True)