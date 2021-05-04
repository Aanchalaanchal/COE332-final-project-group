from flask import Flask, request, send_file
import json
import redis
from datetime import datetime
from collections import Counter
import jobs
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import uuid

app = Flask(__name__)

# redis_ip = os.environ.get('REDIS_IP')
# if not redis_ip:
#    raise Exception()
redis_ip = "localhost"

rd=redis.StrictRedis(host=redis_ip, port=6379, db=0)

@app.route('/jobs', methods=['POST'])
def jobs_api():
   try:
      job = request.get_json(force=True)
   except Exception as e:
      return True, json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
   return json.dumps(jobs.add_job(job['start'], job['end']))

@app.route('/', methods=['GET'])
def reset():
   reset_data()
   return "reset"

@app.route('/name/<name>', methods=['GET'])
def get_name(name):   
   return json.dumps([launch for launch in get_data() if name == launch['A']])

@app.route('/operator/<operator>', methods=['GET'])
def get_operator(operator):   
   return json.dumps([launch for launch in get_data() if operator in launch['E']])

@app.route('/contractor/<contractor>', methods=['GET'])
def get_contractor(contractor):   
   return json.dumps([launch for launch in get_data() if contractor in launch['V']])

@app.route('/lifetime/<lifetime>', methods=['GET'])
def get_lifetime(lifetime):   
   valid = [launch for launch in get_data() if launch['U'] != '']
   return json.dumps([launch for launch in valid if float(lifetime) <= float(launch['U'])])

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
   return json.dumps([launch for launch in get_data() if a <= datetime.strptime(launch['T'], "%d-%m-%Y") <= b])

@app.route('/launch/site/<site>', methods=['GET'])
def get_site(site):   
   return json.dumps([launch for launch in get_data() if site == launch['X']])

@app.route('/launch/vehicle/<vehicle>', methods=['GET'])
def get_vehicle(vehicle):   
   return json.dumps([launch for launch in get_data() if vehicle == launch['Y']])

# @app.route('/launch/recent', methods=['GET'])
# def get_recent():
#    return json.dumps(sorted(get_data(), key = lambda i: i['T'])[0:4])

@app.route('/satellite/<key>', methods=['GET', 'DELETE', 'POST'])
def get_launch_by_id(key):
   if request.method == 'GET':
      bsat = rd.hgetall(key)
      sat = { y.decode('utf-8'): bsat.get(y).decode('utf-8') for y in bsat.keys() }
      return json.dumps(sat)
   elif request.method == 'POST':
      rd.delete(key)
      data = request.form.to_dict()
      data['uid'] = key
      rd.hmset(key,data)
      return f"Successfully updated {key}"
   else:
      rd.delete(key)
      return f"Successfully deleted {key}"

@app.route('/satellite', methods=['POST'])
def add_launch():
   data = request.form.to_dict()
   uid = str(uuid.uuid4())
   data['uid'] = uid
   rd.hmset(uid, data)
   return f"Successfully added with id {uid}"

@app.route('/total/<country>', methods=['GET'])
def get_total_by_country(country):
   sats = [launch['I'] for launch in get_data() if country == launch['D']]
   res = Counter(sats)
   return json.dumps(res)

@app.route('/submit', methods=['POST'])
def submit():
   job.add_job()
   return "Job submitted to the queue"

@app.route('/jobs', methods=['GET'])
def jobs():
   return json.dumps(job.get_jobs())

@app.route('/download/<jobid>', methods=['GET'])
def download(jobid):
   path = f'/app/{jobid}.png'
   with open(path, 'wb') as f:
      f.write(rd.hget(jobid, 'image'))
   return send_file(path, mimetype='image/png', as_attachment=True)

def get_data():
   keys = [key.decode("utf-8") for key in rd.keys()]
   bsats = [rd.hgetall(key) for key in keys]
   sats = [{ y.decode('utf-8'): banimal.get(y).decode('utf-8') for y in banimal.keys() } for banimal in bsats[1:]] 
   return sats

def reset_data():
   rd.flushdb()
   with open("./data/sat-data.json", "r", encoding="utf8") as json_file:
      satdata = json.load(json_file)
      for sat in satdata[1:]:
         rd.hmset(sat['uid'], sat)

if __name__ == '__main__':
   reset_data()
   app.run(debug=True, host='0.0.0.0')
