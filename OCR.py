"""Test - OCR Birth Workflow"""
from projects.Kofile.Lib.test_parent import TestParent
from datetime import datetime
from runner import run_test
from termcolor import colored
import os
import xml.etree.ElementTree as et
from os.path import join
from distutils.dir_util import copy_tree

description = """Create OCR orders, find the last submitted OCR order, process to Archive and find in Clerk Search"""

tags = ["48999_location_2"]


class test(TestParent):                                                                                 # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):

        code = self.data['env']['code']
        env = self.actions.execution.data.get("env").get("name")
        env_name = str(env).split('_')[0]
        if env_name == 'qa':
            web_api_base_url = "https://crs.qa-1.kofile.systems/"
            content_service_web_api_base_url = "http://content.qa.kofile.com/"
        else:
            web_api_base_url = "http://crs.uat-1.kofile.systems/"
            content_service_web_api_base_url = "http://content.uat-1.kofile.systems/"

        device_service_path = 'C:\\QA_Test\\CRS_Agent'

        tree = et.parse(join(device_service_path, "AppSettings.config"))
        root = tree.getroot()
        for child in root:
            if child.get('key') == 'TenantCode':
                print(child.get('value'))
                print(code)
                if child.get('value') != code:
                    child.set('value', code)
                    print("\nTenant Code is updated in AppSettings.config")
                else:
                    print("\nTenant Code is actual in AppSettings.config")
            if child.get('key') == 'WebAPIBaseURL':
                if child.get('value') != web_api_base_url:
                    child.set('value', web_api_base_url)
                    print("\nWebAPIBaseURL is updated in AppSettings.config")
                else:
                    print("\nWebAPIBaseURL is actual in AppSettings.config")
            if child.get('key') == 'ContentServiceWebApiBaseUrl':
                if child.get('value') != content_service_web_api_base_url:
                    child.set('value', content_service_web_api_base_url)
                    print("\nContentServiceWebApiBaseUrl is updated in AppSettings.config")
                else:
                    print("\nContentServiceWebApiBaseUrl is actual in AppSettings.config")

        tree.write(join(device_service_path, "AppSettings.config"), encoding='utf-8', xml_declaration=True)

        # input('press any key...')

        # --------------------------Select-Number-Of-Orders------------------------------------

        oit = str(self.data["OIT"]).lower()
        print('-'*40 + oit + '-'*40)

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

        test_config = self.lib.data_helper.test_config(oit=self.data.get("OIT"))
        dept_id = test_config.get("dept_id")
        doc_number = str(datetime.now().timestamp())[:-7]  # unique number
        # create a Birth/Death OCR order
        self.atom.CRS.indexing.OCR_Image_Upload(birth_count=int(n_of_orders) if "birth" in oit else 0,
                                                death_count=int(n_of_orders) if "death" in oit else 0)
        # wait for OCR service to create the order and get the last submitted OCR order number from DB
        self.actions.wait(20)
        self.data["order_number"] = self.lib.db_with_vpn.get_last_ocr_number_by_host_ip()
        self.actions.step(f"OCR order number is {self.data['order_number']}")


if __name__ == '__main__':
    run_test(__file__)
