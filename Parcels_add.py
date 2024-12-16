from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test
from termcolor import colored
import os

description = """
                  Performance test with ParcelIds 
              """

tags = ['regression']


class test(TestParent):

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        os.system('color')
        os.system('cls')

        self.data["order_number"] = '20241029000001'

        self.atom.CRS.general.go_to_crs()
        self.actions.wait_for_element_displayed(self.pages.CRS.order_queue.lbl_login_user, timeout=60)
        self.atom.CRS.order_search.search_order_by_order_number()
        self.lib.CRS.order_search.verify_order_present_in_result(self.data["order_number"])
        self.lib.CRS.order_search.click_edit_icon(self.data["order_number"])
        # if OIT is still in workflow, click on "in workflow" popup
        self.lib.CRS.order_search.click_pup_in_workflow_btn_yes()

        icn_edit_order = self.lib.general_helper.make_locator(self.pages.CRS.order_finalization.icn_edit_order, 1)
        self.lib.general_helper.find_and_click(icn_edit_order)

        txt_parcel_id = (
            "xpath", "//*[@id='parcels-container']/div[2]/div/section[%s]//input[contains(@placeholder, 'Parcel ID')]",
            "ParcelId")
        lnk_new_parcel_id = (
            "xpath", "//*[@id='parcels-container']//a[contains(text(), 'New Parcel ID')]", "New Parcel link")

        self.actions.wait_for_element_displayed(lnk_new_parcel_id, timeout=2000)
        self.actions.focus_element(lnk_new_parcel_id)
        self.lib.general_helper.scroll_and_click(lnk_new_parcel_id)

        # ------------------------------------------------------

        self.lib.db.connect_to_db(use_vpn=True)
        self.lib.db.connection_test()
        query = '''
                            SELECT parcel_id
                            FROM VG51013.appraisal
                            ORDER BY parcel_id
                            OFFSET 102 ROWS FETCH NEXT 50 ROWS ONLY
                       '''
        self.lib.db.cursor.execute(query)
        parcels = self.lib.db.cursor.fetchall()
        parcel_ids = [parcel[0] for parcel in parcels]
        # print(parcel_ids)

        # ------------------------------------------------------

        row = 103

        for parcel_id in parcel_ids:
            input_parcel_id = self.lib.general_helper.make_locator(txt_parcel_id, row)
            self.actions.wait_for_element_displayed(input_parcel_id)
            self.actions.focus_element(input_parcel_id)
            self.actions.send_keys(input_parcel_id, parcel_id + self.keys.TAB)
            self.lib.general_helper.wait_for_spinner()
            self.actions.focus_element(lnk_new_parcel_id)
            self.lib.general_helper.scroll_and_click(lnk_new_parcel_id)
            # self.actions.click(lnk_new_parcel_id)
            print("\nTest # " + str(row) + " is passed")
            row += 1




        input('Press key...')


if __name__ == '__main__':
    run_test(__file__, env="qa_arlington")
