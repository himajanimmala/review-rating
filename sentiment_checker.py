
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class SentimentAnalyzer:
    """It will provide sentiments analysis of the given text data.
       Written by : Vikram Singh
       Date: 05/01/2022"""

    def sentiments(self, data):
        """Method Name: sentiments
           Description: It will provide the sentiment of the data."""
        try:
            analyzer = SentimentIntensityAnalyzer()
            sentiment_polarity = data.apply(lambda review: analyzer.polarity_scores(review))
            compound = sentiment_polarity.apply(lambda score_dict: score_dict['compound'])
            return sentiment_polarity, compound
        except Exception as e:
            print(e)