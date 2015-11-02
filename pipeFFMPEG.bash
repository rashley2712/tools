#!/bin/bash
cat $(cat $1.list) | ffmpeg -r 12 -f image2pipe -y -vcodec mjpeg -i - -c:v libx264 $1.avi


