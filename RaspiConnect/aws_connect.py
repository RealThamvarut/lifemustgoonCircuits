#For testing purposes only

import time 
import paho.mqtt.client as mqtt
import ssl
import json
import _thread

print("AWS IoT MQTT Test")

def on_connect(client, userdata, flags, rc):
    print("Connect to AWS IoT:" , str(rc))

path = "/home/admin/Documents/aws_cert/"

client = mqtt.Client()
client.on_connect = on_connect
client.tls_set(ca_certs=path + "rootCA1.pem", certfile=path + "certificate.pem.crt", keyfile=path + "private.pem.key", tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
# client.tls.insecure_set(True)
client.connect("a3qvtgigehocs2-ats.iot.ap-southeast-1.amazonaws.com", 8883, 60)

folder_name = "man"

def on_message(client, userdata, message):
    print("Topic: " + message.topic)
    print("Message received: "  + message.payload.decode("utf-8"))

def publish_sensor_data():
    ctr = 1
    while True:
        msg = "Testing"
        print("Publishing message: " + msg)
        client.publish("raspi/data", payload=json.dumps({"folder": folder_name, "counter": ctr}), qos=0)
        ctr += 1
        client.subscribe("raspi/response",1)
        client.onMessage = on_message
        time.sleep(5)

_thread.start_new_thread(publish_sensor_data, ())

client.loop_forever()