import random, json
from helpers.utils import Requests
from lib.colors import *

async def url(ip):
    with open("useragents.txt", "r") as user_file:
        user = user_file.read().splitlines()

    url = f"http://ipwho.is/{ip}"

    try:
        response = await Requests(
            url,
            headers={"User-Agent": random.choice(user)},
            timeout=10
        ).sender()

        if not response or not hasattr(response, "text"):
            return None

        data = json.loads(response.text)

        # ipwho.is returns success=false on failure
        if not data.get("success", True):
            return None

        return data

    except Exception:
        return None


async def lok(ip):
    read = await url(ip)

    if not isinstance(read, dict):
        return "", None

    continent = read.get('continent', 'N/A')
    country = read.get('country', 'N/A')
    region = read.get('region', 'N/A')
    city = read.get('city', 'N/A')

    connection = read.get('connection') or {}
    isp = connection.get('isp', 'N/A')

    output = f"""{CYAN}\rIpWhois{WHITE}\r
└──Continent := {continent}
   └──Country := {country}
      └──Region ~= {region}
         └──City ~= {city}

[{GREEN}+{WHITE}] I.S.P. := {isp}
"""

    return output, city

async def resolv_org(ip):
    read = await url(ip)

    if not isinstance(read, dict):
        return ""

    connection = read.get('connection') or {}
    domain = connection.get('domain')

    if not domain:
        return ""

    org = domain.split(".")[0].upper()
    return f"✔️ {org}\n"

