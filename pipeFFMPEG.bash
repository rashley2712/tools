#!/bin/bash
cat $(cat $1.list) | ffmpeg -r 12 -f image2pipe -y -i - -vcodec libx264 $1.mp4


