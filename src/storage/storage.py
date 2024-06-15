import sys
sys.path.append('../')
from  message.message import MessageHandler
import csv
from config.config import SIMULATION_NAME
import os
import requests

class Storage():
    def createFile(self, device:str):
        #criando nome de diretorio com valores do simulation name e device
        # self.path = str(f"../../data/{str(SIMULATION_NAME)}/{device}.csv")
        self.path = str(f"../../data/{str(SIMULATION_NAME)}/dataLocust.csv")

        # Obtendo todos os atributos da classe
        self.fieldnames =['type',
                'qos',
                'topic',
                'timeout',
                'name',
                'message_count',
                'size',
                'receive_time',
                'send_time']
        directory = os.path.dirname(self.path)
        # cria diretorio. O argumento exist_ok=True garante que o diretório seja criado apenas se ele não existir.
        os.makedirs(directory, exist_ok=True)

        if not os.path.exists(self.path):
            with open(self.path , mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()

    def storageData(self, message: MessageHandler):
        print("self.filename self.filename  self.filename  ", self.path )
        with open(self.path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            data = {
                'type': message.type,
                'qos': message.qos,
                'topic': message.topic,
                'timeout': message.timeout,
                'name': message.name,
                'message_count': message.message_count,
                'size': len(message.payload),
                'receive_time': message.receive_time,
                'send_time': message.send_time,
                }
            writer.writerow(data)
    
  
    def save_results(self):
        locust_base_url = "http://192.168.15.9:8089"
        endpoints = {
            "requests": "/stats/requests/csv",
            "failures": "/stats/failures/csv",
            "exceptions": "/exceptions/csv",
            "report": "/stats/report?download=1&theme=dark"
        }

        def save_csv(endpoint, filename):
            response = requests.get(f"{locust_base_url}{endpoint}")
            if response.status_code == 200:
                with open(filename, "wb") as file:
                    file.write(response.content)
                print(f"Dados salvos com sucesso em {filename}")
            else:
                print(f"Falha ao obter os dados de {endpoint}: {response.status_code}")

        def save_html(endpoint, filename):
            response = requests.get(f"{locust_base_url}{endpoint}")
            if response.status_code == 200:
                # Salvar o conteúdo do relatório HTML em um arquivo
                with open(filename, "wb") as file:
                    file.write(response.content)
                print(f"Relatório HTML salvo com sucesso")
            else:
                print(f"Falha ao obter o relatório HTML")

        for key, endpoint in endpoints.items():
            if key == "report":
                save_html(endpoint, str(f"../../data/{str(SIMULATION_NAME)}/locust_{key}_resultados.html"))
            else:
                save_csv(endpoint, str(f"../../data/{str(SIMULATION_NAME)}/locust_{key}_resultados.csv"))

if __name__ == "__main__":

    message =  MessageHandler(
        "Round Trip Time", 
        1,
        "topic",
        1,
        "mensagem name",
        0,
        10
    )
    storage = Storage()
    storage.createFile("device")
    print(message)
    storage.storageData(message)