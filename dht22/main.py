# -*- coding: utf-8 -*-
import dht
import network
import time
import ujson
import ubinascii

from machine import Pin, unique_id
from umqtt.simple import MQTTClient

DHT22_PIN = Pin(0)

room = 'bedroom'

# Wait for network connection or MQTT connect() will fail
sta_if = network.WLAN(network.STA_IF)

while not sta_if.isconnected():
    time.sleep(3)

# load secrets
with open('secrets.json') as fp:
    secrets = ujson.loads(fp.read())

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
    d = dht.DHT22(DHT22_PIN)
    d.measure()
    t_c = d.temperature()
    hum = d.humidity()

    t_f = t_c * 9.0 / 5 + 32

    return t_c, t_f, hum


while True:
    temp_c, temp_f, hum = get_temp()
    c.publish(
        '{}{}/temp'.format(
            secrets['mqtt']['prefix'],
            room,
        ), '{:.2f}'.format(temp_f),
    )
    c.publish(
        '{}{}/hum'.format(
            secrets['mqtt']['prefix'],
            room,
        ), '{:.2f}'.format(hum),
    )
    time.sleep(60 * 5)
