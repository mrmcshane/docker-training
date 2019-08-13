# Multi-Container Application

How to deploy an application consisting of multiple containers using docker-compose.

The source for this can be found on my [github](https://github.com/mrmcshane/docker-training/tree/master/04-multi-container-application).

## Structure

Build a simple directory structure like the one below:

```
04-multi-container-application
|-- containers
|   `-- python
|       |-- code
|       |   |-- requirements.txt
|       |   `-- test.py
|       `-- Dockerfile
|-- docker-compose.yml
`-- README.md
```

The directories within the `containers` directory would possibly be seperate git repos and pulled/cloned as part of your build pipeline if the applications are able to be updated independently of each other. In this example we will have them statically configured.

## Docker Compose

A Docker Compose file is a yaml file describing how the multi-container application should be configured.

It will look like this:

```
version: '3'
services:
  web:
    build: ./containers/python
    ports:
      - "30015:80"
    networks:
      - network-04
  mariadb:
    image: "mariadb/server"
    environment:
      MARIADB_ROOT_PASSWORD: pass
    ports:
      - "30016:3306"
    volumes:
      - mariadb-data:/var/lib/mysql
    networks:
      - network-04
volumes:
  mariadb-data:
networks:
  network-04:
```

### services

The `services` are the different containers that will make up the application.

### build

The `build` key under a service is the directory where the Dockerfile is located. Not used with `image`.

### image

If the image is external, the name of the image to use. Not used with `build`.

### environment

Specifies environment variables that will be assigned to the container, specified as a set of `key:val` values.

### ports

Essentially the docker command line argument of `-p 30015:80`, this will create a port mapping to the container from externally.

### networks

The `networks` top level key creates an internal network.

The `networks` key under a service attaches a service to a network, allowing inter-container communication.

### volumes

The `volumes` top level key creates a volume that can be attached to a container.

The `volumes` key under a service attaches a volume to a container, specified as `volume:mount/point`.



## Python Application

I won't paste all of the application code as the code itself doesn't matter, if you want to use it, it's hosted [here](https://github.com/mrmcshane/docker-training/blob/master/04-multi-container-application/containers/python/code/test.py).

The main part of the application that matters is the database connection string:
```
host="mariadb"
```
This uses the name of the docker compose service. 

The ports used between the application and the database is the internal port. In this example `3306`, rather than `30016`.

### Dockerfile

This is the basic docker config, it copies over the code, installs the python dependencies, and then runs the application.
```
FROM python:3

WORKDIR /usr/src/app

COPY code/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY code/test.py .
EXPOSE 80

CMD [ "python", "./test.py" ]
```


## Mariadb Deployment

We will deploy the default mariadb image and configure it with a port mapping and environment variables.



## Deploying the application

Deploy the application:
```
docker-compose up
```

Deploy it in detached mode:
```
docker-compose up -d
```

Force a re-build of the docker image each time along with detached mode:
```
docker-compose up -d --build
```

## Note

The [Docker Documentation](https://docs.docker.com/compose/) is a great source for learning docker compose.
