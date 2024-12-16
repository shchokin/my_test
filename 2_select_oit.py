from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test
import subprocess
import csv
from termcolor import colored
import os

# To get the ANSI codes working on windows for support color fonts
os.system('color')
os.system('cls')

description = """
                   1. Select OIT per Environment
                   2. Update CSV data file
                   3. Execute 'Order Creation' bat file
              """


class test(TestParent):

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        """
        Pre-conditions: no
        Post-conditions: Order is processed from Order Queue to Archive
        """

        print("-" * 100)

        path_origin = r"D:\Auto\kofile-automation\Kofile\projects\Kofile\tests\my_test\origin.txt"
        with open(path_origin, 'r') as f:
            origin = f.readline()

        if self.data.env.code == '48000':

            if str(origin).lower() == "crs":
                path = "projects\\Kofile\\tests\\my_test\\crs_oit_workflow_48000.csv"
            else:
                path = "projects\\Kofile\\tests\\my_test\\eform_oit_workflow_48000.csv"
        else:
            if str(origin).lower() == "crs":
                path = "projects\\Kofile\\tests\\my_test\\crs_oit_workflow.csv"
            else:
                path = "projects\\Kofile\\tests\\my_test\\eform_oit_workflow.csv"

        print("\nThe following OITs are configured for current tenant: \n")

        i = 0

        for key in sorted(self.data["config"].config_file.OITs.keys()):

            if str(origin).lower() == "crs":
                if str(key).split("_")[0] != "Eform" and str(key).split("_")[0] != "Export":
                    print('\t' + key)
            else:
                if str(key).split("_")[0] == "Eform":
                    print('\t' + key)

            '''
            if str(key).split("_")[0] != "Eform" and i == 1:
                print("")
                i += 1
            if i == 0 and str(key).split("_")[0] == "Eform":
                print("")
                i += 1
            print('\t' + key)
            '''

        oit = input("\nSelect OIT from the above list > ")
        oit = str(oit).strip()

        if oit not in self.data["config"].config_file.OITs.keys() and oit != "":
            print("\nEntered OIT is incorrect.")
        else:
            if oit == "":
                if self.data.env.code == '48999':
                    oit = "Real_Property_Recordings_W_Page"
                else:
                    oit = "RP_Recordings"
            print("\nOIT " + colored(oit, "green") + " is selected")

            # option = input("\nEnter option (account, email, guest)  > ")
            #
            # if option not in ("account", "email", "guest") and option != "":
            #     print("\nEntered option is incorrect.")
            # else:
            #     if option == "":
            #         option = "email"
            #     print(f"\nOptin " + colored(option, "green") + " is selected")

            # Update CSV
            option = "email"
            with open(path, mode='w', newline='') as file:
                data = csv.writer(file, delimiter=',')
                data.writerows([['OIT', 'orderheader'],
                                [f'{oit}'.strip(), f'{option}'.strip()]])

            # with open(path, 'r') as f:
            #     csv_reader = csv.reader(f, delimiter=',')
            #     page_text = "\n".join([" ".join(i) for i in csv_reader])
            # print(page_text)

            print("\nCSV file is updated successfully..")

            if str(origin).lower() == "crs":
                subprocess.call([r"D:\Dropbox\Kofile\dropbox_scripts\Bat\QA1_my_test_crs_oit_workflow.bat"])
            else:
                subprocess.call([r"D:\Dropbox\Kofile\dropbox_scripts\Bat\QA1_my_test_eform_oit_workflow.bat"])

            # print(self.data)


if __name__ == '__main__':
    run_test(__file__, env="qa_ref")
