import sys
import json
import subprocess
import pymssql
from Data import IP
from Data import Password
from Data import QA1_DB
from Data import UAT_DB
import jsbeautifier
from termcolor import colored
import os

# To get the ANSI codes working on windows for support color fonts
os.system('color')


if __name__ == "__main__":
    with open(r"D:\Auto\kofile-automation\Kofile\projects\Kofile\environments.json", "r") as file:
        data = json.load(file)

    if "qa_dev" not in data:
        with open(r"D:\Auto\kofile-automation\Kofile\projects\Kofile\tests\my_test\Data\QA_DEV.json", "r") as file:
            data["qa_dev"] = json.load(file)
            print("\n<qa_dev> environment is added")

    envs = []

    for key in data.keys():
        envs.append(key)

    print("\n" + "-" * 15 + "The following environments are available: " + "-" * 15 + "\n")

    temp = []
    i = 0

    for env in sorted(envs):
        temp.append(str(env).split("_")[0])
        index = str(env).split("_")[0]
        if i != 0:
            if index != temp[i - 1]:
                print("")
        print(env)
        i += 1

    print("\n" + "-" * 75 + "\n")

    while True:
        e = input("\nSelect environment > ")
        e = e.lower().strip()
        if not e:
            e = "qa_dev"
            print("\nEnvironment " + colored("qa_dev", "green") + " is selected by default")
            break
        elif e not in envs:
            print("\nEnvironment is not available. Repeat entering...")
        else:
            print("\nEnvironment " + colored(e, "green") + " is selected")
            break

    # print(json.dumps(data, indent=4))

    for env, env_data in data.items():
        if env == e:
            e = e.split("_")[0]
            code = env_data["code"]

            if e == "qa":
                # Connect to VPN
                subprocess.call([r"D:\Dropbox\Kofile\dropbox_scripts\Bat\QA1_VPN_On.bat"])
                # Connect to DB
                conn = pymssql.connect(server=QA1_DB.host, user=QA1_DB.user, password=QA1_DB.password,
                                       database=QA1_DB.database)
                cursor = conn.cursor()

            if e == "uat":

                # Connect to VPN
                subprocess.call([r"D:\Dropbox\Kofile\dropbox_scripts\Bat\UAT_VPN_On.bat"])

                # Connect to DB
                conn = pymssql.connect(server=UAT_DB.host, user=UAT_DB.user, password=UAT_DB.password,
                                       database=UAT_DB.database)
                cursor = conn.cursor()

            if e in ["qa", "uat"]:

                # Select workstation_ip via IP address------------------------------------------------------------------
                cursor.execute(f"select WORK_STATION_ID from VG" + str(code) +
                               f".WORK_STATION where WORK_STATION_ADDRESS = '{IP.ip}' "
                               f"AND WORK_STATION_DESC != 'Guest account'")
                result = cursor.fetchone()
                workstation_id = result[0]

                # print(workstation_id)

                # Select scanner_id via workstation_id------------------------------------------------------------------
                cursor.execute(
                    "select scanner_id from VG" + str(code) + ".SCANNER_WORKSTATION where workstation_id = "
                    + str(workstation_id))
                result = cursor.fetchone()
                scanner_id = result[0]

                # Select printer_id-------------------------------------------------------------------------------------
                cursor.execute(
                    "SELECT device_id FROM VG" + str(code) + ".device WHERE device_host_name LIKE '%artyom.shchokin%' "
                                                             "AND DEVICE_TYPE_ID = 2"
                )
                result = cursor.fetchone()
                print_id = result[0]

                # Select user_first-------------------------------------------------------------------------------------
                cursor.execute(
                    "SELECT ADUSER_FIRSTNAME FROM VG" + str(code) + ".ad_user "
                                                                    "WHERE aduser_domain LIKE '%artyom.shchokin%'"
                )
                result = cursor.fetchone()
                user_first = result[0]

                # Select user_last--------------------------------------------------------------------------------------
                cursor.execute(
                    "SELECT ADUSER_LASTNAME FROM VG" + str(code) + ".ad_user "
                                                                   "WHERE aduser_domain LIKE '%artyom.shchokin%'"
                )
                result = cursor.fetchone()
                user_last = result[0]

            password = Password.password

            # print(json.dumps(env_data, indent=4))
            for k, v in env_data.items():
                match k:
                    case "scanned_id":
                        if e == "prod":
                            scanner_id = 70
                        print("-" * 100)
                        print(k + " | old value : " + str(v), end="")
                        print(" | new value : " + str(scanner_id))
                        if v == scanner_id:
                            print("scanner_id is actual.")
                        else:
                            print("scanner_id is updated")
                            env_data[k] = scanner_id
                    case "printer_id":
                        # if e == "prod":
                        #     print_id =
                        print("-" * 100)
                        print(k + " | old value : " + str(v), end="")
                        print(" | new value : " + str(print_id))
                        if v == print_id:
                            print("print_id is actual.")
                        else:
                            print("print_id is updated")
                            env_data[k] = print_id
                    case "user":
                        print("-" * 100)
                        print(k + " | old value : " + str(v[0]), end="")
                        print(" | new value : artyom.shchokin")
                        if v[0] == "artyom.shchokin":
                            print("user_name is actual.")
                        else:
                            print("user_name is updated")
                            env_data[k][0] = "artyom.shchokin"
                    case "user_first":
                        if e == "prod":
                            user_first = "Artyom"
                        print("-" * 100)
                        print(k + " | old value : " + str(v[0]), end="")
                        print(" | new value : " + str(user_first))
                        if v[0] == user_first:
                            print("user_first is actual.")
                        else:
                            print("user_first is updated")
                            env_data[k][0] = user_first
                    case "user_last":
                        if e == "prod":
                            user_last = "Shchokin"
                        print("-" * 100)
                        print(k + " | old value : " + str(v[0]), end="")
                        print(" | new value : " + str(user_last))
                        if v[0] == user_last:
                            print("user_first is actual.")
                        else:
                            print("user_first is updated")
                            env_data[k][0] = user_last
                    case "password":
                        print("-" * 100)
                        print(k + " | old value : " + str(v[0]), end="")
                        print(" | new value : " + str(password))
                        if v[0] == password:
                            print("password is actual.")
                        else:
                            print("password is updated")
                            env_data[k][0] = password
            # Disconnect VPN according to environment
            # if e == "qa":
            #     subprocess.call(["rasdial", "VPN Connection QA1", "/disconnect"])
            # if e == "uat":
            #     subprocess.call(["rasdial", "VPN Connection UAT", "/disconnect"])
            # if e == "prod":
            #     pass
            # print(json.dumps(env_data, indent=4))

    # print(json.dumps(data, indent=4))

    with open(r"D:\Auto\kofile-automation\Kofile\projects\Kofile\environments.json", "w") as file:

        options = jsbeautifier.default_options()
        options.indent_size = 2
        # print(jsbeautifier.beautify(json.dumps(data), options))
        file.write(jsbeautifier.beautify(json.dumps(data), options))

        # json.dump(data, file, indent=2)

    sys.exit(0)
