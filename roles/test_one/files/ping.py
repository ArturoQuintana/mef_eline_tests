"""MEF_ELINE Test 1 ping."""

from pythonping import ping
import sys



class Ping():

    flag = ""
    tartget = ""
    count = 0

    def __init__(self, target="127.0.0.1", count=4, flag=None):
        """

        :param target:
        :param count:
        :param flag:
        """
        self.tartget = target
        self.count = count
        self.flag = flag

    def run_ping(self):

        ping_var = ping(target=self.tartget, count=self.count)

        print(ping_var)




if __name__ == "__main__":
    arg_one = sys.argv[1]
    arg_two = sys.argv[2]
    arg_three = sys.argv[3]

    var = Ping(target=arg_one, count=arg_two, flag=arg_three)
    var.run_ping()

