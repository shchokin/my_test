from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test
from termcolor import colored
import os

description = """
    Go to CS, submit 'Certified Copy' to CRS by DOC number, finalize and check order
        """

tags = ['48999_location_2']


class test(TestParent):                                                                                   # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # --------------------------Select-Number-Of-Orders------------------------------------

        while True:
            n_of_orders = input("\nEnter No. of orders > ").strip()
            if not n_of_orders:
                n_of_orders = 1
                print("\nNumber Of Orders " + colored("1", "green") + " is selected by default\n")
                break
            elif not n_of_orders.isdigit():
                print("\nIncorrect value. Repeat entering...")
            else:
                print("\nNumber Of Orders " + colored(n_of_orders, "green") + " is selected")
                break
        # --------------------------Orders-Creation---------------------------------------------

        for i in range(int(n_of_orders)):
            print("\n" + colored("█" * 50, "white") + f" Test # {i + 1} : Started " + colored("█" * 50,
                                                                                              "white") + "\n")
            while True:
                try:
                    self.atom.CS.general.go_to_cs()
                    # Get random doc number for OIT
                    self.api.clerc_search(self.data).get_document_number()
                    # Submit document to CRS
                    self.atom.CS.general.submit_to_crs()
                    print("\n" + colored("█" * 50, "green") + f" Test # {i + 1} : Finished " + colored("█" * 50,
                                                                                                       "green") + "\n")
                    break
                except Exception as msg:
                    print(colored(msg, "cyan"))
                    print(colored("\n" + "█" * 50 + " TEST IS NOT FINISHED " + "█" * 50 + "\n", "red"))
                    continue

        # # Go to CRS
        # self.atom.CRS.general.go_to_crs()
        # # Check order and finalize
        # self.atom.CS.general.finalize_and_check_in_crs()


if __name__ == '__main__':
    run_test(__file__)
