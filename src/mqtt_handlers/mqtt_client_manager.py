from locust import events
import paho.mqtt.client as mqtt
import sys
import time
import uuid
import ssl

sys.path.append('../')
from storage.storage import Storage

from metrics.round_trip_time import RoundTripTime

class MQTTClientManager():

    def __init__(
        self, broker_address: str, broker_port: int, username: str, password: str, tls: bool
    ):
        self.setup(broker_address, broker_port, username, password, tls)

    def setup(
        self, broker_address: str, broker_port: int, username: str, password: str, tls: bool
    ):
        self.client = self.create_client(broker_address, broker_port)
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_message = self.on_message
        if (tls==True):
            self.client.tls_set("/python/simulator/src/ca.crt",
                                cert_reqs=ssl.CERT_REQUIRED,
                                tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
        self.client.tls_insecure_set(True)
        self.connect(username, password)

    def create_client(self, broker_address, broker_port):
        uuid_generated = uuid.uuid4()
        self.broker_address = broker_address
        self.broker_port = broker_port
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, str(uuid_generated))

    def connect(self, username: str, password: str):
        self.client.username_pw_set(username, password)
        self.client.connect(self.broker_address, self.broker_port, 60)
        # Implementação da conexão com o cliente MQTT

    def publish(self, topic, message, qos):
        return self.client.publish(topic, message, qos)
        # Implementação da publicação de mensagens MQTT

    def subscribe(self, topic):
        self.client.subscribe(topic)
        # Implementação da subscrição a tópicos MQTT com um callback

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    def on_publish(self, client, userdata, mid):
        # Implementação do on_publish com um callback
        pass

    def on_message(self, client, userdata, msg):
        userdata.receive_time = time.monotonic()
        rtt = RoundTripTime(userdata)
        calc = rtt.calculate()
        print(calc)
        events.request.fire(request_type=userdata.type, 
                            name=userdata.topic, 
                            response_time=int(calc), 
                            response_length=len(userdata.payload), 
                            response=None, 
                            context={},
                            exception=None,
                            start_time=userdata.send_time,
                            url=None,)
        storage = Storage()
        storage.createFile(f"{self.client._client_id.decode()}")
        storage.storageData(userdata)
        
    def user_data_set(self, object: object):
        self.client.user_data_set(object)


# from mqtt_handlers.mqtt_client_manager import   MQTTClientManager
# client = MQTTClientManager("localhost", 1883, "admin", "Ap@690#KptLmn8")
# client.publish("topico", "message", 1)
