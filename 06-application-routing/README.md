# Application Routing

Building on the multi-container application project, this details how we would configure routing to multiple docker applications on the same domain using `docker-compose` and `traefik`.

Traefik an example of an application loadbalancer/router for docker, there are many others.

The source for this can be found on my [github](https://github.com/valteck-uk/docker-training/tree/master/06-application-routing).


## Structure

Build a directory structure like the one below:

```
05-application-routing
|-- containers
|   |-- python
|   |   |-- app
|   |   |   `-- ...
|   |   `-- Dockerfile
|   `-- traefik
|       `-- traefik.toml
|-- docker-compose.yml
`-- README.md
```

Please clone the respository to use the sample applications, or create a sample application yourself.


## Docker-Compose

This goes over the main parts of the `docker-compose.yml` file, download the whole file for the full details.

Traefik is used as the application router for docker images as it interacts with docker to receive the configuration of the containers rather than the routing being statically configured in a config file.

This is done via labels:
```
labels:
  - traefik.http.routers.blue-python.rule=Host(`blue-python.localhost`)
```


### Traefik

The traefik container is pretty standard, with the socket file exposed to the image via the volume section, and the config file copied across:
```  
  traefik:
    image: traefik:v2.0-alpine
    restart: always
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro # Access to Docker
      - ./containers/traefik/traefik.yml:/traefik.yml # Traefik configuration
    ports:
      - "80:80"
      - "8080:8080"
    networks:
      - traefik-network
  ```


#### traefik.yml

The config you apply enabled the dashboard, port 80 inbound connections, and the docker provider:
```
api:
  dashboard: true
  insecure: true

# entry point of http/80
entryPoints:
  http:
    address: ":80"

# this allows traefik to interact with docker
providers:
  docker:
    endpoint: "unix:///var/run/docker.sock"
    watch: true
    exposedByDefault: true
```


### Python

The python apps are created as normal, however an additional label is added to show how to route through the application through traefik:
```
  blue-python:
    image: mrmcshane/python:06-blue
    ports:
      - "30003:80"
    labels:
      - traefik.http.routers.blue-python.rule=Host(`blue-python.localhost`)
    networks:
      - traefik-network
```


## Deploying the application

Deploy the application:
```
docker-compose up -d --build
```


## Testing

To access the Traefik dashboard, visit: http://localhost:8080

To access the Blue application, visit: http://blue-python.localhost

To access the Green application, visit: http://green-python.localhost


## Note

The [Traefiok Documentation](https://docs.traefik.io/) is a great source for more information, specifically the [Docker Provider](https://docs.traefik.io/configuration/backends/docker/) page, which will give details of all of the configuration options that you can apply as labels to containers in the `docker-compose.yml` config.
