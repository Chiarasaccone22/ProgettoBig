# Usa l'immagine ufficiale di Nginx come base
FROM nginx

# Copia i file del tuo sito web nell'immagine Nginx
COPY ./index.html /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/nginx.conf  

# Esponi la porta 80 del container
EXPOSE 80

# Comando predefinito per avviare Nginx
CMD ["nginx", "-g", "daemon off;"]

