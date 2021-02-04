echo "AT+SAPBR=3,1,\"CONTYPE\",\"GPRS\"" > /dev/ttyUSB0
sleep 1
#Set bearer parameter
echo "AT+SAPBR=3,1,\"APN\",\"INTERNET.T-MOBILE\"" > /dev/ttyUSB0
sleep 1
#Set bearer context
echo "AT+SAPBR=1,1" > /dev/ttyUSB0
sleep 1
#Active bearer context
echo "AT+SAPBR=2,1" > /dev/ttyUSB0
sleep 1
#Read NTP server and time zone parameter
echo "AT+CNTPCID=1" > /dev/ttyUSB0
sleep 1
echo "AT+CNTP?" > /dev/ttyUSB0
sleep 1
#Synchronize Network Time to local
echo "AT+CNTP" > /dev/ttyUSB0
sleep 30
#Read local time
echo "AT+CCLK?" > /dev/ttyUSB0
sleep 1
#Download EPO File
#Set FTP server address
echo "AT+FTPSERV=\"116.247.119.165\"" > /dev/ttyUSB0
sleep 1
#Set FTP user name
echo "AT+FTPUN=\"customer\"" > /dev/ttyUSB0
sleep 1
#Set FTP password
echo "AT+FTPPW=\"111111\"" > /dev/ttyUSB0
sleep 1
#Set download file name
echo "AT+FTPGETNAME=\"MTK3.EPO\"" > /dev/ttyUSB0
sleep 1
#Set Download file path
echo "AT+FTPGETPATH=\"/\"" > /dev/ttyUSB0
sleep 1
#Download data to local buffer
echo "AT+FTPEXTGET=1" > /dev/ttyUSB0
sleep 120
#save data to local disk as EPO file
echo "AT+FTPEXTGET=4,\"epo\"" > /dev/ttyUSB0
sleep 60
#List Directories/Files
echo "AT+FSLS=C:\User\"" > /dev/ttyUSB0
sleep 1
#Check EPO file size and validation
echo "AT+CGNSCHK=3,1" > /dev/ttyUSB0
sleep 1
#Power on GPS
echo "AT+CGNSPWR=1" > /dev/ttyUSB0
sleep 1
#Send EPO file to GPS
echo "AT+CGNSAID=31,1,1" > /dev/ttyUSB0
sleep 1
echo "AT+CGNSINF" > /dev/ttyUSB0
