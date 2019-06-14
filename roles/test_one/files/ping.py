"""MEF_ELINE Test 1 ping."""

from pythonping import ping

import sys


class Ping():

    flag = ""
    target = ""
    count = 0
    file = "/tmp/ping_result.txt"

    def __init__(self, target="127.0.0.1", count=4, flag=None):
        """

        :param target:
        :param count:
        :param flag:
        """
        self.target = target
        self.count = count
        self.flag = flag

    def run_ping(self):

        ping_var = ping(self.target, count=self.count,verbose=True)

        print(ping_var)

        op = open(self.file, 'a')
        op.write(str(ping_var.output))

        op.close()


if __name__ == "__main__":
    arg_one = sys.argv[1]
    arg_two = sys.argv[2]
    arg_three = sys.argv[3]

    var = Ping(target=arg_one, count=arg_two, flag=arg_three)
    var.run_ping()

