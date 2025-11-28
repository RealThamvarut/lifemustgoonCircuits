import paho.mqtt.client as mqtt

CHANNEL_ID = 3185468
MQTT_SERVER = "mqtt3.thingspeak.com"
MQTT_PORT = 1883
MQTT_USER = "LwEPGy4rLh4tMhMDLQwgBwc"
MQTT_PASSWORD = "/dhZK/IMhUvop5mPCqhQqm4h"
MQTT_CLIENT_ID = "LwEPGy4rLh4tMhMDLQwgBwc"
MQTT_TOPIC = "channels/3185468/publish"


def init_mqtt():
    client = mqtt.Client(MQTT_CLIENT_ID)

    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

    client.connect(MQTT_SERVER, MQTT_PORT, 60)

    print(f"MQTT Connected to {MQTT_SERVER} as {MQTT_CLIENT_ID}")
    return client


def send_to_thingspeak(uid, client):
    payload = f"field1={uid}"

    client.publish(MQTT_TOPIC, payload)
    print(f"Sent to ThingSpeak → Topic: {MQTT_TOPIC}, Payload: {payload}")
