FROM python:3
WORKDIR /usr/src/app
RUN pip install Flask-RESTful Elasticsearch Nameko
COPY . .
CMD ["python", "api.py"]
