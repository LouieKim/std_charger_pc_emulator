from flask import Flask, render_template, jsonify
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import json
import time
import threading
import serial
import signal
import time
import sys

app = Flask(__name__)
UNIT = 0x1

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/gpio_out')
def gpio_out():
    return render_template('gpio_out.html')

@app.route('/gpio_out/<device>/<command>')
def device_gpio_out(device, command):
    try:
        if(command == 'on'): cmd = True
        elif(command == 'off'): cmd = False
        else: print("Error")
        
        rq = client.write_coil(int(device), cmd, unit=UNIT)
        time.sleep(1) # Delay를 두지 않으면 모두 받지 못했다고 투덜댐
        return jsonify(success=True)

    except Exception as e:
        print(e)
    finally:
        print("%s device Control" %device)
    


@app.route('/gpio_in')
def gpio_in():
    return render_template('gpio_in.html')


@app.route('/gpio_in/update')
def gpio_in_update():
    try:
        rr = client.read_coils(20, 13, unit=UNIT)
        time.sleep(0.5) # Delay를 두지 않으면 모두 받지 못했다고 투덜댐
        
        gpio_in_dict = {'DOOR_01': rr.bits[0], 'DOOR_02': rr.bits[1], 'DSEN_01': rr.bits[2], 'DSEN_02': rr.bits[3], 'MC_01': rr.bits[4], 'MC_02': rr.bits[5], 
                  'RELAY_01': rr.bits[6], 'RELAY_02': rr.bits[7], 'RELAY_03': rr.bits[8], 'RELAY_04': rr.bits[9], 'RELAY_05': rr.bits[10], 'RELAY_06': rr.bits[11],
                   'EMERGENCY': rr.bits[12]}

        resource_json = json.dumps(gpio_in_dict)
        return resource_json

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
        print(e)
    except Exception as e:
        print(e)
    finally:
        client.close()
        sys.exit()

if __name__ == "__main__":
    global client

    try:
        #scale = ModbusClient(method='rtu', port='/dev/ttyUSB0', parity='N', baudrate=9600, bytesize=8, stopbits=2, timeout=1, strict=False)
        client = ModbusClient(method='rtu', port='com6', timeout=10, baudrate=9600)
        client.connect()

        modbus_register = client.read_holding_registers(0, 2, unit=UNIT)
        time.sleep(1) # Delay를 두지 않으면 모두 받지 못했다고 투덜댐

        

        if modbus_register.isError():
            # handle error, log?
            print('Modbus Error:', modbus_register)
        else:
            result = modbus_register.registers
            print(result)

        #adc_dict = {"CCS_01_PD": str(modbus_register.registers[0]), "CCS_01_TEMP": str(modbus_register.registers[1])} #"CCS_02_PD": str(modbus_register.registers[2]), 
        #CCS_02_TEMP": str(modbus_register.registers[3]), "DCPT_01": str(modbus_register.registers[4]), "DCPT_02": str(modbus_register.registers[5]), "TEST_TEMP": str(modbus_register.registers[6])}

        #resource_json = json.dumps(adc_dict)
        #print(resource_json)

    except Exception as e:
        print(e)

    finally:
        client.close()

    #main()
    