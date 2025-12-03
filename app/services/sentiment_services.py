import re
from transformers import pipeline
from app.utils.logger import get_logger
from app.utils.exceptions import SentimentPipelineError, PredictionError

logging= get_logger(__name__)

try:
    sentiment_pipeline = pipeline("sentiment-analysis")
except Exception as e:
    logging.error(f"Error loading sentiment analysis pipeline: {e}")
    sentiment_pipeline = None
    raise SentimentPipelineError("Failed to initialize sentiment analysis pipeline.") from e

#Preprocessing function for the input text
def preprocess_text(text: str) -> str:
    """Preprocess the input text for sentiment analysis.
    This can include steps like lowercasing, removing special characters, etc."""
    text = text.lower().strip()
    # remove special characters 
    text=re.sub(r'[^\w\s]', '', text)
    # remove extra spaces
    text=re.sub(r'\s+', ' ', text)
    # remove https links
    text=re.sub(r'http\S+|www\S+https\S','',text)
    return text


def predict_sentiment(text: str) -> dict:
    """Predict the sentiment of the given text using a pre-trained model.
    
    :param text: The input text to analyze.
        
    :return : A dictionary containing the sentiment label and score.
    """
    if sentiment_pipeline is None:
        raise SentimentPipelineError("Sentiment analysis pipeline is not initialized.")
    
    if not text or len(text.strip()) == 0:  
        raise ValueError("Input text cannot be empty.")
    
    preprocessed_text = preprocess_text(text)
    logging.info(f"Preprocessed text: {preprocessed_text}")
    try:
       result = sentiment_pipeline(preprocessed_text)[0]
       logging.info(f"Sentiment analysis result: {result}")
       result["label"]= result["label"].lower() 
       return result
    except Exception as e:
        logging.error(f"Error during sentiment prediction: {e}")
        raise PredictionError("Error occurred during sentiment prediction.") from e
   
    return {"label": result['label'], "score": result['score']}

