import uuid
from hotqueue import HotQueue
from redis import StrictRedis
import os

# redis_ip = os.environ.get('REDIS_IP')
# if not redis_ip:
#    raise Exception()
redis_ip = "localhost"

q = HotQueue("queue", host=redis_ip, port=6379, db=1)
rdjobs = StrictRedis(host=redis_ip, port=6379, db=2)

def _generate_jid():
    return str(uuid.uuid4())

def _generate_job_key(jid):
    return 'job.{}'.format(jid)

def _instantiate_job(jid, status, country):
    if type(jid) == str:
        return {'id': jid,
                'status': status,
                'country': country
        }
    return {'id': jid.decode('utf-8'),
            'status': status.decode('utf-8'),
            'country': country.decode('utf-8')
    }

def _save_job(job_key, job_dict):
    """Save a job object in the Redis database."""
    rdjobs.hmset(job_key, job_dict)

def _queue_job(jid):
    """Add a job to the redis queue."""
    q.put(jid)

def add_job(country, status="submitted"):
    """Add a job to the redis queue."""
    jid = _generate_jid()
    job_dict = _instantiate_job(jid, status, country)
    # update call to save_job:
    _save_job(_generate_job_key(jid), job_dict)
    # update call to queue_job:
    _queue_job(jid)
    return job_dict

def update_job_status(jid, nstatus):
    """Update the status of job with job id `jid` to status `status`."""
    jid, status, country = rdjobs.hmget(_generate_job_key(jid), 'id', 'status', 'country')
    job = _instantiate_job(jid, status, country)
    if job:
        job['status'] = nstatus
        _save_job(_generate_job_key(jid), job)
    else:
        raise Exception()

def get_country(jid):
    jid, status, country = rdjobs.hmget(_generate_job_key(jid), 'id', 'status', 'country')
    return country.decode('utf-8')

def get_jobs():
    keys = [key.decode("utf-8") for key in rdjobs.keys() if key != 'image']
    bjobs = [rdjobs.hgetall(key) for key in keys]
    jobs = [{ y.decode('utf-8'): banimal.get(y).decode('utf-8') for y in banimal.keys() } for banimal in bjobs[1:]] 
    return jobs
