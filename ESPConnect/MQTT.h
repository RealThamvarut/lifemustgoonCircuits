#ifndef MQTT_H
#define MQTT_H

#include <PubSubClient.h>
#include <WiFi.h>

class MQTT {
public:
    MQTT(const char* server, int port, const char* user, const char* password, const char* client_id);
    void setup();
    void loop();
    void publish(const char* topic, const float payload);

private:
    void reconnect();
    WiFiClient espClient;
    PubSubClient client;
    const char* _server;
    int _port;
    const char* _user;
    const char* _password;
    const char* _client_id;
};

#endif // MQTT_H
