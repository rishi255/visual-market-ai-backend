
import os
from google.cloud import speech
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()
KEYDIR_PATH = os.getenv('KEYDIR_PATH')
credentials = service_account.Credentials.from_service_account_file(KEYDIR_PATH)
client = speech.SpeechClient(credentials=credentials)

def get_transcript(content: bytes = None, audio_path: str = None):
    """
    Gets transcript of audio file.

    Args:
        content (bytes): Content of audio file as bytes.
        audio_path (str): Path to audio file.

    Returns:
        object: Processed audio file for speech-to-text.
    """
    if content is None and audio_path is None:
        raise ValueError('At least one parameter cannot be None.')

    audio = speech.RecognitionAudio(uri=audio_path) if content is None else speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)
    for result in response.results:
        print(f'Transcript: {result.alternatives[0].transcript}')

    return response

if __name__ == "__main__":
    # 2:06 minute sample file too big
    print('-' * 100)
    audio_path = '/mnt/d/Users/qcaij/OneDrive - University of Florida/DESKTOP-1S7D2TD/qcaij/Desktop/VisualMarketAI-/backend/data/customer_support_sample_1.wav'
    audio_bytes = open(file=audio_path, mode='rb').read()
    print(audio_bytes)
    response = get_transcript(content=audio_bytes)
