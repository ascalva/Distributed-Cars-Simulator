import requests
import time
import os
import json
import threading
import socket
import struct
import ast

class Car :
    """
    A Car object should be able to move along a simulated board and interact with the
    environment. The environment is simulated by a centralized server, which helps
    simulate distance by providing a car's neighbors. Communication and coordination
    between cars does not involve server.
    """
    

    def __init__(self, name: str, server_hostname: str, server_port: str) -> None :
        self.name        = name
        self.server_host = server_hostname
        self.server_port = server_port
        self.position    = []
        self.neighbors   = {}
        self.env         = {}
        self.MCAST_GRP = '224.1.1.1'
        self.MCAST_PORT = 5000
        self.MULTICAST_TTL = 2



    def login(self) :
        """
        Establish "connection" with simulator (server) and get car position
        along the board.
        """
        res = requests.post(
            f"http://{self.server_host}:{self.server_port}/actions/login",
            data = {"id" : self.name}
        )

        if not res.ok :
            print("!! Error: Failed to connect to server")

        # Get randomly assigned position from server.
        data          = json.loads(res.content)
        self.position = data["position"]


    def getNeighbors(self) :
        """
        Get current car neighbors (threshold determined by server) and their
        corresponding IP addresses.
        """
        res = requests.post(
            f"http://{self.server_host}:{self.server_port}/actions/getNeighbors",
            data = {"id" : self.name}
        )

        if not res.ok :
            print("!! Error: Unable to get neighbors.")

        self.neighbors = json.loads(res.content)


    def move(self) :
        """
        Attempt a move to a new position. Should utilize sensor data, objective,
        (and history) to determine the next move. Sensor data is always returned:
            - If move is successful, gets data about new surroundings.
            - If move is unsuccessful, gets updated data about current surroundings.
        """
        # TODO: Do proper moves.
        data = {
            "id" : self.name,
            "position_x" : self.position[0] + 1,
            "position_y" : self.position[1] + 1
        }

        res = requests.post(
            f"http://{self.server_host}:{self.server_port}/actions/move",
            data = data
        )

        if not res.ok :
            print("!! Error: Unable to move.")

        data        = json.loads(res.content)
        success     = data["success"]
        

    def processNeighborMessage(self, clientAddress, clientSocket):
        message = clientSocket.recv(2048)
        data = message.decode('utf-8')
        res = ast.literal_eval(data)

        if(res["type"] == "REQUEST"):
            message = {
            "type" : "RESPONSE",
            "from" : self.name,
            "to" : res["from"],
            "position" : self.position
            }
            replyThread = threading.Thread(target=self.sender, args=(str(message), res["from"]))
            replyThread.start()
        else:            
            self.env[res["from"]] = res["position"]
            print("ENV = " + str(self.env))

    def receiver(self):
        print("STARTED RECEIVER FOR : " + self.name )
        PORT = 5002
        rcv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rcv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        rcv.bind(('', PORT))
        while True:
            rcv.listen(2)
            clientsock, clientAddress = rcv.accept()
            processThread = threading.Thread(target=self.processNeighborMessage, args=(clientAddress,clientsock))
            processThread.start()


    def sender(self, message, clientId):
        PORT = 5002
        sndr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sndr.connect((clientId, PORT))
        sndr.send(bytes(message,'UTF-8'))
        sndr.close()


    def sendNeighborsMessage(self):
        time.sleep(10)
        for neighbor in self.neighbors.keys():
            message = {
            "type" : "REQUEST",
            "from" : self.name,
            "to" : neighbor
            }

            t = threading.Thread(target=self.sender, args=(str(message), neighbor))
            t.start()
        
    def updateEnvironment(self):
        for client in self.env.keys():
            if client not in self.neighbors.keys():
                del self.env[client]
        

    def run(self) :
        
        t = threading.Thread(target=self.receiver, args=())
        t.start()
        while True :

                # Main execution, do something
                # Actions include :
                #   - get neighbors
                #   - move
                #   - communicate with neighbors
                #   - use sensor info
                # if self.name == "client-1" :
            self.getNeighbors()
            self.updateEnvironment()
            self.sendNeighborsMessage()
            time.sleep(10)


if __name__ == "__main__" :
    params = {
        "name"            : os.environ.get("CLIENT_ID"),
        "server_hostname" : os.environ.get("HOSTNAME"),
        "server_port"     : os.environ.get("PORT")

    }

    print("Creating object")
    c = Car(**params)

    print("Loging in")
    c.login()

    print("Run main function.")
    c.run()

