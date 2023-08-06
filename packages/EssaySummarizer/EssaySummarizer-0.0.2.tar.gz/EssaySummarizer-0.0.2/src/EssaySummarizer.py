import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer

def summarize_essay(essay, num_sentences):
    sentences = sent_tokenize(essay)    # Tokenize the essay into sentences

    # Remove stopwords and tokenize words in each sentence
    stop_words = set(stopwords.words("english"))
    word_tokens = [word_tokenize(sentence.lower()) for sentence in sentences]
    filtered_tokens = [[word for word in words if word.isalnum() and word not in stop_words] for words in word_tokens]

    # Lemmatize words
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [[lemmatizer.lemmatize(word) for word in words] for words in filtered_tokens]

    # Calculate word frequencies
    word_frequencies = {}
    for words in lemmatized_tokens:
        for word in words:
            if word not in word_frequencies:
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    # Assign scores to sentences based on word frequencies
    sentence_scores = {}
    for i, words in enumerate(lemmatized_tokens):
        for word in words:
            if word in word_frequencies:
                if i not in sentence_scores:
                    sentence_scores[i] = word_frequencies[word]
                else:
                    sentence_scores[i] += word_frequencies[word]

    # Sort sentences based on scores and select top sentences
    top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]

    # Generate the summarized essay
    summarized_essay = ""
    for sentence_index in top_sentences:
        summarized_essay += sentences[sentence_index] + " "

    return summarized_essay


