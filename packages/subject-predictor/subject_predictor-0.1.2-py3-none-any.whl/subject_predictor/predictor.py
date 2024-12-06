import os
from typing import Dict, Tuple

class SubjectPredictor:
    def __init__(self, 
                 bi_model='thenlper/gte-base', 
                 cross_model='cross-encoder/ms-marco-TinyBERT-L-2-v2'):
        """Initialize predictor with models."""
        from sentence_transformers import SentenceTransformer, CrossEncoder
        from .embedding_loader import S3EmbeddingLoader
        
        self.embedding_loader = S3EmbeddingLoader()
        self.bi_encoder = SentenceTransformer(bi_model)
        self.cross_encoder = CrossEncoder(cross_model)
    
    def predict_subject_from_text(self, text: str, directory: str = 'subject_embeddings_gte-base') -> Tuple[str, Dict]:
        """Predict subject for input text."""
        # Existing predict_subject method renamed to make purpose clear
        return self._predict_subject(text, directory)
    
    def predict_subject_from_file(self, file_path: str, directory: str = 'subject_embeddings_gte-base') -> Tuple[str, Dict]:
        """Predict subject for text file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return self._predict_subject(text, directory)
    
    def _predict_subject(self, text: str, directory: str) -> Tuple[str, Dict]:
        """Internal method with core prediction logic."""
        import numpy as np
        from scipy.special import softmax
        
        # Get available subjects
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