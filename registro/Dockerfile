# Utiliza la imagen de Alpine Linux como base
FROM python:3.9.7-alpine

# Instala las dependencias necesarias
RUN apk add --no-cache gcc musl-dev postgresql-dev

# Instala pip y las bibliotecas de Flask y SQLAlchemy
RUN pip install --no-cache-dir flask flask_sqlalchemy

# Copia el archivo registro.py al directorio /srv
COPY registro.py /srv/registro.py

# Expone el puerto 6900
EXPOSE 6900

# Establece el directorio de trabajo
WORKDIR /srv

# Ejecuta el servidor Flask
CMD ["python", "registro.py"]
