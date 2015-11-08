#!/bin/bash
cat $(cat $1.list) | ffmpeg -r 12 -f image2pipe -y -i - -vcodec mpeg4 $1.avi


