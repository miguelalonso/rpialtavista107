#actualización en marzo de 2016 con tarjeta 32 Gb

#crontab

@reboot /home/pi/weather/pywwsrestart.sh > /dev/null 2>&1
*/30 * * * /home/pi/weather/pywwsrestart.sh > /dev/null 2>&1
@reboot python /home/pi/raspi-RF24/sendtoemoncms20160306.py > /dev/null 2>&1
*/20 * * *  python /home/pi/raspi-RF24/sendtoemoncms20160306.py > /dev/null 2>&1

