import logging
from time import sleep


def init_gps(ser, use_agps=False):
    at_list = [
        ["ATE0", None],
        ["AT+CGNSTST=0", None],
        ["AT+SAPBR=3,1,\"CONTYPE\",\"GPRS\"", None]  #Set bearer parameter
        ,
        ["AT+SAPBR=3,1,\"APN\",\"INTERNET.T-MOBILE\"",
         None]  #Set bearer context
        ,
        ["AT+SAPBR=1,1", None]  #Active bearer context
        ,
        ["AT+SAPBR=2,1", "+SAPBR"]  #Read NTP server and time zone parameter
        ,
        ["AT+CNTPCID=1", None],
        ["AT+CNTP", "+CNTP"]  #Read local time
        ,
        ["AT+CNTP?", "+CNTP"]  #Synchronize Network Time to local
        ,
        ["AT+CCLK?", "+CCLK"]  #Download EPO File
        ,
        ["AT+FTPSERV=\"116.247.119.165\"", None]  #Set FTP user name
        ,
        ["AT+FTPUN=\"customer\"", None]  #Set FTP password
        ,
        ["AT+FTPPW=\"111111\"", None]  #Set download file name
        ,
        ["AT+FTPGETNAME=\"MTK3.EPO\"", None]  #Set Download file path
        ,
        ["AT+FTPGETPATH=\"/\"", None]  #Download data to local buffer
        ,
        ["AT+FTPEXTGET=1", "+FTPEXTGET"]  #save data to local disk as EPO file
        ,
        ["AT+FTPEXTGET=4,\"epo\"", "+FTPEXTGET"]  #List Directories/Files
        ,
        ["AT+CGNSCHK=3,1", "+CGNSCHK"]  #Power on GPS
        ,
        ["AT+CGNSPWR=1", None]  #Send EPO file to GPS
        ,
        ["AT+CGNSAID=31,1,1", None]  #"+CGNSAID"]
        ,
        ["AT+CGNSTST=1", None]
    ]
    at_list = [
        ["AT+CGNSPWR=1", None]  #Power GPS
        ,
        ["AT+CGNSTST=1", None]
    ]  # Forward NMEA
    logging.info("Preparing GPS")
    for item in at_list:
        at_communicate(ser, item[0], item[1])
        sleep(0.1)


def at_communicate(ser, cmd, expect=None):
    if not cmd.endswith("\r\n"):
        cmd = cmd.join("\r\n")
    ser.write(cmd)
    logging.info(cmd)
    ok_received = False
    expect_received = False
    if expect is None:
        expect_received = True
    while True:
        line = ser.readline()
        if line != "":
            logging.debug(line)
        if line == "OK\r\n":
            ok_received = True
            logging.info("OK Received")
        if line == "ERROR\r\n":
            logging.error("ERROR Received")
            return False
        if expect is not None:
            if expect in line:
                expect_received = True
                logging.info("{} Received".format(line))
        if expect_received and ok_received:
            return True
