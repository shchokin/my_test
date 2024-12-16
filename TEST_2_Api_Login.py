from golem import actions
from runner import run_test
import requests
from requests_ntlm import HttpNtlmAuth
import re
from urllib.parse import urlencode


def test(data):

    env = 69999

    auth_url =  "http://%s:%s@10.11.36.112:8001/%s/?ReturnUrl=http://crs.qa-1.kofile.systems/%s/Account/ReturnClaim&amp;Referrer="
    url = auth_url.replace('%s:%s@', '').replace('%s', f'{env}').replace('&amp;Referrer=', '')
    print(url)  # http://10.11.36.112:8001/69999/?ReturnUrl=http://crs.qa-1.kofile.systems/69999/Account/ReturnClaim

    session = requests.session()
    session.auth = HttpNtlmAuth('artyom.shchokin', '230885ShArVl33')

    result = session.get(url, allow_redirects=False, timeout=30)

    code = result.status_code
    print('Response Status Code : ' + str(code))

    content = result.text
    print('\nContent:')
    print(content)

    token = re.search(r"(?<='saml' value=').*?(</Assertion>)", content).group(0)
    print('\nToken:')
    print(token)

    agent = re.search(r"(?<='agentname' value=').*?(?='><input)", content).group(0)
    print('\nAgent:')
    print(agent)

    payload = {"saml": token, "agentname": agent, "targetUrl": ""}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    url2 = url.split('ReturnUrl=')[1].split("&")[0]
    print(url2)  # http://crs.qa-1.kofile.systems/69999/Account/ReturnClaim
    result2 = session.post(url2, data=urlencode(payload), headers=headers, verify=False)

    code2 = result.status_code
    print('Response Status Code2 : ' + str(code2))

    cookies = result2.request.headers['Cookie']
    print('\nCookies:')
    print(cookies)

    cookies = {'ASP.NET_SessionId': cookies.split("=")[-1]}
    print(cookies)

    #  -------------------------

    url3 = "https://crs.qa-1.kofile.systems/69999/api/Order/GetQueuesItemCounts"

    session.cookies.update(cookies)
    result3 = session.get(url3)

    code3 = result3.status_code
    print('Response Status Code3 : ' + str(code3))

    content3 = result3.text
    print('\nContent3:')
    print(content3)



    # session.cookies.update()
    # response = session.get(url)

    # input('Press key...')

if __name__ == '__main__':
    run_test(__file__)