import sys
sys.path.append('../')
import paho.mqtt.client as mqtt
import time
from locust import task, TaskSet, User, between, events
from message.message import MessageHandler
from mqtt_handlers.mqtt_client_manager import MQTTClientManager
from config.config import BROKER_HOST, BROKER_PORT, MQTT_USERNAME, MQTT_PASSWORD, SIZE_PAYLOAD, SIMULATION_NAME,NUM_REQUESTS, BROKER_PORT_TLS
from storage.storage import Storage

class MqttTaskSet(TaskSet):

    # Setup das task 

    def __init__(self, parent):
        super().__init__(parent)
        pass

    @task
    def publish_message_task(self):

        # Validando quantidade de request realizadas por esse device
        # if self.parent.request_count >   int(NUM_REQUESTS):
        #     return self.user.on_stop()
        message = MessageHandler(
            "Round Trip Time", 0, self.parent.topic, 1, SIMULATION_NAME, self.parent.request_count, int(SIZE_PAYLOAD)
        )
        self.parent.request_count +=1
        print(self.parent.mqtt.client._client_id)
        message_info = self.parent.mqtt.publish(message.topic, message.payload, int(message.qos))
        message_info.wait_for_publish()
        message.insert_send_time()
        print(message.send_time)
        self.parent.mqtt.user_data_set(message)

class MQTTLocustUser(User):

    # Setup do da simulação

    tasks = [MqttTaskSet]
    wait_time = between(0.1, 3)
    
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # inicializando broker mqtt
        self.request_count = 1
        self.mqtt = MQTTClientManager(str(BROKER_HOST), 8883, str(MQTT_USERNAME), str(MQTT_PASSWORD), True)

    def on_start(self):
        self.storage = Storage()
        self.storage.createFile(f"{self.mqtt.client._client_id.decode()}")
        self.mqtt.client.loop_start()
        print(self.mqtt.client._client_id)
        self.topic = f"device/{self.mqtt.client._client_id.decode()}"
        self.mqtt.subscribe(self.topic)
        time.sleep(15)
        
    def on_stop(self):
        print(f"User {self.mqtt.client._client_id.decode()} finished with {self.request_count} requests.")
        self.mqtt.client.loop_stop()
        self.mqtt.client.disconnect()
        self.stop(True)
        self.storage.save_results()
        time.sleep(2)
        self.environment.runner.quit()
