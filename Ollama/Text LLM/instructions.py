# defining the instructions for the model
instruction_1 = """
    You are an AI analyzing restaurant reviews. Classify the sentiment of the provided review into the following categories:
    - Positive
    - Negative
    - Neutral
"""


# defining the instructions for the model
instruction_2 = """
    You are an AI analyzing restaurant reviews. Classify the sentiment of the provided review into the following categories:
    - Positive
    - Negative
    - Neutral

    Format the output as a JSON object with a single key-value pair as shown below:
    {"sentiment": "your_sentiment_prediction"}
"""


# defining the instructions for the model
instruction_3 = """
    You are an AI analyzing restaurant reviews. Classify the overall sentiment of the provided review into the following categories:
    - "Positive"
    - "Negative"
    - "Neutral"

    Once that is done, check for a mention of the following aspects in the review and classify the sentiment of each aspect as "Positive", "Negative", or "Neutral":
    1. "Food Quality"
    2. "Service"
    3. "Ambience"

    Output the overall sentiment and sentiment for each category in a JSON format with the following keys:
    {
        "Overall": "your_sentiment_prediction",
        "Food Quality": "your_sentiment_prediction",
        "Service": "your_sentiment_prediction",
        "Ambience": "your_sentiment_prediction"
    }

    In case one of the three aspects is not mentioned in the review, set "Not Applicable" (including quotes) for the corresponding JSON key value.
    Only return the JSON, do not return any other information.
"""



# defining the instructions for the model
instruction_4 = """
    You are provided a review and it's sentiment.

    Instructions:
    Classify the sentiment of each aspect as either of "Positive", "Negative", or "Neutral" only and not any other for the given review:
    1. "Food Quality"
    2. "Service"
    3. "Ambience"
    In case one of the three aspects is not mentioned in the review, return "Not Applicable" (including quotes) for the corresponding JSON key value.
    Return the output in the format {"Overall": given sentiment input,"Food Quality": "your_sentiment_prediction","Service": "your_sentiment_prediction","Ambience": "your_sentiment_prediction"}

"""


# defining the instructions for the model
instruction_5 = """
    You are an AI tasked with analyzing restaurant reviews. Your goal is to classify the overall sentiment of the provided review into the following categories:
        - Positive
        - Negative
        - Neutral

    Subsequently, assess the sentiment of specific aspects mentioned in the review, namely:
        1. Food quality
        2. Service
        3. Ambience

    Further, identify liked and/or disliked features associated with each aspect in the review.

    Return the output in the specified JSON format, ensuring consistency and handling missing values appropriately:

    {
        "Overall": "your_sentiment_prediction",
        "Food Quality": "your_sentiment_prediction",
        "Service": "your_sentiment_prediction",
        "Ambience": "your_sentiment_prediction",
        "Food Quality Features": ["liked/disliked features"],
        "Service Features": ["liked/disliked features"],
        "Ambience Features": ["liked/disliked features"]
    }

    The sentiment prediction for Overall, Food Quality, Service, and Ambience should be one of "Positive", "Negative", or "Neutral" only.
    In case one of the three aspects is not mentioned in the review, set "Not Applicable" (including quotes) in the corresponding JSON key value for the sentiment.
    In case there are no liked/disliked features for a particular aspect, assign an empty list in the corresponding JSON key value for the aspect.
    Only return the JSON, do NOT return any other text or information.
"""