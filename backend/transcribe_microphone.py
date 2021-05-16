
import json, os, speech_recognition as sr
from dotenv import load_dotenv

load_dotenv()
KEYDIR_PATH = os.getenv(key='KEYDIR_PATH')

def get_transcript_microphone(timeout: int=3, phrase_time_limit: int=30):
    """
    Gets transcript from microphone.

    Args:
        timeout (int, optional): Number of seconds of silence before microphone autocloses with error. Defaults to 3.
        phrase_time_limit (int, optional): Number of seconds in total allowed for recording via microphone. Defaults to 30.
    """
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something!')
        audio = r.listen(source=source, timeout=timeout, phrase_time_limit=phrase_time_limit)

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
#     print(f'SphinxCould not request results from Google Cloud Speech service; {e}')

if __name__ == '__main__':
    transcript = get_transcript_microphone()
