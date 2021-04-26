from flask import Flask, request
import json
import redis
from datetime import datetime

app = Flask(__name__)
rd = redis.StrictRedis(host='redis', port=6379, db=0)

@app.route('/name/<name>', methods=['GET'])
def get_name(name):   
   return 0

@app.route('/operator/<operator>', methods=['GET'])
def get_operator(operator):   
   return 0

@app.route('/contractor/<contractor>', methods=['GET'])
def get_contractor(contractor):   
   return 0

@app.route('/lifetime/<lifetime>', methods=['GET'])
def get_lifetime(lifetime):   
   return 0

@app.route('/country/<country>', methods=['GET'])
def get_country(country):   
   return 0

@app.route('/orbit/<orbit>', methods=['GET'])
def get_orbit(orbit):   
   return 0

@app.route('/orbital-elements/apogee/<apogee>', methods=['GET'])
def get_apogee(apogee):   
   return 0

@app.route('/orbital-elements/perigee/<perigee>', methods=['GET'])
def get_perigee(perigee):   
   return 0

@app.route('/orbital-elements/ecc/<ecc>', methods=['GET'])
def get_ecc(ecc):   
   return 0

@app.route('/orbital-elements/inc/<inc>', methods=['GET'])
def get_inc(inc):   
   return 0

@app.route('/launch/date/<date1>/<date2>', methods=['GET'])
def get_launches_by_date(date1, date2):
   a = datetime.strptime(date1, "%d-%m-%Y")
   b = datetime.strptime(date2, "%d-%m-%Y")
   return json.dumps([launch for launch in get_data() if a <= datetime.strptime(launch['created_on'], "%d/%m/%Y") <= b])

@app.route('/launch/site/<site>', methods=['GET'])
def get_site(site):   
   return 0

@app.route('/launch/vehicle/<vehicle>', methods=['GET'])
def get_vehicle(vehicle):   
   return 0

@app.route('/launch/recent', methods=['GET'])
def get_recent():   
   return 0

@app.route('/satellite/<key>', methods=['GET', 'DELETE', 'POST'])
def get_launch_by_id(key):
    if request.method == 'POST':
        return 0
    elif request.method == 'POST':
        rd.hmset(key, request.form)
        return f"Successfully updated {key}"
    else:
        return 0

@app.route('/satellite', methods=['POST'])
def add_launch():
        rd.hmset(request.form)
        return f"Successfully added"

def get_data():
   return 0

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0')