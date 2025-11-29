import paho.mqtt.publish as publish

# The ThingSpeak Channel ID.
channel_ID = "3186112"
# The hostname of the ThingSpeak MQTT broker.
mqtt_host = "mqtt3.thingspeak.com"
# Your MQTT credentials for the device
mqtt_client_ID = "LwEPGy4rLh4tMhMDLQwgBwc"
mqtt_username  = "LwEPGy4rLh4tMhMDLQwgBwc"
mqtt_password  = "/dhZK/IMhUvop5mPCqhQqm4h"
# Use unsecure tcp port
t_transport = "tcp"
t_port = 1883
# Create the topic string.
topic = "channels/" + channel_ID + "/publish"

def send_to_thingspeak(uid):
    payload = "field1=" + str(uid)

    # attempt to publish this data to the topic.
    try:
        print ("Writing Payload = ", payload," to host: ", mqtt_host, " clientID= ", mqtt_client_ID, " User ", mqtt_username, " PWD ", mqtt_password)
        publish.single(topic, payload, hostname=mqtt_host, transport=t_transport, port=t_port, client_id=mqtt_client_ID, auth={'username':mqtt_username,'password':mqtt_password})
    except Exception as e:
        print (e) 
