
import json, os, speech_recognition as sr
from dotenv import load_dotenv

load_dotenv()
KEYDIR_PATH = os.getenv(key='KEYDIR_PATH')

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print('Say something!')
    audio = r.listen(source)

# recognize speech using Sphinx
try:
    print('Sphinx thinks you said:\n' + r.recognize_sphinx(audio))
except sr.UnknownValueError:
    print('Sphinx could not understand audio')
except sr.RequestError as e:
    print(f'Sphinx error; {e}')


# recognize speech using Google Cloud Speech
credentials_file = open(file=KEYDIR_PATH, mode='rb').read()
credentials = json.dumps(obj=json.loads(s=credentials_file))
# print(credentials)

try:
    print('Google Cloud Speech thinks you said:\n' + r.recognize_google_cloud(audio, credentials_json=credentials))
except sr.UnknownValueError:
    print('Google Cloud Speech could not understand audio')
except sr.RequestError as e:
    print(f'SphinxCould not request results from Google Cloud Speech service; {e}')
