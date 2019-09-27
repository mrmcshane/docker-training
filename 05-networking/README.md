# Networking

A task to learn how networking works in docker/docker-compose.

We will be creating two python applications, one connected to the same virtual network as the dataabse and one that is not to demonstrate how network segregation works in docker.

The source for this can be found on my [github](https://github.com/mrmcshane/docker-training/tree/master/05-networking).

## Structure

Build a simple directory structure like the one below:

```
05-networking
|-- containers
|   `-- python
|       |-- app
|       |   `-- ...
|       `-- Dockerfile
|-- docker-compose.yml
`-- README.md
```

The directories within the `containers` directory would possibly be seperate git repos and pulled/cloned as part of your build pipeline if the applications are able to be updated independently of each other. In this example we will have them statically configured.

## Docker Compose

This is the docker compose file we will be using:

```
version: '3'
services:
  blue:
    image: mrmcshane/python:05-blue
    ports:
      - "30001:80"
    networks:
      - public
      - private
  green:
    image: mrmcshane/python:05-green
    ports:
      - "30002:80"
    networks:
      - public
  mariadb:
    image: "mariadb/server"
    environment:
      MARIADB_ROOT_PASSWORD: pass
    ports:
      - "30003:3306"
    volumes:
      - mariadb-data:/var/lib/mysql
    networks:
      - private
volumes:
  mariadb-data:
networks:
  public:
  private:
```

This is based on `04-multi-container-application`, however 



## Python Application

I won't paste all of the application code as the code itself doesn't matter, if you want to use it, it's hosted [here](https://github.com/mrmcshane/docker-training/blob/master/04-multi-container-application/containers/python/code/test.py).

The main part of the application that matters is the database connection string:
```
host="mariadb"
```
This uses the name of the docker compose database service: `mariadb`. 

The ports used between the application and the database is the internal port. In this example `3306`, rather than `30003`.


We will be creating two versions of the application, `blue` and `green` using the same application, but with different colours. The only difference between them is:
```
background-color: rgb(30, 142, 233); # blue
background-color: rgb(48, 228, 144); # green
```

To build each of these applications:

Set background colour to blue
```
docker build containers/python -t mrmcshane/python:05-blue
docker push mrmcshane/python:05-blue
```
Set background colour to green
```
docker build containers/python -t mrmcshane/python:05-green
docker push mrmcshane/python:05-green
```

### Mariadb

Note that in this excersize, we have not exposed any external ports for the database container.

This is because docker containers have access to the internal port in other containers assigned to the same networks without explicit mapping. A database is a good example of a container that should not be accessed outside of the application network.

### networks

The `networks` top level key creates an internal network.

The `networks` key under a service attaches a service to a network, allowing inter-container communication.


- The `mariadb` container will be connected to the `private` network.

- The `green` container will be connected to the `public` network.

- The `blue` container will be connected to both `public` and `private` networks.

Note: These network names are arbitrary and can be named anything you want.


## Deploying the application

Assuming the containers have already been built (steps earlier in the task), we only need to run docker compose:
```
docker-compose up -d
```


## Testing

The `blue` application should have a database connection and the `green` application should not be able to connect.

To test the blue application, visit: http://localhost:30001/

To test the green application, visit: http://localhost:30002/


## Note

The [Docker Documentation](https://docs.docker.com/compose/) is a great source for learning docker compose.
