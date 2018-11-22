FROM mongo:3.2-jessie
LABEL MAINTAINER="IOHANNES IACOBUS 20170480" EMAIL="jotade100@gmail.com"
WORKDIR /app
#directorio de trabajo
RUN apt-get update && apt-get install -y python3 python3-pip
#Copiar todo al contenedor
COPY . .
RUN pip3 install -r req.txt && apt-get install -y dos2unix \
  && chmod +x *.sh && dos2unix *.sh
#CMD [ "/bin/bash","/app/docker-entrypoint.sh", "start"]
ENTRYPOINT ["/app/docker-entrypoint.sh"]
#CMD ["mongod --fork --logpath /tmp/mongo",  "python3 -u truncateOS.py"]
#se expone un puerto
EXPOSE 27017
