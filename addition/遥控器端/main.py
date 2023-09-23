# 连接wifi，将IP地址等相关信息通过OLED显示（只支持2.4G网络）。
import network,time
from machine import I2C,Pin,ADC,PWM
from ssd1306 import SSD1306_I2C
import _thread
import random
import network,socket

#WIFI连接函数
def WIFI_Connect():
    global status
    WIFI_LED=Pin(2, Pin.OUT) #初始化WIFI指示灯
    wlan = network.WLAN(network.STA_IF) #STA模式
    wlan.active(False)
    time.sleep(1)
    wlan.active(True)                   #激活接口
    start_time=time.time()              #记录时间做超时判断
    print("connect_start")
    while not wlan.isconnected():
        try:
            wlan.active(True)
            wlan.connect('BALMUNG 9685', 'balmung08') #输入WIFI账号密码
            print("doing")
        except Exception as e:
            print(e)
            while not wlan.isconnected():
                print("trying")
                wlan.active(True)
                #wlan.active(False) 
                WIFI_LED.value(1)
                time.sleep_ms(50)
                WIFI_LED.value(0)
                time.sleep_ms(50)
                if time.time()-start_time > 5 :
                    oled.fill(0)   #清屏背景黑色
                    oled.text('internet:defeat',0,0)
                    oled.show()
                    print("defeat")
                break
    if wlan.isconnected():
        print("WLAN_SUCCESS")
        WIFI_LED.value(1)
        oled.fill(0)   #清屏背景黑色
        oled.text('internet:connect',0,0)
        oled.text('status:0', 0, 15)
        oled.text('mode:0',0,30)
        oled.show()
def send_code(code):
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    addr=('8.130.72.154',1177) #服务器IP和端口
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   #设置套接字
    s.connect(addr)
    s.send('up')
    s.send(str(code))
    return s
def send_mode(mode):
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    addr=('8.130.72.154',1177) #服务器IP和端口
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   #设置套接字
    s.connect(addr)
    s.send('mp')
    s.send(str(mode))
    return s
