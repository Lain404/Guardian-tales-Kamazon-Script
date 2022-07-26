adb kill-server 
adb start-server 

adb tcpip 11509
adb connect 127.0.0.1:11509
#adb -s 127.0.0.1:11509 tcpip 11509
#adb connect 127.0.0.1:11509
pause
