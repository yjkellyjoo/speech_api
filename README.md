# Speech-to-Text converter


##Data privacy and security
This program uses Google Speech-to-Text API with Data Logging disabled, which means your audio file data will not be collected. 

For more details, check out the following links:
https://cloud.google.com/speech-to-text/docs/data-logging
https://cloud.google.com/speech-to-text/docs/data-logging-terms


##Setup
###Windows OS

###Mac OS
1. Install Python 3 if you do not already have it installed. 
2. Go to `Spotlight Search (Cmd + Space)` and open `Terminal`.
When Terminal pops up, type in the following: 
> pip install -r requirements.txt


##How to Use



##Caution
###1. Recording Format
 - Using a lossless codec (FLAC or LINEAR16) is recommended.
 - If not, WAV or MP3 files are acceptable.

###2. The clearer your recording, the better the result.
 - If multiple people are talking at the same time, or at different volumes, they may be interpreted as background noise and ignored.

###3. Audio pre-processing
 - Do not use automatic gain control (AGC).
 - Noise reduction processing should be disabled.