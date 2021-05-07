import requests
import os 

ex_post = {
   "A": "SierraSat",
   "B": "SierraSat",
   "C": "USA",
   "D": "USA",
   "E": "Sierra",
   "F": "Kyle Sierra",
   "G": "Technology Development",
   "H": "Earth observation",
   "I": "LEO",
   "J": "Polar",
   "K": "50",
   "L": "600",
   "M": "600",
   "N": "0",
   "O": "50",
   "P": "1000",
   "Q": "100",
   "R": "100",
   "S": "10",
   "T": "09-05-2021",
   "U": "21",
   "V": "SierraAndKyleINC",
   "W": "USA",
   "X": "Austin, TX",
   "Y": "Falcon 9",
   "Z": "2021-000S",
   "AA": "00000",
   "AB": "",
   "AD": "",
   "AE": "",
   "AF": "",
   "AG": "",
   "AH": "",
   "AI": "",
   "AJ": "",
   "AK": ""
}

update_space_bee = {
   "A": "SpaceBEE 10",
   "B": "SpaceBEE 10",
   "C": "NR (12/20)",
   "D": "USA",
   "E": "Swarm Technologies",
   "F": "Commercial",
   "G": "Communications",
   "H": "",
   "I": "LEO",
   "J": "Sun-Synchronous",
   "K": "0",
   "L": "533",
   "M": "535",
   "N": "0.00014484356894553882",
   "O": "97.5",
   "P": "94.5",
   "Q": "2",
   "R": "",
   "S": "",
   "T": "02-09-2020",
   "U": "",
   "V": "Swarm Technologies",
   "W": "USA",
   "X": "Guiana Space Center",
   "Y": "Vega",
   "Z": "2020-061AK",
   "AA": "46305",
   "AB": "",
   "AD": "JMSatcat/12_20",
   "AE": "https://spaceflightnow.com/2020/09/03/vega-rocket-deploys-53-satellites-on-successful-return-to-flight-mission/",
   "AF": "",
   "AG": "https://planet4589.org/space/gcat/data/cat/satcat.html",
   "AH": "https://spacenews.com/swarm-launch-with-exolaunch/",
   "AI": "",
   "AJ": "",
   "AK": "",
   "uid": "2749da22-22a5-4cd4-bbc1-082aef997605"
}

flask_ip = os.environ.get('FLASK_IP')
if not flask_ip:
   raise Exception()
# redis_ip = "localhost"

baseurl = f"http://{flask_ip}:5000"
# Reset data
print("Reseting data")
response = requests.get(url=baseurl + "/")

print("\nGetting satellite named SpaceBEE 10")
response = requests.get(url=baseurl + "/name/SpaceBEE%2010")
print(response.status_code)
print(response.json())
print(response.headers)

print("\nGetting satellites with Swarm Technologies operator")
response = requests.get(url=baseurl + "/operator/Swarm%20Technologies")
print(response.status_code)
print(response.json())
print(response.headers)

print("\nGetting satellites from Turkey")
response = requests.get(url=baseurl + "/country/Turkey")
print(response.status_code)
print(response.json())
print(response.headers)

print("\nGetting satellites with elliptical orbits")
response = requests.get(url=baseurl + "/orbit/Elliptical")
print(response.status_code)
print(response.json())
print(response.headers)

print("\nGetting satellites launuched between 01/01/2020 02/02/2020")
response = requests.get(url=baseurl + "/launch/date/01-01-2020/02-02-2020")
print(response.status_code)
print(response.json())
print(response.headers)

print("\nGetting satellites contracted by Boeing")
response = requests.get(url=baseurl + "/contractor/Boeing")
print(response.status_code)
print(response.json())
print(response.headers)

print("\nGetting satellites with lifetime exceeding 25 year guideline")
response = requests.get(url=baseurl + "/lifetime/25")
print(response.status_code)
print(response.json())
print(response.headers)

print("\nGetting satellites with launch site at Cape Canaveral")
response = requests.get(url=baseurl + "/launch/site/Cape%20Canaveral")
print(response.status_code)
print(response.json())
print(response.headers)

print("\nGetting satellites with Falcon 9 launch vehicle")
response = requests.get(url=baseurl + "/launch/vehicle/Falcon%209")
print(response.status_code)
print(response.json())
print(response.headers)

# GET, DELETE /satellite/<uuid>
print("\nGetting satellite with uuid of 1857f0d9-1531-4385-84f7-ae57aadf6d70")
response = requests.get(url=baseurl + "/satellite/1857f0d9-1531-4385-84f7-ae57aadf6d70")
print(response.status_code)
print(response.json())
print(response.headers)

print("\nDeleting satellite with uuid of 1857f0d9-1531-4385-84f7-ae57aadf6d70")
response = requests.delete(url=baseurl + "/satellite/1857f0d9-1531-4385-84f7-ae57aadf6d70")
print(response.status_code)

print("\nGetting satellite with uuid of 1857f0d9-1531-4385-84f7-ae57aadf6d70 again to confirm deletion")
response = requests.get(url=baseurl + "/satellite/1857f0d9-1531-4385-84f7-ae57aadf6d70")
print(response.status_code)
print(response.json())
print(response.headers)

print("\nPosting new satellite")
response = requests.post(url=baseurl + "/satellite", data = ex_post)
print(response.status_code)

print("\nLets get our new satellite")
response = requests.get(url=baseurl + "/name/SierraSat")
print(response.status_code)
print(response.json())
print(response.headers)

print("\nLets update the space BEE 10 satellite with an of 2749da22-22a5-4cd4-bbc1-082aef997605 with a new source: https://spacenews.com/swarm-launch-with-exolaunch/")
response = requests.post(url=baseurl + "/satellite/2749da22-22a5-4cd4-bbc1-082aef997605", data = update_space_bee)
print(response.status_code)

print("\nLets see the update")
response = requests.get(url=baseurl + "/satellite/2749da22-22a5-4cd4-bbc1-082aef997605")
print(response.status_code)
print(response.json())
print(response.headers)

print("\nGetting total count of orbit types in USA satellites")
response = requests.get(url=baseurl + "/total/USA")
print(response.status_code)
print(response.json())
print(response.headers)
