import os

"""Transcribe the given audio file."""
from google.cloud import speech
from google.oauth2 import service_account
from google.cloud.speech import enums
from google.cloud.speech import types


def transcribe_file(storage_uri):
    # Instantiates a client
    SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
    SERVICE_ACCOUNT_FILE = 'quantum-episode-258704-8b7f974f4cc6.json'

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

    response = operation.result()

    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(u"{}".format(alternative.transcript))


def main():
    storage_uri = os.getcwd() + '/uri.txt'
    f = open(storage_uri, "r")

    for file_name in f.readlines():
        transcribe_file(file_name)


main()