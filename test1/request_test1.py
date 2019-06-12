"""Creating the request curl for test1."""

import requests
import sys


class Request():
    url = "http://67.17.206.252:8181/api/kytos/mef_eline/v2/evc/"

    value = 0

    name = "Test1"
    interface_id_a = "00:00:6c:ec:5a:08:5f:75:10"
    interface_id_z = "00:00:6c:ec:5a:09:be:62:10"

    headers = {"Content-Type": "application/json", "cache-control": "no-cache"}

    def __init__(self, value=None):
        """

        :param value:
        """
        self.value = value

    def create_request(self):

        msg_data = dict({"name": self.name,
                         "uni_a": {"interface_id": self.interface_id_a,
                                   "tag": {"tag_type": 1, "value": self.value}
                                   },
                         "uni_z": {"interface_id": self.interface_id_z,
                                   "tag": {"tag_type": 1, "value": self.value}
                                   },
                         "dynamic_backup_path": True,
                         "active": True,
                         "enabled": True
                         })

        return msg_data

    def request(self):
        req = requests.post(url=self.url, json=self.create_request(),
                           headers=self.headers )
        print(req.text)


if __name__ == "__main__":

    val = 24 # int(sys.argv[1])

    req = Request(value=val)
    req.request()
