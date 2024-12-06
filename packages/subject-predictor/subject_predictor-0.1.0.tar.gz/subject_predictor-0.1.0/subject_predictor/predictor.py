import numpy as np
from scipy.special import softmax
from .models import ModelManager
from .utils import cosine_similarity

class SubjectPredictor:
    def __init__(self, 
                 subject_embeddings, 
                 bi_encoder_model='thenlper/gte-base', 
                 cross_encoder_model='cross-encoder/ms-marco-TinyBERT-L-2-v2'):
        """
        Initialize predictor with pre-loaded subject embeddings.
        
        :param subject_embeddings: Dict of pre-computed subject embeddings
        :param bi_encoder_model: Name of bi-encoder model to use
        :param cross_encoder_model: Name of cross-encoder model to use
        """
        self.subject_embeddings = subject_embeddings
        self.bi_encoder = ModelManager.load_bi_encoder(bi_encoder_model)
        self.cross_encoder = ModelManager.load_cross_encoder(cross_encoder_model)
    
    def predict_subject(self, input_text):
        """
        Predict subject for given text using bi-encoder and cross-encoder.
        
        :param input_text: Text to predict subject for
        :return: Best subject and detailed scores
        """
        # Embed input text
        query_embedding = self.bi_encoder.encode(input_text)
        
        # Get bi-encoder similarities
        bi_encoder_scores, subject_texts = self._get_bi_encoder_similarities(query_embedding)
        
        # Prepare cross-encoder inputs
        cross_encoder_inputs = [(input_text, subject_texts[subject]) 
                                for subject in self.subject_embeddings.keys()]
        
        # Get cross-encoder scores
        cross_scores = self.cross_encoder.predict(cross_encoder_inputs)
        normalized_cross_scores = softmax(cross_scores)
        
        # Calculate final scores
        final_scores = self._calculate_final_scores(
            bi_encoder_scores, 
            dict(zip(self.subject_embeddings.keys(), normalized_cross_scores))
        )
        
        # Get best subject
        best_subject = max(final_scores.items(), key=lambda x: x[1]['combined_score'])[0]
        
        return best_subject, final_scores
    
    def _get_bi_encoder_similarities(self, query_embedding):
        """Calculate maximum similarity for each subject."""
        subject_scores = {}
        subject_texts = {}
        
        for subject, embeddings_list in self.subject_embeddings.items():
            similarities = [cosine_similarity(query_embedding, item['embedding']) 
                            for item in embeddings_list]
            texts = [item['text'] for item in embeddings_list]
            
            max_idx = np.argmax(similarities)
            subject_scores[subject] = similarities[max_idx]
            subject_texts[subject] = texts[max_idx]
        
        return subject_scores, subject_texts
    
    def _calculate_final_scores(self, bi_encoder_scores, cross_encoder_scores):
        """Calculate combined scores for subjects."""
        final_scores = {}
        max_bi_score = max(bi_encoder_scores.values())
        min_bi_score = min(bi_encoder_scores.values())
        bi_score_range = max_bi_score - min_bi_score if max_bi_score != min_bi_score else 1

        for subject in self.subject_embeddings.keys():
            bi_score = bi_encoder_scores[subject]
            normalized_bi_score = (bi_score - min_bi_score) / bi_score_range
            cross_score = cross_encoder_scores[subject]
            
            final_scores[subject] = {
                'bi_encoder_score': bi_score,
                'cross_encoder_score': cross_score,
                'combined_score': float(0.8 * normalized_bi_score + 0.2 * cross_score)
            }
        
        return final_scores
