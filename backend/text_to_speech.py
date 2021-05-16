
import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.cloud import texttospeech

load_dotenv()
KEYDIR_PATH = os.getenv('KEYDIR_PATH')
credentials = service_account.Credentials.from_service_account_file(KEYDIR_PATH)
client = texttospeech.TextToSpeechClient(credentials=credentials)

def synthesize_text(text: str, output_file: str = 'output.wav'):
    """
    Synthesizes speech from the input string of text.

    Args:
        text (str): Text to speak out.
        output_file (str, optional): File name of output save. Defaults to 'output.wav'.
    """

    input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-C",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    # The response's audio_content is binary.
    with open(file=output_file, mode='wb') as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_file}"')


if __name__ == '__main__':
    text = 'This is sample text.'
    synthesize_text(text=text)
