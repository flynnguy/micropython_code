# -*- coding: utf-8 -*-
import ujson
from umqtt.simple import MQTTClient

with open('secrets.json') as fp:
    secrets = ujson.loads(fp.read())

client = MQTTClient(
    client_id='umqtt_client',
    server=secrets['mqtt']['host'],
    user=secrets['mqtt']['user'],
    password=secrets['mqtt']['pass'],
)
client.connect()

topic = 'foo_topic'
value = 'hello'
client.publish('{}'.format(topic), '{}'.format(value))
client.disconnect()
