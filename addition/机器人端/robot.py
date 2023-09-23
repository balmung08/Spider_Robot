import time
import RPi.GPIO as GPIO
import serial
import socket
import pigpio
import cv2
import visual
import imu

def read_code():
    def connect():
        # HOST = 'localhost'
        HOST = '8.130.72.154'  # 服务器的公网IP
        PORT = 1178
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((HOST, PORT))
        return sock
    def read_target():
        sock.send("do".encode())
        status = sock.recv(1).decode()
        return status
    def read_mode():
        sock.send("mo".encode())
        status = sock.recv(1).decode()
        return status
    '''
    def read_mode():
        sock.send("mo".encode())
        status = sock.recv(1).decode()
        return status
    '''
    sock = connect()
    status = read_target()
    sock = connect()
    mode = read_mode()
    #print("status:" + str(status))
    return status,mode
def send_code(code):
    def connect():
        # HOST = 'localhost'
        HOST = '8.130.72.154'  # 服务器的公网IP
        PORT = 1177
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((HOST, PORT))
        return sock

    def update(data):
        sock.send("up".encode())
        sock.send(str(data).encode())
    sock = connect()
    update(code)
    print("sending:"+ str(code))

def go_straight():
    init_angle = imu.return_z()
    print("init_angle:"+str(init_angle))
    #st = b'UU\x05\x06\x01\x01\x00'
    fin = b'UU\x05\x08\x01\x01\x00'
    start = "55 55 05 06 00 01 00"
    left = "55 55 05 06 03 01 00"
    right = "55 55 05 06 04 01 00"
    straight = "55 55 05 06 01 01 00"
    small_right = "55 55 05 06 06 01 00"
    small_left = "55 55 05 06 07 01 00"
    mov = 1
    i = 1
    while True:
        if i==3:
            init_angle = imu.return_z()
        print(imu.return_z())
        err_angle = imu.return_z()-init_angle
        #print(imu.return_z())
        print("err:"+ str(err_angle))
        if -5 <= err_angle and err_angle <= 5:
            ted.write(bytes.fromhex(straight))
            ted.read(14)
            mov = 0
            '''
            if ted.read(7) == fin:
                mov = 0
                print("fin")
            '''
        err_angle = imu.return_z()-init_angle
        if err_angle>= 5:
            ted.write(bytes.fromhex(small_right))
            ted.read(14)
            print('turn right!')
        if err_angle <= -5:
            ted.write(bytes.fromhex(small_left))
            ted.read(14)
            print('turn left!')
        if str(read_code()[0]) != "1":
            #print(str(read_code()))
            print("exit_straight")
            break
        i += 1
        

    #print(imu.return_z())
ted = serial.Serial(port="/dev/ttyAMA1", baudrate=9600)
start = "55 55 05 06 00 01 00"
straight = "55 55 05 06 01 01 00"
back = "55 55 05 06 02 01 00"
left = "55 55 05 06 03 01 00"
right = "55 55 05 06 04 01 00"
small_left = "55 55 05 06 06 01 00"
small_right = "55 55 05 06 07 01 00"
servo1 = 78
servo2 = 20
# PWM1:2-13
GPIO.setmode(GPIO.BCM)
servo_pwm1 = pigpio.pi()
servo_pwm1.set_PWM_frequency(18,50)
servo_pwm1.set_PWM_range(18,1000)

servo_pwm2 = pigpio.pi()
servo_pwm2.set_PWM_frequency(23,50)
servo_pwm2.set_PWM_range(23,1000)

servo_pwm1.set_PWM_dutycycle(18,78)
servo_pwm2.set_PWM_dutycycle(23,20)
time_old = time.time()
video = cv2.VideoCapture(0)
mode = "0"
target = "0"



while True:
    if mode == "0":
        try:
            while True:
                status,mode = read_code()
                print(status,mode)
                if mode != "0":
                    print("out")
                    break
                if status == "0":
                    ted.write(bytes.fromhex(start))
                    time.sleep(0.05)
                if status == "1" :
                    print(2222)
                    go_straight()
                    #ted.write(bytes.fromhex(straight))
                    time.sleep(0.05)
                if status == "2" :
                    ted.write(bytes.fromhex(left))
                    time.sleep(0.05)
                if status == "3" :
                    ted.write(bytes.fromhex(back))
                    time.sleep(0.05)
                if status == "4" :
                    ted.write(bytes.fromhex(right))
                    time.sleep(0.05)
                if status == "5" :
                    if time.time()-time_old>0:
                        servo2 = servo2+10
                        if servo2 <= 25:
                            servo2 = 25
                        servo_pwm2.set_PWM_dutycycle(23,servo2)
                        time_old = time.time()
                        send_code(0)
                if status == "6" :
                    if time.time()-time_old>0.1:
                        servo2 = servo2-10
                        if servo2 >= 250:
                            servo2 = 250
                        servo_pwm2.set_PWM_dutycycle(23,servo2)
                        time_old = time.time()
                        send_code(0)
                if status == "7" :
                    if time.time()-time_old>0.1:
                        servo1 = servo1+10
                        if servo1 >= 125:
                            servo1 = 125
                        servo_pwm1.set_PWM_dutycycle(18,servo1)
                        time_old = time.time()
                        send_code(0)
                if status == "8" :
                    if time.time()-time_old>0.1:
                        servo1 = servo1-10
                        if servo1 <= 25:
                            servo1 = 25
                        servo_pwm1.set_PWM_dutycycle(18,servo1)
                        time_old = time.time()
                        send_code(0)
                print("fin")
        except Exception as e:
            print(e)
            time.sleep(1)
    if mode == "1":
        target = status
        if target == "1" or target == "2":
            s,x,y,w,h = visual.detect(int(target),video)
        if target == "0":
            s,x,y,r = visual.detect(int(target),video)
        print("doing:"+str(x))
        if s==1:
            if x>=1 and x<=240:
                ted.write(bytes.fromhex(small_right))
                #print("l")
                time.sleep(0.05)
            if x>=400:
                ted.write(bytes.fromhex(small_left))
                #print("r")
                time.sleep(0.05)
            if 240<x<400:
                ted.write(bytes.fromhex(start))
        if s==0:
            print("no")
            ted.write(bytes.fromhex(start))
            time.sleep(0.05)

