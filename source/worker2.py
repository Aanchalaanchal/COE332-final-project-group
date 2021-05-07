from jobs2 import q2, update_job_status, get_orbit
from api import get_data
import os
import redis
from collections import Counter
import matplotlib.pyplot as plt

redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
   raise Exception()
# redis_ip = "localhost"

rdimg=redis.StrictRedis(host=redis_ip, port=6379, db=4)

@q2.worker
def execute_job(jid):
    update_job_status(jid, 'in progress')
    create_figure(jid)
    update_job_status(jid, 'complete')

def create_figure(jid):
    orbit = get_orbit(jid)
    sats = [launch['D'] for launch in get_data() if orbit == launch['I']]
    res = Counter(sats)
    labels = list(res.keys())
    sizes = list(res.values())
    
    cutoff = 0.02*sum(sizes)

    cutlabels = []
    cutsizes = []
    other = 0
    for idx in range(len(labels)):
        if sizes[idx] <= cutoff:
            other += sizes[idx]
        else: 
            cutlabels.append(labels[idx])
            cutsizes.append(sizes[idx])
    if other > 0:
        cutlabels.append("Other (< 2%)")
        cutsizes.append(other)

    fig, axs = plt.subplots()
    axs.pie(cutsizes, labels=cutlabels, autopct='%1.1f%%')
    axs.axis('equal')
    plt.title(f"Percentage of Countries for {orbit} Orbits")

    plt.savefig(f'{jid}.png')
    with open(f'{jid}.png', 'rb') as f:
        img = f.read()
    rdimg.hset(jid, 'image', img)

execute_job()
