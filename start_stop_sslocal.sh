#!/bin/bash
ischangedip='ischangedip'
host='167.179.74.191'
port=5112
redis_ps='juhuacha188'
var1=10
change_ip_str='change_ip'
changedip='changedip'
while [ $var1 -gt 1 ]
do
current_status=`redis-cli -h $host -p $port -a $redis_ps get $ischangedip`


echo "current_status is ------  $current_status"
#result=$( echo $change_ip_str | grep change_ip )
if [[ "$current_status" == "change_ip" ]]
then
  echo "开始更换"

  pid=`cat ./sslocal.pid`
  kill -9 $pid
  nohup sslocal -c /etc/shadowsocks.json &
  echo $! > ./sslocal.pid
  redis-cli -h $host -p $port -a $redis_ps set $ischangedip $changedip
else
  echo "不用更换"
fi

sleep 6
done

