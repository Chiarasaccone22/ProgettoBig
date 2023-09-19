# metto python
FROM python:3.8
# mi metto sulla cartella /
WORKDIR /app
# dipendenza flask
RUN pip install flask==2.0.1 requests==2.25.1 psycopg2-binary waitress boto3 pymongo aws awscli py2neo cassandra-driver pandas
# in teoria metto la webapp nell'immagine
COPY ./flask_app/app.py /app
COPY ./flask_app/templates /app/templates
COPY ./flask_app/static /app/static
COPY ./flask_app/caricamentiDB /app
COPY ./../fly.png /app
#inserimento dataset
COPY ./flask_app/Dataset /app
# chiara dice che serve ma bhoooo
ENV FLASK_APP=app
ENV FLASK_ENV=development
#RUN aws configure set aws_access_key_id $AWS_KEY
#RUN aws configure set aws_secret_access_key secretKey
#RUN aws configure set default.region local
#RUN aws configure set default.output json
# espongo una porta su docker
EXPOSE 8080
# comandi all'avvio del container per lanciare la webapp
CMD ["python", "app.py"]
