# Utiliza la imagen de Alpine Linux como base
FROM python:3.9.7-alpine


# Instala pip y las bibliotecas de Flask 
RUN pip install --no-cache-dir flask 

# Copia el archivo tienda.py al directorio /srv
COPY tienda.py /srv/tienda.py

# Expone el puerto 8888
EXPOSE 8888

# Establece el directorio de trabajo
WORKDIR /srv

# Ejecuta el servidor Flask
CMD ["python", "tienda.py"]
