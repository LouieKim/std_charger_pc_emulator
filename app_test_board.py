from flask import Flask, render_template, jsonify
import json
import time
import threading
import serial
import signal
import time
import sys
import threading, requests, time
import platform

app = Flask(__name__)
data_list = list()

@app.route('/')
def hello():   
    return render_template('index.html')

@app.route('/monitoring')
def monitoring():   
    return render_template('monitoring.html')

@app.route('/monitoring/update')
def gpio_in_update():

    ch01_ac_vol = int(data_list[11], 16) << 8 | int(data_list[12], 16)
    ch02_ac_vol = int(data_list[31], 16) << 8 | int(data_list[32], 16)
    ch03_ac_vol = int(data_list[51], 16) << 8 | int(data_list[52], 16)

    try:
        gpio_in_dict = {'ch01_status': data_list[4], 'ch01_pwm_duty': data_list[6], 'ch01_avg_vol': data_list[8], 'ch01_vol': data_list[10], 'ch01_AC_vol': round(ch01_ac_vol*0.1,2), 'ch01_AC_cur': data_list[14], 'ch01_emg': data_list[16], 'ch01_cp_ry': data_list[18], 'ch01_mc': data_list[20], 'ch01_wd': data_list[22]
                    , 'ch02_status': data_list[24], 'ch02_pwm_duty': data_list[26], 'ch02_avg_vol': data_list[28], 'ch02_vol': data_list[30], 'ch02_AC_vol': round(ch02_ac_vol*0.1,2), 'ch02_AC_cur': data_list[34], 'ch02_emg': data_list[36], 'ch02_cp_ry': data_list[38], 'ch02_mc': data_list[40], 'ch02_wd': data_list[42]
                    , 'ch03_status': data_list[44], 'ch03_pwm_duty': data_list[46], 'ch03_avg_vol': data_list[48], 'ch03_vol': data_list[50], 'ch03_AC_vol': round(ch03_ac_vol*0.1,2), 'ch03_AC_cur': data_list[54], 'ch03_emg': data_list[56], 'ch03_cp_ry': data_list[58], 'ch03_mc': data_list[60], 'ch03_wd': data_list[62]}

        resource_json = json.dumps(gpio_in_dict)
        return resource_json

    except Exception as e:
        print(e)

    finally:
        print("gpio_in/update")

#reference: https://jcdgods.tistory.com/358
# default returned value is array 
# If second param is True then returning single value 

