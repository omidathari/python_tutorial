import socket
import threading
import time

class udpServerObject:
    def __init__(self,ip_address, port_number, rx_callback) -> None:
        self.rx_callback = rx_callback
        self.ip_address = ip_address
        self.port_number = port_number
        self.buffersize = 2000
        self.rx_thread = threading.Thread(target = self.__receiver)
        self.tx_mutex = threading.Lock()
        # Create a UDP socket at server side
        self.udpServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def start(self):
        try:
            # Bind to address and ip
            self.udpServerSocket.bind((self.ip_address, self.port_number))
            self.rx_thread.start()
        except BaseException as e:
            print("UDP Server Start Exception")
            print(e)

    def __receiver(self):
        print("Start the UDP Server receiver thread")
        time.sleep(1)
        while True:
            try:
                msgFromClient = self.udpServerSocket.recvfrom(self.buffersize)
                self.rx_callback(msgFromClient[0],msgFromClient[1])
            except BaseException as e:
                print("UDP Server Receiver Exception\r\n" , e)
                time.sleep(3)

    def send(self,data,address):
        try:
            if( True == self.tx_mutex.acquire() ):
                print("UDP Server Send: ",data)
                self.udpServerSocket.sendto(data, address)
                self.tx_mutex.release()
        except BaseException as e:
            print("UDP TX Exception.")
            print(e)

def udp_server_receiver( data, address ):
    print(data,address)
    udps.send(data,address)

udps = udpServerObject("127.0.0.1", 20001,udp_server_receiver)

udps.start()

while True:
    time.sleep(1)
