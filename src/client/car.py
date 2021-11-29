import requests
import time
import os
import json

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

