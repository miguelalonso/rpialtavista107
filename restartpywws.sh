#!/bin/sh
export PATH=$PATH:/usr/local/bin 
pidfile=/var/run/pywws.pid 
datadir=/home/pi/weather/data 
logfile=$datadir/live_logger.log
# exit if process is running
[ -f $pidfile ] && kill -0 `cat $pidfile` && exit
# restart process
sudo pywws-livelog-daemon -v -p $pidfile $datadir $logfile start
