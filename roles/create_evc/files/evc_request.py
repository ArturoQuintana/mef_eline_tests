"""Creating the request curl for test1."""

import requests
import os
import sys


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

            switch_ids = None
            index = 0

            for switch in dict(json_data['switches']).keys():

                swt_id_port = 10

                if not switch_ids:
                    switch_ids = {index: '{}:{}'.format(switch, swt_id_port)}
                else:
                    switch_ids.update({index: '{}:{}'.format(switch, swt_id_port)})

                index += 1

            return switch_ids

        except Exception as e:

            print(e)

class Request():
    """

    """

    value = 0

    action = ""

    # host = "127.0.0.1"

    controller_adr = None

    controller_port = None

    file = "circuits.txt"

    url = "http://67.17.206.252:8181/api/kytos/mef_eline/v2/evc/"

    name = "Test1"
    interface_id_a = "00:00:6c:ec:5a:08:5f:75:10"
    interface_id_z = "00:00:6c:ec:5a:09:be:62:10"

    HEADERS = {"Content-Type": "application/json", "cache-control": "no-cache"}

    def __init__(self, controller_addr=None, controller_port=None,
                 value=None, action=None):
        """

        :param value:
        """
        self.controller_adr = controller_addr
        self.controller_port = controller_port
        self.value = value
        self.action = action
        self.url = "http://{}:{}/api/kytos/mef_eline/v2/evc/".format(self.controller_adr, self.controller_port)

    def save_circuit_request(self, data=None, mode=None):
        exclude = 'Not Acceptable: This evc already exists.'

        if data and data != exclude:

            json_data = ""

            io = None

            if os.path.isfile(self.file) and mode:
                io = open(self.file, 'r+')
                json_data = self.update_circuit_request(io, data)
            elif os.path.isfile(self.file) and not mode:
                io = open(self.file, 'w')
                json_data = data
            else:
                io = open(self.file, 'w')
                json_data = self.create_circuit_request(data)

            io.write(str(json_data))
            io.close()

    def read_circuit_request(self, r_io=None):

        if r_io:

            data = r_io.readlines()
            r_io.close()

            return eval("".join(data))
        else:
            if os.path.isfile(self.file):
                r_io = open(self.file, 'r')

                data = r_io.readlines()
                r_io.close()

                return eval("".join(data))

    def create_circuit_request(self, data=None):
        """

        :param data:
        :return:
        """

        d = {self.interface_id_a: {self.interface_id_z: {self.value: data}}}

        return d

    def update_circuit_request(self, io=None, data=None):

        if data and io:

            file = self.read_circuit_request(io)

            file.update({self.interface_id_a: {self.interface_id_z: {self.value: data}}})

            return file

        else:

            file = self.read_circuit_request()

            file.get(self.interface_id_a).get(self.interface_id_z).pop(self.value)

            if not file.keys(self.interface_id_a):
                file.pop(self.interface_id_a)

            elif not file.get(self.interface_id_a).key(self.interface_id_z):
                file.get(self.interface_id_a).pop(self.interface_id_z)

            return file

    def delete_circuit_request(self, data=None):

        pass

    def create_evc(self, interface_id_a=None, interface_id_z=None):
        """

        :return:
        """

        msg_data = dict({"name": self.name,
                         "uni_a": {"interface_id": interface_id_a,
                                   "tag": {"tag_type": 1, "value": int(self.value)}
                                   },
                         "uni_z": {"interface_id": interface_id_z,
                                   "tag": {"tag_type": 1, "value": int(self.value)}
                                   },
                         "dynamic_backup_path": True,
                         "active": True,
                         "enabled": True
                         })

        return msg_data

    def delete_evc(self):
        """

        :return:
        """
        msg_data = None

        data = self.read_circuit_request()

        if data and self.interface_id_a in data.keys() and self.interface_id_z in \
                data.get(self.interface_id_a).keys() and self.value in \
                data.get(self.interface_id_a).get(self.interface_id_z).keys():

            msg_data = self.url + data.get(self.interface_id_a)\
                .get(self.interface_id_z).get(self.value).get("circuit_id")

        return msg_data

    def actions(self):
        """

        :return:
        """
        links = ControllerConnection(self.controller_adr, self.controller_port)
        switch_ids = links.getting_ids()

        mode = None

        if switch_ids and self.action == "create_evc":
            index_a = 0

            mode = True

            while switch_ids.__len__() > index_a:

                index_z = index_a + 1

                while switch_ids.__len__() > index_z:

                    self.interface_id_a = switch_ids.get(index_a)
                    self.interface_id_z = switch_ids.get(index_z)

                    resp = requests.post(url=self.url,
                                         json=self.create_evc(self.interface_id_a,
                                                              self.interface_id_z),
                                         headers=self.HEADERS)

                    data = eval(resp.text)

                    self.save_circuit_request(data, mode)

                    index_z = index_z + 1
                index_a = index_a + 1

        elif self.action == "delete_evc":

            index_a = 0
            rem_evc = None

            while switch_ids.__len__() > index_a:

                index_z = index_a + 1

                while switch_ids.__len__() > index_z:
                    self.interface_id_a = switch_ids.get(index_a)
                    self.interface_id_z = switch_ids.get(index_z)

                    rem_evc = self.delete_evc()

                    if rem_evc:

                        resp = requests.delete(rem_evc)

                        if resp.text.__contains__("Circuit removed"):
                            data = self.update_circuit_request()

                            self.save_circuit_request(data, mode)

                        print(resp)

                    index_z = index_z + 1
                index_a = index_a + 1


if __name__ == "__main__":

    msg = None
    try:

        if sys.argv.__len__() == 5:

            arg_1 = sys.argv[1]
            arg_2 = sys.argv[2]
            arg_3 = sys.argv[3]
            arg_4 = sys.argv[4]
        else:
            msg = "Error! Missing Arguments."
            raise Exception("Error! Missing Arguments.")

        if not (str(sys.argv[2]).isdecimal() and str(sys.argv[3]).isdecimal()):
            msg = "Error! Argument 2, 4 or both are NOT integers."
            raise Exception("Error! Argument 2, 4 or both are NOT integers.")

        evc_req = Request(controller_addr=arg_1, controller_port=arg_2, value=arg_3, action=arg_4)
        evc_req.actions()

    except Exception as e:

        sys.exit(msg)




