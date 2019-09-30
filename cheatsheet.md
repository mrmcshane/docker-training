# Docker Cheatsheet

## Common

| Command         | Description                                | Example                                  |
|:---------------:|:------------------------------------------:|:----------------------------------------:|
| `docker --help` | Get help with current command              | `docker image --help`                    |
| `docker build`  | Build a docker image                       | `docker build . -t repo/name:1.0.1`      |
| `docker push`   | Push a docker image to a remote registry   | `docker push repo/name:1.0.1`            |
| `docker pull`   | Pull a docker image from a remote registry | `docker pull repo/name:1.0.1`            |
| `docker run`    | Run an image as a container                | `docker run -d -p 80:80 repo/name:1.0.1` |
| `docker ps`     | List containers                            | `docker ps`                              |
| `docker exec`   | Execute a command in a running container   | `docker exec -it aabbccddeeff ps -ef`    |
| `docker logs`   | Display logs from a container              | `docker logs aabbccddeeff`               |
| `docker stop`   | Stop a running container                   | `docker stop aabbccddeeff`               |
| `docker kill`   | Kill a running container                   | `docker kill aabbccddeeff`               |
| `docker rm`     | Remove a stopped container                 | `docker rm aabbccddeeff`                 |
| `docker image`  | Work with docker images                    | `docker image ls`                        |
| `docker volume` | Work with docker volumes                   | `docker volume rm volume-1`              |

## Useful

**Note:** Some of these only work on unix/linux systems

| Command                                     | Description                               |
|:-------------------------------------------:|:-----------------------------------------:|
| `docker exec -it aabbccddeeff /bin/bash`    | Get a shell in a running container        |
| `docker kill $(docker ps -q`)               | Kill all running containers               |
| `docker kill $(docker ps -f publish=80 -q)` | Kill any container with port 80 published |
| `docker rm $(docker ps -aq)`                | Remove all stopped containers             |
| `docker image rm $(docker image ls -q)`     | Remove all local docker images            |
| `docker volume rm $(docker volume ls -q)`   | Remove all docker volumes                 |
