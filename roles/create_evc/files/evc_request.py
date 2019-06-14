"""Creating the request curl for test1."""

import requests
import os
import sys


class Request():
    """

    """

    value = 0

    action = ""

    host = "127.0.0.1"

    file = "/tmp/circuits.json"

    url = "http://67.17.206.252:8181/api/kytos/mef_eline/v2/evc/"

    name = "Test1"
    interface_id_a = "00:00:6c:ec:5a:08:5f:75:10"
    interface_id_z = "00:00:6c:ec:5a:09:be:62:10"

    headers = {"Content-Type": "application/json", "cache-control": "no-cache"}

    def __init__(self, host= None, value=None, action=None):
        """

        :param value:
        """
        self.value = value
        self.action = action
        self.host = host

    def save_circuit_request(self, data=None):

        if data:

            json_data = ""

            w_io = open(self.file, 'w')

            if os.path.isfile(self.file):
                json_data = self.update_circuit_request(data)
            else:
                json_data = self.create_circuit_request(data)

            w_io.write(json_data)
            w_io.close()

    def read_circuit_request(self):

        r_io = open(self.file, 'r')
        data = r_io.read()
        r_io.close()

        return dict(data)

    def create_circuit_request(self, data=None):
        """

        :param data:
        :return:
        """
        return dict.setdefault(self.host, dict.setdefault(self.value, data))

    def update_circuit_request(self, data=None):

        if data:

            file = self.read_circuit_request()

            # dict_data = dict(file)

            file.__setitem__(self.host, self.value, v=data)

            return file

        else:

            file = self.read_circuit_request()

            file.pop(self.host, self.value)

            return file

    def delete_circuit_request(self, data=None):

        pass

    def create_evc(self):
        """

        :return:
        """

        msg_data = dict({"name": self.name,
                         "uni_a": {"interface_id": self.interface_id_a,
                                   "tag": {"tag_type": 1, "value": int(self.value)}
                                   },
                         "uni_z": {"interface_id": self.interface_id_z,
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
        msg_data = self.url + self.read_circuit_request().get(self.host, self.value)

        return msg_data

    def actions(self):
        """

        :return:
        """
        resp = ""
        data = None

        if self.action == "create_evc":

            resp = requests.post(url=self.url, json=self.create_evc(),
                                headers=self.headers)

            data = self.create_circuit_request(resp.text)

        elif self.action == "delete_evc":

            test = self.read_circuit_request().get(self.host, self.value)

            resp = requests.delete(self.delete_evc())

            if resp.text == "":
                data = self.update_circuit_request()

            print(resp)

        self.save_circuit_request(data)


if __name__ == "__main__":

    arg_1 = "127.0.0.1" #sys.argv[1]
    arg_2 = "30" #sys.argv[2]
    arg_3 = "create_evc" #sys.argv[3]

    evc_req = Request(host=arg_1, value=arg_2, action=arg_3)
    evc_req.actions()
