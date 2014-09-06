avconv -i $1 -f mp3 -acodec libmp3lame -aq 6 -ac 1 audio-mp3/$(basename $1 .aiff).mp3
