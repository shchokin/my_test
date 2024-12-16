from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test
from termcolor import colored
import os
from projects.Kofile.Atom.CRS.general import General
from projects.Kofile.Lib.general_helpers import GeneralHelpers

description = """ Scan First Test  """

# To get the ANSI codes working on windows for support color fonts
os.system('color')
os.system('cls')


def print_oits(oits):
    print(f"\n------------------Available OITs--------------------\n")
    for oit in oits:
        print(oit.strip())



class test(TestParent):

    def __init__(self, data):
        # self.order_types = [data["OT_1"], data["OT_2"]]
        super(test, self).__init__(data, __name__)

    def __test__(self):

        # Read data from CSV.Should be filed config OIT in env file otherwise will be default 'Real Property Recordings'
        # Comment it if you want to use oits name without configurations from txt file
        oits = [self.data["config"].test_data(f"{self.data.OIT}.order_type")]
        # print(oits)

        # -------------------------------------------Number-Of-OITs-----------------------------------------------------

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

        # --------------------------------------------------------------------------------------------------------------

        print("\nOrder Actions:\n")
        print("1. Add order")
        print("2. Finalize")
        print("3. Indexing")
        print("4. Verification")
        while True:
            action = input("\nEnter 1-4 > ")
            action = action.strip().lower()
            if not action:
                action = "1"
                print("\nAction " + colored("Add order", "green") + " is selected by default\n")
                break
            elif action not in ["1", "2", "3", "4"]:
                print("\nAction is not available. Repeat entering...")
            else:
                match action:
                    case "1":
                        print("\nAction " + colored("Add order", "green") + " is selected")
                    case "2":
                        print("\nAction " + colored("Finalize", "green") + " is selected")
                    case "3":
                        print("\nAction " + colored("Indexing", "green") + " is selected")
                    case "4":
                        print("\nAction " + colored("Verification", "green") + " is selected")
                break

        # --------------------------------------------------------------------------------------------------------------

        env = GeneralHelpers.get_env_name()

        # Uncomment if you want to use data for oit names (without configuration) from txt file
        '''
        oits = []

        if env == "qa_dev":
            with (open(r"D:\Auto\kofile-automation\Kofile\projects\Kofile\tests\my_test\Data\QA1_SF_69999_OITS.txt", "r") as file):
                oit = file.readline().strip()
                while oit:
                    oits.append(oit)
                    oit = file.readline().strip()
        elif env == "qa_48999_loc_2":
            with (open(r"D:\Auto\kofile-automation\Kofile\projects\Kofile\tests\my_test\Data\QA1_SF_48999_OITS.txt", "r") as file):
                oit = file.readline().strip()
                while oit:
                    oits.append(oit)
                    oit = file.readline().strip()
        elif env == "qa_arlington" or env == "uat_arlington":
            with (open(r"D:\Auto\kofile-automation\Kofile\projects\Kofile\tests\my_test\Data\QA1_SF_51013_OITS.txt", "r") as file):
                oit = file.readline().strip()
                while oit:
                    oits.append(oit)
                    oit = file.readline().strip()
        '''

        order_types = []

        for i in range(0, int(n_of_oits)):
            print_oits(oits)
            while True:
                order_type = input("\n[" + colored(f"{i + 1}", "green") + "] Select OIT from the list > ").strip()
                if not order_type:
                    if env == "qa_dev":
                        order_type = "Real Property Recordings"
                    elif env == "qa_48999_loc_2":
                        order_type = "Real Property OH"
                    elif env == "qa_arlington" or env == "uat_arlington":
                        order_type = "Land Records"
                    print("\nOrder Item Type " + colored(order_type, "green") + " is selected by default\n")
                    order_types.append(order_type)
                    break
                elif order_type not in oits:
                    print("\nSelected Order Item Type is not available. Repeat entering...")
                else:
                    print("\nOrder Item Type " + colored(order_type, "green") + " is selected")
                    order_types.append(order_type)
                    break

        # --------------------------Select-Number-Of-Orders-------------------------------------------------------

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
            print("\n" + colored("█" * 50, "white") + f" Test # {i + 1} : Started " + colored("█" * 50, "white") + "\n")

            while True:
                try:
                    print(colored("\n" + "-" * 50 + " ADDING ORDER" + "-" * 50 + "\n", "yellow"))
                    self.atom.CRS.order_queue.add_order_with_scan_first_flow(order_types=order_types)

                    # Edit OITs
                    for j in range(1, int(n_of_oits) + 1):
                        self.lib.CRS.order_summary.click_edit_icon_by_row_index(j)
                        self.lib.CRS.order_entry.wait_order_item_tab_displayed()
                        self.lib.CRS.order_entry.save_entered_doc_type()
                        self.lib.required_fields.crs_fill_required_fields()
                        self.lib.CRS.order_entry.click_add_to_order()
                        self.lib.CRS.order_summary.verify_status_by_row_index("Reviewed", j)

                    if action in ["2", "3", "4"]:
                        print(colored("\n" + "-" * 50 + " ORDER FINALIZATION" + "-" * 50 + "\n", "yellow"))
                        self.atom.CRS.add_payment.finalize_order()
                        self.data["order_number"] = self.lib.CRS.order_header.get_order_number()
                        # print(self.data["order_number"])

                        if action in ["3", "4"] and int(n_of_oits) == 1:
                            # should be config file with indexing_step = True
                            print(colored("\n" + "-" * 50 + " ORDER INDEXING" + "-" * 50 + "\n", "yellow"))
                            self.lib.CRS.order_item_type.indexing_step()

                            if action == "4":
                                print(colored("\n" + "-" * 50 + " ORDER VERIFICATION" + "-" * 50 + "\n", "yellow"))
                                # should be config file with verification_step = True
                                self.lib.CRS.order_item_type.verification_step()

                    print("\n" + colored("█" * 50, "green") + f" Test # {i + 1} : Finished " + colored("█" * 50, "green") + "\n")

                    break
                except Exception as msg:
                    print(colored(msg, "cyan"))
                    print(colored("\n" + "█" * 50 + " TEST IS NOT FINISHED " + "█" * 50 + "\n", "red"))
                    continue







if __name__ == '__main__':
    # env = input("Enter env > ")
    # env = str(env).lower().strip()
    run_test(__file__, env="qa_arlington")
