import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

# Custom transformer untuk LDA
class LDATransformer(BaseEstimator, TransformerMixin):
    def __init__(self, lda_model, dictionary):
        if lda_model is None or dictionary is None:
            raise ValueError("lda_model and dictionary cannot be None")
        self.lda_model = lda_model
        self.dictionary = dictionary

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if X is None:
            raise ValueError("Input X cannot be None")
        
        try:
            texts = X
            if not hasattr(texts, '__iter__'):
                raise ValueError("Input X must be iterable")
            
            # Filter out None values and keep track of original indices
            valid_texts = []
            valid_indices = []
            for i, text in enumerate(texts):
                if text is not None:
                    valid_texts.append(text)
                    valid_indices.append(i)
                    
            corpus = [self.dictionary.doc2bow(text) for text in valid_texts]
            dense_vectors = np.zeros((len(texts), self.lda_model.num_topics))

            # Map results back to original indices
            for corpus_idx, doc_bow in enumerate(corpus):
                original_idx = valid_indices[corpus_idx]
                for topic_id, prob in self.lda_model.get_document_topics(doc_bow, minimum_probability=0):
                    dense_vectors[original_idx, topic_id] = prob
            return dense_vectors
        except Exception as e:
            print(f"Error in LDATransformer.transform: {e}")
            # Return zero vectors as fallback
            return np.zeros((len(X) if hasattr(X, '__len__') else 1, self.lda_model.num_topics))