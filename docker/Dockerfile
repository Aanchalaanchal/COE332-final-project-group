FROM python:latest
RUN pip install Flask==1.1.2 \
		hotqueue==0.2.8 \
		matplotlib==3.3.4 \
		redis==3.5.3 \
		requests==2.25.1
COPY . /app
WORKDIR /app
ENTRYPOINT ["python"]

