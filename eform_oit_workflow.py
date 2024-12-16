"""smoke test"""
import time
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test
from termcolor import colored
import os

description = """
    1. Go to Portal, submit an e-form order item, get the order number
    2. Go to CRS, find the order number, review OI and finalize the order
    3. Scan and map, index, verify Order
    4. Go To Order Search, find the order and check Order Status
    5. Void the order
    """
os.system('color')
os.system('cls')

tags = ['regression']


class test(TestParent):

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        if self.data.OIT in self.data['config'].get_order_types():
            print("\nOrder Actions:\n")
            print("1. Submit")
            print("2. Finalize")
            while True:
                action = input("\nEnter 1-2 > ")
                action = action.strip().lower()
                if not action:
                    action = "1"
                    print("\nAction " + colored("Submit", "green") + " is selected by default\n")
                    break
                elif action not in ["1", "2"]:
                    print("\nAction is not available. Repeat entering...")
                else:
                    match action:
                        case "1":
                            print("\nAction " + colored("Submit", "green") + " is selected")
                        case "2":
                            print("\nAction " + colored("Finalize", "green") + " is selected")

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
                print("\n" + colored("█" * 50, "white") + f" Test # {i + 1} : Started " + colored("█" * 50,
                                                                                                  "white") + "\n")

                while True:
                    try:
                        print(colored("\n" + "-" * 50 + " SUBMIT E-FORM" + "-" * 50 + "\n", "yellow"))
                        # atom - create and submit e-form
                        self.atom.EForm.general.create_and_submit_eform()
                        if action == "2":
                            print(colored("\n" + "-" * 50 + " ORDER FINALIZATION" + "-" * 50 + "\n", "yellow"))
                            # find and open the order in CRS
                            self.atom.CRS.general.go_to_crs()
                            self.lib.CRS.crs.click_running_man()
                            self.actions.wait_for_element_displayed(self.pages.CRS.order_summary.lbl_order_number)
                            # review and process to archive
                            self.atom.CRS.order_summary.edit_oit()
                            # get usertype
                            self.data["user_type"] = self.data['config'].order_header_fill(f'{self.data.orderheader}.type')
                            self.atom.CRS.add_payment.finalize_and_process_to_archive()
                            # edit order from Order Search and void
                            self.lib.CRS.order_search.click_edit_icon(self.data["order_number"])
                            max_ = time.time() + 3
                            while time.time() < max_:
                                if 'Warning' in self.actions.get_browser().page_source:
                                    self.lib.CRS.order_search.click_pup_in_workflow_btn_yes()
                                    break
                                else:
                                    self.actions.wait(0.5)
                            self.atom.CRS.order_finalization.void_order()
                            # check order status is voided
                            self.lib.CRS.crs.go_to_order_search()
                            self.atom.CRS.order_search.search_order_by_order_number()
                            self.lib.CRS.order_search.verify_order_present_in_result(self.data["order_number"])
                            self.lib.CRS.order_search.verify_order_status_voided()
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
