from golem import actions
from runner import run_test
import requests


def test(data):

    env = "48999"
    user = "artyom.shchokin"
    password = "230885ShArVl33"
    url = ("http://%s:%s@10.11.36.112:8001/%s/?ReturnUrl="
           "http://crs.qa-1.kofile.systems/%s/Account/ReturnClaim&amp;Referrer=") % (user, password, env, env)

    actions.get(url)

    cookies = actions.get_cookie("ASP.NET_SessionId") .get("value")

    print(cookies)

    # -------------------------------------------------------------------

    input('Press key...')


if __name__ == '__main__':
    run_test(__file__)