import paho.mqtt.client as mqtt
import uuid
port =1883



def message_test(client,userdata,message):
 if message:
  print(message.payload.decode())

client = mqtt.Client()
client.connect(hostname,port)
client.subscribe("test",qos=1)
client.message_callback_add("test",message_test)
client.loop_forever()
