from jobs import q, update_job_status
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

@q.worker
def execute_job(jid):
    jobs.update_job_status(jid, 'in progress')
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    jobs.update_job_status(jid, 'complete')
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    res = get_total_by_country('USA')
    labels = res.keys()
    sizes = res.values()
    explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice

    fig = plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    fig.axis('equal')
#    fig = Figure()
#    axis = fig.add_subplot(1, 1, 1)
#    xs = range(100)
#    ys = [random.randint(1, 50) for x in xs]
#    axis.plot(xs, ys)
   return fig