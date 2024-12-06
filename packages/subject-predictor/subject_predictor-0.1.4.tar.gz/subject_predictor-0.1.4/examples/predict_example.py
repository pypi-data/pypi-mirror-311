from subject_predictor import SubjectPredictor

def predict_subjects_from_file(file_path, subject_embeddings):
    """
    Predict subjects for text in a file.
    
    :param file_path: Path to text file
    :param subject_embeddings: Pre-computed subject embeddings
    :return: Best subject and scores
    """
    with open(file_path, 'r') as f:
        text = f.read()
    
    predictor = SubjectPredictor(subject_embeddings)
    return predictor.predict_subject(text)

# Lambda handler example
def lambda_handler(event, context):
    """
    AWS Lambda handler for subject prediction.
    Expects event to contain 'text' or 's3_bucket' and 's3_key'
    """
    import boto3
    
    # Load pre-computed embeddings (you'd need a method to load these)
    subject_embeddings = load_embeddings_from_s3()
    
    # Get text from event
    if 'text' in event:
        text = event['text']
    elif 's3_bucket' in event and 's3_key' in event:
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=event['s3_bucket'], Key=event['s3_key'])
        text = obj['Body'].read().decode('utf-8')
    else:
        raise ValueError("No text provided")
    
    predictor = SubjectPredictor(subject_embeddings)
    best_subject, scores = predictor.predict_subject(text)
    
    return {
        'statusCode': 200,
        'body': {
            'best_subject': best_subject,
            'scores': scores
        }
    }