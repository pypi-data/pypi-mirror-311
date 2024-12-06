import os
import boto3
import pickle
import functools

class S3EmbeddingLoader:
    def __init__(self, bucket='subject-classifier-embeddings'):
        self.s3_client = boto3.client('s3')
        self.bucket = bucket
        self._embedding_cache = {}

    @functools.lru_cache(maxsize=32)
    def load_embedding(self, subject, directory='subject_embeddings_gte-base'):
        """Load embedding for a specific subject with caching."""
        cache_key = f"{directory}/{subject}"
        if cache_key in self._embedding_cache:
            return self._embedding_cache[cache_key]
        
        s3_key = f"{directory}/{subject}_embeddings.pkl"
        
        try:
            response = self.s3_client.get_object(Bucket=self.bucket, Key=s3_key)
            embeddings = pickle.load(response['Body'])
            
            self._embedding_cache[cache_key] = embeddings
            return embeddings
        except Exception as e:
            print(f"Error loading {subject} embeddings: {e}")
            return None

    def list_available_subjects(self, directory='subject_embeddings_gte-base'):
        """List all available subjects in the specified directory."""
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