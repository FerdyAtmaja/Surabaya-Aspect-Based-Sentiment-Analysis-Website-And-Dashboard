import re
import pandas as pd
from nltk.corpus import stopwords
from sklearn.base import BaseEstimator, TransformerMixin
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# Load the CSV file with error handling
try:
    normalization_dict = pd.read_csv('static/assets/normalisasi-dictionary.csv').set_index('takbaku')['baku'].to_dict()
except (FileNotFoundError, pd.errors.EmptyDataError, KeyError) as e:
    print(f"Warning: Could not load normalization dictionary: {e}")
    normalization_dict = {}

class TextPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self, do_stemming=True, do_tokens=True):
        self.do_stemming = do_stemming
        self.do_tokens = do_tokens
        self.processed_data = None
        self.stemmer = StemmerFactory().create_stemmer()
        self.stopword_factory = StopWordRemoverFactory()
        self.stopwords_id = self.stopword_factory.get_stop_words()
        self.stopwords_en = set(stopwords.words('english'))
        self.normalization_dict = normalization_dict
        self.text_to_remove = [
            'e', 'kl', 'hahaha', 'nya', 'dll', 'mah', 'kacau', 'dah', 'tt', 'nge',
            'harieh', 'an', 'up', 'hpp', 'kah', 'ma', 'mpe', 'as', 'brics', 'bkln',
            'bkalan', 'brgak', 'banngakak', 'sih', 'lah', 'ke', 'si', 'nih',
            'aamiinn', 'lha', 'kok', 'iya', 'ajs', 'ab', 'ah', 'ahh', 'ahahaha',
            'ahelah', 'altman', 'alpenliebe', 'alloh', 'amir', 'tts', 'allahumma',
            'amatnape', 'an', 'alamakk', 'amin', 'with', 'abcd', 'aahhh', 'wkwk', 'yang'
        ]
        self.normalization_dict = normalization_dict

    def fit(self, X, y=None):
        return self

    def transform(self, X):
      processed = [self.preprocess_text(text) for text in X]
      if self.do_tokens:
          self.processed_data = [text.split() for text in processed]  # Tokenisasi
      else:
          self.processed_data = processed 
      return self.processed_data



    def preprocess_text(self, text):
        if not isinstance(text, str):
            return ""

        # Casefolding
        text = text.lower()

        # Cleaning
        text = self._remove_html(text)
        text = self._remove_emoji(text)
        text = self._clean_space(text)
        text = self._complete_clean(text)

        # Normalize
        text = self._normalize_text(text)

        # Remove stopwords
        text = self._remove_stopwords_en(text)
        text = self._remove_stopwords_id(text)
        text = self._remove_specific_words(text)

        # Stemming
        if self.do_stemming:
            text = self._stem_text(text)

        return text

    def _remove_html(self, text):
        text = re.sub(r'<a\s+href="[^"]+"[^>]*>(.*?)<\/a>', r'\1', text, flags=re.IGNORECASE)
        text = re.sub(r'https:\/\/\S+', '', text)
        return text

    def _remove_emoji(self, text):
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)

    def _clean_space(self, text):
        text = re.sub(r'<br>', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def _complete_clean(self, text):
        text = re.sub('[^a-zA-Z0-9\s]', ' ', text)
        text = re.sub(r'\b[a-zA-Z]\b', ' ', text)
        text = ' '.join(text.split())
        text = re.sub("\n", " ", text)
        text = re.sub(r'\b\w*\d\w*\b', ' ', text)
        return text

    def _normalize_text(self, text):
        return ' '.join([normalization_dict.get(word, word) for word in text.split()])

    def _remove_stopwords_en(self, text):
        return ' '.join([word for word in text.split() if word not in self.stopwords_en])

    def _remove_stopwords_id(self, text):
        return ' '.join([word for word in text.split() if word not in self.stopwords_id])

    def _remove_specific_words(self, text):
        return ' '.join([word for word in text.split() if word not in self.text_to_remove])

    def _stem_text(self, text):
        return ' '.join([self.stemmer.stem(word) for word in text.split()])