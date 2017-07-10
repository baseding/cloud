#!/bin/bash

PID="cloud.pid"

function start {
python manage.py runserver 0:8000 &
sleep 2
ps -ef | grep "python manage.py runserver 0:8000$" | awk '{print $2}' > $PID
}


function stop {
for i in `cat $PID`; do kill -9 $i; done
echo > $PID
}


# main program
case $1 in 
         start | begin) 
           echo "start django program:" 
	   start
         ;; 
         stop | end) 
           echo "stop django program:" 
	   stop
	 ;; 
         *) 
           echo "Error command,Ignorant" 
         ;; 
 esac 

