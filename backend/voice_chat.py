
import io, os
from dotenv import load_dotenv
from google.cloud import speech
from google.oauth2 import service_account

load_dotenv()
KEYDIR_PATH = os.getenv("KEYDIR_PATH")
credentials = service_account.Credentials.from_service_account_file(KEYDIR_PATH)
client = speech.SpeechClient(credentials=credentials)


def get_transcript(content: bytes = None, audio_path: str = None):
    """
    Gets transcript of audio file.

    Args:
        content (bytes): Content of audio file as bytes.
        audio_path (str): Path or uri to audio file.

    Returns:
        object: Processed audio file for speech-to-text.
    """
    if content is None and audio_path is None:
        raise ValueError("At least one parameter cannot be None.")

    audio = (
        speech.RecognitionAudio(uri=audio_path)
        if content is None
        else speech.RecognitionAudio(content=content)
    )
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)
    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

    return response

def get_transcript_long(content: bytes = None, audio_path: str = None):
    """
    Gets transcript of long audio file asynchonously.

    Args:
        content (bytes): Content of audio file as bytes.
        audio_path (str): Path or uri to audio file.

    Returns:
        object: Processed audio file for speech-to-text.
    """
    if content is None and audio_path is None:
        raise ValueError('At least one parameter cannot be None.')

    audio = speech.RecognitionAudio(uri=audio_path) if content is None else speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))

    return response

def transcribe_streaming(stream_file: str):
    """Streams transcription of the given audio file."""


    audio_file = io.open(stream_file, "rb")
    content = audio_file.read()

    # In practice, stream should be a generator yielding chunks of audio data.
    stream = [content]
    requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in stream)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    streaming_config = speech.StreamingRecognitionConfig(config=config)

    # streaming_recognize returns a generator.
    responses = client.streaming_recognize(
        config=streaming_config,
        requests=requests,
    )

    for response in responses:
        # Once the transcription has settled, the first result will contain the
        # is_final result. The other results will be for subsequent portions of
        # the audio.
        for result in response.results:
            print("Finished: {}".format(result.is_final))
            print("Stability: {}".format(result.stability))
            alternatives = result.alternatives
            # The alternatives are ordered from most likely to least.
            for alternative in alternatives:
                print("Confidence: {}".format(alternative.confidence))
                print(u"Transcript: {}".format(alternative.transcript))

if __name__ == "__main__":
    # 2:06 minute sample file too big
    print('-' * 100)
    audio_path = '/mnt/d/Users/qcaij/OneDrive - University of Florida/DESKTOP-1S7D2TD/qcaij/Desktop/visual-market-ai-backend/backend/data/customer_support_sample_2.wav'
    audio_bytes = open(file=audio_path, mode='rb').read()
    # print(audio_bytes)
    transcribe_streaming(stream_file=audio_path)
