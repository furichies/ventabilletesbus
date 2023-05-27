#!/bin/bash

{

if [ $1 = 1 ]; then
#Creación de imágenes
docker build -t bus:0.1 bus/
docker build -t tienda:0.1 tienda/
docker build -t registro:0.1 registro/
docker build -t cajero:0.1 cajero/

#Creación de conenedores
docker run --name bus01 -p 7000:7000 -d bus:0.1
docker run --name registro01 -p 6900:6900 -d registro:0.1
docker run --name cajero01 -p 6901:6901 -d cajero:0.1
docker run --name tienda01 -p 8888:8888 -d tienda:0.1
elif [ $1 = 0 ]; then

docker stop bus01 tienda01 registro01 cajero01
docker rm bus01 tienda01 registro01 cajero01
docker rmi bus tienda:0.1 registro:0.1 cajero:0.1

fi

} || {

echo ERROR
echo "uso $0: argumentos [1] crear imágenes y contenedores [2] detiene y elimina conetnedores y borra las imágenes"

}
