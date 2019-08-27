#!/bin/bash
var1=10
dockerimage=yyqq188/qcc_asiainfo_cookie_191
docker run -d $dockerimage
sleep 20
dockerid=`docker ps -a | grep $dockerimage | cut -b 1-10 | head -n 1`
while [ $var1 -gt 1 ]
do
    sleep 60
    docker start $dockerid

done
