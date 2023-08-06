from Library.utils import process_file, convert_pdf_to_img, ocr_image
import pickle
import json
import re
import os 

class OCR:
    def process(self, file_path):
        return process_file(file_path)
    
    def classify_document(self, model_path, vectorizer_path, file_path):
        from .utils import convert_pdf_to_img, ocr_image  # Import the new functions
        import os

        # Load the pickled model
        with open(model_path, 'rb') as file:
            model = pickle.load(file)

        # Load the pickled vectorizer
        with open(vectorizer_path, 'rb') as file:
            vectorizer = pickle.load(file)

        # Get the file extension
        _, file_extension = os.path.splitext(file_path)

        # Convert the PDF to image if it's a PDF, otherwise read the image
        if file_extension.lower() == '.pdf':
            image = convert_pdf_to_img(file_path)[0]  # Take only the first page
            text = ocr_image(image)
        else:
            text = ocr_image(file_path)

        # Preprocess the text
        preprocessed_text = text.lower()  # Convert text to lowercase
        preprocessed_text = re.sub('[^a-zA-Z]', ' ', preprocessed_text)  # Remove non-alphabetic characters

        # Vectorize the text
        text_vectorized = vectorizer.transform([preprocessed_text])

        # Perform prediction
        prediction = model.predict(text_vectorized)
        prediction_prob = model.predict_proba(text_vectorized)

        # Convert the predictions to a dictionary
        prediction_dict = {
            't4_probability': prediction_prob[0][0],
            't5_probability': prediction_prob[0][1],
            'classification': 'T4' if prediction[0] == 0 else 'T5'
        }

        # Convert the dictionary to a JSON string
        prediction_json = json.dumps(prediction_dict)

        # Return the JSON string
        return prediction_json
