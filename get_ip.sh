#!/bin/bash
proxypool_key='proxypool_1'
host='167.179.74.191'
port=5112
redis_ps='juhuacha188'
var1=10
while [ $var1 -gt 1 ]
do
redis-cli -h $host -p $port -a $redis_ps del $proxypool_key
/sbin/ifdown ppp0 > /dev/null 2>&1
/sbin/ifup ppp0 > /dev/null 2>&1
new_ip=` ifconfig | grep destination | awk 'BEGIN{FS=" "} {print $2}'`
echo $new_ip
redis-cli -h $host -p $port -a $redis_ps set $proxypool_key $new_ip
sleep 60
done

