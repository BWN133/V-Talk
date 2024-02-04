from flask import Flask, request, jsonify
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import whisper

app = Flask(__name__)

# Load Whisper model for transcription
whisper_model = whisper.load_model("medium")  # You can choose a different model size

# Load the fine-tuned BERT model and tokenizer for sentiment analysis
model_path = "./fine_tuned_model"  # Adjust this path to your fine-tuned model
tokenizer = BertTokenizer.from_pretrained(model_path)
sentiment_model = BertForSequenceClassification.from_pretrained(model_path)
sentiment_model.eval()  # Set the model to evaluation mode

def transcribe_audio(audio_path):
    # Transcribe the audio file
    result = whisper_model.transcribe(audio_path)
    return result['text']

def predict_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = sentiment_model(**inputs)
        predictions = torch.softmax(outputs.logits, dim=1)
    label = torch.argmax(predictions).item()
    score = predictions[0][label].item()
    return label, score

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        # Save the audio file temporarily
        audio_path = "./temp_audio.ogg"
        file.save(audio_path)
        
        # Transcribe audio to text
        text = transcribe_audio(audio_path)
        
        # Perform sentiment analysis on the transcribed text
        label, score = predict_sentiment(text)
        sentiment = 'Positive' if label == 1 else 'Negative'
        
        response = {
            "transcribed_text": text,
            "sentiment": sentiment,
            "confidence": score
        }
        return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
