from fastapi import APIRouter, Depends
from app.schemas.predictions_schema import Prediction, PredictionCreate
from app.services.sentiment_services import predict_sentiment 
from app.utils.logger import get_logger
from app.dependencies import get_db
from sqlalchemy.orm import Session
from app.models.prediction_model import Predictions as PredictionsModel

router = APIRouter(prefix="/sentiment", tags=["Sentiment Analysis"])

logging = get_logger(__name__)


@router.post("/predict", response_model=Prediction)

def predict_sentiment_route(
    request: PredictionCreate,db:Session= Depends(get_db)
):

    """
    Predict the sentiment of the input text.
    :param prediction: The input text to analyze.
    :return: A dictionary with the sentiment label and score.

    """
    
    
    logging.info(f"Received text for sentiment analysis: {request.text}")
    result = predict_sentiment(request.text)
    db_prediction_item = PredictionsModel(text=request.text, prediction=result['label'])
    db.add(db_prediction_item)
    db.commit()
    db.refresh(db_prediction_item)
    return Prediction(text=request.text, sentiment=result['label'])

@router.get("/", response_model=list[Prediction])
def get_all_predictions(db: Session = Depends(get_db)):
    """
    Retrieve all sentiment predictions from the database.
    :param db: Database session.
    :return: List of all predictions.
    """
    predictions = db.query(PredictionsModel).all()
    return [Prediction(text=pred.text, sentiment=pred.prediction) for pred in predictions]