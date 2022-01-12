# -*- coding: utf-8 -*-
import network
import time
import ujson
import ubinascii

from machine import Pin, I2C, unique_id
from umqtt.simple import MQTTClient

sta_if = network.WLAN(network.STA_IF)

while not sta_if.isconnected():
    time.sleep(3)

with open('secrets.json') as fp:
    secrets = ujson.loads(fp.read())

i2c = I2C(scl=Pin(5), sda=Pin(4))
addr = i2c.scan()[0]

c = MQTTClient(
    client_id='esp8266_{}'.format(
        str(ubinascii.hexlify(unique_id()), 'utf-8'),
    ),
    server=secrets['mqtt']['host'],
    user=secrets['mqtt']['user'],
    password=secrets['mqtt']['pass'],
)
c.connect()
time.sleep(2)


def get_temp():
    i2c.start()
    time.sleep(1)
    data = i2c.readfrom(addr, 2)
    negative = (data[0] >> 7) == 1

    if not negative:
        t_c = (((data[0] * 256) + data[1]) >> 4) * 0.0625
    else:
        ti = ((data[0] * 256) + data[1]) >> 4
        ti = ~ti & 0b011111111111
        t_c = -(ti * 0.0625)

    t_f = t_c * 9.0 / 5 + 32

    return t_c, t_f


while True:
    temp_c, temp_f = get_temp()
    c.publish('homeassistant/office/temp', '{:.2f}'.format(temp_f))
    time.sleep(60 * 5)
