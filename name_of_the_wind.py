#! /usr/bin/env python3

from threading import Thread
import socket, ssl
from wind_controller import WindController2
# from calibrator import FitSpeed

__author__ = 'Janez Presern'

wc = WindController2(n_motors=1, pwmFreq=100)
pFreq = int(wc.pwmFreq)
pStop = int(wc.pwmDict[pFreq][0])
pStart = int(wc.pwmDict[pFreq][1])
pMax = int(wc.pwmDict[pFreq][2])


def do_some_stuffs_with_input(input_string):
    """
    This is where all the processing happens.

    Let's just read the string backwards
    """

    print("Processing that nasty input!")
    return input_string[::-1]


def rec_data(conn, MAX_BUFFER_SIZE):
    input_from_client_bytes = conn.recv(MAX_BUFFER_SIZE)

    import sys
    siz = sys.getsizeof(input_from_client_bytes)
    if  siz >= MAX_BUFFER_SIZE:
        print("The length of input is probably too long: {}".format(siz))

    input_from_client = input_from_client_bytes.decode("utf8").rstrip()

    return input_from_client


def client_thread(conn, ip, port, MAX_BUFFER_SIZE = 8888):
# def client_thread(conn, ip, port, fs, MAX_BUFFER_SIZE=8888):

    # read lines periodically without ending connection
    still_listen = True
    count = 1
    while still_listen:
        input_from_client = rec_data(conn, MAX_BUFFER_SIZE)

        # if you receive this, end the connection
        if "--ENDOFDATA--" in input_from_client:
            print('--ENDOFDATA--')
            wc.stopMotors()
            conn.close()
            print('Connection ' + ip + ':' + port + " ended")
            still_listen = False

        elif "arm" in input_from_client:

            wc.armMotors(input_from_client.split("_")[1])
            conn.send(str("armed").encode("utf_8"))

        else:

            wc.setSpeed(int(input_from_client))
            conn.send(str("done").encode("utf_8"))

def start_server():
# def start_server(fit_speed):

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCP_KEEPALIVE = 0x10
    print('Socket created')

    try:
        # soc.bind(("127.0.0.1", 12345))
        soc.bind(("0.0.0.0", 12345))        # for RPi
        print('Socket bind complete')
    except socket.error as msg:
        import sys
        print('Bind failed. Error : ' + str(sys.exc_info()))
        sys.exit()

    #Start listening on socket
    soc.listen(1)
    print('Socket now listening')

    # this will make an infinite loop needed for
    # not reseting server for every client
    while True:
        conn, addr = soc.accept()
        ip, port = str(addr[0]), str(addr[1])
        print('Accepting connection from ' + ip + ':' + port)
        try:
            # Thread(target=client_thread, args=(conn, ip, port, fs)).start()
            Thread(target=client_thread, args=(conn, ip, port)).start()
            # client_thread(conn, ip, port)
        except:
            print("Terible error!")
            import traceback
            traceback.print_exc()
    soc.close()


if __name__ == "__main__":
    # fs = FitSpeed('./kalibracije/kalibracija.csv')
    # start_server(fs)
    start_server()
