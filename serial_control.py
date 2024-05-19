import serial
import time
from configparser import ConfigParser

rotate_motor_key = 0
move_motor_key = 1
conveyor_motor_key = 0
conveyor_motor_speed = 255

degrees_config_data = 'src/configs/degrees.conf'
degrees_config = ConfigParser()
degrees_config.read(degrees_config_data)
serial_config_data = 'src/configs/serial.conf'
serial_config = ConfigParser()
serial_config.read(serial_config_data)

COM_PORT = serial_config['serial_connection']['port']
COM_BAUDRATE = int(serial_config['serial_connection']['port_baudrate'])
serial_connection = serial.Serial(
    port="\\\\.\\" + COM_PORT,
    baudrate=COM_BAUDRATE,
)


def ClosePort():
    serial_connection.close()


def serialSend(data):
    sending_string = ""
    for val in data:
        sending_string += str(val)
        sending_string += ','
    sending_string = sending_string[:-1]
    sending_string += ';'
    serial_connection.write(sending_string.encode())
    serial_connection.flush()


def onRead():
    while True:
        rx = serial_connection.readline()
        data = str(rx, 'utf-8').strip()
        print(data, type(data))
        return data


def rotate(data):
    part_name = data.strip("[]'")
    """
    for item in part_list:
        if part_name == str(item):
            print(str(item), parts_degrees.get(item))
            serialSend(data=[rotate_motor_key, parts_degrees.get(item)])
            move(data=105)
    """
    val = int(str(degrees_config['degrees'][part_name]))
    print(part_name, val)
    serialSend(data=[rotate_motor_key, val])
    move(data=105)


def move(data):
    serialSend(data=[move_motor_key, -data])
    time.sleep(5.5)
    serialSend(data=[move_motor_key, data])
