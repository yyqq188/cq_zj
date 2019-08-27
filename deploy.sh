#!/usr/bin/env bash

#spider_name='yyqq188/qcc_asiainfo_pagelist_spider_3:v1'
#spider_name='yyqq188/qcc_asiainfo_detail_spider_3:v1'
spider_name='yyqq188/qcc_asiainfo_cookie_191'

docker rmi -f $spider_name
docker build -t $spider_name .
docker push $spider_name


#ip='45.77.11.233'
#passwd='(Ps2r{C9sE]FscQL'

#/usr/bin/expect << eeoff
#set time 1
#spawn ssh root@10.1.236.121 -p 22022
#expect {
#"*password:" { send "$passwd\r" }
#}
#expect "*#"
#send "docker rmi -f $spider_name\r"
#expect "*#"
#send "docker pull $spider_name\r"
#expect "*#"
#send "exit\r"
#eeoff
#echo done
