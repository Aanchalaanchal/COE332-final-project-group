import uuid
from hotqueue import HotQueue
from redis import StrictRedis
import os

redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
   raise Exception()
# redis_ip = "localhost"

q2 = HotQueue("queue", host=redis_ip, port=6379, db=5)
rdjobs = StrictRedis(host=redis_ip, port=6379, db=2, charset="utf-8", decode_responses=True)

def _generate_jid():
    return str(uuid.uuid4())

def _generate_job_key(jid):
    return 'job.{}'.format(jid)

def _instantiate_job(jid, status, orbit):
    if type(jid) == str:
        return {'id': jid,
                'status': status,
                'orbit': orbit
        }
    return {'id': jid.decode('utf-8'),
            'status': status.decode('utf-8'),
            'orbit': orbit.decode('utf-8')
    }

def _save_job(job_key, job_dict):
    """Save a job object in the Redis database."""
    rdjobs.hmset(job_key, job_dict)

def _queue_job(jid):
    """Add a job to the redis queue."""
    q2.put(jid)

def add_job2(orbit, status="submitted"):
    """Add a job to the redis queue."""
    jid = _generate_jid()
    job_dict = _instantiate_job(jid, status, orbit)
    # update call to save_job:
    _save_job(_generate_job_key(jid), job_dict)
    # update call to queue_job:
    _queue_job(jid)
    return job_dict

def update_job_status(jid, nstatus):
    """Update the status of job with job id `jid` to status `status`."""
    jid, status, orbit = rdjobs.hmget(_generate_job_key(jid), 'id', 'status', 'orbit')
    job = _instantiate_job(jid, status, orbit)
    if job:
        job['status'] = nstatus
        _save_job(_generate_job_key(jid), job)
    else:
        raise Exception()

def add_image_to_job(jid, img):
    """Add image to job"""
    jid, status, orbit = rdjobs.hmget(_generate_job_key(jid), 'id', 'status', 'orbit')
    job = _instantiate_job(jid, status, orbit)
    if job:
        job['image'] = img.decode('utf-8')
        _save_job(_generate_job_key(jid), job)
    else:
        raise Exception()

def get_orbit(jid):
    jid, status, orbit = rdjobs.hmget(_generate_job_key(jid), 'id', 'status', 'orbit')
    return orbit
