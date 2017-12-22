# -*- coding: utf-8 -*-
import time
import ujson

from machine import Pin, I2C
from umqtt.simple import MQTTClient

time.sleep(10)

with open('secrets.json') as fp:
    secrets = ujson.loads(fp.read())

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
c = MQTTClient(
    client_id=secrets['mqtt']['client_id'],
    server=secrets['mqtt']['host'],
    user=secrets['mqtt']['user'],
    password=secrets['mqtt']['pass'],
)
c.connect()


def getVal():
    values = list(i2c.readfrom_mem(39, 0x00, 4))
    hum = ((((values[0] & 0x3F) << 8) | (values[1])) / 163.83)
    temp_c = (((((values[2] << 6) | (values[3] >> 2)) * 165) / 16383.0) - 40)
    temp_f = 9.0 / 5.0 * temp_c + 32
    return temp_f, hum


while True:
    temp, hum = getVal()
    c.publish(
        '{}/{}/hum'.format(
            secrets['mqtt']['prefix'],
            secrets['mqtt']['client_id'],
        ),
        '{}'.format(hum),
    )
    c.publish(
        '{}/{}/hum'.format(
            secrets['mqtt']['prefix'],
            secrets['mqtt']['client_id'],
        ),
        '{}'.format(temp),
    )
    time.sleep(60 * 5)
