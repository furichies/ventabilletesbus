# Utiliza la imagen de Alpine Linux como base
FROM python:3.9.7-alpine

# Instala las dependencias necesarias
RUN apk add --no-cache gcc musl-dev postgresql-dev

# Instala pip y las bibliotecas de Flask y SQLAlchemy
RUN pip install --no-cache-dir flask flask_restful flask_sqlalchemy

# Copia el archivo srv_bus.py al directorio /srv
COPY srv_bus.py /srv/srv_bus.py

# Expone el puerto 7000
EXPOSE 7000

# Establece el directorio de trabajo
WORKDIR /srv

# Ejecuta el servidor Flask
CMD ["python", "srv_bus.py"]
