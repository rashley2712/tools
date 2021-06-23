#!/bin/bash
ping -c 1 8.8.8.8 | egrep 'time=' | awk '{print $7}' | awk 'BEGIN { FS = "=" }; {print $2}' > /tmp/ping.log
