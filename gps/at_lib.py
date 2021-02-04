import logging


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
