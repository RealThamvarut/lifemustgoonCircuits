#include "MQTT.h"
#include <PubSubClient.h>

MQTT::MQTT(const char* server, int port, const char* user, const char* password, const char* client_id)
  : client(espClient), _server(server), _port(port), _user(user), _password(password), _client_id(client_id) {
}

void MQTT::setup() {
  client.setServer(_server, _port);
}


void MQTT::reconnect() {
while ( !client.connected() )
  {
    // Connect to the MQTT broker.
    if ( client.connect( _client_id, _user, _password ) ) {
      Serial2.print( "MQTT to " );
      Serial2.print( _server );
      Serial2.print (" at port ");
      Serial2.print( _port );
      Serial2.println( " successful." );
    } else {
      Serial2.print( "MQTT connection failed, rc = " );
      // See https://pubsubclient.knolleary.net/api.html#state for the failure code explanation.
      Serial2.print( client.state() );
      Serial2.println( " Will try again in a few seconds" );
      delay( 3*1000 );
    }
  }
}

void MQTT::loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}

void MQTT::publish(const char* topic, const char* payload) {
  client.publish(topic, payload);
}