crcTable=[0x0000,0xC0C1,0xC181,0x0140,0xC301,0x03C0,0x0280,0xC241,0xC601,0x06C0,0x0780,0xC741,0x0500,0xC5C1,0xC481
        ,0x0440,0xCC01,0x0CC0,0x0D80,0xCD41,0x0F00,0xCFC1,0xCE81,0x0E40,0x0A00,0xCAC1,0xCB81,0x0B40,0xC901,0x09C0
        ,0x0880,0xC841,0xD801,0x18C0,0x1980,0xD941,0x1B00,0xDBC1,0xDA81,0x1A40,0x1E00,0xDEC1,0xDF81,0x1F40,0xDD01
        ,0x1DC0,0x1C80,0xDC41,0x1400,0xD4C1,0xD581,0x1540,0xD701,0x17C0,0x1680,0xD641,0xD201,0x12C0,0x1380,0xD341
        ,0x1100,0xD1C1,0xD081,0x1040,0xF001,0x30C0,0x3180,0xF141,0x3300,0xF3C1,0xF281,0x3240,0x3600,0xF6C1,0xF781
        ,0x3740,0xF501,0x35C0,0x3480,0xF441,0x3C00,0xFCC1,0xFD81,0x3D40,0xFF01,0x3FC0,0x3E80,0xFE41,0xFA01,0x3AC0
        ,0x3B80,0xFB41,0x3900,0xF9C1,0xF881,0x3840,0x2800,0xE8C1,0xE981,0x2940,0xEB01,0x2BC0,0x2A80,0xEA41,0xEE01
        ,0x2EC0,0x2F80,0xEF41,0x2D00,0xEDC1,0xEC81,0x2C40,0xE401,0x24C0,0x2580,0xE541,0x2700,0xE7C1,0xE681,0x2640
        ,0x2200,0xE2C1,0xE381,0x2340,0xE101,0x21C0,0x2080,0xE041,0xA001,0x60C0,0x6180,0xA141,0x6300,0xA3C1,0xA281
        ,0x6240,0x6600,0xA6C1,0xA781,0x6740,0xA501,0x65C0,0x6480,0xA441,0x6C00,0xACC1,0xAD81,0x6D40,0xAF01,0x6FC0
        ,0x6E80,0xAE41,0xAA01,0x6AC0,0x6B80,0xAB41,0x6900,0xA9C1,0xA881,0x6840,0x7800,0xB8C1,0xB981,0x7940,0xBB01
        ,0x7BC0,0x7A80,0xBA41,0xBE01,0x7EC0,0x7F80,0xBF41,0x7D00,0xBDC1,0xBC81,0x7C40,0xB401,0x74C0,0x7580,0xB541
        ,0x7700,0xB7C1,0xB681,0x7640,0x7200,0xB2C1,0xB381,0x7340,0xB101,0x71C0,0x7080,0xB041,0x5000,0x90C1,0x9181
        ,0x5140,0x9301,0x53C0,0x5280,0x9241,0x9601,0x56C0,0x5780,0x9741,0x5500,0x95C1,0x9481,0x5440,0x9C01,0x5CC0
        ,0x5D80,0x9D41,0x5F00,0x9FC1,0x9E81,0x5E40,0x5A00,0x9AC1,0x9B81,0x5B40,0x9901,0x59C0,0x5880,0x9841,0x8801
        ,0x48C0,0x4980,0x8941,0x4B00,0x8BC1,0x8A81,0x4A40,0x4E00,0x8EC1,0x8F81,0x4F40,0x8D01,0x4DC0,0x4C80,0x8C41
        ,0x4400,0x84C1,0x8581,0x4540,0x8701,0x47C0,0x4680,0x8641,0x8201,0x42C0,0x4380,0x8341,0x4100,0x81C1,0x8081,0x4040]


def crc16(data): 
    crc= [0xff, 0xff]; 
    for datum in data: 
        ncrc = crcTable[(crc[0] ^ datum)] 
        crc[0] = (ncrc & 0x00FF) ^ crc[1] 
        crc[1] = ncrc >> 8 
    data.append(crc[0])
    data.append(crc[1])
    return data


def main():
    try:
        app.run(host="127.0.0.1", port="5000", debug=False)
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        print(e)
    finally:
        print("Serial Close")
        SER.close()


#Reference: #https://m.blog.naver.com/PostView.nhn?blogId=chandong83&logNo=220941128858&proxyReferer=https:%2F%2Fwww.google.com%2F
def get_data_thread():
    response_num = 65
    
    while(1):
        req_tx = [0x01, 0x04, 0x00, 0x00, 0x00, 0x1e]
        req_tx = crc16(req_tx)

        SER.write(serial.to_bytes(req_tx))

        data_list.clear()

        for i in range(response_num):
            ser_bytes = SER.read()
            data_list.append(ser_bytes.hex())
            
        print(data_list)
        time.sleep(2)

if __name__ == "__main__":
    global COM_PORT
    global SER
    
    if platform.system() == "Linux":
        print("linix")
        COM_PORT = '/dev/ttyUSB0'
    else:
        print("window")
        COM_PORT = 'COM6'

    SER = serial.Serial(COM_PORT, baudrate=38400, timeout=3.0)

    # 데몬 쓰레드
    t1 = threading.Thread(target=get_data_thread)
    t1.daemon = True 
    t1.start()

    main()

    #Start
    #SER.write(serial.to_bytes([0x02,0x01,0x10,0x00,0xc8,0x00,0x04,0x08,0x00,0x08,0x00,0x04,0x00,0x00,0x00,0x00,0x2c,0xe4,0x0d]))


    #ser_bytes = SER.readline()
    #for i in range(10):
    #    ser_bytes = SER.read()
    #    print(ser_bytes.hex())    
    #SER.close()
    
    # This code is ported from modbus CRC16(https://www.modbustools.com/modbus_crc16.htm) 
