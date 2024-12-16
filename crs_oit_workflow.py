from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test
from termcolor import colored
import os

description = """
    Go to CRS, create new order, finalize the order, capture and map, self
    index the order, verify the order, order is in archive"""

tags = ['regression']


class test(TestParent):

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: no
        Post-conditions: Order is processed from Order Queue to Archive
        """

        if self.data.OIT in self.data['config'].get_order_types():

            # To get the ANSI codes working on windows for support color fonts
            os.system('color')
            os.system('cls')

            # --------------------------Select-Order-Action------------------------------------

            print("\nOrder Actions:\n")
            print("1. Finalize")
            print("2. Capture")
            print("3. Indexing")
            print("4. Verification")
            while True:
                action = input("\nEnter 1-4 > ")
                action = action.strip().lower()
                if not action:
                    action = "1"
                    print("\nAction " + colored("Finalize", "green") + " is selected by default\n")
                    break
                elif action not in ["1", "2", "3", "4"]:
                    print("\nAction is not available. Repeat entering...")
                else:
                    match action:
                        case "1": print("\nAction " + colored("Finalize", "green") + " is selected")
                        case "2": print("\nAction " + colored("Capture", "green") + " is selected")
                        case "3": print("\nAction  " + colored("Indexing", "green") + " is selected")
                        case "4": print("\nAction  " + colored("Verification", "green") + " is selected")
                    break

            # --------------------------Select-Number-Of-OITs------------------------------------

            while True:
                n_of_oits = input("\nEnter No. of OITs > ").strip()
                if not n_of_oits:
                    n_of_oits = 1
                    print("\nNumber Of OITs " + colored("1", "green") + " is selected by default\n")
                    break
                elif not n_of_oits.isdigit():
                    print("\nIncorrect value. Repeat entering...")
                else:
                    print("\nNumber Of OITs " + colored(n_of_oits, "green") + " is selected")
                    break

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
                        print(colored("\n" + "-" * 50 + " ADD ORDER and FINALIZE" + "-" * 50 + "\n", "yellow"))
                        self.atom.CRS.order_queue.create_and_action_with_order(self.atom.CRS.add_payment.finalize_order,
                                                                               oi_count=int(n_of_oits))
                        if self.data["OIT"] == "RP_Recordings" or self.data["OIT"] == "Real_Property_Alabama":
                            self.atom.CRS.general.go_to_crs()
                        if action != "1":
                            print(colored("\n" + "-" * 50 + " CAPTURE ORDER" + "-" * 50 + "\n", "yellow"))
                            if int(n_of_oits) != 1:
                                self.lib.CRS.order_item_type.capture_step(oi_count=int(n_of_oits))
                            else:
                                self.lib.CRS.order_item_type.capture_step()
                            if action not in ["1", "2"]:
                                print(colored("\n" + "-" * 50 + " ORDER INDEXING" + "-" * 50 + "\n", "yellow"))
                                self.lib.CRS.order_item_type.indexing_step()
                                if action not in ["1", "2", "3"]:
                                    print(colored("\n" + "-" * 50 + " ORDER VERIFICATION" + "-" * 50 + "\n", "yellow"))
                                    self.lib.CRS.order_item_type.verification_step()
                                    # verify order is in archive
                                    print(colored("\n" + "-" * 50 + " ORDER SEARCH" + "-" * 50 + "\n", "yellow"))
                                    self.atom.CRS.order_search.search_order_by_order_number()
                                    self.lib.CRS.order_search.verify_order_present_in_result(self.data["order_number"])
                                    self.lib.CRS.order_search.verify_order_status("archive_status")
                        print("\n" + colored("█" * 50, "green") + f" Test # {i + 1} : Finished " + colored("█" * 50,
                                                                                                           "green") + "\n")
                        break
                    except Exception as msg:
                        print(colored(msg, "cyan"))
                        print(colored("\n" + "█" * 50 + " TEST IS NOT FINISHED " + "█" * 50 + "\n", "red"))
                        continue

        else:
            self.actions.step(f"{self.data.OIT} does not exist for current tenant")


if __name__ == '__main__':
    run_test(__file__)
