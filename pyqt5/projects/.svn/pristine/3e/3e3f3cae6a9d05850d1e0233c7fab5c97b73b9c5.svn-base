import socket
import threading
import time

class udpClientObject:
    def __init__(self,server_ip, server_port, client_ip, client_port, rx_callback) -> None:
        self.rx_callback = rx_callback
        self.sip_address = server_ip
        self.sport_number = server_port
        self.cip_address = client_ip
        self.cport_number = client_port
        self.buffersize = 2000
        self.rx_thread = threading.Thread(target = self.__receiver)
        self.tx_mutex = threading.Lock()
        self.serverAddressPort = (self.sip_address, self.sport_number)
        # Create a UDP socket at client side
        self.udpClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def start(self):
        print("UDP Client Start")
        self.udpClientSocket.bind((self.cip_address, self.cport_number))
        self.rx_thread.start()

    def stop(self):
        self.udpClientSocket.close()

    def __receiver(self):
        print("Start the UDP Client receiver thread")
        #time.sleep(1)
        while True:
            try:
                msgFromServer = self.udpClientSocket.recvfrom(self.buffersize)
                #print(msgFromServer[1])
                self.rx_callback(msgFromServer[0])
                # print(msgFromServer[0])
                # print(".")
            except BaseException as e:
                print(e.args)
                if( e.args[0] == 10038):
                    break
                print("UDP Receiver Exception" , str(e))

    def send(self,data):
        try:
            if( True == self.tx_mutex.acquire() ):
                #print("UDP Client Send: ",data)
                self.udpClientSocket.sendto(data, self.serverAddressPort)
                self.tx_mutex.release()
        except BaseException as e:
            print("UDP TX Exception.")
            print(str(e))

# Example Usage
# def udp_client_receiver( data ):
#     print(data)

# udpc = udpClientObject("127.0.0.1", 20001,"127.0.0.1", 20003, udp_client_receiver)

# udpc.start()

# num = 0
# while True:
#     time.sleep(1)
#     udpc.send( str.encode("Hello UDP Server" + str(num)))
#     num += 1