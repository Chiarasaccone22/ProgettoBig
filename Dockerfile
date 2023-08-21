# metto python
FROM python:3.8
# mi metto sulla cartella /
WORKDIR /app
# dipendenza flask
RUN pip install flask==2.0.1 requests==2.25.1 psycopg2-binary waitress boto3
# in teoria metto la webapp nell'immagine
COPY ./flask_app/app.py /app
COPY ./flask_app/templates /app/templates
COPY ./flask_app/script /app/script
# chiara dice che serve ma bhoooo
ENV FLASK_APP=app
ENV FLASK_ENV=development
# espongo una porta su docker
EXPOSE 8080
# comandi all'avvio del container per lanciare la webapp
CMD ["python", "app.py"]
