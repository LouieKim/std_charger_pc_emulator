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



@app.route('/')
def hello():   
    return render_template('index.html')

@app.route('/gpio_out')
def gpio_out():
    return render_template('gpio_in_out.html')

@app.route('/gpio_out/<device>/<command>')
def device_gpio_out(device, command):
    try:
        if(command == 'on'): cmd = True
        elif(command == 'off'): cmd = False
        else: print("Error")

        if(int(device) == 0):
            if (cmd):
                #1번 채널 스타트
                SER.write(serial.to_bytes([0x02,0x01,0x10,0x00,0xc8,0x00,0x04,0x08,0x00,0x08,0x00,0x01,0x00,0x00,0x00,0x00,0xe0,0xe4, 0x0d]))
            
            else:
                #1번 채널 종료
                SER.write(serial.to_bytes([0x02,0x01,0x10,0x00,0xc8,0x00,0x04,0x08,0x00,0x10,0x00,0x01,0x00,0x00,0x00,0x00,0x78,0xe5, 0x0d]))
        
        elif(int(device) == 1):
            if (cmd):
                #2번 채널 스타트
                SER.write(serial.to_bytes([0x02,0x02,0x10,0x00,0xc8,0x00,0x04,0x08,0x00,0x08,0x00,0x01,0x00,0x00,0x00,0x00,0xa3,0xe5,0x0d]))
            else:
                #2번 채널 종료
                SER.write(serial.to_bytes([0x02,0x02,0x10,0x00,0xc8,0x00,0x04,0x08,0x00,0x10,0x00,0x01,0x00,0x00,0x00,0x00,0x3b,0xe4,0x0d]))
        
        elif(int(device) == 2):
            if (cmd):
                #3번 채널 스타트
                SER.write(serial.to_bytes([0x02,0x03,0x10,0x00,0xc8,0x00,0x04,0x08,0x00,0x08,0x00,0x01,0x00,0x00,0x00,0x00,0x62,0xe5,0x0d]))
            else:
                #3번 채널 종료
                SER.write(serial.to_bytes([0x02,0x03,0x10,0x00,0xc8,0x00,0x04,0x08,0x00,0x10,0x00,0x01,0x00,0x00,0x00,0x00,0xfa,0xe4,0x0d]))
        
        return jsonify(success=True)

    except Exception as e:
        print(e)
    finally:
        print("%s device Control" %device)
    


@app.route('/gpio_in')
def gpio_in():
    return render_template('gpio_in.html')

data_list = list()

@app.route('/gpio_in/update')
def gpio_in_update():

    try:
        
        #gpio_in_dict = {'DOOR_01': data_list[3], 'DOOR_02': data_list[4], 'DSEN_01': data_list[5], 'DSEN_02': data_list[6], 'MC_01': data_list[7], 'MC_02': data_list[8]
        #        ,'RELAY_01': data_list[9], 'RELAY_02':  data_list[10], 'RELAY_03': data_list[11]}
                #, 'RELAY_04': rr.bits[9], 'RELAY_05': rr.bits[10], 'RELAY_06': rr.bits[11]
                #'EMERGENCY': rr.bits[12]}


        #resource_json = json.dumps(gpio_in_dict)
        #return resource_json
        return "hello"

    except Exception as e:
        print(e)

    finally:
        print("gpio_in/update")


@app.route('/adc')
def adc():
    return render_template('adc.html')


@app.route('/adc/update')
def adc_update():
    try:
        modbus_register = client.read_holding_registers(0, 7, unit=UNIT)
        time.sleep(0.5) # Delay를 두지 않으면 모두 받지 못했다고 투덜댐

        adc_dict = {"CCS_01_PD": str(modbus_register.registers[0]), "CCS_01_TEMP": str(modbus_register.registers[1]), "CCS_02_PD": str(modbus_register.registers[2]), 
        "CCS_02_TEMP": str(modbus_register.registers[3]), "DCPT_01": str(modbus_register.registers[4]), "DCPT_02": str(modbus_register.registers[5]), "TEST_TEMP": str(modbus_register.registers[6])}

        resource_json = json.dumps(adc_dict)
        return resource_json

    except Exception as e:
        print(e)

    finally:
        print("adc/update")

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

def getHtml(url):
    while(1):
        SER.write(serial.to_bytes([0x02,0x01,0x04,0x01,0x2c,0x00,0x0c,0x30,0x3a,0x0d]))

        data_list.clear()

        for i in rang(31):
            ser_bytes = SER.read()
            data_list.append(i)
            
        print(data_list)
        
        time.sleep(1)


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
    
    #t1 = threading.Thread(target=getHtml, args=('http://google.com',))
    #t1.daemon = True 
    #t1.start()

    #SER.write(serial.to_bytes([0x01,0x03,0x00,0x00,0x00,0x03,0x05,0xcb]))
    SER.write(serial.to_bytes([0x01,0x03,0x00,0x00,0x00,0x06,0xc5,0xc8]))
    #SER.write(serial.to_bytes([0x01,0x03,0x00,0x19,0x00,0x03,0xd4,0x0c]))

    #SER.write(serial.to_bytes([0x01,0x10,0x00,0x1b,0x00,0x01,0x02,0x00,0x02,0x24,0x7a]))
    #SER.write(serial.to_bytes([0x02,0x10,0x00,0x1b,0x00,0x01,0x02,0x00,0x02,0x30,0x8a]))
    #SER.write(serial.to_bytes([0x03,0x10,0x00,0x1b,0x00,0x01,0x02,0x00,0x02,0x3d,0x1a]))

    data_list = list()
    data_list.clear()

    for i in range(20):
        ser_bytes = SER.read()
        print(ser_bytes.hex())   

    #for i in range(14):
    #    ser_bytes = SER.read()
    #    data_list.append(ser_bytes.hex())

    #print(data_list)

    #test01_vol = int(data_list[3],16) << 8 | int(data_list[4], 16)
    #test02_vol = int(data_list[5],16) << 8 | int(data_list[6], 16)
    #test03_vol = int(data_list[7],16) << 8 | int(data_list[8], 16)
    
    #print(test01_vol)
    #print(test02_vol)
    #print(test03_vol)
    
    SER.close()
    