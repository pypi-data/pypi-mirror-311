def load_stopwords_from_file(file_path):
    """
    Load stopwords from a text file, where each line is a stopword.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:  # Specify UTF-8 encoding
            stopwords = file.read().splitlines()
        return stopwords
    except FileNotFoundError:
        raise FileNotFoundError(f"Stopwords file not found: {file_path}")
