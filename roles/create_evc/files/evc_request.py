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

    file = "/tmp/circuits.txt"

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
        d = {self.host: {self.value: data}}

        return d

    def update_circuit_request(self, io=None, data=None):

        if data and io:

            file = self.read_circuit_request(io)

            file.update({self.host: {self.value: data}})

            return file

        else:

            file = self.read_circuit_request()

            file.get(self.host).pop(self.value)

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
        msg_data = None

        data = self.read_circuit_request()

        if self.host in data and self.value in data.get(self.host):
            msg_data = self.url + data.get(self.host).get(self.value).get("circuit_id")

        return msg_data

    def actions(self):
        """

        :return:
        """
        resp = ""
        data = None
        mode = None

        if self.action == "create_evc":

            resp = requests.post(url=self.url, json=self.create_evc(),
                                headers=self.headers)

            data = eval(resp.text)

        elif self.action == "delete_evc":

            rem_evc = self.delete_evc()

            if rem_evc:

                resp = requests.delete(rem_evc)

                if resp.text.__contains__("Circuit removed"):
                    data = self.update_circuit_request()

                print(resp)

        self.save_circuit_request(data, mode)


if __name__ == "__main__":

    arg_1 = sys.argv[1]
    arg_2 = sys.argv[2]
    arg_3 = sys.argv[3]

    evc_req = Request(host=arg_1, value=arg_2, action=arg_3)
    evc_req.actions()
