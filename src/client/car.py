import requests
import time
import os
import json

class Car :
    def __init__(self, name, server_hostname, server_port) :
        self.name        = name
        self.server_host = server_hostname
        self.server_port = server_port
        self.neighbors   = {}
        self.position    = []
        self.env         = {}


    def login(self) :
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
        res = requests.post(
            f"http://{self.server_host}:{self.server_port}/actions/getNeighbors",
            data = {"id" : self.name}
        )

        if not res.ok :
            print("!! Error: Unable to get neighbors.")

        self.neighbors = json.loads(res.content)


    def move(self) :
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
        sensor_data = data["sensor_data"]

        if success :
            self.env = sensor_data
            print(self.env)


    def run(self) :
        while True :

            # Main execution, do something
            # Actions include :
            #   - get neighbors
            #   - move
            #   - communicate with neighbors
            #   - use sensor info
            if self.name == "client-1" :
                self.getNeighbors()


            time.sleep(10)
            pass


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

