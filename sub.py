import mysql.connector
import paho.mqtt.client as mqtt
import uuid
hostname = "172.16.20.12"
port =1883

mydb = mysql.connector.connect(
 host="172.16.20.63",
 user="locationwifi",
 passwd="Passw0rd",
 database="LocationWifi",
 port=3306
)

def message_test(client,userdata,message):
 if message:
  mycursor = mydb.cursor()
  sql = "insert into apdevice (name) values (%s)"
  val = (message.payload.decode())
  mycursor.execute(sql,val)
  mydb.commit()
  print(message.payload.decode())

client = mqtt.Client()
client.connect(hostname,port)
client.subscribe("test",qos=1)
client.message_callback_add("test",message_test)
client.loop_forever()



