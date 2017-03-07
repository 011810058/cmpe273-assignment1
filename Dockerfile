FROM python:2.7.10
MAINTAINER Jasmeet Singh "https.jasmeet@gmail.com"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]

