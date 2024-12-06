import os
from .utils import load_stopwords_from_file

class StopwordsFilter:
    def __init__(self, stopwords_file=None):
        # Load stopwords from a default file or custom file
        self.stopwords = load_stopwords_from_file(stopwords_file or 'stopwords.txt')

    def show_stopwords(self):
        """Returns the list of stopwords."""
        return self.stopwords

    def filter_text(self, text):
        """Filters out stopwords from the provided text."""
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in self.stopwords]
        return ' '.join(filtered_words)

    def add_custom_stopwords(self, custom_stopwords):
        """Adds custom stopwords to the existing list."""
        self.stopwords.extend([word.lower() for word in custom_stopwords])
        self.stopwords = list(set(self.stopwords))  # Remove duplicates

