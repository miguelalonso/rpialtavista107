#!/bin/sh

export PATH=$PATH:/usr/local/bin

# exit if NTP hasn't set computer clock
[ `ntpdc -c sysinfo | awk '/stratum:/ {print $2}'` -ge 10 ] && exit

pidfile=/var/run/pywws.pid
datadir=/home/pi/weather/data
logfile=$datadir/live_logger.log

# exit if process is running
[ -f $pidfile ] && kill -0 `cat $pidfile` && exit


# restart process
pywws-livelog-daemon -v -p $pidfile $datadir $logfile start
