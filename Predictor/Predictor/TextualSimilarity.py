from Levenshtein import ratio
from sklearn.feature_extraction.text import TfidfVectorizer
import subprocess
import nltk, string
class TextualSimilarity:
    
    #http://stackoverflow.com/questions/8897593/similarity-between-two-text-documents
    def stem_trimmed_cosine(self, text1, text2):
        def normalize(text):
            def stem_tokens(tokens):
                stemmer = nltk.stem.porter.PorterStemmer()
                return [stemmer.stem(item) for item in tokens]
            remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
            return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))
        vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')
        tfidf = vectorizer.fit_transform([text1, text2])
        return (tfidf * tfidf.T).A[0, 1]

    def cosine_test(self, text1, text2):
        vect = TfidfVectorizer(min_df=1)
        tfidf = vect.fit_transform([text1, text2])
        return (tfidf * tfidf.T).A[0, 1]

    def homebrew_nlp(self, current_text, past_text):
        current_as_set = set(current_text.split(" "))
        past_as_set = set(past_text.split(" "))
        total_len = len(current_as_set) + len(past_as_set)
        percent_similar = len(current_as_set & past_as_set) / float(total_len)
        return percent_similar

    def levenshtein(self, text1, text2):
        return ratio(text1, text2)
