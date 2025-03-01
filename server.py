import socket
import datetime

HOST = "172.20.68.125" # IP address of your Raspberry PI
PORT = 1030          # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            if data != b"":
                ret = data.strip()
                print("Request:", ret)

                if ret == b"ts":
                    ret = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S").encode()

                ret = ret + b"\r\n"
                print("ret", ret)

                client.sendall(ret) # Echo back to client
    finally:
        print("Closing socket")
        client.close()
        s.close()    
