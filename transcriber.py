import os
import sys

"""Transcribe the given audio file."""
from google.cloud import speech
from google.oauth2 import service_account
from google.cloud.speech import enums
from google.cloud.speech import types

if getattr(sys, 'frozen', False):
    app_path = os.path.dirname(sys.executable)
else:
    app_path = os.path.dirname(__file__)

result_dir = app_path + '/result/'
storage_uri = app_path + '/uri.txt'
json_file_name = 'speech-api-project.json'


def transcribe_file(storage_uri, frame_rate):
    # Notification
    print("Working on: {} ...".format(storage_uri))

    # Instantiates a client
    SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
    SERVICE_ACCOUNT_FILE = json_file_name

    cred = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = speech.SpeechClient(credentials=cred)

    # Variables for the setting
    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    language_code = 'ko-KR'

    # Loads the audio into memory
    audio = {"uri": storage_uri}
    config = types.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=int(frame_rate),
        language_code=language_code)

    # Detects speech in the audio file
    operation = client.long_running_recognize(config, audio)

    # get_operation_request = discovery.build('speech', 'v1', credentials=cred).operations().get(name=operation_name)
    # response = get_operation_request.execute()
    #
    # # handle polling
    # retry_count = 10
    # while retry_count > 0 and not response.get('done', False):
    #     retry_count -= 1
    #     time.sleep(60)
    #     response = get_operation_request.execute()

    transcript = u''
    response = operation.result()

    for result in response.results:
        # First alternative is the most probable result
        transcript += result.alternatives[0].transcript

    return transcript


def main():
    f = open(storage_uri, "r")

    for file_name in f.readlines():

        file_name, frame_rate = file_name.split('\t')
        frame_rate = frame_rate.rstrip()
        transcript = transcribe_file(file_name, frame_rate)

        file_name = file_name.split('/')[-1].split('.')[0]
        transcript_file = open(result_dir + file_name + '.txt', "w")

        transcript_file.write(transcript + '\n')
        transcript_file.close()

        print(" --- {} done \n".format(file_name))

    f.close()


main()
input("---\n---\nFinished transcribing process. Press Enter to exit...")
