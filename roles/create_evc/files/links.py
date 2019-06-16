"""Get the information from the switch connection."""

# Imports
import requests
import sys


# Classes


class ControllerConnection():
    """Class to connect to the controller and extract the information."""

    ip_addr = ""
    ip_port = int

    def __init__(self, ip_addr="", ip_port=int):
        """Initialize the the class with the controller information.

        Args:
            ip_addr(str): The ip address for the controller.
            ip_port(int): The port to connect to the controller.
        """
        self.ip_addr = ip_addr
        self.ip_port = ip_port

    def getting_ids(self):
        """Create a dictionary from the switches connected
        and extract the switch's IDs."""

        requested_app_info = "/api/kytos/topology/v3/switches"

        addr_inf = "http://{}:{}{}".format(self.ip_addr,
                                           self.ip_port,
                                           requested_app_info)

        try:

            json_data = requests.get(addr_inf).json()

            switch_ids = ""

            for switch in dict(json_data['switches']).keys():

                swt_id_port = 10

                switch_ids += "{}:{}\n".format(switch, swt_id_port)

            list_ids = list(switch_ids)

            return list_ids

        except Exception as e:

            print(e)

    def write_to_file(self):
        """Create a file with the switch IDs."""

        try:

            file = open("switch_ids.txt", "w")

            file.write(self.getting_ids())

            file.close()

        except Exception as e:

            print(e)


if __name__ == "__main__":

    try:

        ip_addr = str(sys.argv[1])
        ip_port = int(sys.argv[2])

        ControllerConnection.write_to_file(ControllerConnection(ip_addr, ip_port))

    except Exception as e:
        print(e)
