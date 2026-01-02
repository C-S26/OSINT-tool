from helpers.utils import *
from lib.colors import *
from helpers.utils import Requests
import json, random

async def url(ip):
        with open("useragents.txt", "r") as user_file:
                user = user_file.read().split('\n')

        url = "https://ipinfo.io/{}/json".format(ip)

        response = await Requests(url, headers={"User-Agent": random.choice(user)}).sender()

        return json.loads(response.text)

async def look(ip):
        track = await url(ip)

    # If API fails or location is missing
        if not track or 'loc' not in track:
          return track, None, None

        try: 
           lat, lon = track['loc'].split(',')
        except ValueError:
           return track, None, None

        hostname = track.get('hostname')
        org = track.get('org')

        coord = (lat, lon)
        latlong = f"{lat},{lon}"

        return track, coord, latlong




        output = f"""{CYAN}\rIpinfo{WHITE}\r
└──Hostname := {hostname}
└──A.S. := {org}
└──Country := {track['country']}
   └──Region ~= {track['region']}
      └──City ~= {track['city']}"""
        latlong = f"""\r{"-"*55}

[🟢] Latitude ~= {lat}
[🟢] Longitude ~= {long}\n"""
        return output, track['city'], latlong

async def coordinates(ip):
        track = await url(ip)

        coordinates = {track['loc']}
        lat = str(coordinates).split(",")[0].replace("{", "").replace("'", "")
        long = str(coordinates).split(",")[1].replace("}", "").replace("'", "")

        return lat, long
