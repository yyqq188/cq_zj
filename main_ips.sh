#!/bin/bash
proxypool_key='proxypool_1'
host='45.77.11.233'
port=5112
redis_ps='juhuacha188'
var1=10
while [ $var1 -gt 1 ]
do
redis-cli -h 45.77.11.233 -p 5112 -a juhuacha188 del $proxypool_key
/sbin/ifdown ppp0 > /dev/null 2>&1
/sbin/ifup ppp0 > /dev/null 2>&1
new_ip=` ifconfig | grep destination | awk 'BEGIN{FS=" "} {print $2}'`
echo $new_ip
redis-cli -h $host -p $port -a $redis_ps set $proxypool_key $new_ip
sleep 6
done
