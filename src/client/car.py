import requests
import time
import os
import json
import threading
import socket
import struct
import ast
import random

class Car :
    """
    A Car object should be able to move along a simulated board and interact with the
    environment. The environment is simulated by a centralized server, which helps
    simulate distance by providing a car's neighbors. Communication and coordination
    between cars does not involve server.
    """

    def __init__(self, name: str, server_hostname: str, server_port: str) -> None :
        self.name               = name
        self.server_host        = server_hostname
        self.server_port        = server_port
        self.position           = []
        self.neighbors          = {}
        self.env                = {}
        self.obstacles          = []
        possibleDirections      = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        possibleAdjust          = [[0, 1], [0, -1], [0, 1], [0, -1]] 
        randomInit              = random.randint(0, 3)
        self.direction          = possibleDirections[randomInit]
        self.adjust             = possibleAdjust[randomInit]
        self.MCAST_GRP          = '224.1.1.1'
        self.MCAST_PORT         = 5000
        self.MULTICAST_TTL      = 2
        self.obstacleBlock      = False
        self.legalMove          = True
        self.collisionRight     = False
        self.collisionLeft      = False
        self.obstacleRightBlock = False
        self.obstacleLeftBlock  = False


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
        Get current car neighbors (threshold determined by server), their
        corresponding IP addresses and the location of all obstacles in view.
        """

        res = requests.post(
            f"http://{self.server_host}:{self.server_port}/actions/getNeighbors",
            data = {
                "id"        : self.name,
                "neighbors" : {}
            }
        )

        if not res.ok :
            print("!! Error: Unable to get neighbors.")

        data = json.loads(res.content)

        for entry in data["neighbors"].keys():
            if entry.startswith('o'):
                self.obstacles.append(data["neighbors"][entry])
            else:
                self.env[entry] = data["neighbors"][entry]


    def move(self) :
        """
        Attempt a move to a new position. Should utilize sensor data, objective,
        (and history) to determine the next move. Sensor data is always returned:
            - If move is successful, gets data about new surroundings.
            - If move is unsuccessful, gets updated data about current surroundings.
        """

        for obstacle in self.obstacles:
            if obstacle[0] == self.position[0] + self.direction[0] and \
               obstacle[1] == self.position[1] + self.direction[1]:
               self.obstacleBlock = True

        for neighbor in self.env.keys():
            if self.env[neighbor][0] == self.position[0] + self.direction[0] and \
               self.env[neighbor][1] == self.position[1] + self.direction[1]:
                time.sleep(3)
                self.legalMove = False

        if self.legalMove and not self.obstacleBlock:
            self.position[0] += self.direction[0]
            self.position[1] += self.direction[1]
            self.obstacleLeftBlock  = False
            self.obstacleRightBlock = False
            self.collisionLeft  = False
            self.collisionRight = False
        else:
            for neighbor in self.env.keys():
                if self.env[neighbor][0] == self.position[0] + self.adjust[0] and \
                   self.env[neighbor][1] == self.position[1] + self.adjust[1]:
                    self.collisionRight = True
                    break
                elif self.env[neighbor][0] == self.position[0] - self.adjust[0] and \
                     self.env[neighbor][1] == self.position[1] - self.adjust[1]:
                    self.collisionRight = True
                    break
    
            for obstacle in self.obstacles:
                if obstacle[0] == self.position[0] + self.adjust[0] and \
                   obstacle[1] == self.position[1] + self.adjust[1]:
                    self.obstacleRightBlock = True
                    break
                elif obstacle[0] == self.position[0] - self.adjust[0] and \
                     obstacle[1] == self.position[1] - self.adjust[1]:
                    self.obstacleLeftBlock = True
                    break

        if (self.obstacleBlock or not self.legalMove) and not self.obstacleRightBlock and not self.collisionRight:
            self.position[0]   += self.adjust[0]
            self.position[1]   += self.adjust[1]
            self.obstacleBlock =  False
            self.legalMove     =  True
        elif (self.obstacleBlock or not self.legalMove) and not self.obstacleLeftBlock and not self.collisionLeft:
            self.position[0]   -= self.adjust[0]
            self.position[1]   -= self.adjust[1]
            self.obstacleBlock =  False
            self.legalMove     =  True
        elif (self.obstacleBlock and self.obstacleLeftBlock and self.obstacleRightBlock) or \
             (not self.legalMove and self.obstacleLeftBlock and self.obstacleRightBlock):
            self.position[0]   -= self.direction[0]
            self.position[1]   -= self.direction[1]

        data = {
            "id" : self.name,
            "position_x" : self.position[0],
            "position_y" : self.position[1]
        }

        res = requests.post(
            f"http://{self.server_host}:{self.server_port}/actions/move",
            data = data
        )

        if not res.ok :
            print("!! Error: Unable to move.")

        data = json.loads(res.content)
        self.position[0]    = data["position_x"]
        self.position[1]    = data["position_y"]
        

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
        time.sleep(2)
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
            pass
            """
            The execution of the following code demonstrates how cars would lose sight of each other
            in much larger environments when the cars leave the current grid. This environment is small
            enough to allow these cars to always maintain communication with each other
            """
            # if client not in self.neighbors.keys():
            #     del self.env[client]
        

    def run(self) :
        
        t = threading.Thread(target=self.receiver, args=())
        t.start()
        while True :
            self.getNeighbors()
            self.updateEnvironment()
            self.sendNeighborsMessage()
            self.move()
            time.sleep(2)


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