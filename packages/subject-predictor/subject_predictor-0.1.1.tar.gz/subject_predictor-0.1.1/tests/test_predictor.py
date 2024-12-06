import pickle
from subject_predictor import SubjectPredictor

def predict_subject_from_file(file_path, embeddings_path):

    with open(embeddings_path, 'rb') as f:
        subject_embeddings = pickle.load(f)
    
    # Read input text
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Initialize predictor
    predictor = SubjectPredictor(subject_embeddings)
    
    # Predict subject
    best_subject, scores = predictor.predict_subject(text)
    
    return {
        'input_file': file_path,
        'best_subject': best_subject,
        'detailed_scores': scores
    }

# Example usage
if __name__ == "__main__":
    text_file = 'path/to/your/document.txt'
    embeddings_file = 'path/to/your/embeddings.pkl'
    
    result = predict_subject_from_file(text_file, embeddings_file)
    
    print(f"Best Subject: {result['best_subject']}")
    print("\nDetailed Scores:")
    for subject, scores in result['detailed_scores'].items():
        print(f"{subject}: {scores}")