if __name__ == '__main__':
    KEY1=Pin(16,Pin.IN,Pin.PULL_UP) #构建 KEY 对象
    KEY2=Pin(17,Pin.IN,Pin.PULL_UP) #构建 KEY 对象
    KEY3=Pin(18,Pin.IN,Pin.PULL_UP) #构建 KEY 对象
    KEY4=Pin(19,Pin.IN,Pin.PULL_UP) #构建 KEY 对象
    KEY5=Pin(21,Pin.IN,Pin.PULL_UP) #构建 KEY 对象
    state=0 #LED 引脚状态
    i2c = I2C(sda=Pin(27), scl=Pin(26))   #I2C初始化：sda--> 13, scl --> 14
    oled = SSD1306_I2C(128, 64, i2c, addr=0x3c) #OLED显示屏初始化：128*64分辨率,OLED的I2C地址是0x3c
    count = 0
    mode = 0
    print("init_success")
    WIFI_Connect()
    print("connect_success")
    mode_sw = 0
    target = 1
    while True:
        status = 0
        if KEY1.value()==0: #按键被按下
            time.sleep_ms(10) #消除抖动
            if KEY1.value()==0: #确认按键被按下
                if mode == 0:
                    status = 1
                    s = send_code(1)
                    s.close()
                    print(1)
                oled.fill(0)
                oled.text('internet:connect',0,0)
                if mode == 0:
                    oled.text('status:1',0,15)
                    oled.text('target:---',0,45)
                if mode == 1:
                    oled.text('status:---',0,15)
                    oled.text('target:'+str(target),0,45)
                oled.text('mode:'+str(mode),0,30)
                oled.show()   #OLED执行显示
        if KEY2.value()==0: #按键被按下
            time.sleep_ms(10) #消除抖动
            if KEY2.value()==0: #确认按键被按下
                if mode == 0:
                    status = 2
                    oled.fill(0)
                    s= send_code(2)
                    s.close()
                    print(2)
                oled.text('internet:connect',0,0)
                if mode == 0:
                    oled.text('status:2',0,15)
                    oled.text('target:---',0,45)
                if mode == 1:
                    oled.text('status:---',0,15)
                    oled.text('target:'+str(target),0,45)
                oled.text('mode:'+str(mode),0,30)
                oled.show()   #OLED执行显示

        if KEY3.value()==0: #按键被按下
            time.sleep_ms(10) #消除抖动
            if KEY3.value()==0: #确认按键被按下
                if mode == 0:
                    status = 3
                    s = send_code(3)
                    s.close()
                    print(3)
                oled.fill(0)
                oled.text('internet:connect',0,0)
                if mode == 0:
                    oled.text('status:3',0,15)
                    oled.text('target:---',0,45)
                if mode == 1:
                    oled.text('status:---',0,15)
                    oled.text('target:'+str(target),0,45)
                oled.text('mode:'+str(mode),0,30)
                oled.show()   #OLED执行显示
        if KEY4.value()==0: #按键被按下
            time.sleep_ms(10) #消除抖动
            if KEY4.value()==0: #确认按键被按下
                if mode == 0:
                    status = 4
                    s = send_code(4)
                    s.close()
                    print(4)
                oled.fill(0)
                oled.text('internet:connect',0,0)
                if mode == 0:
                    oled.text('status:4',0,15)
                    oled.text('target:---',0,45)
                if mode == 1:
                    oled.text('status:---',0,15)
                    oled.text('target:'+str(target),0,45)
                oled.text('mode:'+str(mode),0,30)
                oled.show()   #OLED执行显示
        if KEY5.value()==0: #按键被按下
            time.sleep_ms(10) #消除抖动
            if KEY5.value()==0: #确认按键被按下
                print(count)
                if count == 2:
                    if mode == 1:
                        target += 1
                        if target == 3:
                            target = 0
                        s = send_code(target)
                        s.close()
                        status = 5
                        oled.fill(0)
                        oled.text('internet:connect',0,0)
                        oled.text('status:---',0,15)
                        oled.text('mode:'+str(mode),0,30)
                        oled.text('target:'+str(target),0,45)
                        oled.show()   #OLED执行显示
                if count==7:
                    mode = int(not(mode))
                    s = send_mode(mode)
                    s.close()
                count+=1

        else:
            count = 0
            mode_sw = 0
        if status==0:
            if mode == 0:
                s = send_code(0)
                s.close()
                s = send_mode(0)
                s.close()
            oled.fill(0)
            oled.text('internet:connect',0,0)
            if mode == 0:
                oled.text('status:0',0,15)
                oled.text('target:---',0,45)
            if mode == 1:
                oled.text('status:---',0,15)
                oled.text('target:'+str(target),0,45)
            oled.text('mode:'+str(mode),0,30)
            oled.show()

    '''
    #初始化相关模块
    i2c = I2C(sda=Pin(26), scl=Pin(27))
    oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)
    control_front=Pin(17,Pin.IN,Pin.PULL_UP) 
    control_back=Pin(35,Pin.IN,Pin.PULL_UP)
    control_left=Pin(34,Pin.IN,Pin.PULL_UP)
    control_right=Pin(16,Pin.IN,Pin.PULL_UP)
    status = 0
    pid_excecution = 1
    outvalue,error1,error2,error3,increase= 0.0,0.0,0.0,0.0,0.0
    WIFI_Connect()
    inputvalue = 0.0
    num = 1
    d = 0
    adc = ADC(Pin(34),bits=12)
    adc.atten(ADC.ATTN_11DB)#配置衰减器。配置衰减器能增加电压测量范围，但是以精度为代价的。
    Beep = PWM(Pin(33), freq=100000, duty=d) #1-40M Hz
    #_thread.start_new_thread(oled_show,()) #开启线程1,参数必须是元组
    #_thread.start_new_thread(PID,(1000,1000,0.1,0.05,0.05)) #开启线程2,参数必须是元组
    while True:
        Beep.duty(d)
        oled.fill(0)   #清屏背景黑色
        oled.text('internet:connect',0,0)
        oled.text('duty:'+str(d), 0, 15)
        oled.text('adc:'+str(adc.read()),0,30)
        oled.show()
        print("adc-v:",adc.read()/4095*3.3)
        d += 1000
        if(d == 8000):
            d = 0
        #print(num,num-int(num/10))
        time.sleep_ms(50)
        '''
