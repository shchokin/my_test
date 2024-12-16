import json
import subprocess
import re
from termcolor import colored
import os

# To get the ANSI codes working on windows for support color fonts
os.system('color')


# -------------------------------Update-environments.json-file-------------------------------

path_bat_0 = r"D:\Dropbox\Kofile\dropbox_scripts\Bat\QA1_my_test\0_update_env.bat"

while True:
    answer = input("\nDo you want update environments.json file ? [y / n] > ")
    if answer.lower() == 'n' or not answer:
        print("\nOption "
              "" + colored("n", "green") + " is selected")
        break
    elif answer.lower() == 'y':
        print("\nOption " + colored("y", "green") + " is selected")
        subprocess.call([path_bat_0])
        input("\nPress " + colored("Enter", "green") + " to continue...")
        os.system('cls')
        break
    else:
        print("\nIncorrect value. Should be [y / n]. Repeat entering...")

# -------------------------------------------------------------------------------------------

envs = []

path_envs = ""

with open('D:\\Auto\\kofile-automation\\Kofile\\projects\\Kofile\\environments.json') as f:
    data = json.load(f)
for key in data.keys():
    envs.append(key)

print("\n" + "-" * 15 + "The following environments are available: " + "-" * 15 + "\n")

temp = []
i = 0

for env in sorted(envs):
    temp.append(str(env).split("_")[0])
    index = str(env).split("_")[0]
    if i != 0:
        if index != temp[i-1]:
            print("")
    print(env)
    i += 1

print("\n" + "-" * 75 + "\n")

while True:
    env = input("\nSelect environment > ")
    env = env.lower().strip()
    if not env:
        env = "qa_48999_loc_2"
        print("\nEnvironment " + colored("qa_48999_loc_2", "green") + " is selected by default\n")
        break
    elif env not in envs:
        print("\nEnvironment is not available. Repeat entering...")
    else:
        print("\nEnvironment " + colored(env, "green") + " is selected")
        break

# ---------------------------------------------------------------------------------

print("\n" + "-" * 18 + "The following origins are available: " + "-" * 18 + "\n")
print("\nCRS")
print("Eforms")
print("Scan_First")
print("Search_Copy")
print("Search_Certified_Copy")
print("OCR")

while True:
    origin = input("\nSelect origin  > ")
    origin = origin.strip().lower()
    if not origin:
        origin = "crs"
        print("\nOrigin " + colored("crs", "green") + " is selected by default\n")
        break
    elif origin not in ("crs", "eforms", "scan_first", "search_copy", "search_certified_copy", "ocr"):
        print("\nOrigin is not available. Repeat entering...")
    else:
        print("\nOrigin " + colored(origin, "green") + " is selected")
        break

# ---------------------------------------------------------------------------------

path_bat_1 = r"D:\Dropbox\Kofile\dropbox_scripts\Bat\QA1_my_test\2_select_oit.bat"

with open(path_bat_1, 'r') as f:
    old_data = f.read()

for line in old_data.split("\n"):
    if "-e" in line:
        new_line = re.sub(r"-e \w+", f"-e {env}", line)
        break

new_data = old_data.replace(line, new_line)

with open(path_bat_1, 'w') as f:
    f.write(new_data)

# ----------------------------------------------------------------------------------

if str(origin).lower() == "crs":
    path_bat_2 = r"D:\Dropbox\Kofile\dropbox_scripts\Bat\QA1_my_test_crs_oit_workflow.bat"
elif str(origin).lower() == "eforms":
    path_bat_2 = r"D:\Dropbox\Kofile\dropbox_scripts\Bat\QA1_my_test_eform_oit_workflow.bat"
elif str(origin).lower() == "search_copy":
    path_bat_2 = r"D:\Dropbox\Kofile\dropbox_scripts\Bat\QA1_my_test_copy.bat"
elif str(origin).lower() == "search_certified_copy":
    path_bat_2 = r"D:\Dropbox\Kofile\dropbox_scripts\Bat\QA1_my_test_certified_copy.bat"
elif str(origin).lower() == "ocr":
    path_bat_2 = r"D:\Dropbox\Kofile\dropbox_scripts\Bat\QA1_my_test_ocr.bat"
else:
    path_bat_2 = r"D:\Dropbox\Kofile\dropbox_scripts\Bat\QA1_my_test_scan_first.bat"

with open(path_bat_2, 'r') as f:
    old_data = f.read()

for line in old_data.split("\n"):
    if "-e" in line:
        new_line = re.sub(r"-e \w+", f"-e {env}", line)
        break

new_data = old_data.replace(line, new_line)

with open(path_bat_2, 'w') as f:
    f.write(new_data)

# ----------------------------------------------------------------------------

path_origin = r"D:\Auto\kofile-automation\Kofile\projects\Kofile\tests\my_test\origin.txt"
with open(path_origin, 'w') as f:
    f.write(origin)


if str(origin).lower() in ("scan_first", "search_copy", "search_certified_copy", "ocr"):
    subprocess.call([path_bat_2])
else:
    subprocess.call([path_bat_1])  # crs/eform -> 2_select_oit.bat

