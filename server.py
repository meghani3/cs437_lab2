import socket
import datetime
from picarx import Picarx
from gpiozero import CPUTemperature

HOST = "192.168.0.107" # IP address of your Raspberry PI
PORT = 1030          # Port to listen on (non-privileged ports are > 1023)

robot = Picarx()
robot.set_cliff_reference([200, 200, 200])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    print("Starting")

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

                if  ret == b"0:0":
                    robot.forward(0)
                    ret = b'ok'

                if  ret == b"0:1":
                    robot.forward(1)
                    ret = b'ok'

                if  ret == b"0:-1":
                    robot.forward(-1)
                    ret = b'ok'

                if  ret == b"1:0":
                    robot.set_dir_servo_angle(0)
                    ret = b'ok'

                if  ret == b"1:1":
                    robot.set_dir_servo_angle(35)
                    ret = b'ok'

                if  ret == b"1:-1":
                    robot.set_dir_servo_angle(-35)
                    ret = b'ok'

                if ret == b"stats":
                    temperature = CPUTemperature().temperature
                    distance = round(robot.ultrasonic.read(), 2)
                    if (distance < 0):
                        distance = '∞'
                    cliff = robot.get_cliff_status(robot.get_grayscale_data())

                    ret = f'Temperature:{temperature}\nDistance:{distance}\nCliff:{cliff}'.encode()


                ret = ret + b"\r\n"
                print("ret", ret)

                client.sendall(ret) # Echo back to client
    finally:
        print("Closing socket")
        client.close()
        s.close()    
        robot.forward(0)
