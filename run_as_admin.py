import subprocess
from Data import QA1_DB
import pymssql


# Run As Admin

subprocess.run(r"D:\Work\VOLO\Tools\Scripts\Bat\QA1_VPN_On.bat", shell=True, check=True)


conn = pymssql.connect(server=QA1_DB.host,
                       user=QA1_DB.user,
                       password=QA1_DB.password,
                       database=QA1_DB.database
                       )

cursor = conn.cursor()

print("\n\t\t\tAll available tenants : \n")

cursor.execute("select tenant_code, tenant_desc  from VANGUARD.tenant order by tenant_desc asc")
result = cursor.fetchone()

codes = []

while result:
    print("code = {:<10} desc = {:<10}".format(result[0], result[1]))
    codes.append(int(result[0]))
    result = cursor.fetchone()

input("Press any key...")

# subprocess.run(r"D:\Work\VOLO\Tools\QA1_VPN\Bat\vpnoff.bat", shell=True, check=True)


