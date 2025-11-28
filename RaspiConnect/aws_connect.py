#For testing purposes only

import time 
import paho.mqtt.client as mqtt
import ssl
import json
import _thread

def on_connect(client, userdata, flags, rc):
    print("Connect to AWS IoT:" , str(rc))

path = "home/admin/Documents/aws_cert/"

client = mqtt.Client()
client.on_connect = on_connect
client.tls_set(ca_certs=path + "rootCA.pem", certfile=path + "certificate.pem.crt", keyfile=path + "private.pem.key", tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
client.tls.insecure_set(True)
client.connect("a3qvtgigehocs2-ats.iot.ap-southeast-1.amazonaws.com", 8883, 60)

def publish_sensor_data():
    ctr = 1
    while True:
        msg = "Testing"
        print("Publishing message: " + msg)
        client.publish("raspi/data", payload=json.dumps({"message": msg, "counter": ctr}), qos=0)
        ctr += 1
        time.sleep(5)

_thread.start_new_thread(publish_sensor_data, ())

client.loop_start()