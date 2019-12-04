from pydub import AudioSegment
import wave
from google.cloud import storage

import os


audio_dir = os.getcwd() + '/audio_source/'
bucketname = open(os.getcwd()+'/bucket.txt', "r").readline()
json_file_name = 'speech-17e53241af23.json'
storage_uri = os.getcwd() + '/uri.txt'


def mp3_to_wav(audio_file_name):
    if audio_file_name.split('.')[-1] == 'mp3':
        audio_file_path = audio_dir + audio_file_name

        sound = AudioSegment.from_mp3(audio_file_path)
        audio_file_path = audio_file_path.split('.')[0] + '.wav'
        audio_file_name = audio_file_name.split('.')[0] + '.wav'
        sound.export(audio_file_path, format="wav")

    return audio_file_name


def stereo_to_mono(audio_file_name):
    audio_file_name = audio_dir + audio_file_name
    sound = AudioSegment.from_wav(audio_file_name)
    sound = sound.set_channels(1)
    sound.export(audio_file_name, format="wav")


def frame_rate_channel(audio_file_name):
    audio_file_name = audio_dir + audio_file_name
    with wave.open(audio_file_name, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        channels = wave_file.getnchannels()
        return frame_rate, channels


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # storage_client = storage.Client()
    storage_client = storage.Client.from_service_account_json(json_file_name)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)


def upload_audio(audio_file):
    print('uploading {} ...'.format(audio_file))

    audio_file = mp3_to_wav(audio_file)
    frame_rate, channels = frame_rate_channel(audio_file)
    if channels > 1:
        stereo_to_mono(audio_file)

    bucket_name = bucketname
    source_file_name = audio_dir + audio_file
    destination_blob_name = audio_file

    upload_blob(bucket_name, source_file_name, destination_blob_name)

    gcs_uri = 'gs://' + bucketname + '/' + audio_file

    return gcs_uri


def main():
    uri_file = open(storage_uri, 'w')

    audio_list = [e for e in os.listdir(audio_dir) if e[0] != '.']
    for audio_file in audio_list:
        if os.path.isfile(audio_dir + audio_file):
            gcs_uri = upload_audio(audio_file)

            print('uri: {}'.format(gcs_uri))
            uri_file.write(gcs_uri)

    uri_file.close()


main()