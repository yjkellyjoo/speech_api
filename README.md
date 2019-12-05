# Speech-to-Text converter


##Data privacy and security
This program uses Google Speech-to-Text API with Data Logging disabled, which means your audio file data will not be collected. 

For more details, check out the following links:
https://cloud.google.com/speech-to-text/docs/data-logging
https://cloud.google.com/speech-to-text/docs/data-logging-terms


##Setup
1. Install ffmpeg.
http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/


##How to Use



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
It occurs because ffmpeg is not installed. 
http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/

