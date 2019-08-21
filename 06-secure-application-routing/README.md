# Secure Application Routing

**Note:** This is currently just a copy of Application Routing until I add the SSL cert sections.

Building on the multi-container application project, this details how we would configure routing to multiple docker applications on the same domain using `docker-compose` and `traefik`.

The source for this can be found on my [github](https://github.com/mrmcshane/docker-training/tree/master/05-application-routing).

## Structure

Build a directory structure like the one below:

```
05-application-routing
|-- containers
|   `-- map
|   |   |-- app
|   |   |   `-- ...
|   |   `-- Dockerfile
|   |-- python
|   |   |-- app
|   |   |   `-- ...
|   |   `-- Dockerfile
|   `-- traefik
|       `-- config
|           `-- traefik.toml
|-- docker-compose.yml
`-- README.md
```

Please clone the respository to use the sample applications, or create a sample application yourself.


## Map

The map application is a simple html application, like we have deployed before.

## Python

The python application is the same application that we have previously deployed.

## Traefik

As we are only adding a config file to the traefik default image, we don't need anything else in this directory.

### Config

The config for traefik is written in TOML, and is pretty simple.

Create the entrypoint defaults:
```
defaultEntryPoints = ["http"]
```

Configure the main entrypoint for the router to be `HTTP/80`:
```
[entryPoints]
  [entryPoints.http]
  address = ":80"
```

Allow traefic to interact with docker via a unix socket:
```
[docker]
endpoint = "unix:///var/run/docker.sock"
domain = "docker.localhost"
watch = true
exposedByDefault = false
```
 
## Docker-Compose

This goes over the main parts of the `docker-compose.yml` file, download the whole file for the full details.

Traefik is used as the application router for docker images as it interacts with docker to receive the configuration of the containers rather than the routing being statically configured in a config file.

This is done via labels:
```
labels:
  - "traefik.docker.network=public"
  - "traefik.enable=true"
  - "traefik.frontend.rule=Host:traefik.localhost"
  - "traefik.port=8080"
  - "traefik.protocol=http"
```

### Traefik

The traefik container is pretty standard, with the socket file exposed to the image via the volume section, and the config file copied across:
```  
traefik:
  image: traefik:latest
  command: "--api --docker"
  restart: always
  networks:
    - public
  volumes:
    - /var/run/docker.sock:/var/run/docker.sock
    - ./traefic/config/traefik.toml:/traefik.toml
  ports:
    - "80:80"
  labels:
    - "traefik.docker.network=public"
    - "traefik.enable=true"
    - "traefik.frontend.rule=Host:traefik.localhost"
    - "traefik.port=8080"
    - "traefik.protocol=http"
  ```

### Map




### Python

As python is connected to two networks, the default network needs to be specified so traefic knows which one to route traffic to. As with the other applications, the host is specified:
```
  python:
  build: ./containers/python
  ports:
    - "30003:80"
  networks:
    - public
    - private
  labels:
    - "traefik.docker.network=public"
    - "traefik.frontend.rule=Host:python.localhost"
```

## Deploying the application

Deploy the application:
```
docker-compose up -d --build
```

## Testing

To access the Traefik dashboard, visit: http://traefik.localhost

To access the Map application, visit: http://map.localhost

To access the Python application, visit: http://python.localhost

## Note

The [Traefiok Documentation](https://docs.traefik.io/) is a great source for more information, specifically the [Docker Provider](https://docs.traefik.io/configuration/backends/docker/) page, which will give details of all of the configuration options that you can apply as labels to containers in the `docker-compose.yml` config.
