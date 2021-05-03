import requests
import os 

redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
   raise Exception()

baseurl = f"http://{redis_ip}:5000"
# Reset data
print("Reseting data")
response = requests.get(url=baseurl + "/")

print("\nGetting satellite named spaceBEE 1")
response = requests.get(url=baseurl + "/name/spaceBEE%201")
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
response = requests.get(url=baseurl + "/orbits/Elliptical")
print(response.status_code)
print(response.json())
print(response.headers)

# /orbital_elements/apogee/<apogee>
# 300

# /orbital_elements/perigee/<perigee>
# 300

# /orbital_elements/eccentricity/<ecc>
# .0008

# /orbital_elements/inclination/<inc>
# 97.80

print("\nGetting satellites launuched between 01/01/2020 02/02/2020")
response = requests.get(url=baseurl + "/launch/date/01-01-2020/12-01-20")
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

# print("\nGetting satellites with launch site at Cape Canaveral")
# response = requests.get(url=baseurl + "/launch/site/Cape%20Canaveral")
# print(response.status_code)
# print(response.json())
# print(response.headers)


# print("\nGetting satellites with Falcon 9 launch vehicle")
# response = requests.get(url=baseurl + "/launch/vehicle/Falcon%209")
# print(response.status_code)
# print(response.json())
# print(response.headers)

# /launch/recent/
# return 5 most recent

# GET, DELETE /satellite/<uuid>

# POST: /satellite/

print("\nGetting total count of orbit types in USA satellites")
response = requests.get(url=baseurl + "/total/USA")
print(response.status_code)
print(response.json())
print(response.headers)