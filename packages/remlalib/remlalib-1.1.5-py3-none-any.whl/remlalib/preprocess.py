import re
import pandas as pd
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from joblib import load
from urllib.request import urlopen


class Preprocess:

    # load a default preprocessor
    def __init__(self):
        self.count_vectorizer = None

    def load_from_url(self, url):
        """Load a preprocessor from a url"""
        with urlopen(url) as file:
            self.count_vectorizer = load(file)

    def load_dataset(data_path):
        """Load dataset from data_path"""
        return pd.read_csv(data_path, delimiter='\t', quoting=3)

    def _get_stopwords():
        """Obtain the list of stopwords"""
        nltk.download('stopwords')

        all_stopwords = stopwords.words('english')
        all_stopwords.remove('not')

        return all_stopwords


    def _get_corpus(self, dataset):
        """produce the corpus from the dataset by applying preprocessing steps"""
        all_stopwords = self.get_stopwords()
        corpus = []

        porter_stemmer = PorterStemmer()

        for i in range(0, 900):
            review = re.sub('[^a-zA-Z]', ' ', dataset['Review'][i])
            review = review.lower()
            review = review.split()
            review = [porter_stemmer.stem(word)
                    for word in review if not word in set(all_stopwords)]
            review = ' '.join(review)
            corpus.append(review)
        return corpus


    def preprocess_dataset(self, dataset):
        """Preprocess the dataset and save it"""
        corpus = self.get_corpus(dataset)
        self.count_vectorizer = CountVectorizer(max_features=1420)
        X = self.count_vectorizer.fit_transform(corpus).toarray()
        y = dataset.iloc[:, -1].values

        return X, y

    def preprocess_sample(self, review):
        """Preprocess the sample review and return it"""
        return self.count_vectorizer.transform([review]).toarray()[0]