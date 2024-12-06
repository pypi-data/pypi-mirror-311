from subject_predictor import predict_subject_from_text, predict_subject_from_file

# Predict from text
best_subject, scores = predict_subject_from_text("Your input text here")

# Predict from file
best_subject, scores = predict_subject_from_file("/path/to/your/file.txt")