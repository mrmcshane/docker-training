# Off-the-shelf Image

How to deploy and work with an off-the-shelf image.

The source for this can be found on my [github](https://github.com/mrmcshane/docker-training/tree/master/01-off-the-shelf-image).

## Run A Container

We will use the [nginx](https://hub.docker.com/_/nginx) image to deploy a basic webserver. The aim of this is to get an nginx webserver online and see the splash page.

To run a container in docker, we use the command `docker run`, so to run nginx, we can use:
```
docker run nginx
```

This will look for a container called `nginx` locally, if it can't find one, it will look a Docker Hub where it will find the correct image.
The image will run in the foreground and you will be connected directly to the output of the container. 


## Detached Mode

Running a container in the foreground is useful for testing if containers run, but not running them for a specific purpose. To stop this, we can run a container in detached mode, using the `-d` flag. Note, the flags come before the name of the image you wish to run:
```
docker run -d nginx
```

You should get an output similar to this:
```
~ docker run -d nginx
4e540d26cdc8e18801fb0e0acc156b6d0131ad613fbb63c6d6db00e9b97b683d
```
This shows that the command executed successfully.


## Port Mapping

To check the status of the container, we can run `docker ps` again:
```
~ docker ps
CONTAINER ID    IMAGE      COMMAND                  CREATED              STATUS              PORTS         NAMES
4e540d26cdc8    nginx      "nginx -g 'daemon of…"   About a minute ago   Up About a minute   80/tcp        distracted_rosalind
```

You can also see that it's showing port `80/tcp` listed on the container, however if you visit `http://localhost` in a browser, you wont be able to connect. that's because even through the application within the container is running on `80/tcp`, that's only accessible from within the container.

First, we will remove the non-working container but running `docker stop` and passing the `CONTAINER ID`:
```
docker stop 4e540d26cdc8
```

To allow access to a container you need to create a port mapping, this can be done with the `-p` flag. Mapping `80/tcp` within the container to `80/tcp` on your local machine is:
```
docker run -d -p 80:80 nginx
```

Now if you visit `http://localhost` on a browser you will see the nginx splash page.

Port mappings are in the format `external:internal`, so the value on the left is what you will browse to, and the value on the right is what is running within the container.