"""Creating the request curl for test1."""

import requests
import sys


class Request():
    """

    """

    value = 0

    type = ""

    url = "http://67.17.206.252:8181/api/kytos/mef_eline/v2/evc/"

    name = "Test1"
    interface_id_a = "00:00:6c:ec:5a:08:5f:75:10"
    interface_id_z = "00:00:6c:ec:5a:09:be:62:10"

    headers = {"Content-Type": "application/json", "cache-control": "no-cache"}

    def __init__(self, value=None, type=None):
        """

        :param value:
        """
        self.value = value
        self.type = type

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
        msg_data = self.url + str(self.value)

        return msg_data

    def action(self):
        """

        :return:
        """
        resp = ""

        if self.type == "create_evc":

            req = requests.post(url=self.url, json=self.create_evc(),
                                headers=self.headers)
            resp = req.text

            print(resp)

        elif self.type == "delete_evc":

            req = requests.delete(self.delete_evc())

            resp = req.text
            print(resp)

    def save_circuit_request(self, data=None):

        if data:
            w_io = open("/tmp/circuits.json", 'w')
            w_io.write(data)
            w_io.close()



    def read_circuit_request(self):

        r_io = open("/tmp/circuits.json", 'r')





if __name__ == "__main__":

    arg_1 = sys.argv[1]
    arg_2 = sys.argv[2]
    evc_req = Request(value=arg_1, type=arg_2)
    evc_req.action()
