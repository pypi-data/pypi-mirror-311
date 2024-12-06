import boto3
import pickle
import os
import functools
from io import BytesIO
from sentence_transformers import SentenceTransformer, CrossEncoder
from scipy.special import softmax
import numpy as np

class S3EmbeddingLoader:
    def __init__(self, bucket='subject-classifier-embeddings'):
        self.s3_client = boto3.client('s3')
        self.bucket = bucket
        self._embedding_cache = {}

    @functools.lru_cache(maxsize=32)
    def load_embedding(self, subject, directory='subject_embeddings_gte-base'):
        """
        Load embedding for a specific subject with caching.
        
        :param subject: Subject name
        :param directory: S3 directory containing embeddings
        :return: Loaded embeddings
        """
        # Check cache first
        cache_key = f"{directory}/{subject}"
        if cache_key in self._embedding_cache:
            return self._embedding_cache[cache_key]
        
        # Construct S3 key
        s3_key = f"{directory}/{subject}_embeddings.pkl"
        
        try:
            response = self.s3_client.get_object(Bucket=self.bucket, Key=s3_key)
            embeddings = pickle.load(response['Body'])
            
            # Cache and return
            self._embedding_cache[cache_key] = embeddings
            return embeddings
        except Exception as e:
            print(f"Error loading {subject} embeddings: {e}")
            return None

    def list_available_subjects(self, directory='subject_embeddings_gte-base'):
        """
        List all available subjects in the specified directory.
        
        :param directory: S3 directory to list subjects from
        :return: List of subject names
        """
        response = self.s3_client.list_objects_v2(
            Bucket=self.bucket, 
            Prefix=f"{directory}/", 
            Delimiter='/'
        )
        
        subjects = []
        for obj in response.get('Contents', []):
            filename = os.path.basename(obj['Key'])
            if filename.endswith('_embeddings.pkl'):
                subjects.append(filename.replace('_embeddings.pkl', ''))
        
        return subjects

class SubjectPredictor:
    def __init__(self, 
                 bi_model='thenlper/gte-base', 
                 cross_model='cross-encoder/ms-marco-TinyBERT-L-2-v2'):
        """
        Initialize predictor with embedding loader and models.
        
        :param bi_model: Bi-encoder model name
        :param cross_model: Cross-encoder model name
        """
        self.embedding_loader = S3EmbeddingLoader()
        self.bi_encoder = SentenceTransformer(bi_model)
        self.cross_encoder = CrossEncoder(cross_model)
    
    def _cosine_similarity(self, a, b):
        """Calculate cosine similarity between two vectors."""
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    def predict_subject(self, text, directory='subject_embeddings_gte-base'):
        """
        Predict subject for given text.
        
        :param text: Input text to classify
        :param directory: S3 directory for embeddings
        :return: Best subject and scores
        """
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
            similarities = [self._cosine_similarity(query_embedding, item['embedding']) 
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
