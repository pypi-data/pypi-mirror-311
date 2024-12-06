import os
from functools import lru_cache
from sentence_transformers import SentenceTransformer, CrossEncoder

class ModelManager:
    @staticmethod
    @lru_cache(maxsize=None)
    def load_bi_encoder(model_name='thenlper/gte-base'):
        """Load bi-encoder with caching."""
        return SentenceTransformer(model_name, cache_folder='/tmp/huggingface')
    
    @staticmethod
    @lru_cache(maxsize=None)
    def load_cross_encoder(model_name='cross-encoder/ms-marco-TinyBERT-L-2-v2'):
        """Load cross-encoder with caching."""
        return CrossEncoder(model_name)


