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

