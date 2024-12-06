from typing import Dict, Tuple
from sentence_transformers import SentenceTransformer, CrossEncoder
from .s3_embedding_loader import S3EmbeddingLoader
import numpy as np
from scipy.special import softmax

# Global predictor instance
_predictor = None

def _get_predictor():
    global _predictor
    if _predictor is None:
        _predictor = SubjectPredictor()
    return _predictor

def predict_subject_from_text(text: str, directory: str = 'subject_embeddings_gte-base') -> Tuple[str, Dict]:
    """Predict subject for input text."""
    predictor = _get_predictor()
    return predictor._predict_subject(text, directory)

def predict_subject_from_file(file_path: str, directory: str = 'subject_embeddings_gte-base') -> Tuple[str, Dict]:
    """Predict subject from text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    predictor = _get_predictor()
    return predictor._predict_subject(text, directory)

class SubjectPredictor:
    def __init__(self, 
                 bi_model='thenlper/gte-base', 
                 cross_model='cross-encoder/ms-marco-TinyBERT-L-2-v2'):
        """Initialize predictor with models."""
        self.embedding_loader = S3EmbeddingLoader()
        self.bi_encoder = SentenceTransformer(bi_model)
        self.cross_encoder = CrossEncoder(cross_model)
    
    def _predict_subject(self, text: str, directory: str) -> Tuple[str, Dict]:
        """Internal method with core prediction logic."""
        # [Rest of the prediction logic remains the same as in previous implementation]
        subjects = self.embedding_loader.list_available_subjects(directory)
        
        # Embed input text
        query_embedding = self.bi_encoder.encode(text)
        
        # Prepare scoring
        subject_scores = {}
        subject_texts = {}
        cross_encoder_inputs = []
        
        # Process each subject
        for subject in subjects:
            embeddings = self.embedding_loader.load_embedding(subject, directory)
            if not embeddings:
                continue
            
            # Get max similarity
            similarities = [np.dot(query_embedding, item['embedding']) / 
                            (np.linalg.norm(query_embedding) * np.linalg.norm(item['embedding'])) 
                            for item in embeddings]
            max_idx = np.argmax(similarities)
            
            subject_scores[subject] = similarities[max_idx]
            subject_texts[subject] = embeddings[max_idx]['text']
            cross_encoder_inputs.append((text, embeddings[max_idx]['text']))
        
        # Cross-encoder reranking
        cross_scores = self.cross_encoder.predict(cross_encoder_inputs)
        normalized_cross_scores = softmax(cross_scores)
        
        # Final scoring
        final_scores = {}
        for (subject, bi_score), cross_score in zip(subject_scores.items(), normalized_cross_scores):
            final_scores[subject] = {
                'bi_encoder_score': bi_score,
                'cross_encoder_score': float(cross_score),
                'combined_score': float(0.8 * bi_score + 0.2 * cross_score)
            }
        
        # Find best subject
        best_subject = max(final_scores.items(), key=lambda x: x[1]['combined_score'])[0]
        
        return best_subject, final_scores