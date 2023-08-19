# metto python
FROM python:3.8
# mi metto sulla cartella /
WORKDIR /app
# dipendenza flask
RUN pip install flask==2.0.1 requests==2.25.1 psycopg2-binary
# in teoria metto la webapp nell'immagine
COPY ./flask_app/app.py /app
# espongo una porta su docker
EXPOSE 5555
# comandi all'avvio del container per lanciare la webapp
CMD ["python", "app.py"]
