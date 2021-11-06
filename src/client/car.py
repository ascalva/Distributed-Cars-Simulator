import requests
import time

class Car :
    def __init__(self, name, server_hostname, server_port) :
        self.name        = name
        self.server_host = server_hostname
        self.server_port = server_port
        self.neighbors   = {}
        self.position    = []


    def login(self) :
        res = requests.post(
            f"http://{self.server_host}:{self.server_port}/actions/login",
            data = {"id" : self.name}
        )

        if not res.ok :
            print("!! Error: Failed to connect to server")

        # TODO: Get randomly assigned position from server.


    def run(self) :
        while True :

            # Main execution, do something
            # Actions include :
            #   - get neighbors
            #   - move
            #   - communicate with neighbors
            #   - use sensor info

            time.sleep(10)
            pass


if __name__ == "__main__" :
    params = {
        "name"            : "test_client",
        "server_hostname" : "simulator",
        "server_port"     : "5000"
    }

    print("Creating object")
    c = Car(**params)

    print("Loging in")
    c.login()

    print("Run main function.")
    c.run()

