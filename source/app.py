from flask import Flask, request
import json
import redis
from datetime import datetime
from collections import Counter

app = Flask(__name__)
rd = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route('/name/<name>', methods=['GET'])
def get_name(name):   
   return json.dumps([launch for launch in get_data() if name == launch['A']])

@app.route('/operator/<operator>', methods=['GET'])
def get_operator(operator):   
   return json.dumps([launch for launch in get_data() if operator == launch['E']])

@app.route('/contractor/<contractor>', methods=['GET'])
def get_contractor(contractor):   
   return json.dumps([launch for launch in get_data() if contractor == launch['V']])

@app.route('/lifetime/<lifetime>', methods=['GET'])
def get_lifetime(lifetime):   
   return json.dumps([launch for launch in get_data() if lifetime <= launch['U']])

@app.route('/country/<country>', methods=['GET'])
def get_country(country):   
   return  json.dumps([launch for launch in get_data() if country == launch['D']])

@app.route('/orbit/<orbit>', methods=['GET'])
def get_orbit(orbit):   
   return  json.dumps([launch for launch in get_data() if orbit == launch['I']])

# @app.route('/orbital-elements/apogee/<apogee>', methods=['GET'])
# def get_apogee(apogee):   
#    return 0

# @app.route('/orbital-elements/perigee/<perigee>', methods=['GET'])
# def get_perigee(perigee):   
#    return 0

# @app.route('/orbital-elements/ecc/<ecc>', methods=['GET'])
# def get_ecc(ecc):   
#    return 0

# @app.route('/orbital-elements/inc/<inc>', methods=['GET'])
# def get_inc(inc):   
#    return 0

@app.route('/launch/date/<date1>/<date2>', methods=['GET'])
def get_launches_by_date(date1, date2):
   a = datetime.strptime(date1, "%d-%m-%Y")
   b = datetime.strptime(date2, "%d-%m-%Y")
   return json.dumps([launch for launch in get_data() if a <= datetime.strptime(launch['T'], "%d/%m/%Y") <= b])

@app.route('/launch/site/<site>', methods=['GET'])
def get_site(site):   
   return json.dumps([launch for launch in get_data() if site == launch['X']])

@app.route('/launch/vehicle/<vehicle>', methods=['GET'])
def get_vehicle(vehicle):   
   return json.dumps([launch for launch in get_data() if vehicle == launch['Y']])

@app.route('/launch/recent', methods=['GET'])
def get_recent():
   return sorted(get_data(), key = lambda i: i['T'])[0:4]

@app.route('/satellite/<key>', methods=['GET', 'DELETE', 'POST'])
def get_launch_by_id(key):
   if request.method == 'GET':
      bsat = rd.hgetall(key)
      sat = { y.decode('utf-8'): bsat.get(y).decode('utf-8') for y in bsat.keys() }
      return json.dumps(sat)
   elif request.method == 'POST':
      rd.hmset(key, request.form)
      return f"Successfully updated {key}"
   else:
      return 0

@app.route('/satellite', methods=['POST'])
def add_launch():
   rd.hmset(request.form)
   return f"Successfully added"

@app.route('/total/<country>', methods=['POST'])
def get_total_by_country(country):
   sats = [launch for launch in get_data() if country == launch['D']]
   res = Counter(sats['I'])
   return json.dumps(res)

def get_data():
   keys = [key.decode("utf-8") for key in rd.keys()]
   bsats = [rd.hgetall(key) for key in keys]
   sats = [{ y.decode('utf-8'): banimal.get(y).decode('utf-8') for y in banimal.keys() } for banimal in bsats[1:]] 
   return sats

def reset_data():
   with open("./data/sat-data.json", "r", encoding="utf8") as json_file:
      satdata = json.load(json_file)
      for sat in satdata[1:]:
         rd.hmset(sat['uid'], sat)

if __name__ == '__main__':
   reset_data()
   app.run(debug=True, host='0.0.0.0')