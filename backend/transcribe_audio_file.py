
import json, os, speech_recognition as sr
from dotenv import load_dotenv

load_dotenv()
KEYDIR_PATH = os.getenv(key='KEYDIR_PATH')


def get_transcript(audio_path: str):
    """
    Gets transcript of audio file.

    Args:
        content (bytes): Content of audio file as bytes.
        audio_path (str): Path or uri to audio file.

    Returns:
        object: Processed audio file for speech-to-text.
    """
    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(filename_or_fileobject=audio_path) as audio_src:
        audio = r.record(source=audio_src)

    # recognize speech using Sphinx
    transcript = str()
    try:
        transcript = r.recognize_sphinx(audio_data=audio)
        print('Sphinx thinks you said:\n' + transcript)
    except sr.UnknownValueError:
        print('Sphinx could not understand audio')
    except sr.RequestError as e:
        print(f'Sphinx error; {e}')

    return transcript

# recognize speech using Google Cloud Speech
# credentials_file = open(file=KEYDIR_PATH, mode='rb').read()
# credentials = json.dumps(obj=json.loads(s=credentials_file))
# print(credentials)

# try:
#     print('Google Cloud Speech thinks you said:\n' + r.recognize_google_cloud(audio_data=audio, credentials_json=credentials))
# except sr.UnknownValueError:
#     print('Google Cloud Speech could not understand audio')
# except sr.RequestError as e:
#     print(f'Could not request results from Google Cloud Speech service; {e}')

if __name__ == '__main__':
    audio_path = './data/customer_support_sample_2.wav'
    transcript = get_transcript(audio_path=audio_path)

