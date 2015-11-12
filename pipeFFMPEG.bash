#!/bin/bash
cat $(cat $1.list) | /home/rashley/bin/ffmpeg -r 12 -f image2pipe -y -i - -vcodec libx264 $1.mp4


