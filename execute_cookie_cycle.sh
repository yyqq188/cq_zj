#!/bin/bash
var1=10
while [ $var1 -gt 1 ]
do
	docker start 7ad5fdcff251
	sleep 60
done
