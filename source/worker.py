from jobs import q, update_job_status, get_country
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from api import get_data
import json
import redis
from collections import Counter
import matplotlib.pyplot as plt

# redis_ip = os.environ.get('REDIS_IP')
# if not redis_ip:
#    raise Exception()
redis_ip = "localhost"

rd=redis.StrictRedis(host=redis_ip, port=6379, db=1)

@q.worker
def execute_job(jid):
    update_job_status(jid, 'in progress')
    create_figure(jid)
    # fig = create_figure()
    # output = io.BytesIO()
    # FigureCanvas(fig).print_png(output)
    update_job_status(jid, 'complete')
    # return Response(output.getvalue(), mimetype='image/png')

def create_figure(jid):
    country = get_country(jid)
    sats = [launch['I'] for launch in get_data() if country == launch['D']]
    res = Counter(sats)
    labels = res.keys()
    sizes = res.values()
    explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice

    fig, axs = plt.subplots()
    axs.pie(sizes, labels=labels, autopct='%1.1f%%')
    axs.axis('equal')
    plt.savefig(f'{jid}.png')
    with open(f'{jid}.png', 'rb') as f:
        img = f.read()

    rd.hset(jid, 'image', img)
    rd.hset(jid, 'status', 'finished')

#    fig = Figure()
#    axis = fig.add_subplot(1, 1, 1)
#    xs = range(100)
#    ys = [random.randint(1, 50) for x in xs]
#    axis.plot(xs, ys)
#    return fig

execute_job()
