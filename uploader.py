import wave
import soundfile as sf
from pydub import AudioSegment

from google.cloud import storage

import os

source_dir = os.path.join(os.getcwd(), 'audio_source')
upload_dir = os.path.join(os.getcwd(), 'audio_upload')
bucketname = open(os.path.join(os.getcwd(), 'bucket.txt'), "r").readline()
json_file_name = 'speech-api-project.json'
storage_uri = os.path.join(os.getcwd(), 'uri.txt')


def to_wav(audio_file_name):
    extension = audio_file_name.split('.')[-1]

    # paths for audio files
    source_file_path = os.path.join(source_dir, audio_file_name)
    audio_file_name = audio_file_name.split('.')[0] + '.wav'
    upload_file_path = os.path.join(upload_dir, audio_file_name)

    # convert it to wav and save it in upload_dir
    if extension == 'mp3':
        sound = AudioSegment.from_mp3(source_file_path)
        sound.export(upload_file_path, format="wav")
    if extension == 'flac':     #TODO: FLAC convert error? uri 생성이 안됨
        sound, frame_rate = sf.read(source_file_path)
        sf.write(upload_file_path, sound, frame_rate)

    frame_rate, channels = frame_rate_channel(audio_file_name)
    if channels > 1:
        stereo_to_mono(audio_file_name)

    return audio_file_name, frame_rate


def stereo_to_mono(audio_file_name):
    audio_file_name = os.path.join(upload_dir, audio_file_name)

    sound = AudioSegment.from_wav(audio_file_name)
    sound = sound.set_channels(1)
    sound.export(audio_file_name, format="wav")


def frame_rate_channel(audio_file_name):
    audio_file_name = os.path.join(upload_dir, audio_file_name)
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

    # convert to wav, if not already wav.
    if audio_file.split('.')[-1] != 'wav':
        audio_file, frame_rate = to_wav(audio_file)
    else:
        frame_rate = frame_rate_channel(audio_file)

    # variables for upload
    bucket_name = bucketname
    source_file_name = os.path.join(upload_dir, audio_file)
    destination_blob_name = audio_file

    # upload
    upload_blob(bucket_name, source_file_name, destination_blob_name)

    gcs_uri = 'gs://' + bucketname + '/' + audio_file + '\t' + str(frame_rate)
    return gcs_uri


def main():
    uri_file = open(storage_uri, 'w+')

    audio_list = [e for e in os.listdir(source_dir) if e[0] != '.']
    for audio_file in audio_list:
        if os.path.isfile(os.path.join(source_dir, audio_file)):
            gcs_uri = upload_audio(audio_file)

            print('uri: {}'.format(gcs_uri))
            uri_file.write(gcs_uri + '\n')      #TODO: uri_file open까진 되는거 같은데 왜 쓰기가 안되는거지!!!!!

    uri_file.close()


main()
input("Finished uploading process. Press Enter to exit...")
