# Speech-to-Text converter


##Data privacy and security
This program uses Google Speech-to-Text API with Data Logging disabled, which means your audio file data will not be collected. 

For more details, check out the following links:
https://cloud.google.com/speech-to-text/docs/data-logging
https://cloud.google.com/speech-to-text/docs/data-logging-terms


##Setup
###1. Install ffmpeg
Following link shows you how to install ffmpeg: http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/
Make sure to reboot your machine after installation. 

###2. Setup your Google Cloud Platform information
Two files from your account are required:
1. A txt file containing your bucket's name. 
2. A json file containing your project's information.

###3. Make two new folders
1. audio_source
The audio recording files you wish to convert must be saved into a folder named 'audio_source'. 
This folder must be placed in the same location as the execution files. 
2. result
The resulting text files will be created into a folder named 'result'.
This folder must be placed in the same location as the execution files.


##How to Use
### 1. Run uploader
When it's run, 
### 2. Run transcriber
When it's run,
 


##Caution
###1. Recording Format
 - Using a lossless codec (WAV or FLAC) is recommended.
 - If not, MP3 files are acceptable.

###2. The clearer your recording, the better the result.
 - If multiple people are talking at the same time, or at different volumes, they may be interpreted as background noise and ignored.

###3. Audio pre-processing
 - Do not use automatic gain control (AGC).
 - Noise reduction processing should be disabled.
 

## Frequently asked Questions
### 1. ffmpeg error
It occurs because ffmpeg is not installed. Follow the instructions at Setup #1.  

