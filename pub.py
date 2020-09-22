import paho.mqtt.publish as publish
import psutil
import time
import uuid
hotsname = "localhost"
port = 1883
while True:
 publish.single(topic="test",payload="55555",qos=1,hostname=hotsname,port=port)
 time.sleep(60)