import os

"""Transcribe the given audio file."""
from google.cloud import speech
from google.oauth2 import service_account
from google.cloud.speech import enums
from google.cloud.speech import types


result_dir = os.getcwd() + '/result/'
storage_uri = os.getcwd() + '/uri.txt'
json_file_name = 'speech-17e53241af23.json'


def transcribe_file(storage_uri):
    # Notification
    print("Working on: {} ...".format(storage_uri))

    # Instantiates a client
    SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
    SERVICE_ACCOUNT_FILE = json_file_name

    cred = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = speech.SpeechClient(credentials=cred)

    # Variables for the setting
    encoding = enums.RecognitionConfig.AudioEncoding.FLAC
    sample_rate_hertz = 48000
    language_code='ko-KR'

    # Loads the audio into memory
    audio = {"uri": storage_uri}
    config = types.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate_hertz,
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
        transcript = transcribe_file(file_name)

        file_name = file_name.split('/')[-1].split('.')[0]
        transcript_file = open(result_dir + file_name + '.txt', "w")

        transcript_file.write(transcript + '\n')
        transcript_file.close()

        print(" --- {} done \n".format(file_name))

    f.close()


main()