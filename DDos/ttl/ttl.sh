#!/bin/bash

for i in {1..5000000}; do echo -n "Run # $i :: ";
curl -w 'Return code: %{http_code}; Bytes Received: %{size_download};
Response Time: %{time_total}\n' http://127.0.0.1:8080/ -m 2 -o /dev/null -s;
sleep 2;
done|tee /dev/tty|awk '{ sum+= $NF; n++ } END { if (n > 0) print "Average Response time =",sum / n; }'