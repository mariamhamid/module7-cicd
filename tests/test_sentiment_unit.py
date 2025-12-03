from app.services.sentiment_services import predict_sentiment

def test_sentiment_position():
    input_text="I love programming"
    result= predict_sentiment(input_text)
    assert result['label'] == 'positive',f"Expected positive but got {result['label']}"
    assert 0.5<result['score'] <=1.0,f"Expected score between 0.5 and 1.0 but got {result['score']}"
    
def test_sentiment_negative():
    input_text="I hate programming"
    result= predict_sentiment(input_text)
    assert result['label'] == 'negative',f"Expected negative but got {result['label']}"
    assert 0.5<result['score'] <=1.0,f"Expected score between 0.5 and 1.0 but got {result['score']}"
    
def test_predict_sentiment_empty_text():
    input_text=""
    try:
        predict_sentiment(input_text)
        assert False, "Expected ValueError for empty input text"
    except ValueError as e:
        assert True,f"ValueError raised as expected: {e}"