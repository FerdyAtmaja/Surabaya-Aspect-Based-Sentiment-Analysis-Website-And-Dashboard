import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

# Custom transformer untuk LDA
class LDATransformer(BaseEstimator, TransformerMixin):
    def __init__(self, lda_model, dictionary):
        self.lda_model = lda_model
        self.dictionary = dictionary

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        texts = X
        corpus = [self.dictionary.doc2bow(text) for text in texts]
        dense_vectors = np.zeros((len(texts), self.lda_model.num_topics))

        for i, doc_bow in enumerate(corpus):
            for topic_id, prob in self.lda_model.get_document_topics(doc_bow, minimum_probability=0):
                dense_vectors[i, topic_id] = prob
        return dense_vectors