#!/bin/bash
var1=10
while [ $var1 -gt 1 ]
do
	docker start 4902d6a0dcd5
	sleep 60
done
