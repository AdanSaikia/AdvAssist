from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn

# Download necessary NLTK datasets
nltk.download('wordnet')
nltk.download('sentiwordnet')

# Initialize VADER SentimentIntensityAnalyzer
vader_analyzer = SentimentIntensityAnalyzer()

# Emotion categories and intensity levels
emotion_categories = {
    'happy': ('Positive', 0.6),
    'sad': ('Negative', 0.6),
    'angry': ('Negative', 0.7),
    'fear': ('Negative', 0.7),
    'surprised': ('Neutral', 0.6),
    'disgust': ('Negative', 0.7),
    'neutral': ('Neutral', 0.5),
    'trust': ('Positive', 0.7),
    'anticipation': ('Neutral', 0.6)
}


def get_sentiment_from_sentiwordnet(word):
    # Get synsets for the word
    synsets = wn.synsets(word)
    if not synsets:
        return 0  # No sentiment score for this word

    sentiment_score = 0
    for synset in synsets:
        # Get the sentiment score for the synset
        senti_synset = swn.senti_synset(synset.name())
        sentiment_score += senti_synset.pos_score() - senti_synset.neg_score()

    # Average sentiment score
    sentiment_score /= len(synsets)
    return sentiment_score


def analyze_sentiment(text):
    # Step 1: Analyze sentiment with TextBlob
    blob = TextBlob(text)
    textblob_polarity = blob.sentiment.polarity

    # Step 2: Analyze sentiment with VADER
    vader_sentiment = vader_analyzer.polarity_scores(text)
    vader_compound = vader_sentiment['compound']

    # Step 3: Analyze sentiment with SentiWordNet
    words = text.split()  # Split the text into words
    sentiwordnet_sentiment = 0
    sentiment_count = 0

    # Analyze each word with SentiWordNet
    for word in words:
        senti_score = get_sentiment_from_sentiwordnet(word)
        if senti_score != 0:
            sentiwordnet_sentiment += senti_score
            sentiment_count += 1

    # Average SentiWordNet sentiment
    if sentiment_count > 0:
        sentiwordnet_sentiment /= sentiment_count

    # Step 4: Combine the sentiment scores
    combined_sentiment = (textblob_polarity + vader_compound + sentiwordnet_sentiment) / 3

    # Step 5: Categorize emotions
    emotion, intensity = categorize_emotion(combined_sentiment)

    # Display results
    print(f"Combined Sentiment Score: {combined_sentiment}")
    print(f"Emotion: {emotion}")
    print(f"Intensity: {intensity}")

    return emotion, intensity


def categorize_emotion(score):
    if score >= 0.75:
        return 'happy', 'strong'
    elif score >= 0.5:
        return 'happy', 'mild'
    elif score >= 0.3:
        return 'trust', 'mild'
    elif score >= 0:
        return 'neutral', 'mild'
    elif score >= -0.3:
        return 'sad', 'mild'
    elif score >= -0.6:
        return 'angry', 'mild'
    elif score >= -0.75:
        return 'disgust', 'mild'
    elif score >= -1:
        return 'fear', 'strong'
    else:
        return 'angry', 'strong'
