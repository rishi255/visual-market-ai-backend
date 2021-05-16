
import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.cloud import language_v1

load_dotenv()
KEYDIR_PATH = os.getenv('KEYDIR_PATH')
credentials = service_account.Credentials.from_service_account_file(KEYDIR_PATH)
client = language_v1.LanguageServiceClient(credentials=credentials)

def sample_analyze_sentiment(text_content: str, text_type: language_v1.Document.Type = language_v1.Document.Type.PLAIN_TEXT):
    """
    Analyzing Sentiment in a String.

    Args:
        text_content (str): The text content to analyze.
        text_type (language_v1.Document.Type, optional): Type of text gi. Defaults to language_v1.Document.Type.PLAIN_TEXT.

    Returns
        (int): Sentiment score.
    """

    # Available types: PLAIN_TEXT, HTML
    type_ = text_type

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8
    response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})

    # Get overall sentiment of the input document
    print(u"Document sentiment score: {}".format(response.document_sentiment.score))
    print(
        u"Document sentiment magnitude: {}".format(
            response.document_sentiment.magnitude
        )
    )
    # Get sentiment for all sentences in the document
    for sentence in response.sentences:
        print(u"Sentence text: {}".format(sentence.text.content))
        print(u"Sentence sentiment score: {}".format(sentence.sentiment.score))
        print(u"Sentence sentiment magnitude: {}".format(sentence.sentiment.magnitude))

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    print(u"Language of the text: {}".format(response.language))

    return response.document_sentiment.score

if __name__ == "__main__":
    text_content = 'I really love the quality of work you put into baking these cakes!'
    score = sample_analyze_sentiment(text_content=text_content)
